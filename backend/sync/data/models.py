"""Structured data classes used throughout the semantic sync pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional


@dataclass
class PageWorkItem:
    snapshot: "PageSnapshot"
    page_title: str
    page_uid: str
    page_num: int


@dataclass
class PageMetadata:
    page_uid: str
    max_edit_time: Optional[int]
    has_children: bool
    page_title: Optional[str] = None
    aggregated_edit_time: Optional[int] = None
    raw: Optional[Dict[str, Any]] = None


@dataclass
class GroupResult:
    docs_added: int = 0
    chunks_created: int = 0
    pages_updated: int = 0
    pages_failed: int = 0
    chunk_duration: float = 0.0
    voyage_duration: float = 0.0
    weaviate_duration: float = 0.0
    chunk_wait: float = 0.0
    voyage_wait: float = 0.0
    weaviate_wait: float = 0.0
    fail_messages: List[str] = field(default_factory=list)
    state_updates: Dict[str, Dict[str, Any]] = field(default_factory=dict)


@dataclass
class MetadataPassResult:
    remaining_uids: List[str]
    metadata_map: Dict[str, PageMetadata]
    state_cache: Dict[str, Dict[str, Any]]
    stats_delta: Dict[str, int]
    durations_delta: Dict[str, float]
    missing_edit_uids: set[str]
    max_edit_time_seen: Optional[int]


@dataclass
class SyncRuntime:
    pending_uids: List[str]
    processed_offset: int
    total_target_pages: int
    state_loaded: bool = False
    state_completed: bool = False
    metadata_applied: bool = False
    metadata_map: Dict[str, PageMetadata] = field(default_factory=dict)
    page_state_cache: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    max_edit_time_seen: Optional[int] = None


@dataclass
class MetadataPhaseOutcome:
    finished: bool
    summary: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class SyncMetadata:
    """Metadata extracted from a Roam page during linearization."""

    page_uid: str
    max_edit_time: Optional[int]
    max_block_edit_time: Optional[int]
    max_create_time: Optional[int]


@dataclass(frozen=True)
class PageSnapshot:
    """Immutable snapshot of a Roam page with linearized content."""

    page_uid: str
    page_title: str
    linearized_text: str
    uid_map: List[Dict[str, Any]]
    meta: SyncMetadata
    has_children: bool

    def get(self, key: str, default: Any = None) -> Any:  # pragma: no cover
        if key == "page_uid":
            return self.page_uid
        if key == "page_title":
            return self.page_title
        if key == "linearized_text":
            return self.linearized_text
        if key == "uid_map":
            return self.uid_map
        if key == "meta":
            return {
                "page_uid": self.meta.page_uid,
                "max_edit_time": self.meta.max_edit_time,
                "max_block_edit_time": self.meta.max_block_edit_time,
                "max_create_time": self.meta.max_create_time,
            }
        if key == "has_children":
            return self.has_children
        return default


@dataclass(frozen=True)
class SyncDecision:
    should_skip: bool
    reason: Optional[Literal["since", "unchanged", "empty"]]
    since_filtered: bool
    metadata: SyncMetadata
    content_hash: str
    missing_edit_time: bool
    empty_linearized: bool


@dataclass(frozen=True)
class WeaviateObjectSet:
    page_object: Dict[str, Any]
    chunk_objects: List[Dict[str, Any]]
    all_objects: List[Dict[str, Any]]
    chunk_texts: List[str]
    content_hash: str


@dataclass(frozen=True)
class PageProcessingResult:
    page_uid: str
    page_title: str
    action: Literal["updated", "skipped", "failed"]
    skip_reason: Optional[str] = None
    error: Optional[Exception] = None
    durations: Dict[str, float] = field(default_factory=dict)
    work_item: Optional[Any] = None

