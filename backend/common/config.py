"""Configuration helpers for semantic sync."""

from __future__ import annotations

import os
import uuid
from dataclasses import dataclass


STATE_FLAG_METADATA_APPLIED = "metadata_applied"


@dataclass(frozen=True)
class SyncConfig:
    batch_size: int
    metadata_batch_size: int
    metadata_state_concurrency: int
    collection_name: str
    weaviate_http_host: str
    weaviate_http_port: int
    weaviate_http_secure: bool
    weaviate_grpc_host: str
    weaviate_grpc_port: int
    weaviate_grpc_secure: bool
    chunker_url: str
    chunker_retries: int
    chunker_retry_delay: int
    sync_version: str
    uuid_namespace: uuid.UUID
    chunker_group_size: int
    chunker_concurrency: int
    voyage_concurrency: int
    weaviate_write_concurrency: int
    roam_requests_per_minute: int


CONFIG = SyncConfig(
    batch_size=20,
    metadata_batch_size=int(os.getenv("ROAM_METADATA_BATCH_SIZE", "500")),
    metadata_state_concurrency=int(os.getenv("ROAM_METADATA_STATE_CONCURRENCY", "8")),
    collection_name="RoamSemanticChunks",
    weaviate_http_host=os.getenv("WEAVIATE_HTTP_HOST", "127.0.0.1"),
    weaviate_http_port=int(os.getenv("WEAVIATE_HTTP_PORT", "8080")),
    weaviate_http_secure=os.getenv("WEAVIATE_HTTP_SECURE", "false").lower() == "true",
    weaviate_grpc_host=os.getenv("WEAVIATE_HTTP_HOST", "127.0.0.1"),
    weaviate_grpc_port=int(os.getenv("WEAVIATE_GRPC_PORT", "50051")),
    weaviate_grpc_secure=os.getenv("WEAVIATE_GRPC_SECURE", "false").lower() == "true",
    chunker_url=os.getenv("CHUNKER_SERVICE_URL", "http://127.0.0.1:8003"),
    chunker_retries=3,
    chunker_retry_delay=2,
    sync_version="semantic_v3_incremental",
    uuid_namespace=uuid.uuid5(uuid.NAMESPACE_URL, "roam-semantic-sync"),
    chunker_group_size=int(os.getenv("CHUNKER_GROUP_SIZE", "8")),
    chunker_concurrency=int(os.getenv("CHUNKER_CONCURRENCY", "1")),
    voyage_concurrency=int(os.getenv("VOYAGE_CONCURRENCY", "4")),
    weaviate_write_concurrency=int(os.getenv("WEAVIATE_WRITE_CONCURRENCY", "1")),
    roam_requests_per_minute=int(os.getenv("ROAM_MAX_REQUESTS_PER_MINUTE", "50")),
)

