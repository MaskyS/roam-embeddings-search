"""Retry helpers for external service calls."""

from __future__ import annotations

from typing import Any, Dict, List

import httpx
from tenacity import AsyncRetrying, retry_if_exception_type, stop_after_attempt, wait_exponential

from clients.chunker import ChunkerClient
from clients.voyage import VoyageEmbeddingClient
from clients.weaviate import WeaviateSyncAdapter
from common.errors import TransientError


def _should_retry(exception: Exception) -> bool:
    """Determine if an exception is transient and should be retried."""
    if isinstance(exception, TransientError):
        return True
    if isinstance(exception, (httpx.ConnectError, httpx.ReadTimeout)):
        return True
    if isinstance(exception, httpx.HTTPStatusError):
        # Retry on rate limits and server errors
        return exception.response.status_code in (429, 500, 502, 503, 504)
    return False


async def chunk_batch_with_retry(client: ChunkerClient, texts: List[str]) -> List[List[Dict[str, Any]]]:
    """Chunk texts with automatic retry on transient failures."""
    async for attempt in AsyncRetrying(
        stop=stop_after_attempt(3),
        wait=wait_exponential(max=4),
        retry=retry_if_exception_type((TransientError, httpx.ConnectError, httpx.ReadTimeout, httpx.HTTPStatusError)),
        reraise=True,
    ):
        with attempt:
            return await client.chunk_batch(texts)


async def embed_documents_with_retry(
    client: VoyageEmbeddingClient, docs: List[List[str]]
) -> List[List[List[float]]]:
    """Embed documents with automatic retry on transient failures."""
    async for attempt in AsyncRetrying(
        stop=stop_after_attempt(3),
        wait=wait_exponential(max=4),
        retry=retry_if_exception_type(TransientError),
        reraise=True,
    ):
        with attempt:
            return await client.embed_documents(docs)


async def weaviate_insert_with_retry(
    adapter: WeaviateSyncAdapter, objects: List[Dict[str, Any]]
):
    """Insert objects into Weaviate with automatic retry on transient failures."""
    async for attempt in AsyncRetrying(
        stop=stop_after_attempt(3),
        wait=wait_exponential(max=4),
        retry=retry_if_exception_type(TransientError),
        reraise=True,
    ):
        with attempt:
            return await adapter.insert_objects(objects)


async def weaviate_delete_with_retry(
    adapter: WeaviateSyncAdapter, page_uid: str, content_hash: str
) -> None:
    """Delete stale objects from Weaviate with automatic retry on transient failures."""
    async for attempt in AsyncRetrying(
        stop=stop_after_attempt(3),
        wait=wait_exponential(max=4),
        retry=retry_if_exception_type(TransientError),
        reraise=True,
    ):
        with attempt:
            await adapter.delete_stale_objects(page_uid, content_hash)
            return

