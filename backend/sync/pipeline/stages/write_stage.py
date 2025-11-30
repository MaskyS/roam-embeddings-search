"""
Stage 5: Weaviate Write

Bulk insert new objects to Weaviate and cleanup old versions
identified by content hash.
"""

from __future__ import annotations

import time
from typing import List, Optional, Tuple, TYPE_CHECKING

from funcy import lcat, lmap

from sync.data.results import WriteStageResult

if TYPE_CHECKING:
    from sync.data.models import PageWorkItem, WeaviateObjectSet
    from sync.resources import SyncResources


async def stage_write(
    validated_payloads: List[Tuple["PageWorkItem", "WeaviateObjectSet"]],
    resources: "SyncResources",
) -> WriteStageResult:
    """
    Stage 5: Write objects to Weaviate and cleanup old versions.

    Performs two operations:
    1. Bulk insert all objects (page + chunks) with their vectors
    2. Delete old objects for each page using content hash filtering

    Args:
        validated_payloads: List of (PageWorkItem, WeaviateObjectSet) with vectors attached
        resources: SyncResources containing Weaviate adapter and semaphore

    Returns:
        WriteStageResult with:
        - docs_added: Total Weaviate objects inserted
        - chunks_created: Number of chunk objects (excludes page objects)
        - pages_updated: Number of pages successfully written
        - state_updates: Dict of page_uid -> state for persistence
        - errors: Error messages if write failed
        - weaviate_duration/weaviate_wait: Timing metrics

    Cleanup Logic:
        After inserting new objects, old versions are deleted by filtering
        on page_uid where content_hash != new_hash. This ensures stale
        embeddings are cleaned up even if the page structure changed.

    Example:
        write_result = await stage_write(validate_result.validated_payloads, resources)
        if write_result.is_err:
            return GroupResult(pages_failed=len(validated_payloads), fail_messages=write_result.errors)

        # Persist state updates
        upsert_page_state(write_result.state_updates)
    """
    result = WriteStageResult()

    if not validated_payloads:
        return result

    # Flatten all objects from all pages
    weaviate_objects = lcat(
        lmap(lambda item_payload: item_payload[1].all_objects, validated_payloads)
    )

    try:
        weaviate_wait_start = time.time()
        async with resources.weaviate_semaphore:
            result.weaviate_wait = time.time() - weaviate_wait_start
            weaviate_start = time.time()

            # Bulk insert (retry handled by decorator on method)
            failed_objects = await resources.weaviate.insert_objects(weaviate_objects)
            result.weaviate_duration = time.time() - weaviate_start

            # Check for insertion failures
            if failed_objects:
                error_samples = ', '.join(
                    (error.message or 'unknown') for error in failed_objects[:3]
                )
                raise RuntimeError(
                    f"Weaviate reported {len(failed_objects)} failed objects: {error_samples}"
                )

            # Delete old versions by content hash (cleanup stale embeddings)
            for item, payload in validated_payloads:
                await resources.weaviate.delete_stale_objects(item.page_uid, payload.content_hash)

    except Exception as exc:
        # Write failure fails all pages in this group
        result.errors.append(f"Weaviate write failed for group: {exc}")
        return result

    # Populate success metrics
    result.docs_added = len(weaviate_objects)
    result.pages_updated = len(validated_payloads)
    result.chunks_created = sum(
        len(payload.chunk_objects) for _, payload in validated_payloads
    )

    # Prepare state updates for persistence
    for item, payload in validated_payloads:
        meta = item.snapshot.meta
        aggregated_edit = meta.max_edit_time or meta.max_block_edit_time
        result.state_updates[item.page_uid] = {
            "last_synced_edit_time": aggregated_edit,
            "content_hash": payload.content_hash,
        }

    return result
