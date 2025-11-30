"""Unit tests for the ChunkerClient."""

from __future__ import annotations

import pytest
import httpx
from unittest.mock import AsyncMock, patch, MagicMock

from clients.chunker import ChunkerClient, ChunkerConfig
from common.errors import TransientError


@pytest.fixture
def chunker_config():
    return ChunkerConfig(url="http://localhost:8001")


@pytest.fixture
def chunker_client(chunker_config):
    return ChunkerClient(chunker_config)


class TestChunkerClientChunkText:
    """Tests for ChunkerClient.chunk_text method."""

    @pytest.mark.asyncio
    async def test_chunk_text_success(self, chunker_client):
        """Should return chunks from successful response."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {
            "chunks": [
                {"text": "chunk1", "start_index": 0, "end_index": 10},
                {"text": "chunk2", "start_index": 11, "end_index": 20},
            ]
        }

        with patch.object(chunker_client._client, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response
            result = await chunker_client.chunk_text("some text to chunk")

        assert len(result) == 2
        assert result[0]["text"] == "chunk1"
        assert result[1]["text"] == "chunk2"

    @pytest.mark.asyncio
    async def test_chunk_text_empty_chunks(self, chunker_client):
        """Should return empty list when no chunks in response."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {}

        with patch.object(chunker_client._client, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response
            result = await chunker_client.chunk_text("text")

        assert result == []

    @pytest.mark.asyncio
    async def test_chunk_text_connect_error_raises_transient(self, chunker_client):
        """Should raise TransientError on connection failure."""
        with patch.object(chunker_client._client, "post", new_callable=AsyncMock) as mock_post:
            mock_post.side_effect = httpx.ConnectError("Connection refused")

            with pytest.raises(TransientError) as exc_info:
                await chunker_client.chunk_text("text")

            assert "Chunker service failed" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_chunk_text_timeout_raises_transient(self, chunker_client):
        """Should raise TransientError on timeout."""
        with patch.object(chunker_client._client, "post", new_callable=AsyncMock) as mock_post:
            mock_post.side_effect = httpx.ReadTimeout("Timeout")

            with pytest.raises(TransientError) as exc_info:
                await chunker_client.chunk_text("text")

            assert "Chunker service failed" in str(exc_info.value)


class TestChunkerClientChunkBatch:
    """Tests for ChunkerClient.chunk_batch method."""

    @pytest.mark.asyncio
    async def test_chunk_batch_success(self, chunker_client):
        """Should return batch chunks from successful response."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {
            "results": [
                {"chunks": [{"text": "doc1-chunk1"}, {"text": "doc1-chunk2"}]},
                {"chunks": [{"text": "doc2-chunk1"}]},
            ]
        }

        with patch.object(chunker_client._client, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response
            result = await chunker_client.chunk_batch(["document 1", "document 2"])

        assert len(result) == 2
        assert len(result[0]) == 2
        assert len(result[1]) == 1
        assert result[0][0]["text"] == "doc1-chunk1"

    @pytest.mark.asyncio
    async def test_chunk_batch_empty_input(self, chunker_client):
        """Should handle empty input list."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {"results": []}

        with patch.object(chunker_client._client, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response
            result = await chunker_client.chunk_batch([])

        assert result == []

    @pytest.mark.asyncio
    async def test_chunk_batch_http_error_raises_transient(self, chunker_client):
        """Should raise TransientError on HTTP error."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Server error", request=MagicMock(), response=mock_response
        )

        with patch.object(chunker_client._client, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response

            with pytest.raises(TransientError) as exc_info:
                await chunker_client.chunk_batch(["text"])

            assert "Chunker batch service failed" in str(exc_info.value)


class TestChunkerClientWaitUntilReady:
    """Tests for ChunkerClient.wait_until_ready method."""

    @pytest.mark.asyncio
    async def test_wait_until_ready_immediate_success(self, chunker_client):
        """Should return True when service is immediately ready."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"chunker_loaded": True}

        with patch.object(chunker_client._client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response
            result = await chunker_client.wait_until_ready(timeout=5.0)

        assert result is True

    @pytest.mark.asyncio
    async def test_wait_until_ready_not_loaded(self, chunker_client):
        """Should return False when chunker never loads within timeout."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"chunker_loaded": False}

        with patch.object(chunker_client._client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response
            # Use very short timeout for test speed
            result = await chunker_client.wait_until_ready(timeout=0.1)

        assert result is False

    @pytest.mark.asyncio
    async def test_wait_until_ready_connection_error(self, chunker_client):
        """Should return False when connection fails throughout timeout."""
        with patch.object(chunker_client._client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.side_effect = httpx.HTTPError("Connection refused")
            result = await chunker_client.wait_until_ready(timeout=0.1)

        assert result is False
