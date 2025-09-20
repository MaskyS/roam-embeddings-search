print("[main.py] Starting imports...")
import chromadb
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings
from chromadb.utils import embedding_functions
from typing import Optional, List, Dict
import httpx
import re
import time
print("[main.py] ChromaDB imports complete")

from roam import query_roam
print("[main.py] Roam import complete")

# 1. Settings Management
# Pydantic will automatically load variables from the environment (provided by docker-compose)
class Settings(BaseSettings):
    roam_graph_name: str
    roam_api_token: str
    google_api_key: str

print("[main.py] Creating Settings...")
settings = Settings()
print(f"[main.py] Settings created: graph={settings.roam_graph_name}")

# 2. ChromaDB Client Initialization - Lazy loading
_collection = None

def get_collection():
    """Get or create the ChromaDB collection. Uses lazy initialization."""
    global _collection
    if _collection is None:
        print("[ChromaDB] Initializing connection...")

        # Use Google's embedding function directly on context documents
        # The sync scripts will pass fully constructed context as documents
        google_ef = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
            api_key=settings.google_api_key,
            model_name="gemini-embedding-001"  # Latest Gemini embedding model
        )

        client = chromadb.HttpClient(host='chromadb', port=8000)

        # Verify connection health
        try:
            client.heartbeat()
            print("[ChromaDB] Connection verified via heartbeat")
        except Exception as e:
            print(f"[ChromaDB] Failed to connect: {e}")
            raise

        # Get or create collection
        _collection = client.get_or_create_collection(
            name="roam_blocks",
            embedding_function=google_ef
        )
        print(f"[ChromaDB] Collection initialized with {_collection.count()} documents")
    return _collection
print("[MAIN.PY] Collection ready")

# 4. FastAPI Application
app = FastAPI()

# Configure CORS to allow requests from Roam Research
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://roamresearch.com",
        "https://*.roamresearch.com",  # Subdomains
        "https://relemma-git-roam-app-store.roamresearch.com",  # Roam Depot dev
        "https://relemma-git-new-renderblockadditions.roamresearch.com",
        "http://localhost:*",  # Local development
        "http://127.0.0.1:*",  # Local development
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

@app.get("/")
def read_root():
    return {
        "message": "Roam Semantic Search Backend is running.",
        "roam_graph_name": settings.roam_graph_name,
        "chroma_collection_count": get_collection().count()
    }

@app.post("/sync")
async def trigger_sync():
    dummy_uid = "_d2aVd1rZ"
    print(f"Sync triggered. Adding dummy UID: {dummy_uid}")
    get_collection().add(ids=[dummy_uid], documents=[dummy_uid])
    return {"message": "Sync process completed.", "uids_added": [dummy_uid]}

@app.get("/health-check")
async def health_check():
    """Performs a simple query to check the Roam API connection."""
    print("Performing Roam API health check...")
    query = "[:find (count ?uid) . :where [?b :block/uid ?uid]]"
    result = await query_roam(
        token=settings.roam_api_token,
        graph_name=settings.roam_graph_name,
        query=query
    )
    if result and result.get('result') is not None:
        return {"status": "ok", "message": "Roam API is responsive.", "block_count": result['result']}
    else:
        return {"status": "error", "message": "Failed to connect to Roam API."}

async def pull_many_blocks(uids: List[str]) -> List[Optional[Dict]]:
    """Pull multiple blocks at once using pull-many for efficiency"""
    if not uids:
        return []

    url = f"https://api.roamresearch.com/api/graph/{settings.roam_graph_name}/pull-many"
    headers = {
        "X-Authorization": f"Bearer {settings.roam_api_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    # Build eids string for pull-many - must be properly formatted Clojure vector
    eids_list = " ".join([f'[:block/uid "{uid}"]' for uid in uids])
    eids_str = f"[{eids_list}]"

    # Simpler selector for search results
    selector_str = "[:block/uid :block/string :node/title {:block/parents [:block/uid :block/string :node/title]} {:block/refs [:block/uid :block/string]}]"

    pull_data = {
        "eids": eids_str,
        "selector": selector_str
    }

    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        try:
            response = await client.post(url, headers=headers, json=pull_data)
            if response.status_code == 200:
                data = response.json()
                return data.get('result', [])
            else:
                print(f"Pull-many failed with status {response.status_code}")
                return [None] * len(uids)
        except Exception as e:
            print(f"Pull-many error: {e}")
            return [None] * len(uids)

def highlight_matches(text: str, query: str, max_length: int = 200) -> Dict:
    """Find and highlight query matches in text"""
    if not text or not query:
        return {"text": text[:max_length] if text else "", "highlights": []}

    # Create case-insensitive pattern for each word in query
    query_words = query.lower().split()
    highlights = []

    # Find all matches
    for word in query_words:
        if len(word) < 2:  # Skip very short words
            continue
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        for match in pattern.finditer(text):
            highlights.append({
                "start": match.start(),
                "end": match.end(),
                "word": match.group()
            })

    # Sort highlights by position
    highlights.sort(key=lambda x: x["start"])

    # Find best snippet around first match or start of text
    if highlights:
        first_match = highlights[0]["start"]
        snippet_start = max(0, first_match - 50)
        snippet_end = min(len(text), snippet_start + max_length)
    else:
        snippet_start = 0
        snippet_end = min(len(text), max_length)

    snippet = text[snippet_start:snippet_end]
    if snippet_start > 0:
        snippet = "..." + snippet
    if snippet_end < len(text):
        snippet = snippet + "..."

    # Adjust highlight positions relative to snippet
    adjusted_highlights = []
    offset = snippet_start - (3 if snippet_start > 0 else 0)  # Account for "..."
    for h in highlights:
        if h["start"] >= snippet_start and h["end"] <= snippet_end:
            adjusted_highlights.append({
                "start": h["start"] - offset,
                "end": h["end"] - offset,
                "word": h["word"]
            })

    return {
        "text": snippet,
        "highlights": adjusted_highlights
    }

@app.get("/search")
async def search(
    q: str = Query(..., description="Search query"),
    limit: int = Query(10, ge=1, le=50, description="Number of results to return"),
    threshold: Optional[float] = Query(None, ge=0, le=1, description="Similarity threshold (0-1)"),
    block_type: Optional[str] = Query(None, regex="^(parent|leaf)$", description="Filter by block type")
):
    """
    Semantic search across Roam blocks.
    Returns blocks most similar to the query with full block data from Roam.
    """
    start_time = time.time()

    # Validate query
    if not q or not q.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    # Truncate query if too long
    MAX_QUERY_LENGTH = 1000
    if len(q) > MAX_QUERY_LENGTH:
        q = q[:MAX_QUERY_LENGTH]

    print(f"[Search] Query: '{q}', limit: {limit}, threshold: {threshold}, block_type: {block_type}")

    # Get collection
    try:
        collection = get_collection()
    except Exception as e:
        print(f"[Search] Failed to get collection: {e}")
        raise HTTPException(status_code=500, detail="Search service unavailable")

    # Build where clause for filtering
    where = {}
    if block_type:
        where["block_type"] = block_type

    # Query ChromaDB
    try:
        results = collection.query(
            query_texts=[q],
            n_results=limit,
            where=where if where else None,
            include=["metadatas", "distances", "documents"]
        )
    except Exception as e:
        print(f"[Search] ChromaDB query error: {e}")
        raise HTTPException(status_code=500, detail="Search query failed")

    # Check if we have results
    if not results['ids'] or not results['ids'][0]:
        return {
            "query": q,
            "results": [],
            "count": 0,
            "execution_time": time.time() - start_time
        }

    # Extract UIDs for pull-many
    result_uids = results['ids'][0]

    # Pull full block data from Roam
    print(f"[Search] Pulling {len(result_uids)} blocks from Roam...")
    block_data_list = await pull_many_blocks(result_uids)

    # Format results
    formatted_results = []
    for i in range(len(result_uids)):
        uid = result_uids[i]
        distance = results['distances'][0][i]

        # Apply threshold if specified (distance is 0-2, where 0 is perfect match)
        # Convert to similarity (0-1 scale where 1 is perfect match)
        similarity = 1 - (distance / 2)  # Normalize assuming max distance is 2
        if threshold and similarity < threshold:
            continue

        # Get metadata and context
        metadata = results['metadatas'][0][i]
        context_used = results['documents'][0][i]

        # Get full block data
        block_data = block_data_list[i] if i < len(block_data_list) else None

        # Extract current block text
        if block_data:
            current_text = block_data.get(':block/string', '') or block_data.get(':node/title', '')
            parents = block_data.get(':block/parents', [])
            parent_text = parents[0].get(':node/title', '') or parents[0].get(':block/string', '') if parents else None
        else:
            current_text = metadata.get('original_text', '')
            parent_text = None

        # Generate highlights
        text_highlights = highlight_matches(current_text, q)
        context_highlights = highlight_matches(context_used, q, max_length=300)

        formatted_results.append({
            "uid": uid,
            "similarity": round(similarity, 4),
            "distance": round(distance, 4),
            "block": {
                "text": current_text,
                "text_preview": text_highlights,
                "parent_text": parent_text,
                "type": metadata.get('block_type', 'unknown'),
                "is_page": metadata.get('is_page', 'False') == 'True',
                "has_children": metadata.get('has_children', 'False') == 'True'
            },
            "context": {
                "used_for_embedding": context_used[:500],  # First 500 chars
                "preview": context_highlights
            },
            "metadata": metadata
        })

    execution_time = time.time() - start_time
    print(f"[Search] Completed in {execution_time:.2f}s, returning {len(formatted_results)} results")

    return {
        "query": q,
        "results": formatted_results,
        "count": len(formatted_results),
        "execution_time": round(execution_time, 3)
    }
