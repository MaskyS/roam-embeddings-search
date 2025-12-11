"""
SQLite-backed persistence for semantic sync state.

Manages incremental sync state by tracking page sync status and run history.
Default location: data/semantic_sync.db
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    create_engine,
    delete,
    select,
)
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.engine import Engine

# Determine project root: go up from sync/state/ to backend/,
# then use data/ subdirectory
_this_file = os.path.abspath(__file__)
# backend/sync/state -> backend
_backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(_this_file)))
_default_db_path = os.path.join(_backend_dir, "data", "semantic_sync.db")

DEFAULT_DB_PATH = os.getenv("SEMANTIC_SYNC_DB", _default_db_path)

_metadata = MetaData()

page_state_table = Table(
    "page_state",
    _metadata,
    Column("page_uid", String, primary_key=True),
    Column("last_synced_edit_time", Integer),
    Column("content_hash", String),
    Column("updated_at", String),
)

sync_runs_table = Table(
    "sync_runs",
    _metadata,
    Column("run_id", String, primary_key=True),
    Column("status", String),
    Column("started_at", String),
    Column("finished_at", String),
    Column("since", Integer),
    Column("test_limit", Integer),
    Column("notes", Text),
)

scheduler_config_table = Table(
    "scheduler_config",
    _metadata,
    Column("id", Integer, primary_key=True, default=1),
    Column("enabled", Integer, default=0),  # SQLite uses 0/1 for boolean
    Column("schedule_time", String, default="02:00"),  # HH:MM format
    Column("timezone", String, default="UTC"),  # IANA timezone
    Column("last_auto_run", String),  # ISO timestamp
    Column("last_auto_status", String),  # success, failed, etc.
    Column("updated_at", String),
)

_engine_cache: Dict[str, Engine] = {}


def _normalise_path(path: str) -> str:
    return str(Path(path).resolve())


def _get_engine(path: str = DEFAULT_DB_PATH) -> Engine:
    normalised = _normalise_path(path)
    engine = _engine_cache.get(normalised)
    if engine is None:
        os.makedirs(Path(normalised).parent, exist_ok=True)
        engine = create_engine(f"sqlite:///{normalised}", future=True)
        _engine_cache[normalised] = engine
    return engine


def initialise(path: str = DEFAULT_DB_PATH) -> None:
    engine = _get_engine(path)
    _metadata.create_all(engine)


def load_page_state(uids: Iterable[str], path: str = DEFAULT_DB_PATH) -> Dict[str, Dict[str, Optional[str]]]:
    tokens = list(uids)
    if not tokens:
        return {}
    engine = _get_engine(path)
    stmt = select(
        page_state_table.c.page_uid,
        page_state_table.c.last_synced_edit_time,
        page_state_table.c.content_hash,
    ).where(page_state_table.c.page_uid.in_(tokens))
    with engine.connect() as conn:
        rows = conn.execute(stmt).fetchall()
    return {
        row.page_uid: {
            "last_synced_edit_time": row.last_synced_edit_time,
            "content_hash": row.content_hash,
        }
        for row in rows
    }


def upsert_page_state(records: Dict[str, Dict[str, Optional[str]]], path: str = DEFAULT_DB_PATH) -> None:
    if not records:
        return
    engine = _get_engine(path)
    timestamp = datetime.utcnow().isoformat() + "Z"
    payload = []
    for uid, data in records.items():
        payload.append(
            {
                "page_uid": uid,
                "last_synced_edit_time": data.get("last_synced_edit_time"),
                "content_hash": data.get("content_hash"),
                "updated_at": timestamp,
            }
        )
    stmt = insert(page_state_table).values(payload)
    stmt = stmt.on_conflict_do_update(
        index_elements=[page_state_table.c.page_uid],
        set_={
            "last_synced_edit_time": stmt.excluded.last_synced_edit_time,
            "content_hash": stmt.excluded.content_hash,
            "updated_at": stmt.excluded.updated_at,
        },
    )
    with engine.begin() as conn:
        conn.execute(stmt)


def record_run(
    run_id: str,
    status: str,
    *,
    since: Optional[int],
    test_limit: Optional[int],
    notes: Optional[Dict[str, Any]] = None,
    path: str = DEFAULT_DB_PATH,
) -> None:
    engine = _get_engine(path)
    now = datetime.utcnow().isoformat() + "Z"
    payload = {
        "run_id": run_id,
        "status": status,
        "started_at": now,
        "finished_at": now,
        "since": since,
        "test_limit": test_limit,
        "notes": json.dumps(notes or {}),
    }
    stmt = insert(sync_runs_table).values(payload)
    stmt = stmt.on_conflict_do_update(
        index_elements=[sync_runs_table.c.run_id],
        set_={
            "status": stmt.excluded.status,
            "finished_at": stmt.excluded.finished_at,
            "notes": stmt.excluded.notes,
        },
    )
    with engine.begin() as conn:
        conn.execute(stmt)


def delete_page_state(uids: Optional[Iterable[str]] = None, path: str = DEFAULT_DB_PATH) -> None:
    engine = _get_engine(path)
    with engine.begin() as conn:
        if uids is None:
            conn.execute(delete(page_state_table))
        else:
            tokens = list(uids)
            if not tokens:
                return
            conn.execute(delete(page_state_table).where(page_state_table.c.page_uid.in_(tokens)))


def list_page_state_uids(path: str = DEFAULT_DB_PATH) -> List[str]:
    engine = _get_engine(path)
    stmt = select(page_state_table.c.page_uid)
    with engine.connect() as conn:
        rows = conn.execute(stmt).fetchall()
    return [row.page_uid for row in rows]


def list_recent_runs(limit: int = 10, path: str = DEFAULT_DB_PATH) -> List[Dict[str, Any]]:
    engine = _get_engine(path)
    stmt = (
        select(sync_runs_table)
        .order_by(sync_runs_table.c.started_at.desc())
        .limit(limit)
    )
    with engine.connect() as conn:
        rows = conn.execute(stmt).fetchall()
    output: List[Dict[str, Any]] = []
    for row in rows:
        output.append(
            {
                "run_id": row.run_id,
                "status": row.status,
                "started_at": row.started_at,
                "finished_at": row.finished_at,
                "since": row.since,
                "test_limit": row.test_limit,
                "notes": json.loads(row.notes or "{}"),
            }
        )
    return output


def get_scheduler_config(path: str = DEFAULT_DB_PATH) -> Dict[str, Any]:
    """Get scheduler configuration. Returns default config if not found."""
    engine = _get_engine(path)
    stmt = select(scheduler_config_table).where(scheduler_config_table.c.id == 1)
    with engine.connect() as conn:
        row = conn.execute(stmt).fetchone()

    if row is None:
        # Return default config
        return {
            "enabled": False,
            "schedule_time": "02:00",
            "timezone": "UTC",
            "last_auto_run": None,
            "last_auto_status": None,
        }

    return {
        "enabled": bool(row.enabled),
        "schedule_time": row.schedule_time,
        "timezone": row.timezone,
        "last_auto_run": row.last_auto_run,
        "last_auto_status": row.last_auto_status,
    }


def update_scheduler_config(
    enabled: Optional[bool] = None,
    schedule_time: Optional[str] = None,
    timezone: Optional[str] = None,
    last_auto_run: Optional[str] = None,
    last_auto_status: Optional[str] = None,
    path: str = DEFAULT_DB_PATH,
) -> Dict[str, Any]:
    """Update scheduler configuration. Creates if doesn't exist."""
    engine = _get_engine(path)
    timestamp = datetime.utcnow().isoformat() + "Z"

    # Build update dict from provided values
    update_data = {"id": 1, "updated_at": timestamp}
    if enabled is not None:
        update_data["enabled"] = 1 if enabled else 0
    if schedule_time is not None:
        update_data["schedule_time"] = schedule_time
    if timezone is not None:
        update_data["timezone"] = timezone
    if last_auto_run is not None:
        update_data["last_auto_run"] = last_auto_run
    if last_auto_status is not None:
        update_data["last_auto_status"] = last_auto_status

    stmt = insert(scheduler_config_table).values(update_data)
    stmt = stmt.on_conflict_do_update(
        index_elements=[scheduler_config_table.c.id],
        set_={k: v for k, v in update_data.items() if k != "id"},
    )

    with engine.begin() as conn:
        conn.execute(stmt)

    return get_scheduler_config(path)
