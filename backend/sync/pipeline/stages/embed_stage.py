"""
Stage 3: Embedding

Generate vector representations using VoyageAI's contextualized embeddings
with automatic token-aware segmentation for large documents.
"""

from __future__ import annotations

import time
from typing import List, Tuple, TYPE_CHECKING

from funcy import lmap

from sync.data.results import EmbedStageResult

if TYPE_CHECKING:
    from sync.data.models import PageWorkItem, WeaviateObjectSet
    from sync.resources import SyncResources


# Import the segmentation function from batch_phase
# This handles the complex token-budget-aware batching logic
from sync.pipeline.batch_phase import (
    _embed_with_segmentation,
    DOCUMENT_TOKEN_BUDGET,
    REQUEST_TOKEN_BUDGET,
)


async def stage_embed(
    processed_items: List[Tuple["PageWorkItem", "WeaviateObjectSet"]],
    resources: "SyncResources",
) -> EmbedStageResult:
    """
    Stage 3: Generate embeddings with token-aware segmentation.

    Uses VoyageAI contextualized embeddings which consider surrounding
    chunks when generating vectors. Large pages are automatically
    segmented to respect Voyage API limits:
    - Per-document: 32K tokens
    - Per-request: 120K tokens

    Args:
        processed_items: List of (PageWorkItem, WeaviateObjectSet) from stage_build_payloads
        resources: SyncResources containing embedder client and semaphore

    Returns:
        EmbedStageResult with:
        - embeddings_nested: List of embeddings preserving input structure
          embeddings_nested[page_idx][chunk_idx] = embedding vector
        - errors: Error messages if embedding failed
        - voyage_duration/voyage_wait: Timing metrics

    Token Segmentation:
        The embedding function handles pages that exceed the 32K token limit
        by splitting them into segments and processing in round-robin order
        across pages for maximum API efficiency.

    Example:
        embed_result = await stage_embed(payload_result.processed_items, resources)
        if embed_result.is_err:
            return GroupResult(pages_failed=len(processed_items), fail_messages=embed_result.errors)

        # embed_result.embeddings_nested[i] corresponds to processed_items[i]
    """
    result = EmbedStageResult()

    if not processed_items:
        return result

    try:
        voyage_wait_start = time.time()
        async with resources.embed_semaphore:
            result.voyage_wait = time.time() - voyage_wait_start
            voyage_start = time.time()

            # Extract chunk texts from all payloads
            pages_texts = lmap(
                lambda item_payload: item_payload[1].chunk_texts,
                processed_items
            )

            # Embed with automatic segmentation for pages exceeding token limits
            result.embeddings_nested = await _embed_with_segmentation(
                pages_texts,
                resources.embedder,
                per_doc_budget=DOCUMENT_TOKEN_BUDGET,
                per_request_budget=REQUEST_TOKEN_BUDGET,
            )

            result.voyage_duration = time.time() - voyage_start

    except Exception as exc:
        # Embedding failure fails all pages in this group
        result.errors.append(f"Voyage embedding failed for group: {exc}")

    return result
