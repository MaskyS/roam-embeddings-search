"""
main_semantic.py

FastAPI application for the new semantic search strategy.
This service is completely independent of main.py and interacts only with
the 'RoamSemanticChunks' collection in Weaviate.
"""

import asyncio
import logging
import os
import re
import time
import uuid
from contextlib import asynccontextmanager, suppress
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

import httpx
import weaviate
from weaviate.classes.query import Filter, Rerank
from fastapi import Body, Depends, FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from funcy import compact, decorator, silent, zipdict
from pydantic_settings import BaseSettings

# Add backend to path to allow local imports
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from semantic_sync import VoyageEmbeddingClient
from utils import async_retry


@dataclass(frozen=True)
class AppContext:
    """Runtime dependencies exposed to request handlers."""

    client: weaviate.WeaviateAsyncClient
    embedder: VoyageEmbeddingClient
    settings: "Settings"


@decorator
async def async_retry(call, *, tries: int = 3, timeout=0.0, errors=(Exception,), filter_errors=None):
    """Retry decorator for async callables, mirroring funcy's retry semantics."""

    attempt = 0
    while True:
        try:
            return await call()
        except errors as exc:  # type: ignore[arg-type]
            if filter_errors and not filter_errors(exc):
                raise
            attempt += 1
            if attempt >= tries:
                raise
            delay = timeout(attempt) if callable(timeout) else timeout
            if delay:
                await asyncio.sleep(delay)
            LOGGER.debug("Retrying async call %s (attempt %s/%s)", call._func.__name__, attempt + 1, tries)

LOGGER = logging.getLogger(__name__)

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
WEAVIATE_HTTP_HOST = os.getenv("WEAVIATE_HTTP_HOST", "127.0.0.1")
WEAVIATE_HTTP_PORT = int(os.getenv("WEAVIATE_HTTP_PORT", "8080"))
WEAVIATE_HTTP_SECURE = os.getenv("WEAVIATE_HTTP_SECURE", "false").lower() == "true"
WEAVIATE_GRPC_HOST = os.getenv("WEAVIATE_GRPC_HOST", WEAVIATE_HTTP_HOST)
WEAVIATE_GRPC_PORT = int(os.getenv("WEAVIATE_GRPC_PORT", "50051"))
WEAVIATE_GRPC_SECURE = os.getenv("WEAVIATE_GRPC_SECURE", "false").lower() == "true"

# --- Weaviate Client Initialization ---

COLLECTION_NAME = "RoamSemanticChunks" # Weaviate class names are capitalized
DEFAULT_STATE_FILE = os.getenv(
    "SYNC_STATE_FILE",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "sync_state.json"),
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle Weaviate client startup and shutdown."""
    LOGGER.info("Initialising Weaviate client")
    client = weaviate.use_async_with_custom(
        http_host=WEAVIATE_HTTP_HOST,
        http_port=WEAVIATE_HTTP_PORT,
        http_secure=WEAVIATE_HTTP_SECURE,
        grpc_host=WEAVIATE_GRPC_HOST,
        grpc_port=WEAVIATE_GRPC_PORT,
        grpc_secure=WEAVIATE_GRPC_SECURE,
        headers={
            "X-VoyageAI-Api-Key": settings.voyageai_api_key
        },
        skip_init_checks=True,
    )
    try:
        @async_retry(tries=5, timeout=lambda attempt: min(2 ** attempt, 10), errors=(Exception,))
        async def connect_with_retry():
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
        yield
    finally:
        ctx: Optional[AppContext] = getattr(app.state, "ctx", None)
        job_state: Dict[str, Any] = getattr(app.state, "sync_job", {})
        task = job_state.get("task") if isinstance(job_state, dict) else None
        if task:
            task.cancel()
            with suppress(asyncio.CancelledError):
                await task
            job_state["task"] = None
            job_state["status"] = "cancelled"
            job_state["finished_at"] = datetime.utcnow().isoformat()
        if ctx and ctx.client.is_connected():
            await ctx.client.close()
            LOGGER.info("Weaviate connection closed")
        if hasattr(app.state, "ctx"):
            delattr(app.state, "ctx")

async def delete_collection(name: str) -> None:
    """Delete a Weaviate collection."""
    client = weaviate.connect_to_custom(
        http_host=WEAVIATE_HTTP_HOST,
        http_port=WEAVIATE_HTTP_PORT,
        http_secure=WEAVIATE_HTTP_SECURE,
        grpc_host=WEAVIATE_GRPC_HOST,
        grpc_port=WEAVIATE_GRPC_PORT,
        grpc_secure=WEAVIATE_GRPC_SECURE,
        skip_init_checks=True,
    )
    try:
        if client.collections.exists(name):
            client.collections.delete(name)
            LOGGER.info("Deleted collection '%s'", name)
    except Exception as exc:  # pragma: no cover - admin helper
        LOGGER.exception("Error deleting collection '%s'", name)
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
    """Return a mapping of block UID -> metadata for the given ``uids``."""

    if not uids:
        return {}

    try:
        results = await _pull_many_blocks(uids)
    except httpx.HTTPError as exc:  # pragma: no cover - network failure
        LOGGER.warning("Pull-many failed after retries: %s", exc)
        return {}

    pairs = zipdict(uids, results or [])
    return {uid: block for uid, block in pairs.items() if block}


def _job_view(job: Dict[str, Any]) -> Dict[str, Any]:
    """Return a JSON-friendly snapshot of the current sync job."""

    public = {k: v for k, v in job.items() if k != "task"}
    if "params" in public and isinstance(public["params"], dict):
        public["params"] = dict(public["params"])
    if "progress" in public and isinstance(public["progress"], dict):
        public["progress"] = dict(public["progress"])
    if "summary" in public and isinstance(public["summary"], dict):
        public["summary"] = dict(public["summary"])
    return public


async def _run_sync_job(app: FastAPI, sync_kwargs: Dict[str, Any]) -> None:
    lock: asyncio.Lock = app.state.sync_lock
    job: Dict[str, Any] = app.state.sync_job
    from sync_semantic import sync_semantic_graph

    async def status_cb(payload: Dict[str, Any]) -> None:
        async with lock:
            progress = dict(job.get("progress", {}))
            progress.update(payload)
            progress["timestamp"] = datetime.utcnow().isoformat()
            job["progress"] = progress

    async def completion_cb(summary: Dict[str, Any]) -> None:
        async with lock:
            job["summary"] = summary

    try:
        summary = await sync_semantic_graph(**sync_kwargs, status_cb=status_cb, completion_cb=completion_cb)
        async with lock:
            job["status"] = "success"
            job["finished_at"] = datetime.utcnow().isoformat()
            job["summary"] = summary
            job["task"] = None
    except asyncio.CancelledError:
        async with lock:
            job["status"] = "cancelled"
            job["finished_at"] = datetime.utcnow().isoformat()
            job["error"] = "cancelled"
            job["task"] = None
        raise
    except Exception as exc:  # pragma: no cover - defensive
        LOGGER.exception("Sync job failed", exc_info=exc)
        async with lock:
            job["status"] = "failed"
            job["finished_at"] = datetime.utcnow().isoformat()
            job["error"] = str(exc)
            job["task"] = None
    finally:
        async with lock:
            task = job.get("task")
            if task is not None and task.done():
                job["task"] = None



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

async def get_context(request: Request) -> AppContext:
    ctx = getattr(request.app.state, "ctx", None)
    if not ctx:
        raise HTTPException(status_code=503, detail="Weaviate is not ready")
    return ctx


@app.post("/sync/start", status_code=202)
async def start_sync(
    payload: Dict[str, Any] = Body(default_factory=dict),
    request: Request = None,
    ctx: AppContext = Depends(get_context),
):
    app_state = request.app
    lock: asyncio.Lock = app_state.state.sync_lock
    job: Dict[str, Any] = app_state.state.sync_job

    mode = str(payload.get("mode", "since")).lower()
    if mode not in {"full", "since", "limit"}:
        raise HTTPException(status_code=400, detail="mode must be 'full', 'since', or 'limit'")

    clear = bool(payload.get("clear", False))
    recreate = bool(payload.get("recreate_collection", False))
    resume = bool(payload.get("resume", False))
    state_file_path = payload.get("state_file") or DEFAULT_STATE_FILE

    to_int = silent(int)

    limit_value: Optional[int] = None
    if mode == "limit":
        raw_limit = payload.get("limit")
        if raw_limit is None:
            raise HTTPException(status_code=400, detail="limit is required when mode='limit'")
        limit_value = to_int(raw_limit)
        if limit_value is None:
            raise HTTPException(status_code=400, detail="limit must be an integer")
        if limit_value <= 0:
            raise HTTPException(status_code=400, detail="limit must be greater than zero")

    since_value: Optional[int] = None
    if mode == "since" and payload.get("since") is not None:
        since_value = to_int(payload["since"])
        if since_value is None:
            raise HTTPException(status_code=400, detail="since must be an integer timestamp")

    async with lock:
        if job.get("status") == "running":
            raise HTTPException(status_code=409, detail=_job_view(job))

        if mode == "since" and since_value is None:
            previous = job.get("summary", {}).get("max_edit_time")
            if previous is not None:
                since_value = previous

        sync_kwargs: Dict[str, Any] = {
            "clear_existing": clear,
            "recreate_collection": recreate,
            "resume": resume,
        }
        if state_file_path:
            sync_kwargs["state_file"] = state_file_path
        if mode == "limit" and limit_value is not None:
            sync_kwargs["test_limit"] = limit_value
        if mode == "since" and since_value is not None:
            sync_kwargs["since"] = since_value

        run_id = str(uuid.uuid4())
        job.update(
            {
                "status": "running",
                "run_id": run_id,
                "mode": mode,
                "params": {
                    "clear": clear,
                    "recreate_collection": recreate,
                    "resume": resume,
                    "state_file": state_file_path,
                    "since": since_value,
                    "limit": limit_value,
                },
                "started_at": datetime.utcnow().isoformat(),
                "finished_at": None,
                "progress": {},
                "summary": {},
                "error": None,
            }
        )

        task = asyncio.create_task(_run_sync_job(app_state, sync_kwargs))
        job["task"] = task

        view = _job_view(job)

    return view


@app.get("/sync/status")
async def get_sync_status(request: Request, ctx: AppContext = Depends(get_context)) -> Dict[str, Any]:
    lock: asyncio.Lock = request.app.state.sync_lock
    async with lock:
        return _job_view(request.app.state.sync_job)


@app.post("/sync/cancel")
async def cancel_sync(request: Request, ctx: AppContext = Depends(get_context)) -> Dict[str, Any]:
    lock: asyncio.Lock = request.app.state.sync_lock
    async with lock:
        job: Dict[str, Any] = request.app.state.sync_job
        task = job.get("task")
        if not task or task.done():
            raise HTTPException(status_code=409, detail="No running sync job to cancel")
        task.cancel()
        job["status"] = "cancelling"
        job["error"] = "cancel requested"
        return _job_view(job)


@app.post("/sync/clear", status_code=202)
async def clear_database(request: Request, ctx: AppContext = Depends(get_context)) -> Dict[str, Any]:
    lock: asyncio.Lock = request.app.state.sync_lock
    async with lock:
        job: Dict[str, Any] = request.app.state.sync_job
        if job.get("status") == "running":
            raise HTTPException(status_code=409, detail=_job_view(job))

        await delete_collection(COLLECTION_NAME)

        cleared_at = datetime.utcnow().isoformat()
        job.setdefault("history", [])
        job["history"].append({"event": "cleared", "at": cleared_at})

        summary = job.get("summary", {})
        summary.update({"status": "cleared", "cleared_at": cleared_at})
        job["summary"] = summary
        job["status"] = job.get("status", "idle")

        return {"status": "cleared", "cleared_at": cleared_at}


@app.get("/")
async def read_root(ctx: AppContext = Depends(get_context)):
    if not await ctx.client.is_ready():
        raise HTTPException(status_code=503, detail="Weaviate is not ready")
    collection = ctx.client.collections.get(COLLECTION_NAME)
    count = await collection.aggregate.over_all(total_count=True)
    return {
        "message": "Roam Semantic Search (Semantic Strategy) Backend is running with Weaviate.",
        "roam_graph_name": ctx.settings.roam_graph_name,
        "collection_name": COLLECTION_NAME,
        "collection_count": count.total_count,
    }

@app.get("/search")
async def search(
    q: str = Query(..., description="Search query"),
    limit: int = Query(10, ge=1, le=50, description="Number of results to return"),
    alpha: float = Query(0.5, ge=0, le=1, description="Balance between keyword and vector search. 0 for pure keyword, 1 for pure vector."),
    exclude_pages: bool = Query(False, description="Exclude page results, only show chunks"),
    rerank: bool = Query(settings.rerank_default_enabled, description="Enable result reranking using VoyageAI"),
    rerank_query: Optional[str] = Query(None, description="Custom query for reranking, if different from search query"),
    rerank_limit: Optional[int] = Query(None, description="Number of top results to rerank (None = all results)"),
    ctx: AppContext = Depends(get_context),
):
    """
    Performs hybrid search on the pre-chunked documents using Weaviate.
    """
    start_time = time.time()
    if not q or not q.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    if not await ctx.client.is_ready():
        raise HTTPException(status_code=503, detail="Weaviate is not ready")

    try:
        query_vector = await ctx.embedder.embed_query(q)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to embed query with VoyageAI: {e}")

    collection = ctx.client.collections.get(COLLECTION_NAME)

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
