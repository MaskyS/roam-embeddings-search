"""
Search + App host for sync router.

FastAPI application for the semantic search strategy. Hosts sync router
mounted from services.sync_service and manages shared app state.
"""

import asyncio
import logging
import os
import re
import time
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict, List, Optional

import httpx
import weaviate
from weaviate.classes.query import Filter, Rerank
from fastapi import Body, Depends, FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from funcy import compact, zipdict
import structlog
from pydantic_settings import BaseSettings

from common.utils import async_retry
from common.logging import configure_logging
from common.config import CONFIG as SYNC_CONFIG
from common.weaviate_factory import create_weaviate_client_from_config
from clients.voyage import VoyageEmbeddingClient
from sync.state.db_persistence import list_recent_runs

configure_logging(json=True)


class Settings(BaseSettings):
    roam_graph_name: str
    roam_api_token: str
    google_api_key: Optional[str] = None
    voyageai_api_key: str
    embedding_provider: str = "voyage_context"
    ollama_url: str = "http://ollama:11434"
    ollama_model: str = "embeddinggemma"
    voyageai_context_model: str = "voyage-context-3"
    voyageai_reranker_model: str = "rerank-2-lite"
    rerank_default_enabled: bool = True


settings = Settings()
WEAVIATE_HTTP_HOST = SYNC_CONFIG.weaviate_http_host
WEAVIATE_HTTP_PORT = SYNC_CONFIG.weaviate_http_port
WEAVIATE_HTTP_SECURE = SYNC_CONFIG.weaviate_http_secure
WEAVIATE_GRPC_HOST = SYNC_CONFIG.weaviate_grpc_host
WEAVIATE_GRPC_PORT = SYNC_CONFIG.weaviate_grpc_port
WEAVIATE_GRPC_SECURE = SYNC_CONFIG.weaviate_grpc_secure


LOGGER = structlog.get_logger(__name__)


class AppContext:
    def __init__(self, client: weaviate.WeaviateAsyncClient, embedder: VoyageEmbeddingClient, settings: Settings) -> None:
        self.client = client
        self.embedder = embedder
        self.settings = settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    LOGGER.info("Initialising Weaviate client")

    client = create_weaviate_client_from_config(
        SYNC_CONFIG,
        headers={"X-VoyageAI-Api-Key": settings.voyageai_api_key},
    )
    try:
        @async_retry(tries=5, timeout=lambda attempt: min(2 ** attempt, 10), errors=(Exception,))
        async def connect_with_retry():
            if SYNC_CONFIG.is_weaviate_cloud:
                LOGGER.info("Connecting to Weaviate Cloud")
            else:
                LOGGER.info("Connecting to Weaviate at %s:%s", WEAVIATE_HTTP_HOST, WEAVIATE_HTTP_PORT)
            await client.connect()

        await connect_with_retry()
        embedder = VoyageEmbeddingClient(
            api_key=settings.voyageai_api_key,
            model=settings.voyageai_context_model,
            input_type="query",
        )
        app.state.ctx = AppContext(client=client, embedder=embedder, settings=settings)
        app.state.sync_lock = asyncio.Lock()
        app.state.sync_job = {
            "status": "idle",
            "run_id": None,
            "mode": None,
            "params": None,
            "started_at": None,
            "finished_at": None,
            "progress": {},
            "summary": {},
            "error": None,
            "task": None,
        }
        LOGGER.info("Weaviate connection established")

        # Initialize auto-sync scheduler
        try:
            from services.scheduler import initialize_scheduler
            from services.sync_service import _run_sync_job

            # Create sync trigger function guarded against concurrent runs
            async def trigger_auto_sync(mode: str = "since"):
                """Trigger an automatic sync job if none is currently running/cancelling."""
                # Determine backend directory: go up from services/ to backend/
                _this_file = os.path.abspath(__file__)
                _backend_dir = os.path.dirname(os.path.dirname(_this_file))
                _default = os.path.join(_backend_dir, "data", "sync_state.json")
                DEFAULT_STATE_FILE = os.getenv("SYNC_STATE_FILE", _default)
                sync_kwargs = {
                    "clear_existing": False,
                    "test_limit": None,
                    "recreate_collection": False,
                    "state_file": DEFAULT_STATE_FILE,
                    "resume": False,
                    "since": None,  # Will use last successful run time
                }

                # Guard against concurrent syncs
                lock: asyncio.Lock = app.state.sync_lock
                job: Dict[str, Any] = app.state.sync_job
                async with lock:
                    if job.get("status") in {"running", "cancelling"}:
                        LOGGER.info("Auto-sync skipped: job already in progress", status=job.get("status"))
                        return
                    # Mirror /sync/start minimal state to avoid overlapping runs
                    job.update(
                        {
                            "status": "running",
                            "mode": mode,
                            "params": {
                                "clear_existing": False,
                                "recreate_collection": False,
                                "resume": False,
                                "state_file": DEFAULT_STATE_FILE,
                                "since": None,
                                "limit": None,
                            },
                            "started_at": datetime.utcnow().isoformat(),
                            "finished_at": None,
                            "progress": {},
                            "summary": {},
                            "error": None,
                        }
                    )
                    task = asyncio.create_task(_run_sync_job(app, sync_kwargs))
                    job["task"] = task

            scheduler = await initialize_scheduler(trigger_auto_sync)
            app.state.scheduler = scheduler
            LOGGER.info("Auto-sync scheduler initialized")
        except Exception as exc:
            LOGGER.error("Failed to initialize scheduler", error=str(exc))
            # Don't fail startup if scheduler fails

        yield
    finally:
        # Shutdown scheduler
        try:
            from services.scheduler import shutdown_scheduler
            await shutdown_scheduler()
        except Exception:
            pass

        ctx: Optional[AppContext] = getattr(app.state, "ctx", None)
        job_state: Dict[str, Any] = getattr(app.state, "sync_job", {})
        task = job_state.get("task") if isinstance(job_state, dict) else None
        if task:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            job_state["task"] = None
            job_state["status"] = "cancelled"
            job_state["finished_at"] = time.time()
        if ctx and ctx.client.is_connected():
            await ctx.client.close()
            LOGGER.info("Weaviate connection closed")
        if hasattr(app.state, "ctx"):
            delattr(app.state, "ctx")


app = FastAPI(
    title="Roam Semantic Search - Semantic Strategy",
    description="Semantic search backend using Weaviate and VoyageAI.",
    lifespan=lifespan,
)

# CORS: allow Roam domains and localhost with any port.
# Note: Starlette CORS does not support wildcard patterns in allow_origins;
# use allow_origin_regex for subdomains and port wildcards.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://roamresearch.com",
        "https://app.roamresearch.com",
        "https://www.roamresearch.com",
    ],
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\\d+)?$|^https://([a-zA-Z0-9-]+\.)?roamresearch\.com$",
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


def highlight_matches(text: str, query: str) -> str:
    if not text or not query:
        return text
    try:
        highlighted_text = re.sub(
            f"({re.escape(query)})",
            r"^^\1^^",
            text,
            flags=re.IGNORECASE
        )
        return highlighted_text
    except re.error:
        return text


async def get_context(request: Request):
    ctx = getattr(request.app.state, "ctx", None)
    if not ctx:
        raise HTTPException(status_code=503, detail="Weaviate is not ready")
    return ctx


@async_retry(tries=3, timeout=lambda attempt: min(2 ** (attempt - 1), 4.0), errors=(httpx.HTTPError,))
async def _pull_many_blocks(uids: List[str]) -> List[Optional[Dict]]:
    url = f"https://api.roamresearch.com/api/graph/{settings.roam_graph_name}/pull-many"
    headers = {
        "X-Authorization": f"Bearer {settings.roam_api_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    selector_str = "[:block/uid :block/string :node/title {:block/_children [:block/uid :block/string :node/title]}]"
    eids_list = ' '.join([f'[:block/uid "{uid}"]' for uid in uids])
    payload = {"eids": f"[{eids_list}]", "selector": selector_str}

    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json().get("result", [])


async def pull_many_blocks_for_context(uids: List[str]) -> Dict[str, Dict]:
    if not uids:
        return {}
    try:
        results = await _pull_many_blocks(uids)
    except httpx.HTTPError:
        return {}
    pairs = zipdict(uids, results or [])
    return {uid: block for uid, block in pairs.items() if block}


@app.get("/health")
async def health_check():
    """Simple health check endpoint that always returns 200 OK."""
    return {"status": "healthy"}


@app.get("/ping")
async def ping():
    """
    Ping endpoint that pings the chunker service to keep both services alive.
    Useful for preventing free tier services from spinning down.
    """
    chunker_url = SYNC_CONFIG.chunker_url
    chunker_hostport = os.getenv("CHUNKER_HOSTPORT", "not set")
    LOGGER.info(
        "Ping endpoint called",
        chunker_url=chunker_url,
        chunker_hostport=chunker_hostport,
        chunker_service_url_env=os.getenv("CHUNKER_SERVICE_URL", "not set"),
    )
    try:
        # Ping the chunker service
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{chunker_url}/health")
            response.raise_for_status()
            chunker_data = response.json()

        return {
            "status": "ok",
            "message": "Backend and chunker services are alive",
            "chunker_url": chunker_url,
            "chunker_hostport": chunker_hostport,
            "chunker_service_url_env": os.getenv("CHUNKER_SERVICE_URL", "not set"),
            "chunker_status": chunker_data.get("status", "unknown"),
            "chunker_loaded": chunker_data.get("chunker_loaded", False),
        }
    except Exception as e:
        LOGGER.error("Failed to ping chunker service", error=str(e), chunker_url=chunker_url)
        return {
            "status": "ok",
            "message": "Backend is alive, but chunker ping failed",
            "chunker_url": chunker_url,
            "chunker_hostport": chunker_hostport,
            "chunker_service_url_env": os.getenv("CHUNKER_SERVICE_URL", "not set"),
            "chunker_error": str(e),
        }


@app.get("/")
async def read_root(ctx=Depends(get_context)):
    # Be resilient: return a 200 with readiness info even if schema is missing
    weaviate_ready = False
    collection_exists = False
    total_count = None
    try:
        weaviate_ready = await ctx.client.is_ready()
        if weaviate_ready:
            try:
                collection_exists = await ctx.client.collections.exists(SYNC_CONFIG.collection_name)
            except Exception:
                collection_exists = False
            if collection_exists:
                try:
                    collection = ctx.client.collections.get(SYNC_CONFIG.collection_name)
                    agg = await collection.aggregate.over_all(total_count=True)
                    total_count = getattr(agg, "total_count", None)
                except Exception:
                    total_count = None
    except Exception:
        weaviate_ready = False
    return {
        "message": "Roam Semantic Search Backend is running.",
        "roam_graph_name": ctx.settings.roam_graph_name,
        "collection_name": SYNC_CONFIG.collection_name,
        "collection_count": total_count,
        "weaviate_ready": weaviate_ready,
        "collection_exists": collection_exists,
    }


@app.get("/search")
async def search(
    q: str = Query(..., description="Search query"),
    limit: int = Query(10, ge=1, le=50),
    alpha: float = Query(0.5, ge=0, le=1),
    exclude_pages: bool = Query(False),
    rerank: bool = Query(True),
    rerank_query: Optional[str] = Query(None),
    rerank_limit: Optional[int] = Query(None),
    ctx=Depends(get_context),
):
    start_time = time.time()
    if not q or not q.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    if not await ctx.client.is_ready():
        raise HTTPException(status_code=503, detail="Weaviate is not ready")

    try:
        query_vector = await ctx.embedder.embed_query(q)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to embed query: {e}")

    collection = ctx.client.collections.get(SYNC_CONFIG.collection_name)

    filters = Filter.by_property("document_type").equal("chunk") if exclude_pages else None
    actual_rerank_query = rerank_query or q
    reranking = None
    fetch_limit = limit
    if rerank:
        fetch_limit = rerank_limit or limit
        reranking = Rerank(prop="chunk_text_preview", query=actual_rerank_query)

    try:
        query_params = compact(
            {
                "query": q,
                "vector": query_vector,
                "alpha": alpha,
                "limit": fetch_limit,
                "filters": filters,
                "rerank": reranking,
                "return_metadata": ["score"],
            }
        )
        results = await collection.query.hybrid(**query_params)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Weaviate search failed: {e}")

    if not results.objects:
        return {"query": q, "results": [], "count": 0}

    primary_uids = [obj.properties.get("primary_uid") for obj in results.objects]
    block_data_map = await pull_many_blocks_for_context(primary_uids)

    formatted_results = []
    for obj in results.objects:
        metadata = obj.properties
        primary_uid = metadata.get("primary_uid")
        block_data = block_data_map.get(primary_uid)
        parent_text = ""
        parent_uid = None
        if block_data and block_data.get(":block/_children"):
            parent_data = block_data[":block/_children"]
            if isinstance(parent_data, list):
                parent_data = parent_data[0] if parent_data else None
            if parent_data:
                parent_text = parent_data.get(":node/title") or parent_data.get(":block/string", "")
                parent_uid = parent_data.get(":block/uid")

        formatted_results.append(
            {
                "uid": primary_uid,
                "parent_uid": parent_uid,
                "page_uid": metadata.get("page_uid"),
                "similarity": round(obj.metadata.score, 4) if obj.metadata and obj.metadata.score is not None else 0.0,
                "page_title": metadata.get("page_title", ""),
                "parent_text": parent_text,
                "chunk_text_preview": highlight_matches(metadata.get("chunk_text_preview", ""), q),
                "document_type": metadata.get("document_type", "chunk"),
            }
        )

    if rerank and rerank_limit and len(formatted_results) > limit:
        formatted_results = formatted_results[:limit]

    return {
        "query": q,
        "results": formatted_results,
        "count": len(formatted_results),
        "execution_time": round(time.time() - start_time, 3),
        "reranked": rerank,
        "rerank_query": actual_rerank_query if rerank else None,
    }


# Mount sync router
from services.sync_service import router as sync_router  # noqa: E402

app.include_router(sync_router)
