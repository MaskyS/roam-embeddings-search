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

DEFAULT_DB_PATH = os.getenv(
    "SEMANTIC_SYNC_DB",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "semantic_sync.db"),
)

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

