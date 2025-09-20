"""
Sync Semantic: A new approach to sync the graph for semantic search.

This script replaces the complex context-building logic of sync_full.py.
It operates on a page-by-page basis, linearizing the entire page's content
and then using Chonkie's SemanticChunker to create semantically coherent
chunks for indexing.

Core pipeline:
1. Fetch all pages from Roam.
2. For each page:
    a. Linearize its content into a single text document with markdown-style formatting.
    b. Generate a character-to-UID map during linearization.
    c. Chunk the linearized text using Chonkie.
    d. For each chunk, create a new document for ChromaDB with a unique ID.
    e. Store a list of all source block UIDs in the metadata.
"""
print("[sync_semantic] Starting...")

import asyncio
import json
import re
import uuid
import argparse
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import httpx
from chonkie import SemanticChunker

# Add backend to path to allow local imports
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from linearize import linearize_page_markdown_style
from roam import query_roam
from main_semantic import settings, get_collection

# --- Constants ---
BATCH_SIZE = 10 # Pages per pull-many request
COLLECTION_NAME = "roam_semantic_chunks"

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

    # COMMENTED OUT: Previously filtered out Daily Note Pages
    # We now include DNPs in semantic search as they often contain valuable content
    # non_dnp_uids = [uid for uid in all_uids if not re.match(r'^\d{2}-\d{2}-\d{4}$', uid)]

    print(f"[sync_semantic] Found {len(all_uids)} total pages ({dnp_count} Daily Notes, {len(all_uids) - dnp_count} regular pages).")
    return all_uids

async def pull_many_pages(uids: List[str]) -> List[Optional[Dict]]:
    """
    Pulls full page data for a list of UIDs.
    This is adapted from sync_full.py's pull_many_blocks.
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

    pull_data = {
        "eids": eids_str,
        "selector": selector_str
    }

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

# --- Main Sync Logic ---

async def sync_semantic_graph(clear_existing: bool = False, test_limit: Optional[int] = None):
    """
    Main function to run the semantic sync process.
    """
    print("\n[sync_semantic] Starting semantic graph sync...")
    start_time = time.time()

    # Step 1: Get all page UIDs
    step1_start = time.time()
    all_page_uids = await get_all_page_uids()
    step1_time = time.time() - step1_start
    print(f"[sync_semantic] ⏱️  Getting page UIDs took {step1_time:.2f}s")

    if not all_page_uids:
        print("[sync_semantic] No pages found to process.")
        return

    total_pages = len(all_page_uids)
    print(f"[sync_semantic] Found {total_pages} pages to process.")

    if test_limit:
        print(f"[sync_semantic] TEST MODE: Limiting to first {test_limit} pages.")
        all_page_uids = all_page_uids[:test_limit]
        total_pages = len(all_page_uids)

    # Step 2: Handle collection based on clear_existing flag
    step2_start = time.time()
    if clear_existing:
        print(f"[sync_semantic] Step 2: Deleting and recreating collection '{COLLECTION_NAME}'...")
        from main_semantic import delete_collection
        # Delete the collection completely
        delete_collection(COLLECTION_NAME)
        # Now get a fresh collection
        collection = get_collection(COLLECTION_NAME)
        print(f"[sync_semantic] Fresh collection '{COLLECTION_NAME}' ready")
    else:
        # Normal get or create
        print(f"[sync_semantic] Step 2: Accessing collection '{COLLECTION_NAME}'...")
        collection = get_collection(COLLECTION_NAME)
    step2_time = time.time() - step2_start
    print(f"[sync_semantic] ⏱️  Collection setup took {step2_time:.2f}s")

    # Step 3: Initialize the Chonkie SemanticChunker
    print("[sync_semantic] Step 3: Initializing SemanticChunker...")
    step3_start = time.time()
    chunker = SemanticChunker(
        embedding_model="sentence-transformers/all-MiniLM-L6-v2", # A good default
        threshold=0.6,
        skip_window=1,
        min_chunk_size=50
    )
    step3_time = time.time() - step3_start
    print(f"[sync_semantic] ⏱️  SemanticChunker initialization took {step3_time:.2f}s")

    # Step 4: Process pages in batches
    print(f"[sync_semantic] Step 4: Processing {total_pages} pages in batches of {BATCH_SIZE}...")

    # Global statistics
    total_documents_added = 0
    total_chunks_created = 0
    total_roam_time = 0
    total_processing_time = 0
    total_chromadb_time = 0

    for i in range(0, total_pages, BATCH_SIZE):
        batch_start_time = time.time()
        batch_uids = all_page_uids[i:i + BATCH_SIZE]
        progress = (i + len(batch_uids)) / total_pages * 100
        print(f"\n[sync_semantic] Processing batch {i//BATCH_SIZE + 1}, pages {i+1}-{i+len(batch_uids)} ({progress:.1f}%)...")

        # Time the Roam API call
        roam_start = time.time()
        pages_data = await pull_many_pages(batch_uids)
        roam_time = time.time() - roam_start
        print(f"  ⏱️  Roam pull-many took {roam_time:.2f}s")

        chroma_docs = []
        chroma_metadatas = []
        chroma_ids = []

        # Time the page processing
        processing_start = time.time()
        pages_processed = 0
        batch_chunks_created = 0

        for page_data in pages_data:
            if not page_data:
                continue

            page_title = page_data.get(':node/title', 'Untitled')
            page_uid = page_data.get(':block/uid')

            if not page_title or not page_uid:
                print(f"  ↳ Skipping page without title or UID")
                continue

            # Always index the page itself as a separate document
            chroma_ids.append(str(uuid.uuid4()))
            chroma_docs.append(page_title)
            chroma_metadatas.append({
                "source_uids_json": json.dumps([page_uid]),
                "primary_uid": page_uid,
                "page_title": page_title,
                "page_uid": page_uid,
                "document_type": "page",
                "sync_version": "semantic_v1"
            })

            # Check if page has any children/content before processing
            if not page_data.get(':block/children'):
                print(f"  ↳ Page '{page_title}' has no content (page title still indexed).")
                pages_processed += 1
                continue

            # Pipeline for a single page's content
            linearize_start = time.time()
            linearized_text, uid_map = linearize_page_markdown_style(page_data)
            linearize_time = time.time() - linearize_start

            if not linearized_text.strip():
                # This shouldn't happen now, but keep as safety check
                print(f"  ↳ Page '{page_title}' linearized to empty (unexpected).")
                pages_processed += 1
                continue

            try:
                # Time the chunking
                chunk_start = time.time()
                chunks = chunker.chunk(linearized_text)
                chunk_time = time.time() - chunk_start
                batch_chunks_created += len(chunks)
                print(f"  ↳ Page '{page_title}': created {len(chunks)} chunks (linearize: {linearize_time:.3f}s, chunk: {chunk_time:.3f}s)")

                for chunk in chunks:
                    # Find all source UIDs that overlap with the chunk's character range
                    source_uids = {
                        mapping['uid']
                        for mapping in uid_map
                        if chunk.start_index < mapping['end'] and chunk.end_index > mapping['start']
                    }

                    if not source_uids:
                        continue

                    # Prepare document for ChromaDB
                    chroma_ids.append(str(uuid.uuid4()))
                    chroma_docs.append(chunk.text)
                    chroma_metadatas.append({
                        "source_uids_json": json.dumps(list(source_uids)),
                        "primary_uid": next(iter(source_uids)), # Simple "first seen" strategy
                        "page_title": page_title,
                        "page_uid": page_uid,
                        "chunk_token_count": chunk.token_count,
                        "document_type": "chunk",
                        "sync_version": "semantic_v1"
                    })
            except Exception as e:
                print(f"  ✗ Error chunking page '{page_title}': {e}")

            pages_processed += 1

        processing_time = time.time() - processing_start
        print(f"  ⏱️  Processing {pages_processed} pages took {processing_time:.2f}s")

        chromadb_time = 0
        if chroma_ids:
            try:
                # Time the ChromaDB add operation (THIS IS WHERE EMBEDDINGS HAPPEN!)
                chromadb_start = time.time()
                collection.add(
                    ids=chroma_ids,
                    documents=chroma_docs,
                    metadatas=chroma_metadatas
                )
                chromadb_time = time.time() - chromadb_start
                print(f"  ✓ Added {len(chroma_ids)} documents to collection in {chromadb_time:.2f}s")
                if len(chroma_ids) > 0:
                    print(f"     → {chromadb_time/len(chroma_ids):.3f}s per document (includes embedding)")
                total_documents_added += len(chroma_ids)
            except Exception as e:
                print(f"  ✗ Error adding batch to ChromaDB: {e}")

        batch_total_time = time.time() - batch_start_time
        print(f"  ⏱️  BATCH TOTAL: {batch_total_time:.2f}s (Roam: {roam_time:.2f}s, Process: {processing_time:.2f}s, ChromaDB: {chromadb_time:.2f}s)")

        # Update global statistics
        total_roam_time += roam_time
        total_processing_time += processing_time
        total_chromadb_time += chromadb_time
        total_chunks_created += batch_chunks_created

    # Final statistics
    elapsed_time = time.time() - start_time
    print("\n" + "="*50)
    print("[sync_semantic] SYNC COMPLETE!")
    print(f"  - Time elapsed: {elapsed_time:.2f} seconds")
    print(f"  - Total pages processed: {total_pages}")
    print(f"  - Total chunks created: {total_chunks_created}")
    print(f"  - Total documents added: {total_documents_added}")
    print(f"  - Documents in collection: {collection.count()}")
    print("\n[sync_semantic] Time breakdown:")
    print(f"  - Roam API calls: {total_roam_time:.2f}s ({total_roam_time/elapsed_time*100:.1f}%)")
    print(f"  - Processing (linearize + chunk): {total_processing_time:.2f}s ({total_processing_time/elapsed_time*100:.1f}%)")
    print(f"  - ChromaDB/Embeddings: {total_chromadb_time:.2f}s ({total_chromadb_time/elapsed_time*100:.1f}%)")
    if total_documents_added > 0:
        print(f"  - Average time per document: {total_chromadb_time/total_documents_added:.3f}s")
    print("="*50)


async def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(description='Sync Roam graph to vector database using semantic chunking.')
    parser.add_argument(
        '--clear',
        action='store_true',
        help='Clear all existing embeddings in the semantic collection before syncing.'
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
    # This script is now runnable, assuming dependencies are installed
    # and .env file is set up.
    asyncio.run(main())
    print("[sync_semantic] Done!")