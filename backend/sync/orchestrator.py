"""High-level orchestration for the semantic sync pipeline."""

from __future__ import annotations

import time
import uuid
from contextlib import suppress
from dataclasses import replace
from datetime import datetime
from typing import Any, Dict, Optional

from funcy import silent
from structlog.stdlib import BoundLogger

from sync.state.db_persistence import (
    delete_page_state,
    initialise as initialise_state,
    list_page_state_uids,
    load_page_state as load_state_rows,
    record_run,
)
from sync.pipeline.batch_phase import process_batches
from common.config import SyncConfig, STATE_FLAG_METADATA_APPLIED
from sync.pipeline.metadata_phase import execute_metadata_phase
from sync.data.models import SyncRuntime
from sync.context import SyncContext
from sync.resources import acquire_resources
from sync.state.run_state import SyncRunParams, SyncRunState, StatusEmitter
from sync.state.file_persistence import load_state, remove_state_file

TO_INT = silent(int)


async def run_sync(
    *,
    params: SyncRunParams,
    roam_graph_name: str,
    roam_api_token: str,
    voyage_api_key: str,
    voyage_model: str,
    voyage_timeout: float,
    logger: BoundLogger,
) -> Dict[str, Any]:
    """Execute a full semantic sync run and return the summary payload."""

    start_time = time.time()
    start_timestamp = datetime.utcnow().isoformat()

    initialise_state()

    page_state_purged = 0
    if params.clear_existing or params.recreate_collection:
        existing_uids = list_page_state_uids()
        if existing_uids:
            delete_page_state(existing_uids)
            page_state_purged += len(existing_uids)
            logger.info("Cleared cached page state rows", count=len(existing_uids))

    run_id = str(uuid.uuid4())

    async with acquire_resources(
        config=params.config,
        roam_graph_name=roam_graph_name,
        roam_api_token=roam_api_token,
        voyage_api_key=voyage_api_key,
        voyage_model=voyage_model,
        voyage_timeout=voyage_timeout,
    ) as resources:
        client = resources.client
        weaviate_adapter = resources.weaviate

        step1_start = time.time()
        all_page_uids = await resources.roam_client.get_all_page_uids()
        step1_time = time.time() - step1_start

        runtime = SyncRuntime(
            pending_uids=list(all_page_uids),
            processed_offset=0,
            total_target_pages=len(all_page_uids),
        )

        state = SyncRunState(
            runtime=runtime,
            params=params,
            total_pages=len(all_page_uids),
            start_time=start_time,
            start_timestamp=start_timestamp,
            state_path=params.state_file,
            page_state_purged=page_state_purged,
        )

        status_emitter = StatusEmitter(
            callback=params.status_callback,
            logger=logger.bind(run_id=run_id),
            state=state,
        )

        await status_emitter.uids_loaded(total_pages=len(all_page_uids), started_at=start_timestamp)

        state.add_duration("uids", step1_time)

        if not all_page_uids:
            summary = status_emitter.build_summary(status="no_pages")
            if params.completion_callback:
                await params.completion_callback(summary)
            record_run(run_id, "no_pages", since=params.since, test_limit=params.test_limit, notes=summary)
            return summary

        stale_state_uids = set(list_page_state_uids()) - set(all_page_uids)
        if stale_state_uids:
            delete_page_state(stale_state_uids)
            state.page_state_purged += len(stale_state_uids)
            logger.info("Removed cached state for deleted pages", count=len(stale_state_uids))

        if params.test_limit:
            logger.info("TEST MODE", limit=params.test_limit)
            all_page_uids = all_page_uids[: params.test_limit]
            runtime.pending_uids = list(all_page_uids)
            runtime.total_target_pages = len(all_page_uids)
            state.total_pages = len(all_page_uids)

        saved_state: Optional[Dict[str, Any]] = None
        if params.resume and params.state_file:
            saved_state = load_state(params.state_file)
            if saved_state:
                runtime.state_loaded = True
                pending = saved_state.get("pending_page_uids", [])
                runtime.processed_offset = saved_state.get("processed_count", 0)
                runtime.total_target_pages = saved_state.get("total_pages", runtime.processed_offset + len(pending))
                runtime.metadata_applied = bool(saved_state.get(STATE_FLAG_METADATA_APPLIED, False))
                if pending:
                    runtime.pending_uids = pending
                    logger.info(
                        "Resuming from state file", path=params.state_file, pending=len(pending), processed=runtime.processed_offset
                    )
                    stored_since = saved_state.get("since")
                    if params.since is None and stored_since is not None:
                        state.params = _replace_params(state.params, since=stored_since)
                    elif params.since is not None and stored_since is not None and params.since != stored_since:
                        logger.warning(
                            "--since differs from stored state; using provided value", provided=params.since, stored=stored_since
                        )
                else:
                    summary = status_emitter.build_summary(status="resume_complete", elapsed_seconds=0.0)
                    if params.completion_callback:
                        await params.completion_callback(summary)
                    if params.state_file:
                        remove_state_file(params.state_file)
                    record_run(run_id, "resume_complete", since=params.since, test_limit=params.test_limit, notes=summary)
                    return summary
            else:
                logger.info("No valid state found at path", path=params.state_file)

        state.total_pages = runtime.total_target_pages
        params = state.params

        db_state_rows = load_state_rows(runtime.pending_uids)
        preloaded_state: Dict[str, Dict[str, Any]] = {}
        for uid, row in db_state_rows.items():
            last_synced = row.get("last_synced_edit_time")
            if last_synced is None:
                continue
            # Only preload authoritative fields from our DB; do not synthesize
            # page_objects/chunk_objects here. Existence will be confirmed via
            # Weaviate when needed in the metadata phase.
            preloaded_state[uid] = {
                "last_synced_edit_time": last_synced,
                "content_hash": row.get("content_hash"),
            }

        try:
            if params.clear_existing:
                logger.info("Deleting collection", collection=params.config.collection_name)
                with suppress(Exception):
                    await client.collections.delete(params.config.collection_name)

            if params.clear_existing or params.recreate_collection:
                await weaviate_adapter.ensure_schema(True)
            else:
                with suppress(Exception):
                    if not await client.collections.exists(params.config.collection_name):
                        await weaviate_adapter.ensure_schema(False)

            metadata_outcome = await execute_metadata_phase(
                state=state,
                config=params.config,
                preloaded_state=preloaded_state,
                weaviate_adapter=weaviate_adapter,
                roam_client=resources.roam_client,
                start_time=start_time,
                step1_time=step1_time,
            )

            if metadata_outcome.finished:
                summary = metadata_outcome.summary or {}
                if params.completion_callback:
                    await params.completion_callback(summary)
                if params.state_file:
                    remove_state_file(params.state_file)
                record_run(run_id, "metadata_skip", since=params.since, test_limit=params.test_limit, notes=summary)
                return summary

            logger.info("Connecting to chunker service")
            step3_start = time.time()
            with state.timer("chunker_wait"):
                chunker_ready = await resources.chunker.wait_until_ready()
            step3_time = time.time() - step3_start
            if not chunker_ready:
                state.record_failure("Chunker service not available")
                summary = status_emitter.build_summary(status="chunker_unavailable", include_full_failures=True)
                if params.completion_callback:
                    await params.completion_callback(summary)
                record_run(run_id, "chunker_unavailable", since=params.since, test_limit=params.test_limit, notes=summary)
                return summary

            await status_emitter.chunker_ready(duration=step3_time)

            if params.since is not None:
                readable_since = datetime.fromtimestamp(params.since / 1000).isoformat()
                logger.info("Applying --since filter", since=params.since, readable=readable_since)
                await status_emitter.since_applied(since=params.since, readable=readable_since)

            context = SyncContext(
                config=params.config,
                resources=resources,
                roam_client=resources.roam_client,
                logger=logger.bind(run_id=run_id),
            )
            await process_batches(state=state, context=context)

            elapsed_time = time.time() - start_time
            summary = status_emitter.build_summary(status="success", elapsed_seconds=elapsed_time, include_full_failures=True)
            if params.completion_callback:
                await params.completion_callback(summary)
            record_run(run_id, "success", since=params.since, test_limit=params.test_limit, notes=summary)
            return summary
        except Exception as exc:
            summary = status_emitter.build_summary(status="failed", error=str(exc), include_full_failures=True)
            if params.completion_callback:
                await params.completion_callback(summary)
            record_run(run_id, "failed", since=params.since, test_limit=params.test_limit, notes=summary)
            raise
        finally:
            if params.state_file and runtime.state_completed:
                remove_state_file(params.state_file)


def _replace_params(params: SyncRunParams, **overrides) -> SyncRunParams:
    return replace(params, **overrides)
