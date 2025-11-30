"""
Pipeline stages for sync processing.

Each stage is an independently testable function that:
1. Takes typed inputs
2. Returns a typed result (with errors or success)
3. Captures timing metrics

Stages:
    stage_chunk: Split pages with children into semantic chunks
    stage_build_payloads: Transform chunks into Weaviate objects
    stage_embed: Generate embeddings with token-aware segmentation
    stage_attach_vectors: Validate and attach embeddings to objects
    stage_write: Bulk insert to Weaviate and cleanup old versions

Usage:
    from sync.pipeline.stages import (
        stage_chunk,
        stage_build_payloads,
        stage_embed,
        stage_attach_vectors,
        stage_write,
    )

    chunk_result = await stage_chunk(items, resources)
    if chunk_result.is_err:
        return early_failure(chunk_result.errors)
    ...
"""

from sync.pipeline.stages.chunk_stage import stage_chunk
from sync.pipeline.stages.payload_stage import stage_build_payloads
from sync.pipeline.stages.embed_stage import stage_embed
from sync.pipeline.stages.validate_stage import stage_attach_vectors
from sync.pipeline.stages.write_stage import stage_write

__all__ = [
    "stage_chunk",
    "stage_build_payloads",
    "stage_embed",
    "stage_attach_vectors",
    "stage_write",
]
