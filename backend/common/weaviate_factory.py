"""Factory for creating Weaviate async clients."""

from __future__ import annotations

from typing import Dict, Optional

import structlog
import weaviate
from weaviate.classes.init import Auth

LOGGER = structlog.get_logger(__name__)


def create_weaviate_client(
    *,
    is_cloud: bool,
    cloud_url: Optional[str] = None,
    cloud_api_key: Optional[str] = None,
    http_host: str = "localhost",
    http_port: int = 8080,
    http_secure: bool = False,
    grpc_host: str = "localhost",
    grpc_port: int = 50051,
    grpc_secure: bool = False,
    headers: Optional[Dict[str, str]] = None,
    skip_init_checks: Optional[bool] = None,
) -> weaviate.WeaviateAsyncClient:
    """
    Create a Weaviate async client based on deployment mode.

    Args:
        is_cloud: If True, use Weaviate Cloud; otherwise use custom/local deployment.
        cloud_url: Weaviate Cloud cluster URL (required if is_cloud=True).
        cloud_api_key: Weaviate Cloud API key (required if is_cloud=True).
        http_host: HTTP host for local deployment.
        http_port: HTTP port for local deployment.
        http_secure: Use HTTPS for local deployment.
        grpc_host: gRPC host for local deployment.
        grpc_port: gRPC port for local deployment.
        grpc_secure: Use secure gRPC for local deployment.
        headers: Additional headers (e.g., API keys for reranker modules).
        skip_init_checks: Skip initialization checks (default: False for cloud, True for local).

    Returns:
        Configured WeaviateAsyncClient (not yet connected).
    """
    if is_cloud:
        if not cloud_url or not cloud_api_key:
            raise ValueError("cloud_url and cloud_api_key are required for Weaviate Cloud")

        LOGGER.info("Creating Weaviate Cloud client", cluster_url=cloud_url)
        return weaviate.use_async_with_weaviate_cloud(
            cluster_url=cloud_url,
            auth_credentials=Auth.api_key(cloud_api_key),
            headers=headers or {},
            skip_init_checks=skip_init_checks if skip_init_checks is not None else False,
        )
    else:
        LOGGER.info("Creating local Weaviate client", http_host=http_host, http_port=http_port)
        return weaviate.use_async_with_custom(
            http_host=http_host,
            http_port=http_port,
            http_secure=http_secure,
            grpc_host=grpc_host,
            grpc_port=grpc_port,
            grpc_secure=grpc_secure,
            headers=headers or {},
            skip_init_checks=skip_init_checks if skip_init_checks is not None else True,
        )


def create_weaviate_client_from_config(config, *, headers: Optional[Dict[str, str]] = None) -> weaviate.WeaviateAsyncClient:
    """
    Create a Weaviate async client from a SyncConfig object.

    Args:
        config: SyncConfig instance with Weaviate connection details.
        headers: Additional headers (e.g., for VoyageAI reranker).

    Returns:
        Configured WeaviateAsyncClient (not yet connected).
    """
    return create_weaviate_client(
        is_cloud=config.is_weaviate_cloud,
        cloud_url=config.weaviate_cloud_url,
        cloud_api_key=config.weaviate_cloud_api_key,
        http_host=config.weaviate_http_host,
        http_port=config.weaviate_http_port,
        http_secure=config.weaviate_http_secure,
        grpc_host=config.weaviate_grpc_host,
        grpc_port=config.weaviate_grpc_port,
        grpc_secure=config.weaviate_grpc_secure,
        headers=headers,
    )
