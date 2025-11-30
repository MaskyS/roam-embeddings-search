"""Unit tests for the VoyageEmbeddingClient."""

from __future__ import annotations

import pytest
from unittest.mock import MagicMock, patch

from clients.voyage import VoyageEmbeddingClient
from common.errors import TransientError


@pytest.fixture
def voyage_client():
    with patch("clients.voyage.voyageai.Client"):
        return VoyageEmbeddingClient(
            api_key="test-api-key",
            model="voyage-context-3",
            input_type="document",
        )


class TestVoyageEmbedDocuments:
    """Tests for VoyageEmbeddingClient.embed_documents method."""

    @pytest.mark.asyncio
    async def test_embed_documents_success(self, voyage_client):
        """Should return embeddings for each document."""
        # Mock the contextualized_embed response
        mock_result = MagicMock()
        mock_result.results = [
            MagicMock(embeddings=[[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]),  # 2 chunks
            MagicMock(embeddings=[[0.7, 0.8, 0.9]]),  # 1 chunk
        ]
        voyage_client._client.contextualized_embed.return_value = mock_result

        pages = [["chunk1", "chunk2"], ["chunk3"]]
        result = await voyage_client.embed_documents(pages)

        assert len(result) == 2
        assert len(result[0]) == 2  # 2 embeddings for first page
        assert len(result[1]) == 1  # 1 embedding for second page
        assert result[0][0] == [0.1, 0.2, 0.3]

    @pytest.mark.asyncio
    async def test_embed_documents_empty_input(self, voyage_client):
        """Should handle empty input gracefully."""
        mock_result = MagicMock()
        mock_result.results = []
        voyage_client._client.contextualized_embed.return_value = mock_result

        result = await voyage_client.embed_documents([])

        assert result == []

    @pytest.mark.asyncio
    async def test_embed_documents_api_error_raises_transient(self, voyage_client):
        """Should raise TransientError on API failure."""
        voyage_client._client.contextualized_embed.side_effect = Exception("API rate limit exceeded")

        with pytest.raises(TransientError) as exc_info:
            await voyage_client.embed_documents([["text"]])

        assert "Voyage embedding failed" in str(exc_info.value)
        assert "voyage-context-3" in exc_info.value.context.get("model", "")

    @pytest.mark.asyncio
    async def test_embed_documents_preserves_batch_structure(self, voyage_client):
        """Should preserve the page/chunk structure in output."""
        mock_result = MagicMock()
        mock_result.results = [
            MagicMock(embeddings=[[1.0] * 1024]),
            MagicMock(embeddings=[[2.0] * 1024, [3.0] * 1024]),
            MagicMock(embeddings=[[4.0] * 1024]),
        ]
        voyage_client._client.contextualized_embed.return_value = mock_result

        pages = [["a"], ["b", "c"], ["d"]]
        result = await voyage_client.embed_documents(pages)

        assert len(result) == 3
        assert len(result[0]) == 1
        assert len(result[1]) == 2
        assert len(result[2]) == 1


class TestVoyageEmbedQuery:
    """Tests for VoyageEmbeddingClient.embed_query method."""

    @pytest.mark.asyncio
    async def test_embed_query_success(self, voyage_client):
        """Should return embedding vector for query."""
        mock_result = MagicMock()
        mock_result.results = [MagicMock(embeddings=[[0.1] * 1024])]
        voyage_client._client.contextualized_embed.return_value = mock_result

        result = await voyage_client.embed_query("search query")

        assert len(result) == 1024
        assert result[0] == 0.1

    @pytest.mark.asyncio
    async def test_embed_query_uses_query_input_type(self, voyage_client):
        """Should use 'query' input type for query embeddings."""
        mock_result = MagicMock()
        mock_result.results = [MagicMock(embeddings=[[0.1]])]
        voyage_client._client.contextualized_embed.return_value = mock_result

        await voyage_client.embed_query("test")

        # Verify the call used input_type="query"
        call_kwargs = voyage_client._client.contextualized_embed.call_args[1]
        assert call_kwargs["input_type"] == "query"

    @pytest.mark.asyncio
    async def test_embed_query_api_error_raises_transient(self, voyage_client):
        """Should raise TransientError on API failure."""
        voyage_client._client.contextualized_embed.side_effect = Exception("Network error")

        with pytest.raises(TransientError) as exc_info:
            await voyage_client.embed_query("query")

        assert "Voyage query embedding failed" in str(exc_info.value)
