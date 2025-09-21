"""
Sync Semantic: A new approach to sync the graph for semantic search.

This script replaces the complex context-building logic of sync_full.py.
It operates on a page-by-page basis, linearizing the entire page's content
and then using Chonkie's SemanticChunker to create semantically coherent
chunks for indexing.

This version is updated to use Weaviate as the vector store and Voyage AI's
contextual embedding models.

Core pipeline:
1. Fetch all pages from Roam.
2. For each page:
    a. Linearize its content into a single text document.
    b. Chunk the linearized text using Chonkie.
3. In batches of pages:
    a. Generate contextual embeddings for all chunks using Voyage AI.
    b. Batch-insert the chunks and their vectors into Weaviate.
"""
print("[sync_semantic] Starting...")

import asyncio
import json
import re
import uuid
import argparse
import time
from typing import Dict, List, Optional, Any

import httpx
import weaviate
import voyageai
from weaviate.classes.config import (Property, DataType, Tokenization, Configure)

# Add backend to path to allow local imports
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from linearize import linearize_page_markdown_style
from roam import query_roam
from main_semantic import settings

voyageai.api_key = settings.voyageai_api_key
voyage_client = voyageai.Client()

# --- Constants ---
BATCH_SIZE = 10 # Pages per Roam pull-many request
COLLECTION_NAME = "RoamSemanticChunks" # Weaviate class names are capitalized
CHUNKER_SERVICE_URL = "http://chunker:8003"  # Docker service name
CHUNKER_RETRY_ATTEMPTS = 3
CHUNKER_RETRY_DELAY = 2  # seconds

# --- Roam API Functions ---

async def get_all_page_uids() -> List[str]:
    """
    Fetches all page UIDs from Roam, including Daily Note Pages.
    """
    print("[sync_semantic] Step 1: Getting all page UIDs...")
    query = """[:find ?uid
               :where [?e :node/title]
                      [?e :block/uid ?uid]]"""

    result = await query_roam(
        token=settings.roam_api_token,
        graph_name=settings.roam_graph_name,
        query=query
    )

    if not result or not result.get('result'):
        return []

    all_uids = [item[0] for item in result['result']]
    # Count DNPs for informational purposes
    dnp_count = len([uid for uid in all_uids if re.match(r'^\d{2}-\d{2}-\d{4}$', uid)])
    print(f"[sync_semantic] Found {len(all_uids)} total pages ({dnp_count} Daily Notes, {len(all_uids) - dnp_count} regular pages).")
    return all_uids

async def pull_many_pages(uids: List[str]) -> List[Optional[Dict]]:
    """
    Pulls full page data for a list of UIDs.
    """
    if not uids:
        return []

    url = f"https://api.roamresearch.com/api/graph/{settings.roam_graph_name}/pull-many"
    headers = {
        "X-Authorization": f"Bearer {settings.roam_api_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    eids_list = " ".join([f'[:block/uid \"{uid}\"]' for uid in uids])
    eids_str = f"[{eids_list}]"
    # Recursive selector to get all children of the page
    selector_str = "[:block/uid :block/string :node/title :block/order {:block/children ...}]"

    pull_data = {"eids": eids_str, "selector": selector_str}

    async with httpx.AsyncClient(timeout=60.0, follow_redirects=True) as client:
        try:
            response = await client.post(url, headers=headers, json=pull_data)
            if response.status_code == 200:
                return response.json().get('result', [])
            else:
                print(f"  ✗ Pull-many failed with status {response.status_code}: {response.text[:200]}")
                return [None] * len(uids)
        except Exception as e:
            print(f"  ✗ Pull-many request error: {e}")
            return [None] * len(uids)

# --- Weaviate Schema ---

def ensure_weaviate_schema(client: weaviate.Client):
    """Ensure the Weaviate collection exists and has the correct schema."""
    print(f"[Weaviate] Ensuring collection '{COLLECTION_NAME}' exists...")
    if client.collections.exists(COLLECTION_NAME):
        print(f"[Weaviate] Collection '{COLLECTION_NAME}' already exists.")
        return

    print(f"[Weaviate] Creating collection '{COLLECTION_NAME}'...")
    try:
        client.collections.create(
            name=COLLECTION_NAME,
            vectorizer_config=Configure.Vectorizer.none(),
            properties=[
                Property(name="chunk_text_preview", data_type=DataType.TEXT),
                Property(name="primary_uid", data_type=DataType.TEXT, tokenization=Tokenization.FIELD),
                Property(name="page_title", data_type=DataType.TEXT, tokenization=Tokenization.WORD),
                Property(name="page_uid", data_type=DataType.TEXT, tokenization=Tokenization.FIELD),
                Property(name="document_type", data_type=DataType.TEXT, tokenization=Tokenization.FIELD),
                Property(name="source_uids_json", data_type=DataType.TEXT, skip_vectorization=True),
                Property(name="chunk_token_count", data_type=DataType.INT),
                Property(name="sync_version", data_type=DataType.TEXT, skip_vectorization=True),
            ]
        )
        print(f"[Weaviate] Collection '{COLLECTION_NAME}' created successfully.")
    except Exception as e:
        print(f"[Weaviate] Failed to create collection: {e}")
        raise

# --- Chunker Service Integration ---

async def chunk_text_via_service(text: str, max_retries: int = CHUNKER_RETRY_ATTEMPTS) -> Optional[List[Dict[str, Any]]]:
    """
    Call the chunker service to chunk text.
    Returns list of chunks with text, start_index, end_index, token_count.
    Returns None if service is unavailable after retries.
    """
    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{CHUNKER_SERVICE_URL}/chunk",
                    json={"text": text}
                )
                if response.status_code == 200:
                    result = response.json()
                    return result.get("chunks", [])
                elif response.status_code == 503:
                    # Service still initializing
                    print(f"  ↳ Chunker service initializing, attempt {attempt + 1}/{max_retries}...")
                    await asyncio.sleep(CHUNKER_RETRY_DELAY * (2 ** attempt))  # Exponential backoff
                else:
                    print(f"  ✗ Chunker service error: {response.status_code}")
                    return None
        except (httpx.ConnectError, httpx.TimeoutException) as e:
            if attempt == max_retries - 1:
                print(f"  ✗ Cannot connect to chunker service: {e}")
                return None
            await asyncio.sleep(CHUNKER_RETRY_DELAY * (2 ** attempt))
    return None

async def wait_for_chunker_service(timeout: int = 60) -> bool:
    """
    Wait for the chunker service to be ready.
    Returns True if service is ready, False if timeout.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{CHUNKER_SERVICE_URL}/health")
                if response.status_code == 200:
                    data = response.json()
                    if data.get("chunker_loaded"):
                        print(f"[sync_semantic] Chunker service ready (init took {data.get('chunker_init_time_seconds', 0):.2f}s)")
                        return True
        except (httpx.ConnectError, httpx.TimeoutException):
            pass
        await asyncio.sleep(2)
    return False

# Simple chunk class to mimic Chonkie's chunk structure
class SimpleChunk:
    def __init__(self, text: str, start_index: int, end_index: int, token_count: int):
        self.text = text
        self.start_index = start_index
        self.end_index = end_index
        self.token_count = token_count

# --- Main Sync Logic ---

async def sync_semantic_graph(clear_existing: bool = False, test_limit: Optional[int] = None):
    """
    Main function to run the semantic sync process.
    """
    print("\n[sync_semantic] Starting semantic graph sync with Weaviate...")
    start_time = time.time()

    # Step 1: Get all page UIDs
    step1_start = time.time()
    all_page_uids = await get_all_page_uids()
    step1_time = time.time() - step1_start
    if not all_page_uids:
        print("[sync_semantic] No pages found to process.")
        return

    total_pages = len(all_page_uids)
    if test_limit:
        print(f"[sync_semantic] TEST MODE: Limiting to first {test_limit} pages.")
        all_page_uids = all_page_uids[:test_limit]
        total_pages = len(all_page_uids)

    # Step 2: Handle collection and client
    client = weaviate.connect_to_custom(
        http_host="weaviate",
        http_port=8080,
        http_secure=False,
        grpc_host="weaviate",
        grpc_port=50051,
        grpc_secure=False,
    )
    try:
        if clear_existing:
            print(f"[sync_semantic] Step 2: Deleting collection '{COLLECTION_NAME}'...")
            client.collections.delete(COLLECTION_NAME)
        
        ensure_weaviate_schema(client)
        collection = client.collections.get(COLLECTION_NAME)

        # Step 3: Wait for chunker service to be ready
        print("[sync_semantic] Step 3: Connecting to chunker service...")
        step3_start = time.time()
        chunker_ready = await wait_for_chunker_service()
        if not chunker_ready:
            print("[sync_semantic] WARNING: Chunker service not available, sync cannot proceed")
            return
        step3_time = time.time() - step3_start

        # Step 4: Process pages in batches
        print(f"[sync_semantic] Step 4: Processing {total_pages} pages in batches of {BATCH_SIZE}...")
        
        # Global statistics
        total_documents_added = 0
        total_chunks_created = 0  # Total chunks across all pages
        total_roam_time = 0
        total_processing_time = 0
        total_linearize_time = 0
        total_chunk_time = 0
        total_voyageai_time = 0
        total_weaviate_time = 0

        for i in range(0, total_pages, BATCH_SIZE):
            batch_start_time = time.time()
            batch_uids = all_page_uids[i:i + BATCH_SIZE]
            progress = (i + len(batch_uids)) / total_pages * 100
            print(f"\n[sync_semantic] Processing batch {i//BATCH_SIZE + 1}, pages {i+1}-{i+len(batch_uids)} ({progress:.1f}%)...", flush=True)

            roam_start = time.time()
            pages_data = await pull_many_pages(batch_uids)
            total_roam_time += time.time() - roam_start

            batch_page_chunks: List[List[str]] = []
            flat_objects_for_weaviate: List[Dict[str, Any]] = []
            batch_chunks_created = 0

            processing_start = time.time()
            batch_linearize_time = 0
            batch_chunk_time = 0

            for page_data in pages_data:
                if not page_data or not page_data.get(':block/uid'):
                    continue

                page_title = page_data.get(':node/title', 'Untitled')
                page_uid = page_data.get(':block/uid')

                # Always index the page title itself as a document
                page_title_obj = {
                    "properties": {
                        "chunk_text_preview": page_title,
                        "primary_uid": page_uid,
                        "page_title": page_title,
                        "page_uid": page_uid,
                        "document_type": "page",
                        "sync_version": "semantic_v2_weaviate"
                    },
                    "uuid": str(uuid.uuid4())
                }
                flat_objects_for_weaviate.append(page_title_obj)
                batch_page_chunks.append([page_title])

                if not page_data.get(':block/children'):
                    continue

                # Time linearization
                linearize_start = time.time()
                linearized_text, uid_map = linearize_page_markdown_style(page_data)
                batch_linearize_time += time.time() - linearize_start

                if not linearized_text.strip():
                    continue

                try:
                    # Time chunking via service
                    chunk_start = time.time()
                    chunk_results = await chunk_text_via_service(linearized_text)
                    batch_chunk_time += time.time() - chunk_start

                    if not chunk_results:
                        continue

                    # Convert service results to chunk objects
                    chunks = [SimpleChunk(
                        text=c["text"],
                        start_index=c["start_index"],
                        end_index=c["end_index"],
                        token_count=c["token_count"]
                    ) for c in chunk_results]

                    batch_chunks_created += len(chunks)
                    batch_page_chunks.append([chunk.text for chunk in chunks])

                    for chunk in chunks:
                        # Find all source UIDs that overlap with the chunk's character range
                        source_uids = {mapping['uid'] for mapping in uid_map if chunk.start_index < mapping['end'] and chunk.end_index > mapping['start']}
                        if not source_uids:
                            continue

                        flat_objects_for_weaviate.append({
                            "properties": {
                                "chunk_text_preview": chunk.text,
                                "primary_uid": next(iter(source_uids)),
                                "page_title": page_title,
                                "page_uid": page_uid,
                                "document_type": "chunk",
                                "chunk_token_count": chunk.token_count,
                                "source_uids_json": json.dumps(list(source_uids)),
                                "sync_version": "semantic_v2_weaviate"
                            },
                            "uuid": str(uuid.uuid4())
                        })

                except Exception as e:
                    print(f"  ✗ Error chunking page '{page_title}': {e}")

            total_processing_time += time.time() - processing_start
            total_linearize_time += batch_linearize_time
            total_chunk_time += batch_chunk_time
            total_chunks_created += batch_chunks_created

            if not batch_page_chunks:
                continue
            
            voyageai_start = time.time()
            try:
                print(f"  ↳ Getting {sum(len(p) for p in batch_page_chunks)} embeddings from Voyage AI...", flush=True)
                voyage_result = voyage_client.contextualized_embed(
                    inputs=batch_page_chunks, 
                    model=settings.voyageai_context_model, 
                    input_type="document"
                )
                flat_embeddings = [emb for res in voyage_result.results for emb in res.embeddings]

                for i, obj in enumerate(flat_objects_for_weaviate):
                    if i < len(flat_embeddings):
                        obj["vector"] = flat_embeddings[i]

            except Exception as e:
                print(f"  ✗ Voyage AI embedding failed: {e}", flush=True)
                total_voyageai_time += time.time() - voyageai_start
                continue
            total_voyageai_time += time.time() - voyageai_start

            weaviate_start = time.time()
            with collection.batch.fixed_size(batch_size=100) as batch:
                for obj in flat_objects_for_weaviate:
                    if "vector" in obj:
                        batch.add_object(
                            properties=obj["properties"],
                            uuid=obj["uuid"],
                            vector=obj["vector"]
                        )
            total_weaviate_time += time.time() - weaviate_start
            
            if collection.batch.failed_objects:
                print(f"  ✗ Failed to import {len(collection.batch.failed_objects)} objects.", flush=True)
                for failed in collection.batch.failed_objects:
                    print(f"    - {failed.message}", flush=True)
            else:
                print(f"  ✓ Added {len(flat_objects_for_weaviate)} documents to Weaviate.", flush=True)
            total_documents_added += len(flat_objects_for_weaviate)

        # Final statistics
        elapsed_time = time.time() - start_time
        print("\n" + "="*50)
        print("[sync_semantic] SYNC COMPLETE!")
        print(f"  - Time elapsed: {elapsed_time:.2f} seconds")
        print(f"  - Total pages processed: {total_pages}")
        print(f"  - Total chunks created: {total_chunks_created}")
        print(f"  - Total documents added: {total_documents_added}")
        # count = await collection.aggregate.over_all(total_count=True)
        # print(f"  - Documents in collection: {count.total_count}")
        print("\n[sync_semantic] Time breakdown:")
        print(f"  - Initial setup: {step1_time + step3_time:.2f}s ({(step1_time + step3_time)/elapsed_time*100:.1f}%)")
        print(f"    - Getting page UIDs: {step1_time:.2f}s")
        print(f"    - Connecting to chunker service: {step3_time:.2f}s")
        print(f"  - Roam API calls: {total_roam_time:.2f}s ({total_roam_time/elapsed_time*100:.1f}%)")
        print(f"  - Processing (total): {total_processing_time:.2f}s ({total_processing_time/elapsed_time*100:.1f}%)")
        print(f"    - Linearization: {total_linearize_time:.2f}s ({total_linearize_time/elapsed_time*100:.1f}%)")
        print(f"    - Chunking: {total_chunk_time:.2f}s ({total_chunk_time/elapsed_time*100:.1f}%)")
        print(f"  - Voyage AI Embeddings: {total_voyageai_time:.2f}s ({total_voyageai_time/elapsed_time*100:.1f}%)")
        print(f"  - Weaviate Batch Import: {total_weaviate_time:.2f}s ({total_weaviate_time/elapsed_time*100:.1f}%)")

        # Calculate unaccounted time
        accounted_time = step1_time + step3_time + total_roam_time + total_processing_time + total_voyageai_time + total_weaviate_time
        unaccounted_time = elapsed_time - accounted_time
        if unaccounted_time > 0.1:  # Only show if significant
            print(f"  - Other (Weaviate connection, etc.): {unaccounted_time:.2f}s ({unaccounted_time/elapsed_time*100:.1f}%)")

        if total_documents_added > 0:
            print(f"  - Average time per document: {elapsed_time/total_documents_added:.3f}s")
        print("="*50)

    finally:
        if client.is_connected():
            client.close()
            print("[Weaviate] Sync client connection closed.")

async def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(description='Sync Roam graph to Weaviate using contextual embeddings.')
    parser.add_argument(
        '--clear',
        action='store_true',
        help='Clear all existing objects in the Weaviate collection before syncing.'
    )
    parser.add_argument(
        '--test',
        type=int,
        metavar='N',
        help='Test mode: only process first N pages.'
    )

    args = parser.parse_args()

    await sync_semantic_graph(clear_existing=args.clear, test_limit=args.test)


if __name__ == "__main__":
    asyncio.run(main())
    print("[sync_semantic] Done!")