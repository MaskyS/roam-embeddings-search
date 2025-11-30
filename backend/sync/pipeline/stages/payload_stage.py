"""
Stage 2: Payload Building

Transform chunks into Weaviate object structures with proper UUIDs,
metadata, and text previews.
"""

from __future__ import annotations

from typing import Any, Dict, List, TYPE_CHECKING

from sync.data.results import PayloadStageResult
from sync.data.transform import build_weaviate_objects

if TYPE_CHECKING:
    from sync.data.models import PageWorkItem
    from common.config import SyncConfig


def stage_build_payloads(
    group_items: List[PageWorkItem],
    chunk_results_by_index: Dict[int, List[Dict[str, Any]]],
    config: "SyncConfig",
) -> PayloadStageResult:
    """
    Stage 2: Build Weaviate object payloads from chunks.

    Transforms each page's chunks into Weaviate object structures
    with deterministic UUIDs, metadata properties, and text previews.

    Individual page failures are recorded but don't fail the entire stage.
    Other pages can still proceed.

    Args:
        group_items: List of PageWorkItem to process
        chunk_results_by_index: Mapping from page index to chunks (from stage_chunk)
        config: SyncConfig containing sync_version and uuid_namespace

    Returns:
        PayloadStageResult with:
        - processed_items: Successfully built (item, payload) tuples
        - errors: Error messages for failed pages

    Example:
        payload_result = stage_build_payloads(items, chunk_result.chunk_results_by_index, config)

        for item, payload in payload_result.processed_items:
            # payload.all_objects contains Weaviate objects
            # payload.chunk_texts contains text for embedding
            pass
    """
    result = PayloadStageResult()

    for idx, item in enumerate(group_items):
        chunk_data = chunk_results_by_index.get(idx, [])
        try:
            payload = build_weaviate_objects(
                snapshot=item.snapshot,
                chunk_results=chunk_data,
                sync_version=config.sync_version,
                namespace=config.uuid_namespace,
            )
            result.processed_items.append((item, payload))
        except Exception as exc:
            # Individual page failures are recorded but don't stop the group
            result.errors.append(
                f"Failed building payload for page '{item.page_title}' ({item.page_uid}): {exc}"
            )

    return result
