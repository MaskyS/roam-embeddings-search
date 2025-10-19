"""Typed status events for sync progress reporting."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from typing import Dict


class Progress(BaseModel):
    processed: int
    total: int
    percent: float


class StatusEvent(BaseModel):
    """Base for typed status events."""

    model_config = ConfigDict(extra="allow")
    event: str


class UidsLoadedEvent(StatusEvent):
    event: str = "uids_loaded"
    total_pages: int
    started_at: str
    progress: Progress


class MetadataFilteredEvent(StatusEvent):
    event: str = "metadata_filtered"
    remaining: int
    skipped: int
    durations: Dict[str, float]


class BatchStartEvent(StatusEvent):
    event: str = "batch_start"
    batch: int
    page_start: int
    page_end: int
    progress: Progress


class BatchCompleteEvent(StatusEvent):
    event: str = "batch_complete"
    batch: int
    processed: Progress


class ChunkerReadyEvent(StatusEvent):
    event: str = "chunker_ready"
    duration: float


class SinceAppliedEvent(StatusEvent):
    event: str = "since_applied"
    since: int
    readable: str

