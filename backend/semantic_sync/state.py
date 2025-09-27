"""State persistence helpers for semantic sync."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

from funcy import suppress


LOGGER = logging.getLogger(__name__)

def _resolve_path(path: str | Path) -> Path:
    target = Path(path)
    if not target.is_absolute():
        target = target.resolve()
    return target


def load_state(path: Optional[str]) -> Optional[Dict[str, Any]]:
    """Load stored sync state from ``path`` if it exists and is valid JSON."""
    if not path:
        return None

    state_path = _resolve_path(path)
    with suppress(FileNotFoundError):
        try:
            raw = state_path.read_text(encoding="utf-8")
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            LOGGER.warning("Failed to parse sync state file '%s': %s", state_path, exc)
    return None


def persist_state(path: str, payload: Dict[str, Any]) -> None:
    """Persist ``payload`` to ``path`` atomically."""
    state_path = _resolve_path(path)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = state_path.with_suffix(state_path.suffix + ".tmp")
    tmp_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    tmp_path.replace(state_path)


def remove_state_file(path: Optional[str]) -> None:
    """Delete the stored state file if present."""
    if not path:
        return
    state_path = _resolve_path(path)
    with suppress(FileNotFoundError):
        state_path.unlink()
