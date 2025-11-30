"""
Stage 4: Validation and Vector Attachment

Validate that embedding counts match object counts and attach
vectors to their corresponding Weaviate objects.
"""

from __future__ import annotations

from typing import List, Tuple, TYPE_CHECKING

from sync.data.results import ValidateStageResult

if TYPE_CHECKING:
    from sync.data.models import PageWorkItem, WeaviateObjectSet


def stage_attach_vectors(
    processed_items: List[Tuple["PageWorkItem", "WeaviateObjectSet"]],
    embeddings_nested: List[List[List[float]]],
) -> ValidateStageResult:
    """
    Stage 4: Validate and attach embeddings to Weaviate objects.

    For each page, verifies that the number of embeddings matches
    the number of Weaviate objects, then attaches vectors to objects
    in preparation for the write stage.

    Args:
        processed_items: List of (PageWorkItem, WeaviateObjectSet) from stage_build_payloads
        embeddings_nested: List of embeddings from stage_embed
            embeddings_nested[page_idx][chunk_idx] = embedding vector

    Returns:
        ValidateStageResult with:
        - validated_payloads: Successfully validated (item, payload) pairs
          with vectors attached to each object
        - errors: Error messages for pages with mismatched counts

    Mutation Note:
        This function mutates the WeaviateObjectSet.all_objects by adding
        the "vector" key to each object. The payload reference is preserved
        to avoid unnecessary copying.

    Example:
        validate_result = stage_attach_vectors(
            payload_result.processed_items,
            embed_result.embeddings_nested
        )
        if validate_result.is_err:
            # Some pages had embedding count mismatches
            pass

        # validated_payloads[i] has vectors attached to all_objects
    """
    result = ValidateStageResult()

    for (item, payload), embeddings in zip(processed_items, embeddings_nested):
        # Sanity check: embedding count must match object count
        if len(embeddings) != len(payload.all_objects):
            result.errors.append(
                f"Embedding count mismatch for page '{item.page_title}' ({item.page_uid}): "
                f"got {len(embeddings)} embeddings for {len(payload.all_objects)} objects"
            )
            continue

        # Attach vector to each Weaviate object
        for obj, vector in zip(payload.all_objects, embeddings):
            obj["vector"] = vector

        result.validated_payloads.append((item, payload))

    return result
