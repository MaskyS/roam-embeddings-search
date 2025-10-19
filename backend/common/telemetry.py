"""Lightweight telemetry aggregation for sync runs.

Provides counters, durations, skip reasons and failures with a simple
timer context manager for measuring code sections.
"""

from __future__ import annotations

import time
from collections import Counter, defaultdict
from contextlib import contextmanager
from typing import DefaultDict, Dict, Iterator, List


class Telemetry:
    """Aggregate counters and durations for a sync run."""

    def __init__(self) -> None:
        self._stats: Counter[str] = Counter()
        self._durations: DefaultDict[str, float] = defaultdict(float)
        self._skips: Counter[str] = Counter()
        self._failures: List[str] = []

    # --- Counters ---
    def inc(self, key: str, amount: int = 1) -> None:
        self._stats[key] += amount

    # --- Durations ---
    def add_duration(self, key: str, delta: float) -> None:
        self._durations[key] += float(delta)

    @contextmanager
    def timer(self, key: str) -> Iterator[None]:
        start = time.time()
        try:
            yield
        finally:
            self.add_duration(key, time.time() - start)

    # --- Skips / Failures ---
    def skip(self, reason: str, amount: int = 1) -> None:
        self._skips[reason] += amount

    def fail(self, message: str) -> None:
        self._failures.append(message)

    # --- Snapshots ---
    def snapshot(self) -> Dict[str, object]:
        return {
            "stats": dict(self._stats),
            "durations": dict(self._durations),
            "skip_breakdown": self._skip_breakdown(),
            "failures": list(self._failures),
        }

    def _skip_breakdown(self) -> Dict[str, int]:
        data = dict(self._skips)
        data["total"] = sum(self._skips.values())
        return data

