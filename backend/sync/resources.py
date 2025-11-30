"""Resource management helpers for semantic sync."""

from __future__ import annotations

import asyncio
import contextlib
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator, Optional

import structlog
import weaviate
from weaviate.classes.init import Auth

from clients.chunker import ChunkerClient, ChunkerConfig
from clients.voyage import VoyageEmbeddingClient
from clients.weaviate import WeaviateSyncAdapter
from clients.roam import RoamClient

LOGGER = structlog.get_logger(__name__)


@dataclass
class SyncResources:
    """Bundle of external clients and concurrency guards."""

    client: weaviate.WeaviateAsyncClient
    weaviate: WeaviateSyncAdapter
    chunker: ChunkerClient
    embedder: VoyageEmbeddingClient
    roam_client: RoamClient
    chunk_semaphore: asyncio.Semaphore
    embed_semaphore: asyncio.Semaphore
    weaviate_semaphore: asyncio.Semaphore


@asynccontextmanager
async def acquire_resources(
    *,
    config,
    roam_graph_name: str,
    roam_api_token: str,
    voyage_api_key: str,
    voyage_model: str,
    voyage_timeout: Optional[float] = None,
) -> AsyncIterator[SyncResources]:
    """Yield prepared resources for the sync pipeline and ensure cleanup."""

    # Create Weaviate client based on deployment mode
    if config.is_weaviate_cloud:
        LOGGER.info("Using Weaviate Cloud for sync", cluster_url=config.weaviate_cloud_url)
        client = weaviate.use_async_with_weaviate_cloud(
            cluster_url=config.weaviate_cloud_url,
            auth_credentials=Auth.api_key(config.weaviate_cloud_api_key),
            skip_init_checks=False,  # Fail fast for cloud
        )
    else:
        LOGGER.info(
            "Using local Weaviate for sync",
            http_host=config.weaviate_http_host,
            http_port=config.weaviate_http_port,
        )
        client = weaviate.use_async_with_custom(
            http_host=config.weaviate_http_host,
            http_port=config.weaviate_http_port,
            http_secure=config.weaviate_http_secure,
            grpc_host=config.weaviate_grpc_host,
            grpc_port=config.weaviate_grpc_port,
            grpc_secure=config.weaviate_grpc_secure,
            skip_init_checks=True,
        )
    await client.connect()

    chunker_client = ChunkerClient(
        ChunkerConfig(
            url=config.chunker_url,
            retries=config.chunker_retries,
            base_delay=config.chunker_retry_delay,
        )
    )

    embedder = VoyageEmbeddingClient(
        api_key=voyage_api_key,
        model=voyage_model,
        timeout=voyage_timeout,
    )

    roam_client = RoamClient(
        graph_name=roam_graph_name,
        token=roam_api_token,
        requests_per_minute=config.roam_requests_per_minute,
    )

    chunk_semaphore = asyncio.Semaphore(max(1, config.chunker_concurrency))
    embed_semaphore = asyncio.Semaphore(max(1, config.voyage_concurrency))
    weaviate_semaphore = asyncio.Semaphore(max(1, config.weaviate_write_concurrency))

    adapter = WeaviateSyncAdapter(client, config.collection_name)

    resources = SyncResources(
        client=client,
        weaviate=adapter,
        chunker=chunker_client,
        embedder=embedder,
        roam_client=roam_client,
        chunk_semaphore=chunk_semaphore,
        embed_semaphore=embed_semaphore,
        weaviate_semaphore=weaviate_semaphore,
    )

    try:
        yield resources
    finally:
        with contextlib.suppress(Exception):
            await chunker_client.close()
        with contextlib.suppress(Exception):
            was_connected = client.is_connected()
            await client.close()
            if was_connected:
                LOGGER.info("Weaviate sync client connection closed")

