"""Thin async wrapper around VoyageAI contextual embeddings."""

from __future__ import annotations

import asyncio
from typing import Any, Dict, List, Optional, Sequence

import voyageai

from common.errors import TransientError


class VoyageEmbeddingClient:
    """Thin async wrapper around VoyageAI contextual embeddings."""

    def __init__(
        self,
        api_key: str,
        model: str,
        input_type: str = "document",
        timeout: Optional[float] = None,
    ) -> None:
        kwargs: Dict[str, Any] = {"api_key": api_key}
        if timeout is not None:
            kwargs["timeout"] = timeout
        self._client = voyageai.Client(**kwargs)
        self._model = model
        self._input_type = input_type

    async def embed_documents(
        self,
        pages: Sequence[Sequence[str]],
        *,
        retries: int = 3,
    ) -> List[List[List[float]]]:
        loop = asyncio.get_running_loop()

        def call() -> List[List[List[float]]]:
            result = self._client.contextualized_embed(
                inputs=list(pages),
                model=self._model,
                input_type=self._input_type,
            )
            return [item.embeddings for item in result.results]

        for attempt in range(max(1, retries)):
            try:
                return await loop.run_in_executor(None, call)
            except Exception as exc:
                if attempt >= retries - 1:
                    raise TransientError(
                        f"Voyage embedding failed after {attempt + 1} attempts",
                        context={"model": self._model, "batch_size": len(pages), "original_error": str(exc)},
                    ) from exc
                await asyncio.sleep(min(2 ** (attempt + 1), 10))

    async def embed_query(self, query: str, *, retries: int = 3) -> List[float]:
        loop = asyncio.get_running_loop()

        def call() -> List[float]:
            result = self._client.contextualized_embed(
                inputs=[[query]],
                model=self._model,
                input_type="query",
            )
            return result.results[0].embeddings[0]

        for attempt in range(max(1, retries)):
            try:
                return await loop.run_in_executor(None, call)
            except Exception as exc:
                if attempt >= retries - 1:
                    raise TransientError(
                        f"Voyage query embedding failed after {attempt + 1} attempts",
                        context={"model": self._model, "query_length": len(query), "original_error": str(exc)},
                    ) from exc
                await asyncio.sleep(min(2 ** (attempt + 1), 10))

