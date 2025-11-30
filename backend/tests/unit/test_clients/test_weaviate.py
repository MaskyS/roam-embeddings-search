"""Unit tests for the WeaviateSyncAdapter."""

from __future__ import annotations

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from clients.weaviate import WeaviateSyncAdapter


@pytest.fixture
def mock_weaviate_client():
    """Create a mock Weaviate async client."""
    client = MagicMock()
    client.collections = MagicMock()
    return client


@pytest.fixture
def weaviate_adapter(mock_weaviate_client):
    return WeaviateSyncAdapter(
        client=mock_weaviate_client,
        collection_name="TestCollection",
    )


class TestWeaviateEnsureSchema:
    """Tests for WeaviateSyncAdapter.ensure_schema method."""

    @pytest.mark.asyncio
    async def test_ensure_schema_creates_when_not_exists(self, weaviate_adapter, mock_weaviate_client):
        """Should create collection when it doesn't exist."""
        mock_weaviate_client.collections.exists = AsyncMock(return_value=False)
        mock_weaviate_client.collections.create = AsyncMock()

        await weaviate_adapter.ensure_schema()

        mock_weaviate_client.collections.create.assert_called_once()
        call_kwargs = mock_weaviate_client.collections.create.call_args[1]
        assert call_kwargs["name"] == "TestCollection"

    @pytest.mark.asyncio
    async def test_ensure_schema_skips_when_exists(self, weaviate_adapter, mock_weaviate_client):
        """Should not create collection when it already exists."""
        mock_weaviate_client.collections.exists = AsyncMock(return_value=True)
        mock_weaviate_client.collections.create = AsyncMock()

        await weaviate_adapter.ensure_schema()

        mock_weaviate_client.collections.create.assert_not_called()

    @pytest.mark.asyncio
    async def test_ensure_schema_recreate_deletes_first(self, weaviate_adapter, mock_weaviate_client):
        """Should delete existing collection when recreate=True."""
        mock_weaviate_client.collections.exists = AsyncMock(return_value=True)
        mock_weaviate_client.collections.delete = AsyncMock()
        mock_weaviate_client.collections.create = AsyncMock()

        await weaviate_adapter.ensure_schema(recreate=True)

        mock_weaviate_client.collections.delete.assert_called_once_with("TestCollection")
        mock_weaviate_client.collections.create.assert_called_once()


class TestWeaviateFetchExistingPageState:
    """Tests for WeaviateSyncAdapter.fetch_existing_page_state method."""

    @pytest.mark.asyncio
    async def test_fetch_state_empty(self, weaviate_adapter, mock_weaviate_client):
        """Should return empty state when no objects found."""
        mock_collection = MagicMock()
        mock_collection.query.fetch_objects = AsyncMock(return_value=MagicMock(objects=[]))
        mock_weaviate_client.collections.get.return_value = mock_collection

        state = await weaviate_adapter.fetch_existing_page_state("page-123")

        assert state["page_objects"] == []
        assert state["chunk_objects"] == []
        assert state["last_synced_edit_time"] is None
        assert state["content_hash"] is None

    @pytest.mark.asyncio
    async def test_fetch_state_with_page_and_chunks(self, weaviate_adapter, mock_weaviate_client):
        """Should categorize objects by document type."""
        page_obj = MagicMock()
        page_obj.properties = {
            "document_type": "page",
            "last_synced_edit_time": "1700000000000",
            "content_hash": "abc123",
        }
        chunk_obj = MagicMock()
        chunk_obj.properties = {"document_type": "chunk"}

        mock_response = MagicMock()
        mock_response.objects = [page_obj, chunk_obj]

        mock_collection = MagicMock()
        mock_collection.query.fetch_objects = AsyncMock(return_value=mock_response)
        mock_weaviate_client.collections.get.return_value = mock_collection

        state = await weaviate_adapter.fetch_existing_page_state("page-123")

        assert len(state["page_objects"]) == 1
        assert len(state["chunk_objects"]) == 1
        assert state["last_synced_edit_time"] == "1700000000000"
        assert state["content_hash"] == "abc123"

    @pytest.mark.asyncio
    async def test_fetch_state_handles_query_error(self, weaviate_adapter, mock_weaviate_client):
        """Should return empty state on query error."""
        mock_collection = MagicMock()
        mock_collection.query.fetch_objects = AsyncMock(side_effect=Exception("Query failed"))
        mock_weaviate_client.collections.get.return_value = mock_collection

        state = await weaviate_adapter.fetch_existing_page_state("page-123")

        assert state["page_objects"] == []
        assert state["chunk_objects"] == []


class TestWeaviateDeleteStaleObjects:
    """Tests for WeaviateSyncAdapter.delete_stale_objects method."""

    @pytest.mark.asyncio
    async def test_delete_stale_with_content_hash(self, weaviate_adapter, mock_weaviate_client):
        """Should delete objects with different content hash."""
        mock_collection = MagicMock()
        mock_collection.data.delete_many = AsyncMock()
        mock_weaviate_client.collections.get.return_value = mock_collection

        await weaviate_adapter.delete_stale_objects("page-123", "new-hash")

        mock_collection.data.delete_many.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_stale_without_content_hash(self, weaviate_adapter, mock_weaviate_client):
        """Should delete all page objects when no hash provided."""
        mock_collection = MagicMock()
        mock_collection.data.delete_many = AsyncMock()
        mock_weaviate_client.collections.get.return_value = mock_collection

        await weaviate_adapter.delete_stale_objects("page-123", "")

        mock_collection.data.delete_many.assert_called_once()


class TestWeaviateInsertObjects:
    """Tests for WeaviateSyncAdapter.insert_objects method."""

    @pytest.mark.asyncio
    async def test_insert_objects_success(self, weaviate_adapter, mock_weaviate_client):
        """Should insert objects and return empty error list."""
        mock_result = MagicMock()
        mock_result.has_errors = False

        mock_collection = MagicMock()
        mock_collection.data.insert_many = AsyncMock(return_value=mock_result)
        mock_weaviate_client.collections.get.return_value = mock_collection

        objects = [
            {"uuid": "uuid1", "properties": {"text": "chunk1"}, "vector": [0.1] * 1024},
            {"uuid": "uuid2", "properties": {"text": "chunk2"}, "vector": [0.2] * 1024},
        ]
        errors = await weaviate_adapter.insert_objects(objects)

        assert errors == []
        mock_collection.data.insert_many.assert_called_once()

    @pytest.mark.asyncio
    async def test_insert_objects_empty(self, weaviate_adapter, mock_weaviate_client):
        """Should handle empty input."""
        errors = await weaviate_adapter.insert_objects([])
        assert errors == []

    @pytest.mark.asyncio
    async def test_insert_objects_duplicate_replaced(self, weaviate_adapter, mock_weaviate_client):
        """Should replace duplicate objects instead of failing."""
        error_obj = MagicMock()
        error_obj.message = "Object already exists"

        mock_result = MagicMock()
        mock_result.has_errors = True
        mock_result.errors = {0: error_obj}

        mock_collection = MagicMock()
        mock_collection.data.insert_many = AsyncMock(return_value=mock_result)
        mock_collection.data.replace = AsyncMock()
        mock_weaviate_client.collections.get.return_value = mock_collection

        objects = [{"uuid": "uuid1", "properties": {"text": "chunk1"}, "vector": [0.1] * 1024}]
        errors = await weaviate_adapter.insert_objects(objects)

        # Should have attempted replace and returned no errors
        mock_collection.data.replace.assert_called_once()
        assert errors == []

    @pytest.mark.asyncio
    async def test_insert_objects_unrecoverable_error(self, weaviate_adapter, mock_weaviate_client):
        """Should return unrecoverable errors."""
        error_obj = MagicMock()
        error_obj.message = "Invalid vector dimension"

        mock_result = MagicMock()
        mock_result.has_errors = True
        mock_result.errors = {0: error_obj}

        mock_collection = MagicMock()
        mock_collection.data.insert_many = AsyncMock(return_value=mock_result)
        mock_weaviate_client.collections.get.return_value = mock_collection

        objects = [{"uuid": "uuid1", "properties": {"text": "chunk1"}, "vector": [0.1]}]
        errors = await weaviate_adapter.insert_objects(objects)

        assert len(errors) == 1
        assert "Invalid vector dimension" in errors[0].message
