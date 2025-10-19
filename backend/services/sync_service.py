"""Sync management API router (mounted into the search service)."""

from __future__ import annotations

import asyncio
import os
from datetime import datetime
from typing import Any, Dict, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query, Request

from services.search_service import get_context  # reuse app context dependency
from sync.state.db_persistence import list_recent_runs, delete_page_state, list_page_state_uids

router = APIRouter()


DEFAULT_STATE_FILE = os.getenv(
    "SYNC_STATE_FILE",
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "sync_state.json"),
)


def _job_view(job: Dict[str, Any]) -> Dict[str, Any]:
    public = {k: v for k, v in job.items() if k != "task"}
    if "params" in public and isinstance(public["params"], dict):
        public["params"] = dict(public["params"])
    if "progress" in public and isinstance(public["progress"], dict):
        public["progress"] = dict(public["progress"])
    if "summary" in public and isinstance(public["summary"], dict):
        public["summary"] = dict(public["summary"])
    return public


async def _run_sync_job(app, sync_kwargs: Dict[str, Any]) -> None:
    lock: asyncio.Lock = app.state.sync_lock
    job: Dict[str, Any] = app.state.sync_job

    from cli.sync import sync_semantic_graph  # local import to avoid circular

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


@router.post("/sync/start", status_code=202)
async def start_sync(
    payload: Dict[str, Any] = Body(default_factory=dict),
    request: Request = None,
    ctx=Depends(get_context),
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

    since_value: Optional[int] = None
    if mode == "since":
        since_value = payload.get("since")
        if since_value is not None and not isinstance(since_value, int):
            raise HTTPException(status_code=400, detail="since must be epoch milliseconds")
    elif mode == "limit":
        limit_value = payload.get("limit")
        # Be lenient: coerce numeric strings like "25" to int
        if isinstance(limit_value, str):
            try:
                limit_value = int(limit_value)
            except ValueError:
                pass
        if limit_value is None or not isinstance(limit_value, int) or limit_value <= 0:
            raise HTTPException(status_code=400, detail="limit must be a positive integer")
    else:
        limit_value = None

    async with lock:
        if job.get("status") == "running":
            raise HTTPException(status_code=409, detail=_job_view(job))

        job.update(
            {
                "status": "running",
                "run_id": datetime.utcnow().strftime("%Y%m%d-%H%M%S"),
                "mode": mode,
                "params": {
                    "clear": clear,
                    "recreate_collection": recreate,
                    "resume": resume,
                    "state_file": state_file_path,
                    "since": since_value,
                    "limit": payload.get("limit"),
                },
                "started_at": datetime.utcnow().isoformat(),
                "finished_at": None,
                "progress": {},
                "summary": {},
                "error": None,
            }
        )

        sync_kwargs: Dict[str, Any] = {
            "clear_existing": clear,
            "test_limit": limit_value if mode == "limit" else None,
            "recreate_collection": recreate,
            "state_file": state_file_path,
            "resume": resume,
            "since": since_value,
        }

        task = asyncio.create_task(_run_sync_job(app_state, sync_kwargs))
        job["task"] = task

        view = _job_view(job)

    return view


@router.get("/sync/status")
async def get_sync_status(request: Request, ctx=Depends(get_context)) -> Dict[str, Any]:
    lock: asyncio.Lock = request.app.state.sync_lock
    async with lock:
        return _job_view(request.app.state.sync_job)


@router.get("/sync/runs")
async def get_recent_runs(limit: int = Query(10, ge=1, le=100)) -> Dict[str, Any]:
    runs = list_recent_runs(limit=limit)
    return {"runs": runs, "count": len(runs)}


@router.post("/sync/cancel")
async def cancel_sync(request: Request, ctx=Depends(get_context)) -> Dict[str, Any]:
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


@router.post("/sync/clear", status_code=202)
async def clear_database(request: Request, ctx=Depends(get_context)) -> Dict[str, Any]:
    import weaviate
    from common.config import CONFIG as SYNC_CONFIG

    lock: asyncio.Lock = request.app.state.sync_lock
    async with lock:
        job: Dict[str, Any] = request.app.state.sync_job
        if job.get("status") == "running":
            raise HTTPException(status_code=409, detail=_job_view(job))

        client = weaviate.connect_to_custom(
            http_host=SYNC_CONFIG.weaviate_http_host,
            http_port=SYNC_CONFIG.weaviate_http_port,
            http_secure=SYNC_CONFIG.weaviate_http_secure,
            grpc_host=SYNC_CONFIG.weaviate_grpc_host,
            grpc_port=SYNC_CONFIG.weaviate_grpc_port,
            grpc_secure=SYNC_CONFIG.weaviate_grpc_secure,
            skip_init_checks=True,
        )
        try:
            name = SYNC_CONFIG.collection_name
            if client.collections.exists(name):
                client.collections.delete(name)
        finally:
            client.close()

        cleared_at = datetime.utcnow().isoformat()
        # Clear cached page_state rows in SQLite to keep state consistent with Weaviate
        try:
            stale_uids = list_page_state_uids()
            if stale_uids:
                delete_page_state(stale_uids)
                job.setdefault("history", [])
                job["history"].append({"event": "state_cleared", "at": cleared_at, "count": len(stale_uids)})
        except Exception:
            # Non-fatal: log history note without blocking the response
            job.setdefault("history", [])
            job["history"].append({"event": "state_clear_failed", "at": cleared_at})
        job.setdefault("history", [])
        job["history"].append({"event": "collection_cleared", "at": cleared_at})

        summary = job.get("summary", {})
        summary.update({"status": "cleared", "cleared_at": cleared_at})
        job["summary"] = summary
        job["status"] = job.get("status", "idle")

        return {"status": "cleared", "cleared_at": cleared_at}
