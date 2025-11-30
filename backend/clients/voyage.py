"""Thin async wrapper around VoyageAI contextual embeddings."""

from __future__ import annotations

import asyncio
from typing import Any, Dict, List, Optional, Sequence

import voyageai

from common.errors import TransientError
from common.retry import transient_retry


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

    @transient_retry()
    async def embed_documents(
        self,
        pages: Sequence[Sequence[str]],
    ) -> List[List[List[float]]]:
        """Embed documents with contextualized embeddings."""
        loop = asyncio.get_running_loop()

        def call() -> List[List[List[float]]]:
            result = self._client.contextualized_embed(
                inputs=list(pages),
                model=self._model,
                input_type=self._input_type,
            )
            return [item.embeddings for item in result.results]

        try:
            return await loop.run_in_executor(None, call)
        except Exception as exc:
            raise TransientError(
                "Voyage embedding failed",
                context={"model": self._model, "batch_size": len(pages), "original_error": str(exc)},
            ) from exc

    @transient_retry()
    async def embed_query(self, query: str) -> List[float]:
        """Embed a single query."""
        loop = asyncio.get_running_loop()

        def call() -> List[float]:
            result = self._client.contextualized_embed(
                inputs=[[query]],
                model=self._model,
                input_type="query",
            )
            return result.results[0].embeddings[0]

        try:
            return await loop.run_in_executor(None, call)
        except Exception as exc:
            raise TransientError(
                "Voyage query embedding failed",
                context={"model": self._model, "query_length": len(query), "original_error": str(exc)},
            ) from exc
