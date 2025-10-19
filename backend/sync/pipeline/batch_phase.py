"""Batch processing phase: chunk (if needed), embed, write."""

from __future__ import annotations

import asyncio
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from funcy import chunks, compact, lcat, lmap, lpluck, lsplit, reductions, last

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

# Voyage context-3 model limits (see docs/external/voyageai/context-model-guide.md:81-84)
# - Context length: 32,000 tokens per document
# - Total tokens: 120,000 tokens per request
# - Total chunks: 16,000 chunks per request
# - Max inputs: 1,000 documents per request
VOYAGE_CONTEXT_3_MAX_DOCUMENT_TOKENS = 32_000
VOYAGE_CONTEXT_3_MAX_REQUEST_TOKENS = 120_000
VOYAGE_CONTEXT_3_MAX_CHUNKS = 16_000
VOYAGE_CONTEXT_3_MAX_INPUTS = 1_000

# Safety margins (3% for document, 8% for request to account for estimation errors)
DOCUMENT_TOKEN_BUDGET = int(VOYAGE_CONTEXT_3_MAX_DOCUMENT_TOKENS * 0.97)  # 31,040
REQUEST_TOKEN_BUDGET = int(VOYAGE_CONTEXT_3_MAX_REQUEST_TOKENS * 0.92)    # 110,400

# Token estimation heuristic
# Note: Conservative estimate. English text averages 4-5 chars/token,
# but technical content and code can be lower. Consider using tiktoken for accuracy.
CHARS_PER_TOKEN_ESTIMATE = 4


# Type aliases for clarity in the 3-dimensional segment structure
Segment = List[str]        # One segment of texts that fits in 32K token budget
PageSegments = List[Segment]  # All segments for one page
BatchedSegments = List[Segment]  # Segments batched together for one API call


def _estimate_tokens(text: str) -> int:
    """
    Estimate token count using character-based heuristic.
    
    Uses 4 chars per token as a conservative estimate. For production accuracy,
    consider using tiktoken with the 'cl100k_base' encoding (Voyage AI compatible).
    
    Args:
        text: Text to estimate token count for
        
    Returns:
        Estimated token count (minimum 1)
    """
    return max(1, len(text) // CHARS_PER_TOKEN_ESTIMATE)


def _split_into_segments(texts: List[str], *, per_doc_budget: int) -> PageSegments:
    """
    Split a page's texts into segments that respect the per-document token budget.
    
    Segments have no overlap and preserve the original text order. Each text is
    placed into the current segment unless adding it would exceed the budget,
    in which case a new segment is started.
    
    Args:
        texts: List of text chunks from a single page (e.g., title + chunk texts)
        per_doc_budget: Maximum tokens allowed per segment (Voyage limit: 32K)
        
    Returns:
        List of segments, each segment being a list of texts that fit the budget
        
    Example:
        texts = ["chunk1 (15K tok)", "chunk2 (15K tok)", "chunk3 (10K tok)"]
        per_doc_budget = 31_000
        → [["chunk1", "chunk2"], ["chunk3"]]  # 2 segments
    """
    segments: PageSegments = []
    current_segment: Segment = []
    current_tokens = 0

    for text in texts:
        text_tokens = _estimate_tokens(text)

        # Would adding this text overflow the current segment?
        if current_segment and current_tokens + text_tokens > per_doc_budget:
            # Finalize current segment and start a new one
            segments.append(current_segment)
            current_segment = []
            current_tokens = 0

        # Add text to current segment
        current_segment.append(text)
        current_tokens += text_tokens

    # Don't forget the final segment
    if current_segment:
        segments.append(current_segment)

    return segments


def _batch_segments_for_round(
    segments_by_page: List[PageSegments],
    round_index: int,
    ready_pages: List[int],
    per_request_budget: int
) -> List[Tuple[List[int], BatchedSegments]]:
    """
    Batch segments from ready pages into API calls respecting per-request token budget.
    
    Uses funcy's reductions pattern to accumulate segments into batches while
    tracking token counts. When a segment would overflow the current batch,
    flushes the batch and starts a new one.
    
    Args:
        segments_by_page: All segments for all pages (3D structure)
        round_index: Current round (which segment index to process)
        ready_pages: Page indices that have a segment at this round
        per_request_budget: Maximum tokens allowed per API request (Voyage limit: 120K)
        
    Returns:
        List of (page_indices, batched_segments) tuples ready to send to API
        
    Example:
        ready_pages = [0, 1, 2]
        segments_by_page[0][round_index] = ["A1", "A2"]  # 30K tokens
        segments_by_page[1][round_index] = ["B1", "B2"]  # 25K tokens
        segments_by_page[2][round_index] = ["C1", "C2"]  # 30K tokens
        per_request_budget = 110_000
        
        → [([0, 1, 2], [["A1", "A2"], ["B1", "B2"], ["C1", "C2"]])]
        # Single API call with 85K tokens total
        
        If one segment is 60K tokens:
        → [([0], [["A1", "A2"]]), ([1, 2], [["B1", "B2"], ["C1", "C2"]])]
        # Two API calls to stay under 110K limit
    """
    # Prepare page data with precomputed token counts
    # Each element: (page_index, segment, token_count)
    page_segment_data = [
        (
            page_idx,
            segments_by_page[page_idx][round_index],
            sum(_estimate_tokens(text) for text in segments_by_page[page_idx][round_index])
        )
        for page_idx in ready_pages
    ]

    # Accumulator function for funcy's reductions
    # State: (completed_batches, current_batch, current_indices, current_token_count)
    def accumulate_batch(state, page_segment_tokens):
        batches, curr_batch, curr_indices, curr_tokens = state
        page_idx, segment, segment_tokens = page_segment_tokens

        # Would adding this segment overflow the current batch?
        if curr_batch and curr_tokens + segment_tokens > per_request_budget:
            # Finalize current batch and start fresh
            return (
                batches + [(curr_indices, curr_batch)],  # Add completed batch
                [segment],              # Start new batch with this segment
                [page_idx],             # Track this page index
                segment_tokens          # Reset token count
            )

        # Accumulate into current batch
        return (
            batches,
            curr_batch + [segment],
            curr_indices + [page_idx],
            curr_tokens + segment_tokens
        )

    # Use reductions to build batches with token-aware accumulation
    # Initial state: ([], [], [], 0) = (no batches, empty batch, no indices, 0 tokens)
    initial_state = ([], [], [], 0)
    final_state = last(reductions(accumulate_batch, page_segment_data, initial_state))
    final_batches, final_batch, final_indices, _ = final_state

    # Don't forget to include the final batch if it has content
    if final_batch:
        final_batches = final_batches + [(final_indices, final_batch)]

    # Validate each batch respects Voyage per-request limits
    # This catches batching logic bugs before they reach the API
    for _indices, batched_segments in final_batches:
        # Check chunk count per batch (16K limit is per-request, not per-group)
        total_chunks_in_batch = sum(len(segment) for segment in batched_segments)
        if total_chunks_in_batch > VOYAGE_CONTEXT_3_MAX_CHUNKS:
            raise ValueError(
                f"Batch contains {total_chunks_in_batch:,} chunks but Voyage limit is "
                f"{VOYAGE_CONTEXT_3_MAX_CHUNKS:,}. This indicates a bug in batching logic."
            )

        # Check input count per batch
        if len(batched_segments) > VOYAGE_CONTEXT_3_MAX_INPUTS:
            raise ValueError(
                f"Batch contains {len(batched_segments)} inputs but Voyage limit is "
                f"{VOYAGE_CONTEXT_3_MAX_INPUTS}. Reduce chunker_group_size in config."
            )

    return final_batches


async def _embed_with_segmentation(
    pages_texts: List[List[str]],
    embedder,
    *,
    per_doc_budget: int = DOCUMENT_TOKEN_BUDGET,
    per_request_budget: int = REQUEST_TOKEN_BUDGET,
) -> List[List[List[float]]]:
    """
    Embed pages with automatic segmentation to respect Voyage AI token limits.
    
    Three-phase strategy:
        1. SEGMENT: Split each page into segments that fit per-document budget (32K tokens)
        2. BATCH: Process segments round-robin across pages to maximize API efficiency
        3. ACCUMULATE: Collect embeddings back to their source pages
    
    The round-robin approach prevents large pages from blocking small pages and
    maximizes the number of segments processed per API call.
    
    Args:
        pages_texts: List of pages, each page is a list of text chunks
        embedder: Embedding service (passed from resources)
        per_doc_budget: Max tokens per document (default: 31,040 with 3% safety margin)
        per_request_budget: Max tokens per API request (default: 110,400 with 8% margin)
    
    Returns:
        List of embedding lists, preserving input structure
        
    Example:
        Input: [
            ["page0_chunk1", "page0_chunk2"],  # 40K tokens → 2 segments
            ["page1_chunk1"]                    # 10K tokens → 1 segment
        ]
        
        Processing:
        - Round 0: Batch segment[0] from both pages → 1 API call (50K tokens)
        - Round 1: Process segment[1] from page 0 → 1 API call (10K tokens)
        
        Output: [
            [[vec1], [vec2]],  # Page 0: 2 chunk embeddings
            [[vec3]]            # Page 1: 1 chunk embedding
        ]

    Note:
        Per-request validation (16K chunks, 1K inputs) happens in _batch_segments_for_round.
        This function can handle arbitrarily large groups as long as individual batches
        respect Voyage's limits.
    """
    # Phase 1: Split each page into segments that fit per-document budget
    # Using lmap for eager evaluation since we need the full structure for iteration
    segments_by_page: List[PageSegments] = lmap(
        lambda page_texts: _split_into_segments(page_texts, per_doc_budget=per_doc_budget),
        pages_texts
    )

    # Phase 2: Initialize accumulator for embeddings (one list per page)
    embeddings_by_page: List[List[List[float]]] = [[] for _ in segments_by_page]

    # Phase 3: Round-robin processing across pages
    # Process segment[0] from all pages, then segment[1], etc.
    # This maximizes batching efficiency and prevents large pages from blocking small ones
    max_segments = max((len(segments) for segments in segments_by_page), default=0)

    for round_index in range(max_segments):
        # Identify pages that still have a segment at this round
        ready_pages = [
            page_idx
            for page_idx, segments in enumerate(segments_by_page)
            if round_index < len(segments)
        ]

        if not ready_pages:
            break  # All segments processed

        # Batch segments from ready pages into one or more API calls
        api_calls = _batch_segments_for_round(
            segments_by_page,
            round_index,
            ready_pages,
            per_request_budget
        )

        # Execute each batch and accumulate results back to source pages
        for page_indices, batched_segments in api_calls:
            # Call embedding API with retry logic
            embeddings_batch = await embed_documents_with_retry(embedder, batched_segments)

            # Distribute embeddings back to their source pages
            # zip pairs each page_idx with its corresponding embeddings
            for page_idx, page_embeddings in zip(page_indices, embeddings_batch):
                embeddings_by_page[page_idx].extend(page_embeddings)

    return embeddings_by_page


async def process_page_group(
    group_items: List[PageWorkItem],
    resources: SyncResources,
    *,
    config: SyncConfig,
) -> GroupResult:
    """
    Process a group of pages through the full pipeline: chunk → embed → write.
    
    Pipeline stages:
        1. CHUNK: Split pages with children into smaller chunks (optional, via external service)
        2. BUILD: Transform chunks into Weaviate object structures
        3. EMBED: Generate embeddings with automatic segmentation for token limits
        4. VALIDATE: Ensure embedding counts match object counts
        5. WRITE: Bulk insert to Weaviate and cleanup old versions
    
    Args:
        group_items: Pages to process in this group
        resources: Shared resources (chunker, embedder, weaviate, semaphores)
        config: Sync configuration (batch size, version, namespace)
        
    Returns:
        GroupResult with stats, state updates, and failure messages
    """
    result = GroupResult()

    # ============================================================================
    # STAGE 1: CHUNKING
    # Split pages with children into smaller chunks for better embedding quality
    # ============================================================================
    try:
        # Separate pages that need chunking from those that don't
        # need_chunk: pages with children (need external chunking service)
        # no_chunk: leaf pages or pages without children (skip chunking)
        need_chunk, no_chunk = lsplit(
            lambda p: p[1].snapshot.has_children,
            enumerate(group_items)
        )

        chunk_results_by_index: Dict[int, List[Dict[str, Any]]] = {}

        if need_chunk:
            # Extract linearized text from pages that need chunking
            texts = lmap(lambda p: p[1].snapshot.linearized_text or "", need_chunk)

            # Chunk with semaphore-based rate limiting
            chunk_wait_start = time.time()
            async with resources.chunk_semaphore:
                result.chunk_wait = time.time() - chunk_wait_start
                chunk_start = time.time()
                chunk_batches = await chunk_batch_with_retry(resources.chunker, texts)
                result.chunk_duration = time.time() - chunk_start

            # Map chunk results back to page indices
            for (idx, _), chunks in zip(need_chunk, chunk_batches):
                chunk_results_by_index[idx] = chunks or []

        # Pages without children get empty chunk lists
        for idx, _ in no_chunk:
            chunk_results_by_index[idx] = []

    except Exception as exc:  # pragma: no cover
        # Chunking failure fails the entire group (all-or-nothing for consistency)
        result.pages_failed = len(group_items)
        result.fail_messages.append(f"  ✗ Chunker failed for group: {exc}")
        return result

    # ============================================================================
    # STAGE 2: PAYLOAD BUILDING
    # Transform chunks into Weaviate object structures
    # ============================================================================
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
            # Individual page failures are recorded but don't stop the group
            result.pages_failed += 1
            result.fail_messages.append(
                f"  ✗ Failed building payload for page '{item.page_title}' ({item.page_uid}): {exc}"
            )

    if not processed_items:
        return result

    # ============================================================================
    # STAGE 3: EMBEDDING WITH SEGMENTATION
    # Generate embeddings with automatic handling of Voyage AI token limits
    # ============================================================================
    try:
        voyage_wait_start = time.time()
        async with resources.embed_semaphore:
            result.voyage_wait = time.time() - voyage_wait_start
            voyage_start = time.time()

            # Extract chunk texts from all payloads
            pages_texts = lmap(lambda item_payload: item_payload[1].chunk_texts, processed_items)

            # Embed with automatic segmentation for pages exceeding token limits
            embeddings_nested = await _embed_with_segmentation(
                pages_texts,
                resources.embedder,
                per_doc_budget=DOCUMENT_TOKEN_BUDGET,
                per_request_budget=REQUEST_TOKEN_BUDGET,
            )

            result.voyage_duration = time.time() - voyage_start
    except Exception as exc:
        # Embedding failure fails all remaining pages in this group
        result.pages_failed += len(processed_items)
        result.fail_messages.append(f"  ✗ Voyage embedding failed for group: {exc}")
        return result

    # ============================================================================
    # STAGE 4: VALIDATION & VECTOR ATTACHMENT
    # Ensure embedding counts match and attach vectors to objects
    # ============================================================================
    successful_payloads: List[Tuple[PageWorkItem, WeaviateObjectSet]] = []
    for (item, payload), embeddings in zip(processed_items, embeddings_nested):
        # Sanity check: embedding count must match object count
        if len(embeddings) != len(payload.all_objects):
            result.pages_failed += 1
            result.fail_messages.append(
                f"  ✗ Embedding count mismatch for page '{item.page_title}' ({item.page_uid})"
            )
            continue

        # Attach vector to each Weaviate object
        for obj, vector in zip(payload.all_objects, embeddings):
            obj["vector"] = vector

        successful_payloads.append((item, payload))

    if not successful_payloads:
        return result

    # ============================================================================
    # STAGE 5: WEAVIATE WRITE & CLEANUP
    # Bulk insert new objects and delete old versions
    # ============================================================================
    # Flatten all objects from all pages using funcy's lcat (concatenate lists)
    weaviate_objects = lcat(lmap(lambda p: p[1].all_objects, successful_payloads))

    try:
        weaviate_wait_start = time.time()
        async with resources.weaviate_semaphore:
            result.weaviate_wait = time.time() - weaviate_wait_start
            weaviate_start = time.time()

            # Bulk insert with retry logic
            failed_objects = await weaviate_insert_with_retry(resources.weaviate,
weaviate_objects)
            result.weaviate_duration = time.time() - weaviate_start

            # Check for insertion failures
            if failed_objects:
                raise RuntimeError(
                    f"Weaviate reported {len(failed_objects)} failed objects: "
                    f"{', '.join((error.message or '') for error in failed_objects[:3])}"
                )

            # Delete old versions by content hash (cleanup stale embeddings)
            for item, payload in successful_payloads:
                await weaviate_delete_with_retry(
                    resources.weaviate,
                    item.page_uid,
                    payload.content_hash,
                )

    except Exception as exc:
        # Write failure fails all pages in this group
        result.pages_failed += len(successful_payloads)
        result.fail_messages.append(f"  ✗ Weaviate write failed for group: {exc}")
        return result

    # ============================================================================
    # RESULT ASSEMBLY
    # Populate result with stats and state updates
    # ============================================================================
    result.docs_added = len(weaviate_objects)
    result.pages_updated = len(successful_payloads)
    result.chunks_created = sum(len(payload.chunk_objects) for _, payload in successful_payloads)

    # Prepare state updates for persistence
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
    """
    Main orchestration loop for processing batches of pages.
    
    Workflow:
        1. Fetch page data from Roam (optimized: childless pages skip full pull)
        2. Convert to work items with snapshots
        3. Dispatch groups to parallel processing via asyncio.TaskGroup
        4. Aggregate results, metrics, and state updates
        5. Persist checkpoint state for resumability
    
    Args:
        state: Runtime state (pending UIDs, stats, timers)
        context: Sync context (resources, config, Roam client)
        
    Returns:
        Total number of pages processed in this run
    """
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

        # Optimize: separate childless pages (skip full pull) from pages with children
        uids_childless, uids_with_children = lsplit(
            lambda uid: runtime.metadata_map.get(uid) and not
runtime.metadata_map[uid].has_children,
            batch
        )

        # Pull full page data only for pages with children
        pulled_map: Dict[str, Optional[Dict[str, Any]]] = {}
        if uids_with_children:
            with state.timer("roam"):
                pulled_pages = await roam_client.pull_many_pages(uids_with_children)
            for uid, pdata in zip(uids_with_children, pulled_pages):
                pulled_map[uid] = pdata

        # Synthesize minimal page data for childless pages (avoid expensive pull)
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

        # Reconstruct pages_data in original batch order
        pages_data = [pulled_map.get(uid) for uid in batch]

        # Build work items from page data
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

            # Track diagnostic info
            max_edit_time_val = snapshot.meta.max_edit_time or snapshot.meta.max_block_edit_time
            if max_edit_time_val is None:
                state.pages_missing_edit_time.add(page_uid)
            if not snapshot.linearized_text.strip() and snapshot.has_children:
                state.pages_empty_linearized.add(page_uid)

            # Track maximum edit time across all pages
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

        # Process work items in parallel groups
        results: List[GroupResult] = []

        async def add_group(items: List[PageWorkItem]) -> None:
            """Helper to process a group and append result."""
            result = await process_page_group(items, resources, config=config)
            results.append(result)

        # Use asyncio.TaskGroup for structured concurrency (Python 3.11+)
        async with asyncio.TaskGroup() as tg:
            for group in chunks(config.chunker_group_size, work_items):
                group_list = list(group)
                if not group_list:
                    continue
                tg.create_task(add_group(group_list))

        # Aggregate results from all groups
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

            # Persist state updates and update cache
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

        # Collect failure messages using funcy's lcat + lmap pattern
        for msg in lcat(lmap(lambda r: r.fail_messages, results)):
            state.record_failure(msg)

        pages_processed += batch_size
        runtime.pending_uids = runtime.pending_uids[batch_size:]

        await status_emitter.batch_complete(
            batch=batch_num,
            processed_after=runtime.processed_offset + pages_processed,
        )

        # Persist checkpoint state for resumability
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