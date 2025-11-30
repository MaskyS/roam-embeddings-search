"""
Stage 1: Chunking

Split pages with children into smaller semantic chunks using the
external chunker service (Chonkie).

Pages without children skip chunking and get empty chunk lists.
"""

from __future__ import annotations

import time
from typing import List, TYPE_CHECKING

from funcy import lmap, lsplit

from sync.data.results import ChunkStageResult

if TYPE_CHECKING:
    from sync.data.models import PageWorkItem
    from sync.resources import SyncResources


async def stage_chunk(
    group_items: List[PageWorkItem],
    resources: "SyncResources",
) -> ChunkStageResult:
    """
    Stage 1: Split pages with children into semantic chunks.

    Pages with children are sent to the chunker service for semantic
    splitting. Pages without children get empty chunk lists and skip
    the chunker entirely.

    Args:
        group_items: List of PageWorkItem to process
        resources: SyncResources containing chunker client and semaphore

    Returns:
        ChunkStageResult with either:
        - chunk_results_by_index populated (success)
        - errors populated (failure)

    Example:
        result = await stage_chunk(items, resources)
        if result.is_err:
            return GroupResult(pages_failed=len(items), fail_messages=result.errors)

        # Access chunks for page at index 0
        chunks = result.chunk_results_by_index[0]
    """
    result = ChunkStageResult()

    try:
        # Separate pages that need chunking from those that don't
        # need_chunk: pages with children (need external chunking service)
        # no_chunk: leaf pages or pages without children (skip chunking)
        need_chunk, no_chunk = lsplit(
            lambda indexed_item: indexed_item[1].snapshot.has_children,
            enumerate(group_items)
        )

        if need_chunk:
            # Extract linearized text from pages that need chunking
            texts = lmap(
                lambda indexed_item: indexed_item[1].snapshot.linearized_text or "",
                need_chunk
            )

            # Chunk with semaphore-based rate limiting
            chunk_wait_start = time.time()
            async with resources.chunk_semaphore:
                result.chunk_wait = time.time() - chunk_wait_start
                chunk_start = time.time()
                chunk_batches = await resources.chunker.chunk_batch(texts)
                result.chunk_duration = time.time() - chunk_start

            # Map chunk results back to page indices
            for (idx, _), chunks in zip(need_chunk, chunk_batches):
                result.chunk_results_by_index[idx] = chunks or []

        # Pages without children get empty chunk lists
        for idx, _ in no_chunk:
            result.chunk_results_by_index[idx] = []

    except Exception as exc:
        # Chunking failure fails the entire group (all-or-nothing for consistency)
        result.errors.append(f"Chunker failed for group: {exc}")

    return result
