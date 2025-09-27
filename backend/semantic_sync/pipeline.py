"""Pure helpers for semantic sync page processing."""

from __future__ import annotations

import json
import hashlib
from typing import Any, Dict, List, Mapping, Optional, Sequence

from funcy import notnone, select_values

from linearize import linearize_page_markdown_style


def deterministic_uuid(namespace, *parts: str) -> str:
    """Generate a stable UUID5 within ``namespace`` from ``parts``."""
    import uuid  # local import to avoid circulars during module load

    name = "::".join(parts)
    return str(uuid.uuid5(namespace, name))


def compute_content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()


def normalize_time(value: Optional[Any]) -> Optional[str]:
    if value is None:
        return None
    try:
        return str(int(value))
    except (ValueError, TypeError):
        return str(value)


def parse_int(value: Optional[str]) -> Optional[int]:
    if value is None:
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def collect_page_snapshot(page_data: Mapping[str, Any]) -> Dict[str, Any]:
    linearized_text, uid_map, page_meta = linearize_page_markdown_style(page_data)
    return {
        "page_uid": page_meta.get("page_uid"),
        "page_title": page_data.get(":node/title") or page_data.get(":block/string") or "Untitled",
        "linearized_text": linearized_text,
        "uid_map": uid_map,
        "meta": page_meta,
        "has_children": bool(page_data.get(":block/children")),
        "raw": page_data,
    }


def decide_sync_action(
    snapshot: Mapping[str, Any],
    existing_state: Mapping[str, Any],
    since_ms: Optional[int] = None,
) -> Dict[str, Any]:
    meta = snapshot.get("meta", {})
    max_edit_time = normalize_time(meta.get("max_edit_time"))
    max_edit_time_int = parse_int(max_edit_time)
    content_hash = compute_content_hash(snapshot.get("linearized_text") or "")

    missing_edit_time = max_edit_time_int is None
    empty_linearized = not (snapshot.get("linearized_text") or "").strip() and snapshot.get("has_children")

    if since_ms is not None and max_edit_time_int is not None:
        if max_edit_time_int <= since_ms:
            return {
                "should_skip": True,
                "reason": "since",
                "since_filtered": True,
                "max_edit_time": max_edit_time,
                "max_edit_time_int": max_edit_time_int,
                "content_hash": content_hash,
                "missing_edit_time": missing_edit_time,
                "empty_linearized": empty_linearized,
            }

    stored_edit_time = existing_state.get("last_synced_edit_time")
    stored_hash = existing_state.get("content_hash")

    if existing_state.get("page_objects") and stored_edit_time == max_edit_time and stored_hash == content_hash:
        return {
            "should_skip": True,
            "reason": "unchanged",
            "since_filtered": False,
            "max_edit_time": max_edit_time,
            "max_edit_time_int": max_edit_time_int,
            "content_hash": content_hash,
            "missing_edit_time": missing_edit_time,
            "empty_linearized": empty_linearized,
        }

    return {
        "should_skip": False,
        "reason": None,
        "since_filtered": False,
        "max_edit_time": max_edit_time,
        "max_edit_time_int": max_edit_time_int,
        "content_hash": content_hash,
        "missing_edit_time": missing_edit_time,
        "empty_linearized": empty_linearized,
    }


def _uids_for_span(uid_map: Sequence[Mapping[str, Any]], start: int, end: int) -> List[str]:
    return list(
        {
            mapping["uid"]
            for mapping in uid_map
            if mapping.get("uid") and start < mapping.get("end", 0) and end > mapping.get("start", 0)
        }
    )


def build_weaviate_objects(
    snapshot: Mapping[str, Any],
    chunk_results: Sequence[Mapping[str, Any]],
    sync_version: str,
    namespace,
) -> Dict[str, Any]:
    page_uid = snapshot.get("page_uid")
    if not page_uid:
        raise ValueError("Page snapshot missing page UID")

    page_title = snapshot.get("page_title") or "Untitled"
    uid_map = snapshot.get("uid_map") or []
    max_edit_time = snapshot.get("meta", {}).get("max_edit_time")
    content_hash = compute_content_hash(snapshot.get("linearized_text") or "")

    chunk_texts: List[str] = [page_title]
    page_properties = select_values(
        notnone,
        {
            "chunk_text_preview": page_title,
            "primary_uid": page_uid,
            "page_title": page_title,
            "page_uid": page_uid,
            "document_type": "page",
            "sync_version": sync_version,
            "last_synced_edit_time": normalize_time(max_edit_time) if max_edit_time is not None else None,
            "content_hash": content_hash,
        },
    )

    objects: List[Dict[str, Any]] = [
        {
            "uuid": deterministic_uuid(namespace, "page", page_uid),
            "properties": page_properties,
        }
    ]

    chunk_objects: List[Dict[str, Any]] = []

    for index, chunk in enumerate(chunk_results):
        text = chunk.get("text", "")
        start = chunk.get("start_index", 0)
        end = chunk.get("end_index", 0)
        token_count = chunk.get("token_count")

        chunk_texts.append(text)
        source_uids = _uids_for_span(uid_map, start, end) or [page_uid]
        non_page_uids = [uid for uid in source_uids if uid != page_uid]
        primary_uid = non_page_uids[0] if non_page_uids else page_uid

        chunk_props = select_values(
            notnone,
            {
                "chunk_text_preview": text,
                "primary_uid": primary_uid,
                "page_title": page_title,
                "page_uid": page_uid,
                "document_type": "chunk",
                "source_uids_json": json.dumps(source_uids),
                "sync_version": sync_version,
                "chunk_token_count": token_count,
                "last_synced_edit_time": normalize_time(max_edit_time) if max_edit_time is not None else None,
                "content_hash": content_hash,
            },
        )

        chunk_objects.append(
            {
                "uuid": deterministic_uuid(namespace, "chunk", page_uid, str(index)),
                "properties": chunk_props,
            }
        )

    objects.extend(chunk_objects)

    return {
        "page_object": objects[0],
        "chunk_objects": chunk_objects,
        "all_objects": objects,
        "chunk_texts": chunk_texts,
        "content_hash": content_hash,
    }
