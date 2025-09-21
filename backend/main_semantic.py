"""
main_semantic.py

FastAPI application for the new semantic search strategy.
This service is completely independent of main.py and interacts only with
the 'RoamSemanticChunks' collection in Weaviate.
"""
print("[main_semantic] Starting imports...")
import weaviate
import voyageai
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings
from typing import Optional, List, Dict
import httpx
import re
import time
import json
from contextlib import asynccontextmanager

# Add backend to path to allow local imports
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from roam import query_roam

# --- Settings & Weaviate Client ---

class Settings(BaseSettings):
    roam_graph_name: str
    roam_api_token: str
    google_api_key: str # Kept for potential future use
    voyageai_api_key: str
    embedding_provider: str = "voyage_context"  # New default
    ollama_url: str = "http://ollama:11434"
    ollama_model: str = "embeddinggemma"
    voyageai_context_model: str = "voyage-context-3" # Contextual model for both queries and documents
    voyageai_reranker_model: str = "rerank-2-lite" # Reranker model
    rerank_default_enabled: bool = True # Enable reranking by default

settings = Settings()
voyageai.api_key = settings.voyageai_api_key
voyage_client = voyageai.Client()

# --- Weaviate Client Initialization ---

weaviate_client: Optional[weaviate.WeaviateAsyncClient] = None
COLLECTION_NAME = "RoamSemanticChunks" # Weaviate class names are capitalized

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle Weaviate client startup and shutdown."""
    global weaviate_client
    print("[Weaviate] Initializing connection...")
    # In a docker-compose setup, the service name is the hostname
    weaviate_client = weaviate.use_async_with_custom(
        http_host="weaviate",
        http_port=8080,
        http_secure=False,
        grpc_host="weaviate",
        grpc_port=50051,
        grpc_secure=False,
        headers={
            "X-VoyageAI-Api-Key": settings.voyageai_api_key
        }
    )
    try:
        await weaviate_client.connect()
        print("[Weaviate] Connection successful.")
        yield
    finally:
        if weaviate_client and weaviate_client.is_connected():
            await weaviate_client.close()
            print("[Weaviate] Connection closed.")

async def delete_collection(name: str) -> None:
    """Delete a Weaviate collection."""
    # This function is intended to be called from the sync script, which will have its own client.
    # This avoids issues with async event loops if called from a sync context.
    client = weaviate.connect_to_local(port=8080, grpc_port=50051)
    try:
        if client.collections.exists(name):
            client.collections.delete(name)
            print(f"[Weaviate] Deleted collection '{name}'")
    except Exception as e:
        print(f"[Weaviate] Error deleting collection '{name}': {e}")
        raise
    finally:
        client.close()


# --- FastAPI Application ---

app = FastAPI(
    title="Roam Semantic Search - Semantic Strategy",
    description="A separate service for handling the Chonkie-based semantic search strategy with Weaviate.",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://roamresearch.com", "https://*.roamresearch.com", "http://localhost:*", "http://127.0.0.1:*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# --- Helper Functions ---

async def pull_many_blocks_for_context(uids: List[str]) -> List[Optional[Dict]]:
    """Pulls block context for search results. Uses a minimal selector."""
    if not uids:
        return []

    url = f"https://api.roamresearch.com/api/graph/{settings.roam_graph_name}/pull-many"
    headers = {
        "X-Authorization": f"Bearer {settings.roam_api_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    # This selector uses :block/_children reverse lookup to get the immediate parent
    # :block/_children asks "who has me as a child?" which gives us the direct parent
    selector_str = "[:block/uid :block/string :node/title {:block/_children [:block/uid :block/string :node/title]}]"
    eids_list = ' '.join([f'[:block/uid "{uid}"]' for uid in uids])
    pull_data = {
        "eids": f"[{eids_list}]",
        "selector": selector_str
    }

    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        try:
            response = await client.post(url, headers=headers, json=pull_data)
            return response.json().get('result', []) if response.status_code == 200 else [None] * len(uids)
        except Exception as e:
            print(f"Pull-many error: {e}")
            return [None] * len(uids)

def highlight_matches(text: str, query: str) -> str:
    """
    Finds all case-insensitive matches of a query in a text and wraps them
    with Roam's ^^highlight^^ syntax.
    """
    if not text or not query:
        return text
    try:
        # We escape the query to handle special regex characters.
        # The parentheses create a capturing group.
        # In the replacement string, \1 refers to the text captured by this group.
        highlighted_text = re.sub(
            f"({re.escape(query)})",
            r"^^\1^^",
            text,
            flags=re.IGNORECASE
        )
        return highlighted_text
    except re.error:
        # If the query is an invalid regex, just return the original text
        return text

# --- API Endpoints ---

@app.get("/")
async def read_root():
    if not weaviate_client or not weaviate_client.is_ready():
         raise HTTPException(status_code=503, detail="Weaviate is not ready")
    collection = weaviate_client.collections.get(COLLECTION_NAME)
    count = await collection.aggregate.over_all(total_count=True)
    return {
        "message": "Roam Semantic Search (Semantic Strategy) Backend is running with Weaviate.",
        "roam_graph_name": settings.roam_graph_name,
        "collection_name": COLLECTION_NAME,
        "collection_count": count.total_count
    }

@app.get("/search")
async def search(
    q: str = Query(..., description="Search query"),
    limit: int = Query(10, ge=1, le=50, description="Number of results to return"),
    alpha: float = Query(0.5, ge=0, le=1, description="Balance between keyword and vector search. 0 for pure keyword, 1 for pure vector."),
    exclude_pages: bool = Query(False, description="Exclude page results, only show chunks"),
    rerank: bool = Query(settings.rerank_default_enabled, description="Enable result reranking using VoyageAI"),
    rerank_query: Optional[str] = Query(None, description="Custom query for reranking, if different from search query"),
    rerank_limit: Optional[int] = Query(None, description="Number of top results to rerank (None = all results)")
):
    """
    Performs hybrid search on the pre-chunked documents using Weaviate.
    """
    start_time = time.time()
    if not q or not q.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    if not weaviate_client or not weaviate_client.is_ready():
        raise HTTPException(status_code=503, detail="Weaviate is not ready")

    try:
        # For queries, use contextualized_embed with single-element list
        query_result = voyage_client.contextualized_embed([[q]], model=settings.voyageai_context_model, input_type="query")
        query_vector = query_result.results[0].embeddings[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to embed query with VoyageAI: {e}")

    collection = weaviate_client.collections.get(COLLECTION_NAME)

    # Build filter for Weaviate based on exclude_pages
    filters = None
    if exclude_pages:
        # Only return chunks, not pages
        from weaviate.classes.query import Filter
        filters = Filter.by_property("document_type").equal("chunk")

    # Build reranking configuration
    reranking = None
    if rerank:
        from weaviate.classes.query import Rerank
        # Use custom rerank_query if provided, otherwise use the original query
        actual_rerank_query = rerank_query if rerank_query else q
        # If rerank_limit is specified, first fetch more results then rerank subset
        fetch_limit = rerank_limit if rerank_limit else limit
        reranking = Rerank(
            prop="chunk_text_preview",
            query=actual_rerank_query
        )
    else:
        fetch_limit = limit

    try:
        results = await collection.query.hybrid(
            query=q,
            vector=query_vector,
            alpha=alpha,
            limit=fetch_limit,
            filters=filters,
            rerank=reranking,
            return_metadata=["score"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Weaviate search failed: {e}")


    if not results.objects:
        return {"query": q, "results": [], "count": 0}

    # Extract primary UIDs to fetch their context
    primary_uids = [obj.properties.get('primary_uid') for obj in results.objects]
    block_data_list = await pull_many_blocks_for_context(primary_uids)
    block_data_map = {b.get(':block/uid'): b for b in block_data_list if b}

    formatted_results = []
    for obj in results.objects:
        metadata = obj.properties
        primary_uid = metadata.get("primary_uid")

        block_data = block_data_map.get(primary_uid)
        parent_text = ""
        parent_uid = None
        if block_data and block_data.get(':block/_children'):
            # :block/_children gives us the immediate parent
            parent_data = block_data[':block/_children']
            # Handle both single object and list responses
            if isinstance(parent_data, list):
                parent_data = parent_data[0] if parent_data else None
            if parent_data:
                parent_text = parent_data.get(':node/title') or parent_data.get(':block/string', '')
                parent_uid = parent_data.get(':block/uid')

        formatted_results.append({
            "uid": primary_uid,
            "parent_uid": parent_uid,
            "page_uid": metadata.get("page_uid"),
            "similarity": round(obj.metadata.score, 4) if obj.metadata and obj.metadata.score is not None else 0.0,
            "page_title": metadata.get("page_title", ""),
            "parent_text": parent_text,
            "chunk_text_preview": highlight_matches(metadata.get("chunk_text_preview", ""), q),
            "document_type": metadata.get("document_type", "chunk"),
        })

    # Limit results if rerank_limit was specified and we got more
    if rerank and rerank_limit and len(formatted_results) > limit:
        formatted_results = formatted_results[:limit]

    return {
        "query": q,
        "results": formatted_results,
        "count": len(formatted_results),
        "execution_time": round(time.time() - start_time, 3),
        "reranked": rerank,
        "rerank_query": actual_rerank_query if rerank else None
    }