"""Shared test fixtures and mock factories for the Roam Semantic Search backend."""

from __future__ import annotations

import asyncio
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional
from unittest.mock import AsyncMock, MagicMock

import pytest

# Fixtures directory
FIXTURES_DIR = Path(__file__).parent / "fixtures"


# ============================================================================
# Pytest Configuration
# ============================================================================

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "integration: mark test as integration test (requires real APIs)")


def pytest_collection_modifyitems(config, items):
    """Skip integration tests by default unless --run-integration is passed."""
    if config.getoption("--run-integration", default=False):
        return

    skip_integration = pytest.mark.skip(reason="need --run-integration option to run")
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip_integration)


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--run-integration",
        action="store_true",
        default=False,
        help="run integration tests (requires real API credentials)",
    )


# ============================================================================
# Sample Data Factories
# ============================================================================

def make_roam_page(
    uid: str = "test-page-uid",
    title: str = "Test Page",
    edit_time: int = 1700000000000,
    children: Optional[List[Dict]] = None,
) -> Dict[str, Any]:
    """Create a sample Roam page structure."""
    page = {
        ":block/uid": uid,
        ":node/title": title,
        ":edit/time": edit_time,
    }
    if children:
        page[":block/children"] = children
    return page


def make_roam_block(
    uid: str = "test-block-uid",
    string: str = "Test block content",
    order: int = 0,
    edit_time: int = 1700000000000,
    children: Optional[List[Dict]] = None,
) -> Dict[str, Any]:
    """Create a sample Roam block structure."""
    block = {
        ":block/uid": uid,
        ":block/string": string,
        ":block/order": order,
        ":edit/time": edit_time,
    }
    if children:
        block[":block/children"] = children
    return block


def make_page_with_children(page_uid: str = "page-123") -> Dict[str, Any]:
    """Create a sample page with nested children."""
    return make_roam_page(
        uid=page_uid,
        title="Sample Page with Children",
        children=[
            make_roam_block(
                uid=f"{page_uid}-block-1",
                string="First block with some content",
                order=0,
                children=[
                    make_roam_block(
                        uid=f"{page_uid}-block-1-1",
                        string="Nested child block",
                        order=0,
                    ),
                ],
            ),
            make_roam_block(
                uid=f"{page_uid}-block-2",
                string="Second block with different content",
                order=1,
            ),
        ],
    )


def make_childless_page(page_uid: str = "page-456") -> Dict[str, Any]:
    """Create a sample page without children."""
    return make_roam_page(
        uid=page_uid,
        title="Leaf Page Title Only",
    )


# ============================================================================
# Mock Clients
# ============================================================================

@dataclass
class MockChunkerClient:
    """Mock chunker client for testing."""

    chunks_to_return: List[List[Dict]] = None
    should_fail: bool = False
    fail_message: str = "Chunker mock failure"

    async def chunk_text(self, text: str) -> List[Dict[str, Any]]:
        if self.should_fail:
            from common.errors import TransientError
            raise TransientError(self.fail_message)
        if self.chunks_to_return:
            return self.chunks_to_return[0] if self.chunks_to_return else []
        # Default: return single chunk with the input text
        return [{"text": text, "start_index": 0, "end_index": len(text)}]

    async def chunk_batch(self, texts: List[str]) -> List[List[Dict[str, Any]]]:
        if self.should_fail:
            from common.errors import TransientError
            raise TransientError(self.fail_message)
        if self.chunks_to_return:
            return self.chunks_to_return
        # Default: each text becomes a single chunk
        return [[{"text": t, "start_index": 0, "end_index": len(t)}] for t in texts]

    async def wait_until_ready(self, timeout: float = 60.0) -> bool:
        return True

    async def close(self):
        pass


@dataclass
class MockVoyageClient:
    """Mock VoyageAI embedding client for testing."""

    embedding_dim: int = 1024
    should_fail: bool = False
    fail_message: str = "Voyage mock failure"

    async def embed_documents(self, pages: List[List[str]]) -> List[List[List[float]]]:
        if self.should_fail:
            from common.errors import TransientError
            raise TransientError(self.fail_message)
        # Return fake embeddings: one vector per chunk in each page
        return [
            [[0.1] * self.embedding_dim for _ in chunks]
            for chunks in pages
        ]

    async def embed_query(self, query: str) -> List[float]:
        if self.should_fail:
            from common.errors import TransientError
            raise TransientError(self.fail_message)
        return [0.1] * self.embedding_dim


@dataclass
class MockWeaviateAdapter:
    """Mock Weaviate adapter for testing."""

    existing_state: Optional[Dict[str, Any]] = None
    should_fail_insert: bool = False
    should_fail_delete: bool = False
    inserted_objects: List[Dict] = None
    deleted_pages: List[str] = None

    def __post_init__(self):
        self.inserted_objects = []
        self.deleted_pages = []

    async def ensure_schema(self, recreate: bool = False) -> None:
        pass

    async def fetch_existing_page_state(self, page_uid: str) -> Dict[str, Any]:
        if self.existing_state:
            return self.existing_state
        return {
            "page_objects": [],
            "chunk_objects": [],
            "last_synced_edit_time": None,
            "content_hash": None,
        }

    async def insert_objects(self, objects: List[Dict[str, Any]]) -> List:
        if self.should_fail_insert:
            from common.errors import TransientError
            raise TransientError("Weaviate insert mock failure")
        self.inserted_objects.extend(objects)
        return []  # No errors

    async def delete_stale_objects(self, page_uid: str, content_hash: str) -> None:
        if self.should_fail_delete:
            from common.errors import TransientError
            raise TransientError("Weaviate delete mock failure")
        self.deleted_pages.append(page_uid)


@dataclass
class MockRoamClient:
    """Mock Roam API client for testing."""

    pages: Dict[str, Dict[str, Any]] = None
    all_uids: List[str] = None
    should_fail: bool = False

    def __post_init__(self):
        if self.pages is None:
            self.pages = {}
        if self.all_uids is None:
            self.all_uids = list(self.pages.keys())

    async def get_all_page_uids(self) -> List[str]:
        if self.should_fail:
            return []
        return self.all_uids

    async def pull_many_pages(self, uids: List[str], **kwargs) -> List[Optional[Dict]]:
        if self.should_fail:
            return [None] * len(uids)
        return [self.pages.get(uid) for uid in uids]

    async def pull_many_metadata(self, uids: List[str], **kwargs) -> List[Optional[Dict]]:
        if self.should_fail:
            return [None] * len(uids)
        # Return minimal metadata
        return [
            {":block/uid": uid, ":edit/time": 1700000000000}
            if uid in self.pages else None
            for uid in uids
        ]


# ============================================================================
# Async Event Loop Fixture
# ============================================================================

@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# ============================================================================
# Mock Client Fixtures
# ============================================================================

@pytest.fixture
def mock_chunker():
    """Provide a mock chunker client."""
    return MockChunkerClient()


@pytest.fixture
def mock_voyage():
    """Provide a mock VoyageAI client."""
    return MockVoyageClient()


@pytest.fixture
def mock_weaviate():
    """Provide a mock Weaviate adapter."""
    return MockWeaviateAdapter()


@pytest.fixture
def mock_roam():
    """Provide a mock Roam client with sample pages."""
    pages = {
        "page-with-children": make_page_with_children("page-with-children"),
        "leaf-page": make_childless_page("leaf-page"),
    }
    return MockRoamClient(pages=pages, all_uids=list(pages.keys()))


# ============================================================================
# Fixture Data Loading
# ============================================================================

def load_fixture(name: str) -> Any:
    """Load a JSON fixture file by name."""
    fixture_path = FIXTURES_DIR / f"{name}.json"
    if fixture_path.exists():
        with open(fixture_path) as f:
            return json.load(f)
    return None


@pytest.fixture
def sample_roam_page():
    """Load a sample Roam page from fixtures or generate one."""
    data = load_fixture("sample_page")
    if data:
        return data
    return make_page_with_children()


@pytest.fixture
def sample_childless_page():
    """Load a sample childless Roam page from fixtures or generate one."""
    data = load_fixture("sample_childless_page")
    if data:
        return data
    return make_childless_page()


# ============================================================================
# Temp Database Fixture
# ============================================================================

@pytest.fixture
def temp_db(tmp_path):
    """Create a temporary SQLite database for testing."""
    db_path = tmp_path / "test_sync.db"
    os.environ["SEMANTIC_SYNC_DB"] = str(db_path)
    yield db_path
    # Cleanup happens automatically when tmp_path is removed


# ============================================================================
# Integration Test Fixtures (require real credentials)
# ============================================================================

@pytest.fixture
def integration_config():
    """Load integration test configuration from environment."""
    return {
        "roam_graph_name": os.getenv("ROAM_GRAPH_NAME"),
        "roam_api_token": os.getenv("ROAM_API_TOKEN"),
        "voyageai_api_key": os.getenv("VOYAGEAI_API_KEY"),
        "weaviate_cloud_url": os.getenv("WEAVIATE_CLOUD_URL"),
        "weaviate_cloud_api_key": os.getenv("WEAVIATE_CLOUD_API_KEY"),
    }
