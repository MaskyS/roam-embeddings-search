"""Unit tests for the chunking stage."""

from __future__ import annotations

import asyncio
import pytest
from dataclasses import dataclass
from unittest.mock import AsyncMock, MagicMock

from sync.data.models import PageSnapshot, PageWorkItem, SyncMetadata
from sync.data.results import ChunkStageResult
from sync.pipeline.stages.chunk_stage import stage_chunk
from common.errors import TransientError


@dataclass
class MockChunkerClient:
    """Mock chunker client for testing."""
    chunks_to_return: list = None
    should_fail: bool = False
    fail_message: str = "Chunker mock failure"

    async def chunk_batch(self, texts):
        if self.should_fail:
            raise TransientError(self.fail_message)
        if self.chunks_to_return:
            return self.chunks_to_return
        # Default: each text becomes a single chunk
        return [[{"text": t, "start_index": 0, "end_index": len(t)}] for t in texts]


@dataclass
class MockResources:
    """Mock resources for testing."""
    chunker: MockChunkerClient
    chunk_semaphore: asyncio.Semaphore


def make_page_snapshot(
    page_uid: str,
    page_title: str,
    linearized_text: str,
    has_children: bool,
) -> PageSnapshot:
    """Create a PageSnapshot for testing."""
    return PageSnapshot(
        page_uid=page_uid,
        page_title=page_title,
        linearized_text=linearized_text,
        uid_map=[],
        meta=SyncMetadata(
            page_uid=page_uid,
            max_edit_time=1700000000000,
            max_block_edit_time=1700000000000,
            max_create_time=None,
        ),
        has_children=has_children,
    )


def make_work_item(
    page_uid: str,
    page_title: str,
    linearized_text: str,
    has_children: bool,
    page_num: int = 0,
) -> PageWorkItem:
    """Create a PageWorkItem for testing."""
    return PageWorkItem(
        snapshot=make_page_snapshot(page_uid, page_title, linearized_text, has_children),
        page_title=page_title,
        page_uid=page_uid,
        page_num=page_num,
    )


class TestStageChunk:
    """Tests for stage_chunk function."""

    @pytest.mark.asyncio
    async def test_chunks_pages_with_children(self):
        """Should chunk pages that have children."""
        chunker = MockChunkerClient(
            chunks_to_return=[
                [{"text": "chunk1", "start_index": 0, "end_index": 6}],
            ]
        )
        resources = MockResources(chunker=chunker, chunk_semaphore=asyncio.Semaphore(1))

        items = [
            make_work_item("page1", "Page 1", "Some content", has_children=True),
        ]

        result = await stage_chunk(items, resources)

        assert result.is_ok
        assert 0 in result.chunk_results_by_index
        assert len(result.chunk_results_by_index[0]) == 1
        assert result.chunk_results_by_index[0][0]["text"] == "chunk1"

    @pytest.mark.asyncio
    async def test_skips_pages_without_children(self):
        """Should give empty chunks to pages without children."""
        chunker = MockChunkerClient()
        resources = MockResources(chunker=chunker, chunk_semaphore=asyncio.Semaphore(1))

        items = [
            make_work_item("page1", "Page 1", "", has_children=False),
        ]

        result = await stage_chunk(items, resources)

        assert result.is_ok
        assert 0 in result.chunk_results_by_index
        assert result.chunk_results_by_index[0] == []

    @pytest.mark.asyncio
    async def test_mixed_pages(self):
        """Should handle mix of pages with and without children."""
        chunker = MockChunkerClient(
            chunks_to_return=[
                [{"text": "chunk-for-page-1", "start_index": 0, "end_index": 15}],
            ]
        )
        resources = MockResources(chunker=chunker, chunk_semaphore=asyncio.Semaphore(1))

        items = [
            make_work_item("page1", "With Children", "text", has_children=True, page_num=0),
            make_work_item("page2", "No Children", "", has_children=False, page_num=1),
        ]

        result = await stage_chunk(items, resources)

        assert result.is_ok
        # Page with children got chunked
        assert 0 in result.chunk_results_by_index
        assert len(result.chunk_results_by_index[0]) == 1
        # Page without children got empty list
        assert 1 in result.chunk_results_by_index
        assert result.chunk_results_by_index[1] == []

    @pytest.mark.asyncio
    async def test_empty_input(self):
        """Should handle empty input list."""
        chunker = MockChunkerClient()
        resources = MockResources(chunker=chunker, chunk_semaphore=asyncio.Semaphore(1))

        result = await stage_chunk([], resources)

        assert result.is_ok
        assert result.chunk_results_by_index == {}

    @pytest.mark.asyncio
    async def test_chunker_failure_returns_error(self):
        """Should return error result when chunker fails."""
        chunker = MockChunkerClient(should_fail=True, fail_message="Service unavailable")
        resources = MockResources(chunker=chunker, chunk_semaphore=asyncio.Semaphore(1))

        items = [
            make_work_item("page1", "Page 1", "content", has_children=True),
        ]

        result = await stage_chunk(items, resources)

        assert result.is_err
        assert len(result.errors) == 1
        assert "Chunker failed" in result.errors[0]

    @pytest.mark.asyncio
    async def test_records_timing_metrics(self):
        """Should record chunk_duration and chunk_wait."""
        chunker = MockChunkerClient()
        resources = MockResources(chunker=chunker, chunk_semaphore=asyncio.Semaphore(1))

        items = [
            make_work_item("page1", "Page 1", "content", has_children=True),
        ]

        result = await stage_chunk(items, resources)

        assert result.is_ok
        assert result.chunk_duration >= 0
        assert result.chunk_wait >= 0

    @pytest.mark.asyncio
    async def test_preserves_index_mapping(self):
        """Should map chunks back to correct page indices."""
        chunker = MockChunkerClient(
            chunks_to_return=[
                [{"text": "a1"}, {"text": "a2"}],  # For first page with children
                [{"text": "b1"}],  # For second page with children
            ]
        )
        resources = MockResources(chunker=chunker, chunk_semaphore=asyncio.Semaphore(1))

        items = [
            make_work_item("pageA", "A", "contentA", has_children=True, page_num=0),
            make_work_item("pageB", "B", "", has_children=False, page_num=1),
            make_work_item("pageC", "C", "contentC", has_children=True, page_num=2),
        ]

        result = await stage_chunk(items, resources)

        assert result.is_ok
        # Index 0 (pageA): 2 chunks
        assert len(result.chunk_results_by_index[0]) == 2
        # Index 1 (pageB): empty (no children)
        assert result.chunk_results_by_index[1] == []
        # Index 2 (pageC): 1 chunk
        assert len(result.chunk_results_by_index[2]) == 1
