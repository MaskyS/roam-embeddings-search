"""Async HTTP client for the chunker microservice."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any, Dict, List, Sequence

import httpx
import structlog
from funcy import suppress

from common.errors import TransientError

LOGGER = structlog.get_logger(__name__)


@dataclass
class ChunkerConfig:
    url: str
    retries: int = 3
    base_delay: float = 2.0


class ChunkerClient:
    """Async HTTP client for the chunker microservice."""

    def __init__(self, config: ChunkerConfig) -> None:
        self._config = config
        self._client = httpx.AsyncClient(timeout=60.0)

    async def close(self) -> None:
        await self._client.aclose()

    async def wait_until_ready(self, timeout: float = 60.0) -> bool:
        loop = asyncio.get_running_loop()
        end_time = loop.time() + timeout
        while loop.time() < end_time:
            with suppress(httpx.HTTPError):
                response = await self._client.get(f"{self._config.url}/health", timeout=5.0)
                if response.status_code == 200 and response.json().get("chunker_loaded"):
                    return True
            await asyncio.sleep(2)
        return False

    async def chunk_text(self, text: str) -> List[Dict[str, Any]]:
        """Chunk ``text`` returning list of chunk dictionaries."""

        attempt = 0
        while True:
            try:
                response = await self._client.post(
                    f"{self._config.url}/chunk",
                    json={"text": text},
                )
                response.raise_for_status()
                data = response.json()
                return data.get("chunks", [])
            except (httpx.ConnectError, httpx.HTTPStatusError, httpx.ReadTimeout) as exc:
                attempt += 1
                if attempt >= self._config.retries:
                    raise TransientError(
                        f"Chunker service failed after {attempt} attempts",
                        context={"url": self._config.url, "original_error": str(exc)},
                    ) from exc
                await asyncio.sleep(self._config.base_delay * (2 ** (attempt - 1)))

    async def chunk_batch(self, texts: Sequence[str]) -> List[List[Dict[str, Any]]]:
        attempt = 0
        while True:
            try:
                response = await self._client.post(
                    f"{self._config.url}/chunk/batch",
                    json={"texts": list(texts)},
                )
                response.raise_for_status()
                data = response.json()
                return [entry.get("chunks", []) for entry in data.get("results", [])]
            except (httpx.ConnectError, httpx.HTTPStatusError, httpx.ReadTimeout) as exc:
                attempt += 1
                if attempt >= self._config.retries:
                    raise TransientError(
                        f"Chunker batch service failed after {attempt} attempts",
                        context={"url": self._config.url, "batch_size": len(texts), "original_error": str(exc)},
                    ) from exc
                await asyncio.sleep(self._config.base_delay * (2 ** (attempt - 1)))

