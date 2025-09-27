"""SQLite-backed persistence for semantic sync runs."""

from __future__ import annotations

import json
import os
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Iterable, Optional


DEFAULT_DB_PATH = os.getenv(
    "SEMANTIC_SYNC_DB",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "semantic_sync.db"),
)


@contextmanager
def db_cursor(path: str = DEFAULT_DB_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn.cursor()
        conn.commit()
    finally:
        conn.close()


def initialise(path: str = DEFAULT_DB_PATH) -> None:
    with db_cursor(path) as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS page_state (
                page_uid TEXT PRIMARY KEY,
                last_synced_edit_time INTEGER,
                content_hash TEXT,
                updated_at TEXT
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS sync_runs (
                run_id TEXT PRIMARY KEY,
                status TEXT,
                started_at TEXT,
                finished_at TEXT,
                since INTEGER,
                test_limit INTEGER,
                notes TEXT
            )
            """
        )


def load_page_state(uids: Iterable[str], path: str = DEFAULT_DB_PATH) -> Dict[str, Dict[str, Optional[str]]]:
    placeholders = ",".join("?" for _ in uids)
    if not placeholders:
        return {}
    with db_cursor(path) as cur:
        cur.execute(
            f"SELECT page_uid, last_synced_edit_time, content_hash FROM page_state WHERE page_uid IN ({placeholders})",
            list(uids),
        )
        return {
            row["page_uid"]: {
                "last_synced_edit_time": row["last_synced_edit_time"],
                "content_hash": row["content_hash"],
            }
            for row in cur.fetchall()
        }


def upsert_page_state(records: Dict[str, Dict[str, Optional[str]]], path: str = DEFAULT_DB_PATH) -> None:
    timestamp = datetime.utcnow().isoformat() + "Z"
    with db_cursor(path) as cur:
        for uid, data in records.items():
            cur.execute(
                """
                INSERT INTO page_state (page_uid, last_synced_edit_time, content_hash, updated_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(page_uid) DO UPDATE SET
                    last_synced_edit_time=excluded.last_synced_edit_time,
                    content_hash=excluded.content_hash,
                    updated_at=excluded.updated_at
                """,
                (uid, data.get("last_synced_edit_time"), data.get("content_hash"), timestamp),
            )


def record_run(run_id: str, status: str, *, since: Optional[int], test_limit: Optional[int], notes: Optional[Dict[str, any]] = None, path: str = DEFAULT_DB_PATH) -> None:
    with db_cursor(path) as cur:
        cur.execute(
            """
            INSERT INTO sync_runs (run_id, status, started_at, finished_at, since, test_limit, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(run_id) DO UPDATE SET
                status=excluded.status,
                finished_at=excluded.finished_at,
                notes=excluded.notes
            """,
            (
                run_id,
                status,
                datetime.utcnow().isoformat() + "Z",
                datetime.utcnow().isoformat() + "Z",
                since,
                test_limit,
                json.dumps(notes or {}),
            ),
        )

