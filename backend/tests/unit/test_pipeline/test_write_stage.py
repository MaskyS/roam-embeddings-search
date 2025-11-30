"""Unit tests for the write stage."""

from __future__ import annotations

import asyncio
import pytest
from dataclasses import dataclass, field
from typing import Any, Dict, List

from sync.data.models import PageSnapshot, PageWorkItem, SyncMetadata, WeaviateObjectSet
from sync.data.results import WriteStageResult
from sync.pipeline.stages.write_stage import stage_write
from common.errors import TransientError


@dataclass
class MockWeaviateAdapter:
    """Mock Weaviate adapter for testing."""
    should_fail_insert: bool = False
    should_fail_delete: bool = False
    fail_message: str = "Weaviate mock failure"
    return_errors: list = None
    inserted_objects: List[Dict] = field(default_factory=list)
    deleted_pages: List[str] = field(default_factory=list)

    async def insert_objects(self, objects):
        if self.should_fail_insert:
            raise TransientError(self.fail_message)
        self.inserted_objects.extend(objects)
        return self.return_errors or []

    async def delete_stale_objects(self, page_uid, content_hash):
        if self.should_fail_delete:
            raise TransientError(self.fail_message)
        self.deleted_pages.append(page_uid)


@dataclass
class MockResources:
    """Mock resources for testing."""
    weaviate: MockWeaviateAdapter
    weaviate_semaphore: asyncio.Semaphore


def make_page_snapshot(
    page_uid: str,
    max_edit_time: int = 1700000000000,
) -> PageSnapshot:
    """Create a PageSnapshot for testing."""
    return PageSnapshot(
        page_uid=page_uid,
        page_title=f"Title for {page_uid}",
        linearized_text="Some text",
        uid_map=[],
        meta=SyncMetadata(
            page_uid=page_uid,
            max_edit_time=max_edit_time,
            max_block_edit_time=max_edit_time,
            max_create_time=None,
        ),
        has_children=True,
    )


def make_work_item(page_uid: str, page_num: int = 0) -> PageWorkItem:
    """Create a PageWorkItem for testing."""
    snapshot = make_page_snapshot(page_uid)
    return PageWorkItem(
        snapshot=snapshot,
        page_title=snapshot.page_title,
        page_uid=page_uid,
        page_num=page_num,
    )


def make_weaviate_object_set(
    page_uid: str,
    num_chunks: int = 2,
    content_hash: str = "test-hash",
) -> WeaviateObjectSet:
    """Create a WeaviateObjectSet for testing."""
    page_obj = {
        "uuid": f"uuid-page-{page_uid}",
        "properties": {"page_uid": page_uid, "document_type": "page"},
        "vector": [0.1] * 1024,
    }
    chunk_objs = [
        {
            "uuid": f"uuid-chunk-{page_uid}-{i}",
            "properties": {"page_uid": page_uid, "document_type": "chunk"},
            "vector": [0.2] * 1024,
        }
        for i in range(num_chunks)
    ]
    return WeaviateObjectSet(
        page_object=page_obj,
        chunk_objects=chunk_objs,
        all_objects=[page_obj] + chunk_objs,
        chunk_texts=[f"Chunk {i}" for i in range(num_chunks)],
        content_hash=content_hash,
    )


class TestStageWrite:
    """Tests for stage_write function."""

    @pytest.mark.asyncio
    async def test_writes_objects_successfully(self):
        """Should write objects and return success metrics."""
        weaviate = MockWeaviateAdapter()
        resources = MockResources(weaviate=weaviate, weaviate_semaphore=asyncio.Semaphore(1))

        item = make_work_item("page1")
        payload = make_weaviate_object_set("page1", num_chunks=2)

        result = await stage_write([(item, payload)], resources)

        assert result.is_ok
        assert result.docs_added == 3  # 1 page + 2 chunks
        assert result.chunks_created == 2
        assert result.pages_updated == 1
        assert "page1" in result.state_updates

    @pytest.mark.asyncio
    async def test_empty_input_returns_empty_result(self):
        """Should handle empty input."""
        weaviate = MockWeaviateAdapter()
        resources = MockResources(weaviate=weaviate, weaviate_semaphore=asyncio.Semaphore(1))

        result = await stage_write([], resources)

        assert result.is_ok
        assert result.docs_added == 0
        assert result.pages_updated == 0

    @pytest.mark.asyncio
    async def test_multiple_pages(self):
        """Should aggregate metrics across multiple pages."""
        weaviate = MockWeaviateAdapter()
        resources = MockResources(weaviate=weaviate, weaviate_semaphore=asyncio.Semaphore(1))

        payloads = [
            (make_work_item("page1"), make_weaviate_object_set("page1", num_chunks=3)),
            (make_work_item("page2"), make_weaviate_object_set("page2", num_chunks=1)),
        ]

        result = await stage_write(payloads, resources)

        assert result.is_ok
        # page1: 1 page + 3 chunks = 4
        # page2: 1 page + 1 chunk = 2
        assert result.docs_added == 6
        assert result.chunks_created == 4
        assert result.pages_updated == 2
        assert "page1" in result.state_updates
        assert "page2" in result.state_updates

    @pytest.mark.asyncio
    async def test_insert_failure_returns_error(self):
        """Should return error when insert fails."""
        weaviate = MockWeaviateAdapter(should_fail_insert=True)
        resources = MockResources(weaviate=weaviate, weaviate_semaphore=asyncio.Semaphore(1))

        item = make_work_item("page1")
        payload = make_weaviate_object_set("page1")

        result = await stage_write([(item, payload)], resources)

        assert result.is_err
        assert len(result.errors) == 1
        assert "Weaviate write failed" in result.errors[0]

    @pytest.mark.asyncio
    async def test_partial_insert_failure(self):
        """Should return error when some objects fail to insert."""
        mock_error = type("MockError", (), {"message": "Vector dimension mismatch"})()
        weaviate = MockWeaviateAdapter(return_errors=[mock_error])
        resources = MockResources(weaviate=weaviate, weaviate_semaphore=asyncio.Semaphore(1))

        item = make_work_item("page1")
        payload = make_weaviate_object_set("page1")

        result = await stage_write([(item, payload)], resources)

        assert result.is_err
        assert "failed objects" in result.errors[0]

    @pytest.mark.asyncio
    async def test_delete_stale_called(self):
        """Should call delete_stale_objects for each page."""
        weaviate = MockWeaviateAdapter()
        resources = MockResources(weaviate=weaviate, weaviate_semaphore=asyncio.Semaphore(1))

        payloads = [
            (make_work_item("page1"), make_weaviate_object_set("page1", content_hash="hash1")),
            (make_work_item("page2"), make_weaviate_object_set("page2", content_hash="hash2")),
        ]

        await stage_write(payloads, resources)

        assert "page1" in weaviate.deleted_pages
        assert "page2" in weaviate.deleted_pages

    @pytest.mark.asyncio
    async def test_state_updates_contain_edit_time_and_hash(self):
        """Should populate state updates with edit time and content hash."""
        weaviate = MockWeaviateAdapter()
        resources = MockResources(weaviate=weaviate, weaviate_semaphore=asyncio.Semaphore(1))

        item = make_work_item("page1")
        payload = make_weaviate_object_set("page1", content_hash="abc123")

        result = await stage_write([(item, payload)], resources)

        state = result.state_updates["page1"]
        assert state["content_hash"] == "abc123"
        assert state["last_synced_edit_time"] is not None

    @pytest.mark.asyncio
    async def test_records_timing_metrics(self):
        """Should record weaviate_duration and weaviate_wait."""
        weaviate = MockWeaviateAdapter()
        resources = MockResources(weaviate=weaviate, weaviate_semaphore=asyncio.Semaphore(1))

        item = make_work_item("page1")
        payload = make_weaviate_object_set("page1")

        result = await stage_write([(item, payload)], resources)

        assert result.is_ok
        assert result.weaviate_duration >= 0
        assert result.weaviate_wait >= 0

    @pytest.mark.asyncio
    async def test_flattens_objects_from_all_pages(self):
        """Should insert all objects in a single batch."""
        weaviate = MockWeaviateAdapter()
        resources = MockResources(weaviate=weaviate, weaviate_semaphore=asyncio.Semaphore(1))

        payloads = [
            (make_work_item("page1"), make_weaviate_object_set("page1", num_chunks=2)),
            (make_work_item("page2"), make_weaviate_object_set("page2", num_chunks=1)),
        ]

        await stage_write(payloads, resources)

        # All objects should be inserted in one batch
        # page1: 1 page + 2 chunks = 3
        # page2: 1 page + 1 chunk = 2
        assert len(weaviate.inserted_objects) == 5
