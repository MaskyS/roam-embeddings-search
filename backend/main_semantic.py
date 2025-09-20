"""
main_semantic.py

FastAPI application for the new semantic search strategy.
This service is completely independent of main.py and interacts only with
the 'roam_semantic_chunks' collection in ChromaDB.
"""
print("[main_semantic] Starting imports...")
import chromadb
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings
from chromadb.utils import embedding_functions
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
from typing import Optional, List, Dict
import httpx
import re
import time
import json

# Add backend to path to allow local imports
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from roam import query_roam

# --- Settings & ChromaDB Client ---

class Settings(BaseSettings):
    roam_graph_name: str
    roam_api_token: str
    google_api_key: str
    voyageai_api_key: str
    embedding_provider: str = "voyageai"  # Options: "ollama", "google", or "voyageai"
    ollama_url: str = "http://ollama:11434"  # Default Ollama URL in Docker
    ollama_model: str = "embeddinggemma"  # Default Ollama embedding model
    voyageai_model: str = "voyage-3.5-lite"  # Default VoyageAI model

settings = Settings()

_collections: Dict[str, chromadb.Collection] = {}
_chroma_client = None
COLLECTION_NAME = "roam_semantic_chunks" # Default for this service

def get_collection(name: str) -> chromadb.Collection:
    """Get or create a ChromaDB collection by name. Uses lazy initialization."""
    global _collections, _chroma_client
    if name not in _collections:
        print(f"[ChromaDB] Initializing connection for collection: {name}...")

        if _chroma_client is None:
            _chroma_client = chromadb.HttpClient(host='chromadb', port=8000)
            try:
                _chroma_client.heartbeat()
            except Exception as e:
                print(f"[ChromaDB] Failed to connect: {e}")
                _chroma_client = None # Reset on failure
                raise

        # Choose embedding function based on provider setting
        if settings.embedding_provider == "google":
            embedding_function = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
                api_key=settings.google_api_key,
                model_name="gemini-embedding-001"
            )
            print(f"[ChromaDB] Using Google Gemini embeddings")
        elif settings.embedding_provider == "ollama":
            embedding_function = OllamaEmbeddingFunction(
                url=settings.ollama_url,
                model_name=settings.ollama_model
            )
            print(f"[ChromaDB] Using Ollama embeddings: {settings.ollama_model} at {settings.ollama_url}")
        else:  # Default to VoyageAI
            embedding_function = embedding_functions.VoyageAIEmbeddingFunction(
                api_key=settings.voyageai_api_key,
                model_name=settings.voyageai_model
            )
            print(f"[ChromaDB] Using VoyageAI embeddings: {settings.voyageai_model}")

        _collections[name] = _chroma_client.get_or_create_collection(
            name=name,
            embedding_function=embedding_function
        )
        print(f"[ChromaDB] Collection '{name}' initialized with {_collections[name].count()} documents")
    return _collections[name]

def delete_collection(name: str) -> None:
    """Delete a ChromaDB collection and remove it from cache."""
    global _collections, _chroma_client

    # Ensure client is initialized
    if _chroma_client is None:
        _chroma_client = chromadb.HttpClient(host='chromadb', port=8000)
        try:
            _chroma_client.heartbeat()
        except Exception as e:
            print(f"[ChromaDB] Failed to connect: {e}")
            _chroma_client = None
            raise

    # Delete the collection from ChromaDB
    try:
        _chroma_client.delete_collection(name)
        print(f"[ChromaDB] Deleted collection '{name}'")
    except Exception as e:
        print(f"[ChromaDB] Error deleting collection '{name}': {e}")
        # Don't re-raise if collection doesn't exist
        if "does not exist" not in str(e).lower():
            raise

    # Remove from cache
    if name in _collections:
        del _collections[name]
        print(f"[ChromaDB] Removed collection '{name}' from cache")

# --- FastAPI Application ---

app = FastAPI(
    title="Roam Semantic Search - Semantic Strategy",
    description="A separate service for handling the Chonkie-based semantic search strategy."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://roamresearch.com", "https://*.roamresearch.com", "http://localhost:*", "http://127.0.0.1:*"]
,
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
    # This selector is designed to get the block's text and its parent's title for context.
    selector_str = "[:block/uid :block/string :node/title {:block/parents [:block/uid :block/string :node/title]}]"
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
def read_root():
    return {
        "message": "Roam Semantic Search (Semantic Strategy) Backend is running.",
        "collection_name": COLLECTION_NAME,
        "collection_count": get_collection(COLLECTION_NAME).count()
    }

@app.get("/search")
async def search(
    q: str = Query(..., description="Search query"),
    limit: int = Query(10, ge=1, le=50, description="Number of results to return"),
    exclude_pages: bool = Query(False, description="Exclude page results, only show chunks")
):
    """
    Performs semantic search on the pre-chunked documents.
    """
    start_time = time.time()
    if not q or not q.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    collection = get_collection(COLLECTION_NAME)

    # Build where filter for ChromaDB based on exclude_pages
    where_filter = None
    if exclude_pages:
        # Only return chunks, not pages
        where_filter = {"document_type": {"$eq": "chunk"}}

    results = collection.query(
        query_texts=[q],
        n_results=limit,
        where=where_filter,
        include=["metadatas", "documents", "distances"]  # Ensure distances are included
    )

    if not results['ids'] or not results['ids'][0]:
        return {"query": q, "results": [], "count": 0}

    # Extract primary UIDs to fetch their context
    primary_uids = [meta['primary_uid'] for meta in results['metadatas'][0]]
    block_data_list = await pull_many_blocks_for_context(primary_uids)
    block_data_map = {b.get(':block/uid'): b for b in block_data_list if b}

    formatted_results = []
    for i, chunk_id in enumerate(results['ids'][0]):
        metadata = results['metadatas'][0][i]
        chunk_text = results['documents'][0][i]
        distance = results['distances'][0][i]
        primary_uid = metadata.get("primary_uid")

        # Calculate similarity from distance (assuming L2 distance, where 0 is identical)
        similarity = 1 - (distance / 2)

        block_data = block_data_map.get(primary_uid)
        parent_text = ""
        if block_data and block_data.get(':block/parents'):
            parent_data = block_data[':block/parents'][0]
            parent_text = parent_data.get(':node/title') or parent_data.get(':block/string', '')

        formatted_results.append({
            "uid": primary_uid, # The UID to navigate to
            "similarity": round(similarity, 4),
            "page_title": metadata.get("page_title", ""),
            "parent_text": parent_text,
            "chunk_text_preview": highlight_matches(chunk_text, q),
            "document_type": metadata.get("document_type", "chunk"),  # "page" or "chunk"
        })

    return {
        "query": q,
        "results": formatted_results,
        "count": len(formatted_results),
        "execution_time": round(time.time() - start_time, 3)
    }
