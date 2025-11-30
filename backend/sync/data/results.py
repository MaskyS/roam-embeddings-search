"""Stage-specific result types for the sync pipeline.

Each stage in the pipeline returns a typed result that captures:
- The stage's output data (if successful)
- Any errors encountered
- Timing metrics for observability

These result types enable:
1. Independent testing of each stage
2. Clear error propagation without exceptions
3. Metrics collection at each stage boundary
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from sync.data.models import PageWorkItem, WeaviateObjectSet


@dataclass
class ChunkStageResult:
    """
    Result from the chunking stage.

    Chunking splits pages with children into smaller semantic chunks
    using an external chunking service (Chonkie).

    Attributes:
        chunk_results_by_index: Mapping from page index to list of chunks.
            Each chunk is a dict with 'text' and other metadata.
        errors: List of error messages if chunking failed
        chunk_duration: Time spent in chunker service (seconds)
        chunk_wait: Time spent waiting for semaphore (seconds)

    Example:
        result = await stage_chunk(items, resources)
        if result.is_err:
            return early_with(result.errors)
        chunks_for_page_0 = result.chunk_results_by_index[0]
    """
    chunk_results_by_index: Dict[int, List[Dict[str, Any]]] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    chunk_duration: float = 0.0
    chunk_wait: float = 0.0

    @property
    def is_ok(self) -> bool:
        return not self.errors

    @property
    def is_err(self) -> bool:
        return bool(self.errors)


@dataclass
class PayloadStageResult:
    """
    Result from the payload building stage.

    Payload building transforms chunked pages into Weaviate object structures
    with proper UUIDs, metadata, and text previews.

    Attributes:
        processed_items: List of (PageWorkItem, WeaviateObjectSet) tuples
            representing successfully built payloads
        errors: List of error messages for failed pages

    Note:
        Individual page failures are recorded in errors but don't fail
        the entire stage. Other pages can still proceed.
    """
    processed_items: List[Tuple["PageWorkItem", "WeaviateObjectSet"]] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    @property
    def is_ok(self) -> bool:
        return not self.errors

    @property
    def is_err(self) -> bool:
        return bool(self.errors)

    @property
    def pages_failed(self) -> int:
        """Count of pages that failed payload building."""
        return len(self.errors)


@dataclass
class EmbedStageResult:
    """
    Result from the embedding stage.

    Embedding generates vector representations using VoyageAI's
    contextualized embeddings with automatic token-aware segmentation.

    Attributes:
        embeddings_nested: Nested list of embeddings, preserving input structure.
            embeddings_nested[page_idx][chunk_idx] = embedding vector
        errors: List of error messages if embedding failed
        voyage_duration: Time spent in VoyageAI API (seconds)
        voyage_wait: Time spent waiting for semaphore (seconds)

    Token Budget Handling:
        Large pages are automatically segmented to respect Voyage limits:
        - Per-document: 32K tokens
        - Per-request: 120K tokens
        Segmentation happens transparently via _embed_with_segmentation.
    """
    embeddings_nested: List[List[List[float]]] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    voyage_duration: float = 0.0
    voyage_wait: float = 0.0

    @property
    def is_ok(self) -> bool:
        return not self.errors

    @property
    def is_err(self) -> bool:
        return bool(self.errors)


@dataclass
class ValidateStageResult:
    """
    Result from the validation and vector attachment stage.

    Validation ensures embedding counts match object counts and
    attaches vectors to their corresponding Weaviate objects.

    Attributes:
        validated_payloads: Successfully validated (item, payload) pairs
            with vectors attached to each object
        errors: List of error messages for mismatched pages
    """
    validated_payloads: List[Tuple["PageWorkItem", "WeaviateObjectSet"]] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    @property
    def is_ok(self) -> bool:
        return not self.errors

    @property
    def is_err(self) -> bool:
        return bool(self.errors)

    @property
    def pages_failed(self) -> int:
        """Count of pages that failed validation."""
        return len(self.errors)


@dataclass
class WriteStageResult:
    """
    Result from the Weaviate write stage.

    Writing performs bulk insert of new objects and cleanup of
    old versions identified by content hash.

    Attributes:
        docs_added: Total number of Weaviate objects inserted
        chunks_created: Number of chunk objects (excludes page objects)
        pages_updated: Number of pages successfully written
        state_updates: Mapping of page_uid -> sync state to persist.
            Each state contains last_synced_edit_time and content_hash.
        errors: List of error messages if write failed
        weaviate_duration: Time spent in Weaviate operations (seconds)
        weaviate_wait: Time spent waiting for semaphore (seconds)
    """
    docs_added: int = 0
    chunks_created: int = 0
    pages_updated: int = 0
    state_updates: Dict[str, Dict[str, Optional[str]]] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    weaviate_duration: float = 0.0
    weaviate_wait: float = 0.0

    @property
    def is_ok(self) -> bool:
        return not self.errors

    @property
    def is_err(self) -> bool:
        return bool(self.errors)


def aggregate_stage_results(
    chunk_result: ChunkStageResult,
    payload_result: PayloadStageResult,
    embed_result: EmbedStageResult,
    validate_result: ValidateStageResult,
    write_result: WriteStageResult,
) -> "GroupResult":
    """
    Aggregate results from all stages into a GroupResult.

    This helper combines timing metrics, error messages, and stats
    from individual stages into the final GroupResult expected by
    the batch processing loop.

    Args:
        chunk_result: Result from chunking stage
        payload_result: Result from payload building stage
        embed_result: Result from embedding stage
        validate_result: Result from validation stage
        write_result: Result from write stage

    Returns:
        GroupResult with combined metrics and errors

    Note:
        When write fails, ALL validated pages are counted as failed since
        the entire batch write is atomic. This ensures metrics reflect the
        real scope of failure.
    """
    from sync.data.models import GroupResult

    all_errors = (
        chunk_result.errors +
        payload_result.errors +
        embed_result.errors +
        validate_result.errors +
        write_result.errors
    )

    # When write fails, count all validated payloads as failed (batch is atomic)
    write_failed_count = (
        len(validate_result.validated_payloads) if write_result.is_err else 0
    )

    return GroupResult(
        docs_added=write_result.docs_added,
        chunks_created=write_result.chunks_created,
        pages_updated=write_result.pages_updated,
        pages_failed=(
            payload_result.pages_failed +
            validate_result.pages_failed +
            write_failed_count
        ),
        chunk_duration=chunk_result.chunk_duration,
        voyage_duration=embed_result.voyage_duration,
        weaviate_duration=write_result.weaviate_duration,
        chunk_wait=chunk_result.chunk_wait,
        voyage_wait=embed_result.voyage_wait,
        weaviate_wait=write_result.weaviate_wait,
        fail_messages=all_errors,
        state_updates=write_result.state_updates,
    )
