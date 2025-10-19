"""Runtime state helpers for semantic sync orchestration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable, Dict, Optional, Set, TYPE_CHECKING, Union

import time
from contextlib import contextmanager

import structlog
import structlog.stdlib
from pydantic import BaseModel
from common.telemetry import Telemetry
from common.events import (
    UidsLoadedEvent,
    MetadataFilteredEvent,
    BatchStartEvent,
    BatchCompleteEvent,
    ChunkerReadyEvent,
    SinceAppliedEvent,
    Progress,
    StatusEvent,
)

if TYPE_CHECKING:  # pragma: no cover - for type-checking only
    from common.config import SyncConfig
    from sync.data.models import SyncRuntime


class MinimalSummary(BaseModel):
    """Lean summary focused on business-relevant fields only."""

    status: str
    total_pages: int
    processed: int
    updated: int
    skipped_since: int
    skipped_content: int
    failed: int
    cursor_max_edit_time: Optional[int]
    elapsed_seconds: Optional[float] = None
    error: Optional[str] = None


StatusCallback = Callable[[Dict[str, Any]], Awaitable[None]]


@dataclass(frozen=True)
class SyncRunParams:
    """Immutable options supplied for a sync run."""

    config: "SyncConfig"
    since: Optional[int]
    test_limit: Optional[int]
    resume: bool
    clear_existing: bool
    recreate_collection: bool
    state_file: Optional[str]
    status_callback: Optional[StatusCallback]
    completion_callback: Optional[StatusCallback]


@dataclass
class SyncRunState:
    """Mutable runtime state shared across orchestration stages."""

    runtime: "SyncRuntime"
    params: SyncRunParams
    total_pages: int
    start_time: float
    start_timestamp: str
    state_path: Optional[str]
    page_state_purged: int = 0
    pages_missing_edit_time: Set[str] = field(default_factory=set)
    pages_empty_linearized: Set[str] = field(default_factory=set)
    status_emitter: Optional["StatusEmitter"] = None
    telemetry: "Telemetry" = field(default_factory=lambda: Telemetry())

    def attach_emitter(self, emitter: "StatusEmitter") -> None:
        self.status_emitter = emitter

    def record_failure(self, message: str) -> None:
        self.telemetry.fail(message)

    def record_skip(self, reason: str, amount: int = 1) -> None:
        self.telemetry.skip(reason, amount)

    def add_duration(self, key: str, delta: float) -> None:
        self.telemetry.add_duration(key, delta)

    def increment_stat(self, key: str, amount: int = 1) -> None:
        self.telemetry.inc(key, amount)

    @contextmanager
    def timer(self, key: str):
        start = time.time()
        try:
            yield
        finally:
            self.add_duration(key, time.time() - start)


@dataclass
class MetadataOutcome:
    finished: bool
    summary: Optional[Dict[str, Any]] = None


class StatusEmitter:
    """Coalesce status payload construction and delivery with typed events."""

    def __init__(self, *, callback: Optional[StatusCallback], logger: structlog.stdlib.BoundLogger, state: SyncRunState) -> None:
        self._callback = callback
        self._logger = logger
        self._state = state
        state.attach_emitter(self)

    def _common_fields(self, *, include_full_failures: bool = False) -> Dict[str, Any]:
        snap = self._state.telemetry.snapshot()
        runtime = self._state.runtime
        failures = snap["failures"] if include_full_failures else snap["failures"][-5:]
        return {
            "stats": snap["stats"],
            "durations": snap["durations"],
            "skip_breakdown": snap["skip_breakdown"],
            "failures": failures,  # type: ignore[assignment]
            "total_pages": self._state.total_pages,
            "max_edit_time": runtime.max_edit_time_seen,
            "aggregated_max_edit_time": runtime.max_edit_time_seen,
        }

    def progress(self, *, processed: Optional[int] = None, total: Optional[int] = None) -> Dict[str, float]:
        runtime = self._state.runtime
        processed_value = processed if processed is not None else runtime.processed_offset
        total_value = total if total is not None else runtime.total_target_pages
        denominator = total_value if total_value else processed_value or 1
        percent = (processed_value / denominator) * 100
        return {
            "processed": processed_value,
            "total": total_value,
            "percent": percent,
        }

    async def _dispatch(self, payload: Union[StatusEvent, Dict[str, Any]], *, include_common: bool, include_full_failures: bool = False) -> None:
        if isinstance(payload, BaseModel):
            full_payload = payload.model_dump()
        else:
            full_payload = dict(payload)
        if include_common:
            common = self._common_fields(include_full_failures=include_full_failures)
            common.update(full_payload)
            full_payload = common

        # Avoid passing duplicate 'event' both positionally and as kwarg.
        # Use the event field (if present) as the log event name and drop it from kwargs.
        event_name = full_payload.pop("event", "status_event")
        self._logger.info(event_name, **full_payload)
        if self._callback:
            try:
                await self._callback(full_payload)
            except Exception:  # pragma: no cover - defensive
                self._logger.warning("status_callback_failed", failed_event=full_payload.get("event"), exc_info=True)

    async def uids_loaded(self, *, total_pages: int, started_at: str) -> None:
        evt = UidsLoadedEvent(
            total_pages=total_pages,
            started_at=started_at,
            progress=Progress(processed=0, total=total_pages, percent=0.0),
        )
        await self._dispatch(evt, include_common=False)

    async def metadata_filtered(
        self,
        *,
        remaining: int,
        skipped: int,
        metadata_durations: Dict[str, float],
    ) -> None:
        evt = MetadataFilteredEvent(remaining=remaining, skipped=skipped, durations=metadata_durations)
        await self._dispatch(evt, include_common=False)

    async def batch_start(
        self,
        *,
        batch: int,
        page_range: tuple[int, int],
        processed_before: int,
    ) -> None:
        prog = self.progress(processed=processed_before)
        evt = BatchStartEvent(batch=batch, page_start=page_range[0], page_end=page_range[1], progress=Progress(**prog))
        await self._dispatch(evt, include_common=True)

    async def batch_complete(self, *, batch: int, processed_after: int) -> None:
        prog = self.progress(processed=processed_after)
        evt = BatchCompleteEvent(batch=batch, processed=Progress(**prog))
        await self._dispatch(evt, include_common=True)

    async def chunker_ready(self, *, duration: float) -> None:
        evt = ChunkerReadyEvent(duration=duration)
        await self._dispatch(evt, include_common=False)

    async def since_applied(self, *, since: int, readable: str) -> None:
        evt = SinceAppliedEvent(since=since, readable=readable)
        await self._dispatch(evt, include_common=False)

    def build_summary(
        self,
        *,
        status: str,
        elapsed_seconds: Optional[float] = None,
        error: Optional[str] = None,
        include_full_failures: bool = False,
    ) -> Dict[str, Any]:
        base = self._common_fields(include_full_failures=include_full_failures)
        stats: Dict[str, int] = base.get("stats", {})  # type: ignore[assignment]
        skip_bd: Dict[str, int] = base.get("skip_breakdown", {})  # type: ignore[assignment]
        runtime = self._state.runtime
        processed = runtime.total_target_pages - len(runtime.pending_uids)
        summary = MinimalSummary(
            status=status,
            total_pages=self._state.total_pages,
            processed=processed,
            updated=int(stats.get("pages_updated", 0)),
            skipped_since=int(skip_bd.get("since", 0)),
            skipped_content=int(skip_bd.get("content", 0)),
            failed=int(stats.get("pages_failed", 0)),
            cursor_max_edit_time=runtime.max_edit_time_seen,
            elapsed_seconds=elapsed_seconds,
            error=error,
        )
        return summary.model_dump()
