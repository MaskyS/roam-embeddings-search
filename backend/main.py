print("[main.py] Starting imports...")
import chromadb
from fastapi import FastAPI
from pydantic_settings import BaseSettings
from chromadb import Documents, EmbeddingFunction, Embeddings
from chromadb.utils import embedding_functions
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

# 2. Custom Embedding Function for Roam
class RoamAdaptiveContextEmbeddingFunction(EmbeddingFunction):
    def __init__(self, settings: Settings):
        self.settings = settings
        # We instantiate the standard Google EF internally
        self.google_ef = embedding_functions.GoogleGenerativeAiEmbeddingFunction(api_key=self.settings.google_api_key)

    def __call__(self, input: Documents) -> Embeddings:
        # The input to this function will be the Roam block UIDs
        print(f"[Custom EF] Received {len(input)} UIDs to process.")

        # --- Placeholder Logic for now ---
        # In the future, this is where we will:
        # 1. Call Roam API to get context for the input UIDs.
        # 2. Construct the context-enriched documents based on our "Adaptive Context" strategy.
        # For now, we will just embed the UIDs themselves as a test.
        print(f"[Custom EF] Embedding placeholder content for UIDs: {input}")
        
        # We use the internal Google EF to perform the actual embedding
        return self.google_ef(input)

# 3. ChromaDB Client Initialization - Lazy loading
_collection = None

def get_collection():
    """Get or create the ChromaDB collection. Uses lazy initialization."""
    global _collection
    if _collection is None:
        print("[ChromaDB] Initializing connection...")
        roam_embedding_function = RoamAdaptiveContextEmbeddingFunction(settings)
        client = chromadb.HttpClient(host='chromadb', port=8000)
        
        # Verify connection health
        try:
            client.heartbeat()
            print("[ChromaDB] Connection verified via heartbeat")
        except Exception as e:
            print(f"[ChromaDB] Failed to connect: {e}")
            raise
        
        _collection = client.get_or_create_collection(
            name="roam_blocks",
            embedding_function=roam_embedding_function
        )
        print(f"[ChromaDB] Collection initialized with {_collection.count()} documents")
    return _collection
print("[MAIN.PY] Collection ready")

# 4. FastAPI Application
app = FastAPI()

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