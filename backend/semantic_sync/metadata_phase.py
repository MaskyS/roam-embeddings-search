"""Metadata pre-pass (single decision point for skip/keep)."""

from __future__ import annotations

import asyncio
import time
from typing import Any, Dict, List, Mapping, Optional

from funcy import chunks, merge, silent

from ..persistent_state import upsert_page_state
from .config import SyncConfig
from .models import MetadataPassResult, MetadataPhaseOutcome, PageMetadata
from .roam_io import RoamClient
from .run_state import SyncRunState

TO_INT = silent(int)


async def execute_metadata_phase(
    *,
    state: SyncRunState,
    config: SyncConfig,
    preloaded_state: Dict[str, Dict[str, Any]],
    weaviate_adapter,
    roam_client: RoamClient,
    start_time: float,
    step1_time: float,
) -> MetadataPhaseOutcome:
    runtime = state.runtime
    params = state.params
    status_emitter = state.status_emitter
    if status_emitter is None:
        raise RuntimeError("StatusEmitter not attached to SyncRunState")

    should_run = (
        not runtime.metadata_applied
        and not params.clear_existing
        and not params.recreate_collection
        and bool(runtime.pending_uids)
    )

    if not should_run:
        return MetadataPhaseOutcome(finished=False)

    metadata_result = await run_metadata_pass(
        runtime.pending_uids,
        since=params.since,
        adapter=weaviate_adapter,
        config=config,
        preloaded_state=preloaded_state,
        roam_client=roam_client,
    )

    # Record skip reasons derived from metadata analysis only
    since_cnt = int(metadata_result.stats_delta.get("pages_since_filtered", 0) or 0)
    if since_cnt:
        state.record_skip("since", since_cnt)
    # metadata_filtered includes both since and content-based unchanged; derive content-only
    meta_filtered = int(metadata_result.stats_delta.get("metadata_filtered", 0) or 0)
    content_cnt = max(0, meta_filtered - since_cnt)
    if content_cnt:
        state.record_skip("content", content_cnt)
    for key, delta in metadata_result.durations_delta.items():
        if delta is not None:
            state.add_duration(key, float(delta))
    # Do not track a separate 'metadata' skip bucket; normalized to 'since'/'content' above

    state.pages_missing_edit_time.update(metadata_result.missing_edit_uids)
    if metadata_result.max_edit_time_seen is not None:
        runtime.max_edit_time_seen = (
            metadata_result.max_edit_time_seen
            if runtime.max_edit_time_seen is None
            else max(runtime.max_edit_time_seen, metadata_result.max_edit_time_seen)
        )

    upsert_payload: Dict[str, Dict[str, Any]] = {}
    for uid, meta in metadata_result.metadata_map.items():
        aggregated_edit_time = (
            meta.aggregated_edit_time if meta.aggregated_edit_time is not None else meta.max_edit_time
        )
        if aggregated_edit_time is None:
            continue

        existing_state = (
            metadata_result.state_cache.get(uid)
            or preloaded_state.get(uid)
            or {}
        )

        record: Dict[str, Any] = {"last_synced_edit_time": TO_INT(aggregated_edit_time)}
        existing_hash = existing_state.get("content_hash") if isinstance(existing_state, dict) else None
        if existing_hash is not None:
            record["content_hash"] = existing_hash

        upsert_payload[uid] = record

    if upsert_payload:
        upsert_page_state(upsert_payload)

    runtime.pending_uids = metadata_result.remaining_uids
    runtime.metadata_map = metadata_result.metadata_map
    runtime.page_state_cache = dict(metadata_result.state_cache)
    runtime.metadata_applied = True

    await status_emitter.metadata_filtered(
        remaining=len(runtime.pending_uids),
        skipped=int(metadata_result.stats_delta.get("metadata_filtered", 0) or 0),
        metadata_durations={
            "metadata_pull": metadata_result.durations_delta.get("metadata_pull", 0.0),
            "weaviate_meta": metadata_result.durations_delta.get("weaviate_meta", 0.0),
        },
    )

    if runtime.pending_uids:
        return MetadataPhaseOutcome(finished=False)

    summary = status_emitter.build_summary(
        status="metadata_skip",
        elapsed_seconds=time.time() - start_time,
        include_full_failures=True,
    )
    return MetadataPhaseOutcome(finished=True, summary=summary)


async def run_metadata_pass(
    uids: List[str],
    *,
    since: Optional[int],
    adapter,
    config: SyncConfig,
    preloaded_state: Optional[Dict[str, Dict[str, Any]]] = None,
    roam_client: RoamClient,
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
        results = await roam_client.pull_many_metadata(batch)
        for uid, payload in zip(batch, results or []):
            meta = extract_page_metadata(payload)
            if meta:
                aggregated = meta.aggregated_edit_time if meta.aggregated_edit_time is not None else meta.max_edit_time
                metadata_map[uid] = meta
                if aggregated is not None:
                    max_edit_seen = aggregated if max_edit_seen is None else max(max_edit_seen, aggregated)
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
        aggregated = None
        if meta:
            aggregated = meta.aggregated_edit_time if meta.aggregated_edit_time is not None else meta.max_edit_time
        if aggregated is not None and since is not None and aggregated <= since:
            stats_delta["pages_since_filtered"] += 1
            stats_delta["pages_skipped"] += 1
            stats_delta["metadata_filtered"] += 1
            continue
        remaining_after_since.append(uid)

    state_fetch_uids = [
        uid
        for uid in remaining_after_since
        if metadata_map.get(uid)
        and (
            metadata_map[uid].aggregated_edit_time is not None
            or metadata_map[uid].max_edit_time is not None
        )
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
                if isinstance(result, Exception):
                    state_cache[uid] = {}
                else:
                    state_cache[uid] = result or {}

    remaining_uids: List[str] = []
    retained_state_cache: Dict[str, Dict[str, Any]] = dict(state_cache)
    for uid in remaining_after_since:
        meta = metadata_map.get(uid)
        state_entry = state_cache.get(uid)

        aggregated = None
        if meta:
            aggregated = meta.aggregated_edit_time if meta.aggregated_edit_time is not None else meta.max_edit_time
        if aggregated is not None and state_entry:
            stored_edit = TO_INT(state_entry.get("last_synced_edit_time")) if state_entry.get("last_synced_edit_time") is not None else None
            if stored_edit is not None and stored_edit >= aggregated and state_entry.get("page_objects"):
                stats_delta["metadata_filtered"] += 1
                stats_delta["pages_skipped"] += 1
                continue

        remaining_uids.append(uid)
        if state_entry is not None:
            retained_state_cache[uid] = state_entry

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


def extract_page_metadata(page_data: Optional[Dict[str, Any]]) -> Optional[PageMetadata]:
    if not page_data or not isinstance(page_data, dict):
        return None

    page_uid = page_data.get(":block/uid")
    if not page_uid:
        return None

    max_edit: Optional[int] = None
    has_children = bool(page_data.get(":block/children"))
    page_title = page_data.get(":node/title") or page_data.get(":block/string")

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
    return PageMetadata(
        page_uid=page_uid,
        max_edit_time=max_edit,
        has_children=has_children,
        page_title=page_title,
        aggregated_edit_time=max_edit,
        raw=page_data,
    )
