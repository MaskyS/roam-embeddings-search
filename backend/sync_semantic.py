"""
Semantic sync pipeline for Roam -> Weaviate using contextual embeddings.

The sync now relies on a functional core (``backend.semantic_sync``) and a
thin orchestration layer which wires together Roam pulls, chunking, embedding
and Weaviate persistence. This keeps the business logic declarative and makes
incremental sync behaviour easier to reason about.
"""

import argparse
import asyncio
import logging
import re
import time
import uuid
from collections import deque
from contextlib import suppress
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional, Callable, Awaitable

import httpx
import weaviate
from funcy import chunks, compact, decorator, merge, merge_with, silent

# Add backend to path to allow local imports
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

LOGGER = logging.getLogger(__name__)

from main_semantic import settings
from persistent_state import (
    DEFAULT_DB_PATH,
    initialise as initialise_state,
    load_page_state as load_state_rows,
    record_run,
    upsert_page_state,
)
from roam import query_roam
from semantic_sync import (
    ChunkerClient,
    ChunkerConfig,
    VoyageEmbeddingClient,
    WeaviateSyncAdapter,
    build_weaviate_objects,
    collect_page_snapshot,
    decide_sync_action,
    load_state,
    persist_state,
    remove_state_file,
)

# --- Constants ---


@dataclass(frozen=True)
class SyncConfig:
    batch_size: int
    metadata_batch_size: int
    metadata_state_concurrency: int
    collection_name: str
    weaviate_http_host: str
    weaviate_http_port: int
    weaviate_http_secure: bool
    weaviate_grpc_host: str
    weaviate_grpc_port: int
    weaviate_grpc_secure: bool
    chunker_url: str
    chunker_retries: int
    chunker_retry_delay: int
    sync_version: str
    uuid_namespace: uuid.UUID
    chunker_group_size: int
    chunker_concurrency: int
    voyage_concurrency: int
    weaviate_write_concurrency: int
    roam_requests_per_minute: int


CONFIG = SyncConfig(
    batch_size=20,
    metadata_batch_size=int(os.getenv("ROAM_METADATA_BATCH_SIZE", "500")),
    metadata_state_concurrency=int(os.getenv("ROAM_METADATA_STATE_CONCURRENCY", "8")),
    collection_name="RoamSemanticChunks",
    weaviate_http_host=os.getenv("WEAVIATE_HTTP_HOST", "127.0.0.1"),
    weaviate_http_port=int(os.getenv("WEAVIATE_HTTP_PORT", "8080")),
    weaviate_http_secure=os.getenv("WEAVIATE_HTTP_SECURE", "false").lower() == "true",
    weaviate_grpc_host=os.getenv("WEAVIATE_GRPC_HOST", os.getenv("WEAVIATE_HTTP_HOST", "127.0.0.1")),
    weaviate_grpc_port=int(os.getenv("WEAVIATE_GRPC_PORT", "50051")),
    weaviate_grpc_secure=os.getenv("WEAVIATE_GRPC_SECURE", "false").lower() == "true",
    chunker_url=os.getenv("CHUNKER_SERVICE_URL", "http://127.0.0.1:8003"),
    chunker_retries=3,
    chunker_retry_delay=2,
    sync_version="semantic_v3_incremental",
    uuid_namespace=uuid.uuid5(uuid.NAMESPACE_URL, "roam-semantic-sync"),
    chunker_group_size=int(os.getenv("CHUNKER_GROUP_SIZE", "4")),
    chunker_concurrency=int(os.getenv("CHUNKER_CONCURRENCY", "1")),
    voyage_concurrency=int(os.getenv("VOYAGE_CONCURRENCY", "4")),
    weaviate_write_concurrency=int(os.getenv("WEAVIATE_WRITE_CONCURRENCY", "1")),
    roam_requests_per_minute=int(os.getenv("ROAM_MAX_REQUESTS_PER_MINUTE", "50")),
)


METADATA_SELECTOR = (
    "[:block/uid :create/time :edit/time "
    "{:block/children [:block/uid :create/time :edit/time {:block/children ...}]}]"
)

FULL_PAGE_SELECTOR = (
    "[:block/uid :block/string :node/title :block/order :create/time :edit/time "
    "{:create/user [:user/uid]} {:edit/user [:user/uid]} {:block/refs [:block/uid :node/title :block/string]} "
    "{:block/children ...}]"
)

# Flag stored in persisted state once metadata filtering has been applied.
STATE_FLAG_METADATA_APPLIED = "metadata_applied"

TO_INT = silent(int)

ROAM_BASE_URL = f"https://api.roamresearch.com/api/graph/{settings.roam_graph_name}/"
ROAM_HEADERS = {
    "X-Authorization": f"Bearer {settings.roam_api_token}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}


# --- Rate limiter ---------------------------------------------------------


class RateLimiter:
    """Simple async rate limiter using a sliding window."""

    def __init__(self, max_calls: int, period: float) -> None:
        self.max_calls = max_calls
        self.period = period
        self.calls: deque[float] = deque()
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        loop = asyncio.get_running_loop()
        while True:
            async with self._lock:
                now = loop.time()
                while self.calls and now - self.calls[0] > self.period:
                    self.calls.popleft()
                if len(self.calls) < self.max_calls:
                    self.calls.append(now)
                    return
                sleep_for = self.period - (now - self.calls[0]) + 0.01
            await asyncio.sleep(max(sleep_for, 0.01))


ROAM_RATE_LIMITER = RateLimiter(CONFIG.roam_requests_per_minute, 60.0)


@decorator
async def async_retry(call, *, tries: int = 3, timeout=0.0, errors=(Exception,), filter_errors=None):
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


def _sum_values(*values: Optional[float]) -> float:
    if len(values) == 1 and isinstance(values[0], (list, tuple)):
        values = tuple(values[0])
    return sum((value or 0) for value in values)


def merge_stats(base: Dict[str, int], delta: Optional[Dict[str, int]]) -> Dict[str, int]:
    if not delta:
        return base
    return merge_with(_sum_values, base, delta)


def merge_durations(base: Dict[str, float], delta: Optional[Dict[str, float]]) -> Dict[str, float]:
    if not delta:
        return base
    return merge_with(_sum_values, base, delta)


def make_summary(
    *,
    status: str,
    stats: Optional[Dict[str, int]] = None,
    durations: Optional[Dict[str, float]] = None,
    metadata_applied: bool,
    extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    summary = {
        "status": status,
        "stats": dict(stats or {}),
        "durations": dict(durations or {}),
        STATE_FLAG_METADATA_APPLIED: metadata_applied,
    }
    if extra:
        summary.update(extra)
    return summary

@async_retry(tries=3, timeout=lambda attempt: min(2 ** attempt, 4), errors=(httpx.HTTPError,))
async def _post_roam(endpoint: str, payload: Dict[str, Any], *, timeout: float) -> httpx.Response:
    await ROAM_RATE_LIMITER.acquire()
    async with httpx.AsyncClient(
        base_url=ROAM_BASE_URL,
        headers=ROAM_HEADERS,
        follow_redirects=True,
        timeout=timeout,
    ) as client:
        response = await client.post(endpoint, json=payload)

    if response.status_code >= 500 or response.status_code == 429:
        response.raise_for_status()
    return response


@async_retry(tries=3, timeout=lambda attempt: min(2 ** attempt, 4), errors=(Exception,))
async def chunk_batch_with_retry(client: ChunkerClient, texts: List[str]) -> List[List[Dict[str, Any]]]:
    return await client.chunk_batch(texts)


@async_retry(tries=3, timeout=lambda attempt: min(2 ** attempt, 4), errors=(Exception,))
async def embed_documents_with_retry(client: VoyageEmbeddingClient, docs: List[List[str]]) -> List[List[List[float]]]:
    return await client.embed_documents(docs)


@async_retry(tries=3, timeout=lambda attempt: min(2 ** attempt, 4), errors=(Exception,))
async def weaviate_insert_with_retry(adapter: WeaviateSyncAdapter, objects: List[Dict[str, Any]]):
    return await adapter.insert_objects(objects)


@async_retry(tries=3, timeout=lambda attempt: min(2 ** attempt, 4), errors=(Exception,))
async def weaviate_delete_with_retry(adapter: WeaviateSyncAdapter, page_uid: str, content_hash: str) -> None:
    await adapter.delete_stale_objects(page_uid, content_hash)


# --- Data containers ------------------------------------------------------


@dataclass
class PageWorkItem:
    snapshot: Dict[str, Any]
    page_title: str
    page_uid: str
    page_num: int


@dataclass
class PageMetric:
    page_uid: str
    chunk_duration: float
    embed_duration: float
    weaviate_duration: float


@dataclass
class PageMetadata:
    page_uid: str
    max_edit_time: Optional[int]
    has_children: bool
    raw: Optional[Dict[str, Any]] = None


@dataclass
class GroupResult:
    metrics: List[PageMetric] = field(default_factory=list)
    docs_added: int = 0
    chunks_created: int = 0
    pages_updated: int = 0
    pages_failed: int = 0
    chunk_duration: float = 0.0
    voyage_duration: float = 0.0
    weaviate_duration: float = 0.0
    chunk_wait: float = 0.0
    voyage_wait: float = 0.0
    weaviate_wait: float = 0.0
    fail_messages: List[str] = field(default_factory=list)
    state_updates: Dict[str, Dict[str, Any]] = field(default_factory=dict)


@dataclass
class MetadataPassResult:
    remaining_uids: List[str]
    metadata_map: Dict[str, PageMetadata]
    state_cache: Dict[str, Dict[str, Any]]
    stats_delta: Dict[str, int]
    durations_delta: Dict[str, float]
    missing_edit_uids: set[str]
    max_edit_time_seen: Optional[int]


# --- Roam API helpers -----------------------------------------------------

async def get_all_page_uids() -> List[str]:
    LOGGER.info("Step 1: getting all page UIDs")
    query = """[:find ?uid
               :where [?e :node/title]
                      [?e :block/uid ?uid]]"""

    result = await query_roam(
        token=settings.roam_api_token,
        graph_name=settings.roam_graph_name,
        query=query,
    )
    if not result or not result.get("result"):
        return []

    all_uids = [item[0] for item in result["result"]]
    dnp_count = sum(1 for uid in all_uids if re.match(r"^\d{2}-\d{2}-\d{4}$", uid))
    LOGGER.info(
        "Found %d total pages (%d Daily Notes, %d regular pages)",
        len(all_uids),
        dnp_count,
        len(all_uids) - dnp_count,
    )
    return all_uids


async def pull_many_pages(uids: Iterable[str]) -> List[Optional[Dict[str, Any]]]:
    batch = list(uids)
    if not batch:
        return []

    eids_list = " ".join([f'[:block/uid \"{uid}\"]' for uid in batch])
    payload = {"eids": f"[{eids_list}]", "selector": FULL_PAGE_SELECTOR}

    try:
        response = await _post_roam("pull-many", payload, timeout=60.0)
    except Exception as exc:  # pragma: no cover - defensive logging
        LOGGER.exception("Pull-many request error: %s", exc)
        return [None] * len(batch)

    if response.status_code == 200:
        return response.json().get("result", [])

    LOGGER.warning(
        "Pull-many failed with status %s: %s",
        response.status_code,
        response.text[:200],
    )
    return [None] * len(batch)


async def pull_many_metadata(uids: Iterable[str]) -> List[Optional[Dict[str, Any]]]:
    batch = list(uids)
    if not batch:
        return []

    eids_list = " ".join([f'[:block/uid \"{uid}\"]' for uid in batch])
    payload = {"eids": f"[{eids_list}]", "selector": METADATA_SELECTOR}

    try:
        response = await _post_roam("pull-many", payload, timeout=30.0)
    except Exception as exc:  # pragma: no cover - defensive logging
        LOGGER.exception("Metadata pull-many request error: %s", exc)
        return [None] * len(batch)

    if response.status_code == 200:
        return response.json().get("result", [])

    LOGGER.warning(
        "Metadata pull-many failed with status %s: %s",
        response.status_code,
        response.text[:200],
    )
    return [None] * len(batch)


def extract_page_metadata(page_data: Optional[Dict[str, Any]]) -> Optional[PageMetadata]:
    if not page_data or not isinstance(page_data, dict):
        return None

    page_uid = page_data.get(":block/uid")
    if not page_uid:
        return None

    max_edit: Optional[int] = None
    has_children = bool(page_data.get(":block/children"))

    def walk(node: Optional[Dict[str, Any]]) -> None:
        nonlocal max_edit, has_children
        if not node or not isinstance(node, dict):
            return
        edit_raw = node.get(":edit/time")
        edit_int = TO_INT(edit_raw) if edit_raw is not None else None
        if edit_int is not None:
            max_edit = edit_int if max_edit is None else max(max_edit, edit_int)

        children = node.get(":block/children") or []
        if children and isinstance(children, list):
            has_children = True
            for child in children:
                if isinstance(child, dict):
                    walk(child)

    walk(page_data)
    return PageMetadata(page_uid=page_uid, max_edit_time=max_edit, has_children=has_children, raw=page_data)


async def run_metadata_pass(
    uids: List[str],
    *,
    since: Optional[int],
    adapter: WeaviateSyncAdapter,
    config: SyncConfig,
    preloaded_state: Optional[Dict[str, Dict[str, Any]]] = None,
) -> MetadataPassResult:
    if not uids:
        return MetadataPassResult([], {}, {}, {}, {}, set(), None)

    metadata_map: Dict[str, PageMetadata] = {}
    missing_edit_uids: set[str] = set()
    max_edit_seen: Optional[int] = None

    metadata_start = time.time()
    failures = 0

    preloaded_state = preloaded_state or {}

    for batch in chunks(config.metadata_batch_size, uids):
        results = await pull_many_metadata(batch)
        for uid, payload in zip(batch, results or []):
            meta = extract_page_metadata(payload)
            if meta:
                metadata_map[uid] = meta
                if meta.max_edit_time is not None:
                    max_edit_seen = meta.max_edit_time if max_edit_seen is None else max(max_edit_seen, meta.max_edit_time)
                else:
                    missing_edit_uids.add(uid)
            else:
                missing_edit_uids.add(uid)
                failures += 1

    metadata_duration = time.time() - metadata_start

    stats_delta: Dict[str, int] = {
        "metadata_candidates": 0,
        "metadata_filtered": 0,
        "pages_skipped": 0,
        "pages_since_filtered": 0,
    }

    remaining_after_since: List[str] = []
    for uid in uids:
        meta = metadata_map.get(uid)
        if meta and meta.max_edit_time is not None and since is not None and meta.max_edit_time <= since:
            stats_delta["pages_since_filtered"] += 1
            stats_delta["pages_skipped"] += 1
            stats_delta["metadata_filtered"] += 1
            continue
        remaining_after_since.append(uid)

    # Fetch Weaviate states for candidates with known metadata; others will be processed later without comparison.
    state_fetch_uids = [
        uid
        for uid in remaining_after_since
        if metadata_map.get(uid)
        and metadata_map[uid].max_edit_time is not None
        and uid not in preloaded_state
    ]
    stats_delta["metadata_candidates"] = len(state_fetch_uids)

    state_cache: Dict[str, Dict[str, Any]] = dict(preloaded_state)
    weaviate_duration = 0.0

    if state_fetch_uids:
        for group in chunks(config.metadata_state_concurrency, state_fetch_uids):
            group_start = time.time()
            fetch_tasks = [asyncio.create_task(adapter.fetch_existing_page_state(uid)) for uid in group]
            results = await asyncio.gather(*fetch_tasks, return_exceptions=True)
            weaviate_duration += time.time() - group_start
            for uid, result in zip(group, results):
                if isinstance(result, Exception):  # pragma: no cover - defensive logging
                    LOGGER.exception("Failed to fetch existing state for %s during metadata pass", uid, exc_info=result)
                    state_cache[uid] = {}
                else:
                    state_cache[uid] = result or {}

    remaining_uids: List[str] = []
    retained_state_cache: Dict[str, Dict[str, Any]] = dict(state_cache)
    for uid in remaining_after_since:
        meta = metadata_map.get(uid)
        state = state_cache.get(uid)

        if meta and meta.max_edit_time is not None and state:
            stored_edit = TO_INT(state.get("last_synced_edit_time")) if state.get("last_synced_edit_time") is not None else None
            if stored_edit is not None and stored_edit >= meta.max_edit_time and state.get("page_objects"):
                stats_delta["metadata_filtered"] += 1
                stats_delta["pages_skipped"] += 1
                continue

        remaining_uids.append(uid)
        if state is not None:
            retained_state_cache[uid] = state

    if failures:
        LOGGER.warning("Metadata pull left %d pages without metadata; scheduling full pulls", failures)

    durations_delta = {
        "metadata_pull": metadata_duration,
        "weaviate_meta": weaviate_duration,
    }

    return MetadataPassResult(
        remaining_uids=remaining_uids,
        metadata_map=metadata_map,
        state_cache=retained_state_cache,
        stats_delta=stats_delta,
        durations_delta=durations_delta,
        missing_edit_uids=missing_edit_uids,
        max_edit_time_seen=max_edit_seen,
    )


# --- Sync -----------------------------------------------------------------

async def sync_semantic_graph(
    clear_existing: bool = False,
    test_limit: Optional[int] = None,
    recreate_collection: bool = False,
    state_file: Optional[str] = None,
    resume: bool = False,
    since: Optional[int] = None,
    config: SyncConfig = CONFIG,
    status_cb: Optional[Callable[[Dict[str, Any]], Awaitable[None]]] = None,
    completion_cb: Optional[Callable[[Dict[str, Any]], Awaitable[None]]] = None,
) -> Dict[str, Any]:
    LOGGER.info("Starting semantic graph sync with Weaviate")
    start_time = time.time()
    start_timestamp = datetime.utcnow().isoformat()

    initialise_state()
    run_id = str(uuid.uuid4())

    summary: Dict[str, Any] = {}

    async def emit_status(payload: Dict[str, Any]) -> None:
        if status_cb:
            await status_cb(payload)

    async def emit_completion(payload: Dict[str, Any]) -> None:
        if completion_cb:
            await completion_cb(payload)

    state_path = os.path.abspath(state_file) if state_file else None
    if resume and not state_path:
        LOGGER.warning("--resume requested without --state-file; ignoring resume flag")
        resume = False

    step1_start = time.time()
    all_page_uids = await get_all_page_uids()
    step1_time = time.time() - step1_start
    total_pages_discovered = len(all_page_uids)
    await emit_status(
        {
            "event": "uids_loaded",
            "total_pages": total_pages_discovered,
            "started_at": start_timestamp,
            "progress": {
                "processed": 0,
                "total": total_pages_discovered,
                "percent": 0.0,
            },
        }
    )
    if not all_page_uids:
        LOGGER.info("No pages found to process")
        summary = make_summary(
            status="no_pages",
            stats={},
            durations={"uids": step1_time},
            metadata_applied=False,
            extra={
                "total_pages": 0,
                "since": since,
                "test_limit": test_limit,
                "state_file": state_path,
                "resume": resume,
            },
        )
        record_run(run_id, "no_pages", since=since, test_limit=test_limit, notes=summary)
        await emit_completion(summary)
        return summary

    if test_limit:
        LOGGER.info("TEST MODE: limiting to first %d pages", test_limit)
        all_page_uids = all_page_uids[:test_limit]

    processed_offset = 0
    pending_uids = list(all_page_uids)
    total_target_pages = len(pending_uids)
    state_loaded = False
    state_completed = False

    saved_state: Optional[Dict[str, Any]] = None
    metadata_applied_from_state = False

    if resume and state_path:
        saved_state = load_state(state_path)
        if saved_state:
            state_loaded = True
            pending = saved_state.get("pending_page_uids", [])
            processed_offset = saved_state.get("processed_count", 0)
            total_target_pages = saved_state.get("total_pages", processed_offset + len(pending))
            stored_since = saved_state.get("since")
            metadata_applied_from_state = bool(saved_state.get(STATE_FLAG_METADATA_APPLIED, False))
            if pending:
                pending_uids = pending
                LOGGER.info(
                    "Resuming from state file '%s'. Pending pages: %d, already processed: %d.",
                    state_path,
                    len(pending_uids),
                    processed_offset,
                )
                if since is None and stored_since is not None:
                    since = stored_since
                elif since is not None and stored_since is not None and since != stored_since:
                    LOGGER.warning(
                        "--since (%s) differs from stored state (%s); using provided value",
                        since,
                        stored_since,
                    )
            else:
                LOGGER.info("State file '%s' has no pending pages. Nothing to resume.", state_path)
                durations_empty = {
                    "uids": step1_time,
                    "chunker_wait": 0.0,
                    "roam": 0.0,
                    "linearize": 0.0,
                    "chunk": 0.0,
                    "voyage": 0.0,
                    "weaviate": 0.0,
                    "chunk_wait": 0.0,
                    "voyage_wait": 0.0,
                    "weaviate_wait": 0.0,
                }
                stats_empty = {
                    "documents_added": 0,
                    "chunks_created": 0,
                    "pages_updated": 0,
                    "pages_skipped": 0,
                    "pages_failed": 0,
                    "pages_since_filtered": 0,
                }
                summary = make_summary(
                    status="resume_complete",
                    stats=stats_empty,
                    durations=durations_empty,
                    metadata_applied=metadata_applied_from_state,
                    extra={
                        "elapsed_seconds": 0.0,
                        "pages_processed": 0,
                        "processed_offset": processed_offset,
                        "total_target_pages": total_target_pages,
                        "total_pages": total_pages_discovered,
                        "missing_edit_time_count": 0,
                        "empty_linearized_count": 0,
                        "max_edit_time": None,
                        "since": since,
                        "test_limit": test_limit,
                        "state_file": state_path,
                        "state_loaded": True,
                        "resume": True,
                        "started_at": start_timestamp,
                        "failures": [],
                        "step1_time": step1_time,
                        "chunker_time": 0.0,
                    },
                )
                await emit_completion(summary)
                if state_path:
                    remove_state_file(state_path)
                record_run(run_id, "resume_complete", since=since, test_limit=test_limit, notes=summary)
                return summary
        else:
            LOGGER.info("No valid state found at '%s', starting fresh.", state_path)

    db_state_rows = load_state_rows(pending_uids)
    preloaded_state = {}
    for uid, row in db_state_rows.items():
        last_synced = row.get("last_synced_edit_time")
        if last_synced is None:
            continue
        preloaded_state[uid] = {
            "page_objects": [
                {
                    "properties": {
                        "last_synced_edit_time": str(last_synced),
                        "content_hash": row.get("content_hash"),
                    }
                }
            ],
            "chunk_objects": [],
            "last_synced_edit_time": last_synced,
            "content_hash": row.get("content_hash"),
        }

    client = weaviate.use_async_with_custom(
        http_host=config.weaviate_http_host,
        http_port=config.weaviate_http_port,
        http_secure=config.weaviate_http_secure,
        grpc_host=config.weaviate_grpc_host,
        grpc_port=config.weaviate_grpc_port,
        grpc_secure=config.weaviate_grpc_secure,
        skip_init_checks=True,
    )
    await client.connect()

    chunker_client = ChunkerClient(
        ChunkerConfig(
            url=config.chunker_url,
            retries=config.chunker_retries,
            base_delay=config.chunker_retry_delay,
        )
    )
    voyage_timeout = float(os.getenv("VOYAGE_TIMEOUT", "60"))
    voyage_client = VoyageEmbeddingClient(
        api_key=settings.voyageai_api_key,
        model=settings.voyageai_context_model,
        timeout=voyage_timeout,
    )
    weaviate_adapter = WeaviateSyncAdapter(client, config.collection_name)

    durations: Dict[str, float] = {
        "roam": 0.0,
        "linearize": 0.0,
        "chunk": 0.0,
        "voyage": 0.0,
        "weaviate": 0.0,
        "chunk_wait": 0.0,
        "voyage_wait": 0.0,
        "weaviate_wait": 0.0,
        "metadata_pull": 0.0,
        "weaviate_meta": 0.0,
    }
    stats: Dict[str, int] = {
        "documents_added": 0,
        "chunks_created": 0,
        "pages_updated": 0,
        "pages_skipped": 0,
        "pages_failed": 0,
        "pages_since_filtered": 0,
        "metadata_candidates": 0,
        "metadata_filtered": 0,
    }
    max_edit_time_seen: Optional[int] = None

    def bump_stat(key: str, delta: int = 1) -> None:
        nonlocal stats
        stats = merge_stats(stats, {key: delta})

    def add_duration(key: str, delta: float) -> None:
        nonlocal durations
        durations = merge_durations(durations, {key: delta})

    pages_missing_edit_time: set[str] = set()
    pages_empty_linearized: set[str] = set()
    failures: List[str] = []

    pages_processed_this_run = 0
    per_page_metrics: List[PageMetric] = []
    metadata_applied = metadata_applied_from_state
    metadata_map: Dict[str, PageMetadata] = {}
    page_state_cache: Dict[str, Dict[str, Any]] = dict(preloaded_state)

    chunk_semaphore = asyncio.Semaphore(max(1, config.chunker_concurrency))
    voyage_semaphore = asyncio.Semaphore(max(1, config.voyage_concurrency))
    weaviate_semaphore = asyncio.Semaphore(max(1, config.weaviate_write_concurrency))

    async def process_group(group_items: List[PageWorkItem]) -> GroupResult:
        result = GroupResult()
        try:
            texts = [item.snapshot.get("linearized_text") or "" for item in group_items]
            chunk_wait_start = time.time()
            await chunk_semaphore.acquire()
            result.chunk_wait = time.time() - chunk_wait_start
            try:
                chunk_start = time.time()
                chunk_batches = await chunk_batch_with_retry(chunker_client, texts)
                result.chunk_duration = time.time() - chunk_start
            finally:
                chunk_semaphore.release()
        except Exception as exc:  # pragma: no cover - defensive logging
            result.pages_failed = len(group_items)
            result.fail_messages.append(f"  ✗ Chunker failed for group: {exc}")
            return result

        processed_items: List[tuple[PageWorkItem, Dict[str, Any]]] = []
        for item, chunk_data in zip(group_items, chunk_batches):
            try:
                payload = build_weaviate_objects(
                    snapshot=item.snapshot,
                    chunk_results=chunk_data,
                    sync_version=config.sync_version,
                    namespace=config.uuid_namespace,
                )
                processed_items.append((item, payload))
            except Exception as exc:
                result.pages_failed += 1
                result.fail_messages.append(
                    f"  ✗ Failed building payload for page '{item.page_title}' ({item.page_uid}): {exc}"
                )

        if not processed_items:
            return result

        try:
            voyage_wait_start = time.time()
            await voyage_semaphore.acquire()
            result.voyage_wait = time.time() - voyage_wait_start
            try:
                voyage_start = time.time()
                embeddings_nested = await embed_documents_with_retry(
                    voyage_client,
                    [payload["chunk_texts"] for _, payload in processed_items],
                )
                result.voyage_duration = time.time() - voyage_start
            finally:
                voyage_semaphore.release()
        except Exception as exc:
            result.pages_failed += len(processed_items)
            result.fail_messages.append(f"  ✗ Voyage embedding failed for group: {exc}")
            return result

        successful_payloads: List[tuple[PageWorkItem, Dict[str, Any]]] = []
        for (item, payload), embeddings in zip(processed_items, embeddings_nested):
            if len(embeddings) != len(payload["all_objects"]):
                result.pages_failed += 1
                result.fail_messages.append(
                    f"  ✗ Embedding count mismatch for page '{item.page_title}' ({item.page_uid})"
                )
                continue
            for obj, vector in zip(payload["all_objects"], embeddings):
                obj["vector"] = vector
            successful_payloads.append((item, payload))

        if not successful_payloads:
            return result

        weaviate_objects = [obj for _, payload in successful_payloads for obj in payload["all_objects"]]
        try:
            weaviate_wait_start = time.time()
            await weaviate_semaphore.acquire()
            result.weaviate_wait = time.time() - weaviate_wait_start
            try:
                weaviate_start = time.time()
                failed_objects = await weaviate_insert_with_retry(weaviate_adapter, weaviate_objects)
                result.weaviate_duration = time.time() - weaviate_start
                if failed_objects:
                    sample_messages = ", ".join((error.message or "") for error in failed_objects[:3])
                    raise RuntimeError(
                        f"Weaviate reported {len(failed_objects)} failed objects: {sample_messages}"
                    )
                for item, payload in successful_payloads:
                    await weaviate_delete_with_retry(
                        weaviate_adapter,
                        item.page_uid,
                        payload["content_hash"],
                    )
            finally:
                weaviate_semaphore.release()
        except Exception as exc:
            result.pages_failed += len(successful_payloads)
            result.fail_messages.append(f"  ✗ Weaviate write failed for group: {exc}")
            return result

        result.docs_added = len(weaviate_objects)
        result.pages_updated = len(successful_payloads)
        result.chunks_created = sum(len(payload["chunk_objects"]) for _, payload in successful_payloads)

        state_updates = {}
        for item, payload in successful_payloads:
            meta = item.snapshot.get("meta", {})
            state_updates[item.page_uid] = {
                "last_synced_edit_time": TO_INT(meta.get("max_edit_time")),
                "content_hash": payload["content_hash"],
            }
        result.state_updates = state_updates

        per_page_chunk = result.chunk_duration / max(1, len(processed_items))
        per_page_embed = result.voyage_duration / max(1, len(processed_items))
        per_page_weaviate = result.weaviate_duration / max(1, len(successful_payloads))

        for item, _payload in successful_payloads:
            result.metrics.append(
                PageMetric(
                    page_uid=item.page_uid,
                    chunk_duration=per_page_chunk,
                    embed_duration=per_page_embed,
                    weaviate_duration=per_page_weaviate,
                )
            )

        return result

    try:
        if clear_existing:
            LOGGER.info("Deleting collection '%s'", config.collection_name)
            with suppress(Exception):
                await client.collections.delete(config.collection_name)

        if clear_existing or recreate_collection:
            await weaviate_adapter.ensure_schema(True)
        else:
            with suppress(Exception):
                if not await client.collections.exists(config.collection_name):
                    await weaviate_adapter.ensure_schema(False)

        metadata_should_run = (
            not metadata_applied
            and not clear_existing
            and not recreate_collection
            and bool(pending_uids)
        )

        if metadata_should_run:
            LOGGER.info(
                "Running metadata pre-pass on %d pages (batch size %d)",
                len(pending_uids),
                config.metadata_batch_size,
            )
            metadata_result = await run_metadata_pass(
                pending_uids,
                since=since,
                adapter=weaviate_adapter,
                config=config,
                preloaded_state=preloaded_state,
            )

            stats = merge_stats(stats, metadata_result.stats_delta)
            durations = merge_durations(durations, metadata_result.durations_delta)

            pages_missing_edit_time.update(metadata_result.missing_edit_uids)
            if metadata_result.max_edit_time_seen is not None:
                max_edit_time_seen = (
                    metadata_result.max_edit_time_seen
                    if max_edit_time_seen is None
                    else max(max_edit_time_seen, metadata_result.max_edit_time_seen)
                )

            upsert_page_state(
                {
                    uid: {
                        "last_synced_edit_time": TO_INT(meta.max_edit_time),
                        "content_hash": None,
                    }
                    for uid, meta in metadata_result.metadata_map.items()
                    if meta.max_edit_time is not None
                }
            )

            pending_uids = metadata_result.remaining_uids
            total_target_pages = processed_offset + len(pending_uids)
            metadata_map = metadata_result.metadata_map
            page_state_cache = metadata_result.state_cache
            metadata_applied = True
            page_state_cache = dict(metadata_result.state_cache)

            LOGGER.info(
                "Metadata pre-pass skipped %d pages; %d remain for full processing",
                metadata_result.stats_delta.get("metadata_filtered", 0),
                len(pending_uids),
            )

            await emit_status(
                {
                    "event": "metadata_filtered",
                    "remaining": len(pending_uids),
                    "skipped": metadata_result.stats_delta.get("metadata_filtered", 0),
                    "durations": {
                        "metadata_pull": metadata_result.durations_delta.get("metadata_pull", 0.0),
                        "weaviate_meta": metadata_result.durations_delta.get("weaviate_meta", 0.0),
                    },
                }
            )

            if not pending_uids:
                LOGGER.info("All pages filtered by metadata pre-pass; finishing early")
                summary = make_summary(
                    status="metadata_skip",
                    stats=stats,
                    durations=merge(durations, {"uids": step1_time, "chunker_wait": 0.0}),
                    metadata_applied=True,
                    extra={
                        "elapsed_seconds": time.time() - start_time,
                        "pages_processed": 0,
                        "processed_offset": processed_offset,
                        "total_target_pages": total_target_pages,
                        "total_pages": total_pages_discovered,
                        "missing_edit_time_count": len(pages_missing_edit_time),
                        "empty_linearized_count": len(pages_empty_linearized),
                        "max_edit_time": max_edit_time_seen,
                        "since": since,
                        "test_limit": test_limit,
                        "state_file": state_path,
                        "state_loaded": state_loaded,
                        "resume": resume,
                        "started_at": start_timestamp,
                        "step1_time": step1_time,
                        "chunker_time": 0.0,
                        "failures": failures,
                    },
                )
                await emit_completion(summary)
                if state_path:
                    remove_state_file(state_path)
                record_run(run_id, "metadata_skip", since=since, test_limit=test_limit, notes=summary)
                return summary

        LOGGER.info("Connecting to chunker service")
        step3_start = time.time()
        chunker_ready = await chunker_client.wait_until_ready()
        step3_time = time.time() - step3_start
        if not chunker_ready:
            LOGGER.error("Chunker service not available, sync cannot proceed")
            failures.append("Chunker service not available")
            summary = make_summary(
                status="chunker_unavailable",
                stats=stats,
                durations=merge(durations, {"uids": step1_time, "chunker_wait": step3_time}),
                metadata_applied=metadata_applied,
                extra={
                    "since": since,
                    "test_limit": test_limit,
                    "state_file": state_path,
                    "state_loaded": state_loaded,
                    "resume": resume,
                    "started_at": start_timestamp,
                    "total_pages": total_pages_discovered,
                    "failures": failures,
                },
            )
            await emit_completion(summary)
            record_run(run_id, "chunker_unavailable", since=since, test_limit=test_limit, notes=summary)
            return summary

        await emit_status(
            {
                "event": "chunker_ready",
                "duration": step3_time,
            }
        )

        if since is not None:
            readable_since = datetime.fromtimestamp(since / 1000).isoformat()
            LOGGER.info("Applying --since filter at %s (%s)", since, readable_since)
            await emit_status({"event": "since_applied", "since": since, "readable": readable_since})

        batch_num = 0
        while pending_uids:
            batch = pending_uids[:config.batch_size]
            batch_size = len(batch)
            if not batch:
                break

            batch_num += 1
            current_start = processed_offset + pages_processed_this_run + 1
            current_end = current_start + batch_size - 1
            progress_numerator = processed_offset + pages_processed_this_run + batch_size
            progress_denominator = total_target_pages or progress_numerator
            progress = (progress_numerator / progress_denominator) * 100

            LOGGER.info(
                "Processing batch %d, pages %d-%d (%.1f%%)",
                batch_num,
                current_start,
                current_end,
                progress,
            )
            await emit_status(
                {
                    "event": "batch_start",
                    "batch": batch_num,
                    "page_range": [current_start, current_end],
                    "progress": {
                        "processed": processed_offset + pages_processed_this_run,
                        "total": total_target_pages,
                        "percent": progress,
                    },
                    "stats": stats.copy(),
                    "durations": durations.copy(),
                    "failures": failures[-5:],
                    "total_pages": total_pages_discovered,
                }
            )

            roam_start = time.time()
            pages_data = await pull_many_pages(batch)
            add_duration("roam", time.time() - roam_start)

            work_items: List[PageWorkItem] = []

            for offset, page_data in enumerate(pages_data):
                if not page_data or not page_data.get(":block/uid"):
                    bump_stat("pages_failed")
                    continue

                page_uid = page_data.get(":block/uid")
                page_title = page_data.get(":node/title") or page_data.get(":block/string") or "Untitled"
                page_number = current_start + offset

                linearize_start = time.time()
                snapshot = collect_page_snapshot(page_data)
                linearize_duration = time.time() - linearize_start
                add_duration("linearize", linearize_duration)

                if snapshot.get("meta", {}).get("max_edit_time") is None:
                    pages_missing_edit_time.add(page_uid)
                if not (snapshot.get("linearized_text") or "").strip() and snapshot.get("has_children"):
                    pages_empty_linearized.add(page_uid)

                existing_state = page_state_cache.get(page_uid)
                if existing_state is None:
                    existing_state = await weaviate_adapter.fetch_existing_page_state(page_uid)
                    page_state_cache[page_uid] = existing_state
                decision = decide_sync_action(snapshot, existing_state, since_ms=since)
                max_edit_time_int = decision.get("max_edit_time_int")
                if max_edit_time_int is not None:
                    max_edit_time_seen = max_edit_time_int if max_edit_time_seen is None else max(max_edit_time_seen, max_edit_time_int)

                if decision.get("should_skip"):
                    bump_stat("pages_skipped")
                    if decision.get("since_filtered"):
                        bump_stat("pages_since_filtered")
                    continue

                work_items.append(
                    PageWorkItem(
                        snapshot=snapshot,
                        page_title=page_title,
                        page_uid=page_uid,
                        page_num=page_number,
                    )
                )

            group_tasks = [
                asyncio.create_task(process_group(list(group)))
                for group in chunks(config.chunker_group_size, work_items)
            ]

            if group_tasks:
                results = await asyncio.gather(*group_tasks)
                for result in results:
                    bump_stat("documents_added", result.docs_added)
                    bump_stat("chunks_created", result.chunks_created)
                    bump_stat("pages_updated", result.pages_updated)
                    bump_stat("pages_failed", result.pages_failed)
                    add_duration("chunk", result.chunk_duration)
                    add_duration("voyage", result.voyage_duration)
                    add_duration("weaviate", result.weaviate_duration)
                    add_duration("chunk_wait", result.chunk_wait)
                    add_duration("voyage_wait", result.voyage_wait)
                    add_duration("weaviate_wait", result.weaviate_wait)
                    per_page_metrics.extend(result.metrics)
                    for msg in result.fail_messages:
                        LOGGER.error(msg)
                        failures.append(msg)
                    if result.state_updates:
                        upsert_page_state(result.state_updates)
                        for uid, state in result.state_updates.items():
                            last_synced = state.get("last_synced_edit_time")
                            if last_synced is None:
                                continue
                            page_state_cache[uid] = {
                                "page_objects": [
                                    {
                                        "properties": {
                                            "last_synced_edit_time": str(last_synced),
                                            "content_hash": state.get("content_hash"),
                                        }
                                    }
                                ],
                                "chunk_objects": [],
                                "last_synced_edit_time": last_synced,
                                "content_hash": state.get("content_hash"),
                            }

            pages_processed_this_run += batch_size
            pending_uids = pending_uids[batch_size:]

            await emit_status(
                {
                    "event": "batch_complete",
                    "batch": batch_num,
                    "progress": {
                        "processed": processed_offset + pages_processed_this_run,
                        "total": total_target_pages,
                        "percent": (
                            (processed_offset + pages_processed_this_run)
                            / (total_target_pages or 1)
                        )
                        * 100,
                    },
                    "stats": stats.copy(),
                    "durations": durations.copy(),
                    "max_edit_time": max_edit_time_seen,
                    "pages_missing_edit_time": len(pages_missing_edit_time),
                    "pages_empty_linearized": len(pages_empty_linearized),
                    "failures": failures[-5:],
                    "total_pages": total_pages_discovered,
                }
            )

            if state_path:
                state_payload = compact(
                    {
                        "created_at": datetime.utcnow().isoformat() + "Z",
                        "total_pages": total_target_pages,
                        "processed_count": processed_offset + pages_processed_this_run,
                        "pending_page_uids": pending_uids,
                        "since": since,
                        "test_limit": test_limit,
                        STATE_FLAG_METADATA_APPLIED: metadata_applied,
                    }
                )
                persist_state(state_path, state_payload)
                state_loaded = True

        state_completed = True

        elapsed_time = time.time() - start_time
        LOGGER.info("\n%s", "=" * 50)
        LOGGER.info("SYNC COMPLETE!")
        LOGGER.info("  • Time elapsed: %.2f seconds", elapsed_time)
        LOGGER.info("  • Pages attempted this run: %d", pages_processed_this_run)
        if processed_offset:
            LOGGER.info("  • Previously completed pages: %d", processed_offset)
            LOGGER.info("  • Total target pages (state): %d", total_target_pages)
        LOGGER.info("  • Total chunks created: %d", stats.get("chunks_created", 0))
        LOGGER.info("  • Total documents added: %d", stats.get("documents_added", 0))
        LOGGER.info("  • Pages updated: %d", stats.get("pages_updated", 0))
        LOGGER.info("  • Pages skipped (unchanged): %d", stats.get("pages_skipped", 0))
        if stats.get("pages_since_filtered", 0):
            LOGGER.info("    ◦ of which skipped by --since: %d", stats.get("pages_since_filtered", 0))
        if stats.get("pages_failed", 0):
            LOGGER.warning("  • Pages failed: %d", stats.get("pages_failed", 0))
        if pages_missing_edit_time:
            LOGGER.info("  • Pages missing edit timestamps: %d", len(pages_missing_edit_time))
        if pages_empty_linearized:
            LOGGER.info("  • Pages with empty linearized text: %d", len(pages_empty_linearized))

        LOGGER.info("\nTime breakdown:")
        LOGGER.info("  • Initial setup: %.2fs", step1_time + step3_time)
        LOGGER.info("    ◦ Getting page UIDs: %.2fs", step1_time)
        LOGGER.info("    ◦ Connecting to chunker service: %.2fs", step3_time)
        LOGGER.info("  • Roam API calls: %.2fs", durations.get("roam", 0.0))
        LOGGER.info("  • Linearization: %.2fs", durations.get("linearize", 0.0))
        LOGGER.info("  • Metadata pull: %.2fs", durations.get("metadata_pull", 0.0))
        LOGGER.info("  • Weaviate metadata fetch: %.2fs", durations.get("weaviate_meta", 0.0))
        LOGGER.info("  • Chunking: %.2fs", durations.get("chunk", 0.0))
        LOGGER.info("  • Voyage embeddings: %.2fs", durations.get("voyage", 0.0))
        LOGGER.info("  • Weaviate storage: %.2fs", durations.get("weaviate", 0.0))
        LOGGER.info("  • Chunk semaphore wait: %.2fs", durations.get("chunk_wait", 0.0))
        LOGGER.info("  • Voyage semaphore wait: %.2fs", durations.get("voyage_wait", 0.0))
        LOGGER.info("  • Weaviate semaphore wait: %.2fs", durations.get("weaviate_wait", 0.0))

        if per_page_metrics:
            slow_chunk = [
                m
                for m in sorted(per_page_metrics, key=lambda x: x.chunk_duration, reverse=True)
                if m.chunk_duration
            ][:3]
            slow_embed = [
                m
                for m in sorted(per_page_metrics, key=lambda x: x.embed_duration, reverse=True)
                if m.embed_duration
            ][:3]
            slow_write = [
                m
                for m in sorted(per_page_metrics, key=lambda x: x.weaviate_duration, reverse=True)
                if m.weaviate_duration
            ][:3]
            if slow_chunk:
                LOGGER.info(
                    "  • Slowest chunk durations (s): %s",
                    ", ".join(f"{m.page_uid}:{m.chunk_duration:.3f}" for m in slow_chunk),
                )
            if slow_embed:
                LOGGER.info(
                    "  • Slowest embed durations (s): %s",
                    ", ".join(f"{m.page_uid}:{m.embed_duration:.3f}" for m in slow_embed),
                )
            if slow_write:
                LOGGER.info(
                    "  • Slowest write durations (s): %s",
                    ", ".join(f"{m.page_uid}:{m.weaviate_duration:.3f}" for m in slow_write),
                )

        summary = make_summary(
            status="success",
            stats=stats,
            durations=merge(durations, {"uids": step1_time, "chunker_wait": step3_time}),
            metadata_applied=metadata_applied,
            extra={
                "elapsed_seconds": elapsed_time,
                "pages_processed": pages_processed_this_run,
                "processed_offset": processed_offset,
                "total_target_pages": total_target_pages,
                "total_pages": total_pages_discovered,
                "missing_edit_time_count": len(pages_missing_edit_time),
                "empty_linearized_count": len(pages_empty_linearized),
                "max_edit_time": max_edit_time_seen,
                "since": since,
                "test_limit": test_limit,
                "state_file": state_path,
                "state_loaded": state_loaded,
                "resume": resume,
                "started_at": start_timestamp,
                "step1_time": step1_time,
                "chunker_time": step3_time,
                "failures": failures,
            },
        )
        await emit_completion(summary)
        record_run(run_id, "success", since=since, test_limit=test_limit, notes=summary)
        return summary
    except Exception as exc:
        summary = make_summary(
            status="failed",
            stats=stats,
            durations=durations,
            metadata_applied=metadata_applied,
            extra={
                "error": str(exc),
                "pages_processed": pages_processed_this_run,
                "processed_offset": processed_offset,
                "total_target_pages": total_target_pages,
                "max_edit_time": max_edit_time_seen,
                "since": since,
                "test_limit": test_limit,
                "state_file": state_path,
                "state_loaded": state_loaded,
                "resume": resume,
                "started_at": start_timestamp,
                "total_pages": total_pages_discovered,
                "failures": failures,
            },
        )
        await emit_completion(summary)
        record_run(run_id, "failed", since=since, test_limit=test_limit, notes=summary)
        raise

    finally:
        if state_path and state_completed:
            remove_state_file(state_path)
        with suppress(Exception):
            await chunker_client.close()
        with suppress(Exception):
            was_connected = client.is_connected()
            await client.close()
            if was_connected:
                LOGGER.info("Weaviate sync client connection closed")


async def main() -> None:
    parser = argparse.ArgumentParser(description="Sync Roam graph to Weaviate using contextual embeddings.")
    parser.add_argument("--clear", action="store_true", help="Clear all existing objects before syncing.")
    parser.add_argument("--test", type=int, metavar="N", help="Test mode: only process first N pages.")
    parser.add_argument(
        "--recreate-collection",
        action="store_true",
        help="Force recreate the collection even if it exists.",
    )
    parser.add_argument("--state-file", type=str, help="Path to persist incremental sync progress.")
    parser.add_argument("--resume", action="store_true", help="Resume from a previously saved state file.")
    parser.add_argument(
        "--since",
        type=int,
        help="Only process pages whose max edit time is greater than the provided epoch milliseconds.",
    )

    args = parser.parse_args()

    await sync_semantic_graph(
        clear_existing=args.clear,
        test_limit=args.test,
        recreate_collection=args.recreate_collection,
        state_file=args.state_file,
        resume=args.resume,
        since=args.since,
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    asyncio.run(main())
    LOGGER.info("Done!")
