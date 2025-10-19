"""Batch processing phase: chunk (if needed), embed, write."""

from __future__ import annotations

import asyncio
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from funcy import chunks, compact, lcat, lmap, lpluck, lsplit

from sync.state.file_persistence import persist_state
from sync.state.db_persistence import upsert_page_state
from common.config import SyncConfig, STATE_FLAG_METADATA_APPLIED
from sync.context import SyncContext
from sync.data.models import GroupResult, PageSnapshot, PageWorkItem, WeaviateObjectSet
from sync.data.transform import collect_page_snapshot, build_weaviate_objects
from sync.resources import SyncResources
from common.retry import (
    chunk_batch_with_retry,
    embed_documents_with_retry,
    weaviate_delete_with_retry,
    weaviate_insert_with_retry,
)
from sync.state.run_state import SyncRunState


async def process_page_group(
    group_items: List[PageWorkItem],
    resources: SyncResources,
    *,
    config: SyncConfig,
) -> GroupResult:
    result = GroupResult()
    try:
        need_chunk, no_chunk = lsplit(
            lambda p: p[1].snapshot.has_children,
            enumerate(group_items)
        )

        chunk_results_by_index: Dict[int, List[Dict[str, Any]]] = {}

        if need_chunk:
            texts = lmap(lambda p: p[1].snapshot.linearized_text or "", need_chunk)
            chunk_wait_start = time.time()
            async with resources.chunk_semaphore:
                result.chunk_wait = time.time() - chunk_wait_start
                chunk_start = time.time()
                chunk_batches = await chunk_batch_with_retry(resources.chunker, texts)
                result.chunk_duration = time.time() - chunk_start
            for (idx, _), chunks in zip(need_chunk, chunk_batches):
                chunk_results_by_index[idx] = chunks or []
        for idx, _ in no_chunk:
            chunk_results_by_index[idx] = []
    except Exception as exc:  # pragma: no cover
        result.pages_failed = len(group_items)
        result.fail_messages.append(f"  ✗ Chunker failed for group: {exc}")
        return result

    processed_items: List[Tuple[PageWorkItem, WeaviateObjectSet]] = []
    for idx, item in enumerate(group_items):
        chunk_data = chunk_results_by_index.get(idx, [])
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
        async with resources.embed_semaphore:
            result.voyage_wait = time.time() - voyage_wait_start
            voyage_start = time.time()
            embeddings_nested = await embed_documents_with_retry(
                resources.embedder,
                [payload.chunk_texts for _, payload in processed_items],
            )
            result.voyage_duration = time.time() - voyage_start
    except Exception as exc:
        result.pages_failed += len(processed_items)
        result.fail_messages.append(f"  ✗ Voyage embedding failed for group: {exc}")
        return result

    successful_payloads: List[Tuple[PageWorkItem, WeaviateObjectSet]] = []
    for (item, payload), embeddings in zip(processed_items, embeddings_nested):
        if len(embeddings) != len(payload.all_objects):
            result.pages_failed += 1
            result.fail_messages.append(
                f"  ✗ Embedding count mismatch for page '{item.page_title}' ({item.page_uid})"
            )
            continue
        for obj, vector in zip(payload.all_objects, embeddings):
            obj["vector"] = vector
        successful_payloads.append((item, payload))

    if not successful_payloads:
        return result

    weaviate_objects = lcat(lmap(lambda p: p[1].all_objects, successful_payloads))
    try:
        weaviate_wait_start = time.time()
        async with resources.weaviate_semaphore:
            result.weaviate_wait = time.time() - weaviate_wait_start
            weaviate_start = time.time()
            failed_objects = await weaviate_insert_with_retry(resources.weaviate, weaviate_objects)
            result.weaviate_duration = time.time() - weaviate_start
            if failed_objects:
                raise RuntimeError(
                    f"Weaviate reported {len(failed_objects)} failed objects: {', '.join((error.message or '') for error in failed_objects[:3])}"
                )
            for item, payload in successful_payloads:
                await weaviate_delete_with_retry(
                    resources.weaviate,
                    item.page_uid,
                    payload.content_hash,
                )
    except Exception as exc:
        result.pages_failed += len(successful_payloads)
        result.fail_messages.append(f"  ✗ Weaviate write failed for group: {exc}")
        return result

    result.docs_added = len(weaviate_objects)
    result.pages_updated = len(successful_payloads)
    result.chunks_created = sum(len(payload.chunk_objects) for _, payload in successful_payloads)

    state_updates: Dict[str, Dict[str, Optional[str]]] = {}
    for item, payload in successful_payloads:
        meta = item.snapshot.meta
        aggregated_edit = meta.max_edit_time or meta.max_block_edit_time
        state_updates[item.page_uid] = {
            "last_synced_edit_time": aggregated_edit,
            "content_hash": payload.content_hash,
        }
    result.state_updates = state_updates

    return result


async def process_batches(*, state: SyncRunState, context: SyncContext) -> int:
    runtime = state.runtime
    params = state.params
    status_emitter = state.status_emitter
    if status_emitter is None:
        raise RuntimeError("StatusEmitter not attached to SyncRunState")

    resources = context.resources
    config = context.config
    roam_client = context.roam_client

    pages_processed = 0
    batch_num = 0

    while runtime.pending_uids:
        batch = runtime.pending_uids[: config.batch_size]
        batch_size = len(batch)
        if not batch:
            break

        batch_num += 1
        current_start = runtime.processed_offset + pages_processed + 1
        current_end = current_start + batch_size - 1

        await status_emitter.batch_start(
            batch=batch_num,
            page_range=(current_start, current_end),
            processed_before=runtime.processed_offset + pages_processed,
        )

        uids_childless, uids_with_children = lsplit(
            lambda uid: runtime.metadata_map.get(uid) and not runtime.metadata_map[uid].has_children,
            batch
        )

        pulled_map: Dict[str, Optional[Dict[str, Any]]] = {}
        if uids_with_children:
            with state.timer("roam"):
                pulled_pages = await roam_client.pull_many_pages(uids_with_children)
            for uid, pdata in zip(uids_with_children, pulled_pages):
                pulled_map[uid] = pdata

        for uid in uids_childless:
            meta = runtime.metadata_map.get(uid)
            title = (meta.page_title if meta else None) or ""
            pulled_map[uid] = {
                ":block/uid": uid,
                ":node/title": title,
                ":block/children": [],
                ":edit/time": (
                    meta.aggregated_edit_time
                    if meta and meta.aggregated_edit_time is not None
                    else (meta.max_edit_time if meta else None)
                ),
            }

        pages_data = [pulled_map.get(uid) for uid in batch]

        work_items: List[PageWorkItem] = []
        for offset, page_data in enumerate(pages_data):
            if not page_data or not page_data.get(":block/uid"):
                state.increment_stat("pages_failed")
                continue

            page_uid = page_data.get(":block/uid")
            page_title = page_data.get(":node/title") or page_data.get(":block/string") or "Untitled"
            page_number = current_start + offset

            with state.timer("linearize"):
                snapshot: PageSnapshot = collect_page_snapshot(page_data)

            max_edit_time_val = snapshot.meta.max_edit_time or snapshot.meta.max_block_edit_time
            if max_edit_time_val is None:
                state.pages_missing_edit_time.add(page_uid)
            if not snapshot.linearized_text.strip() and snapshot.has_children:
                state.pages_empty_linearized.add(page_uid)

            meta_entry = runtime.metadata_map.get(page_uid)
            candidate_time = (
                max_edit_time_val
                if max_edit_time_val is not None
                else (
                    meta_entry.aggregated_edit_time
                    if meta_entry and meta_entry.aggregated_edit_time is not None
                    else (meta_entry.max_edit_time if meta_entry else None)
                )
            )
            if candidate_time is not None:
                runtime.max_edit_time_seen = (
                    candidate_time
                    if runtime.max_edit_time_seen is None
                    else max(runtime.max_edit_time_seen, candidate_time)
                )

            work_items.append(
                PageWorkItem(
                    snapshot=snapshot,
                    page_title=page_title,
                    page_uid=page_uid,
                    page_num=page_number,
                )
            )

        results: List[GroupResult] = []

        async def add_group(items: List[PageWorkItem]) -> None:
            result = await process_page_group(items, resources, config=config)
            results.append(result)

        async with asyncio.TaskGroup() as tg:
            for group in chunks(config.chunker_group_size, work_items):
                group_list = list(group)
                if not group_list:
                    continue
                tg.create_task(add_group(group_list))

        for result in results:
            if result.pages_updated:
                state.increment_stat("pages_updated", result.pages_updated)
            if result.pages_failed:
                state.increment_stat("pages_failed", result.pages_failed)
            state.add_duration("chunk", result.chunk_duration)
            state.add_duration("voyage", result.voyage_duration)
            state.add_duration("weaviate", result.weaviate_duration)
            state.add_duration("chunk_wait", result.chunk_wait)
            state.add_duration("voyage_wait", result.voyage_wait)
            state.add_duration("weaviate_wait", result.weaviate_wait)

            if result.state_updates:
                upsert_page_state(result.state_updates)
                for uid, update in result.state_updates.items():
                    last_synced = update.get("last_synced_edit_time")
                    if last_synced is None:
                        continue
                    runtime.page_state_cache[uid] = {
                        "page_objects": [
                            {
                                "properties": {
                                    "last_synced_edit_time": str(last_synced),
                                    "content_hash": update.get("content_hash"),
                                }
                            }
                        ],
                        "chunk_objects": [],
                        "last_synced_edit_time": last_synced,
                        "content_hash": update.get("content_hash"),
                    }

        # Collect fail_messages from GroupResult instances without subscripting
        for msg in lcat(lmap(lambda r: r.fail_messages, results)):
            state.record_failure(msg)

        pages_processed += batch_size
        runtime.pending_uids = runtime.pending_uids[batch_size:]

        await status_emitter.batch_complete(
            batch=batch_num,
            processed_after=runtime.processed_offset + pages_processed,
        )

        if state.state_path:
            state_payload = compact(
                {
                    "created_at": datetime.utcnow().isoformat() + "Z",
                    "total_pages": runtime.total_target_pages,
                    "processed_count": runtime.processed_offset + pages_processed,
                    "pending_page_uids": runtime.pending_uids,
                    "since": params.since,
                    "test_limit": params.test_limit,
                    STATE_FLAG_METADATA_APPLIED: runtime.metadata_applied,
                }
            )
            persist_state(state.state_path, state_payload)
            runtime.state_loaded = True

    runtime.state_completed = True
    return pages_processed
