"""Domain helpers and linearization for semantic sync.

Contains pure functions for:
- Linearizing page data into text + UID maps
- Computing content hashes and stable UUIDs
- Building Weaviate object payloads from snapshots + chunks

No network or IO here; safe to unit test.
"""

from __future__ import annotations

import json
import hashlib
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from funcy import notnone, select_values

from .models import PageSnapshot, SyncMetadata, WeaviateObjectSet


def linearize_page_markdown_style(page_data: Dict) -> Tuple[str, List[Dict], Dict]:
    """Linearize a Roam page into a markdown-style string and track UIDs at a character level."""
    text_parts: List[str] = []
    uid_map: List[Dict] = []
    current_pos = 0
    page_meta = {
        "page_uid": page_data.get(":block/uid"),
        "max_edit_time": None,
        "max_block_edit_time": None,
        "max_create_time": None,
    }

    def process_block(block: Dict, level: int = 0):
        nonlocal current_pos

        text = block.get(":block/string") or block.get(":node/title", "")
        uid = block.get(":block/uid")
        edit_time = block.get(":edit/time")
        create_time = block.get(":create/time")

        if edit_time is not None:
            if page_meta["max_edit_time"] is None or edit_time > page_meta["max_edit_time"]:
                page_meta["max_edit_time"] = edit_time
                page_meta["max_block_edit_time"] = edit_time
        if create_time is not None:
            if page_meta["max_create_time"] is None or create_time > page_meta["max_create_time"]:
                page_meta["max_create_time"] = create_time

        if not uid:
            return

        stripped = text.strip() if text else ""
        if stripped:
            if level > 0:
                indent = "    " * (level - 1)
                full_line = f"{indent}- {stripped}"
            else:
                full_line = f"[[{stripped}]]"

            start_pos = current_pos
            end_pos = start_pos + len(full_line)

            text_parts.append(full_line)
            mapping_entry = {
                "start": start_pos,
                "end": end_pos,
                "uid": uid,
            }

            if edit_time is not None:
                mapping_entry["edit_time"] = edit_time
            if create_time is not None:
                mapping_entry["create_time"] = create_time

            uid_map.append(mapping_entry)

            current_pos = end_pos + 1

        children = block.get(":block/children", [])
        if children:
            sorted_children = sorted(children, key=lambda x: x.get(":block/order", 0))
            for child in sorted_children:
                process_block(child, level + 1)

    process_block(page_data)

    full_text = "\n".join(text_parts)
    return full_text, uid_map, page_meta


def deterministic_uuid(namespace, *parts: str) -> str:
    import uuid
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


def _normalise_title(value: str) -> str:
    cleaned = (value or "").strip()
    if cleaned.startswith("[[") and cleaned.endswith("]]"):
        cleaned = cleaned[2:-2]
    cleaned = cleaned.strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.lower()


def _is_page_only_chunk(text: str, page_title: str, primary_uid: str, source_uids, page_uid: str) -> bool:
    if primary_uid != page_uid:
        return False
    if any(uid != page_uid for uid in source_uids):
        return False
    chunk_clean = _normalise_title(text)
    page_clean = _normalise_title(page_title)
    return bool(chunk_clean) and chunk_clean == page_clean


def collect_page_snapshot(page_data: Mapping[str, Any]) -> PageSnapshot:
    """Convert raw Roam page data into an immutable PageSnapshot."""
    linearized_text, uid_map, page_meta_dict = linearize_page_markdown_style(page_data)

    metadata = SyncMetadata(
        page_uid=page_meta_dict.get("page_uid", ""),
        max_edit_time=page_meta_dict.get("max_edit_time"),
        max_block_edit_time=page_meta_dict.get("max_block_edit_time"),
        max_create_time=page_meta_dict.get("max_create_time"),
    )

    return PageSnapshot(
        page_uid=metadata.page_uid,
        page_title=page_data.get(":node/title") or page_data.get(":block/string") or "Untitled",
        linearized_text=linearized_text,
        uid_map=uid_map,
        meta=metadata,
        has_children=bool(page_data.get(":block/children")),
    )


def _uids_for_span(uid_map: Sequence[Mapping[str, Any]], start: int, end: int) -> List[str]:
    return list(
        {
            mapping["uid"]
            for mapping in uid_map
            if mapping.get("uid") and start < mapping.get("end", 0) and end > mapping.get("start", 0)
        }
    )


def build_weaviate_objects(
    snapshot: PageSnapshot,
    chunk_results: Sequence[Mapping[str, Any]],
    sync_version: str,
    namespace,
) -> WeaviateObjectSet:
    if not snapshot.page_uid:
        raise ValueError("Page snapshot missing page UID")

    content_hash = compute_content_hash(snapshot.linearized_text or "")
    max_edit_time = snapshot.meta.max_edit_time

    chunk_texts: List[str] = [snapshot.page_title]
    page_properties = select_values(
        notnone,
        {
            "chunk_text_preview": snapshot.page_title,
            "primary_uid": snapshot.page_uid,
            "page_title": snapshot.page_title,
            "page_uid": snapshot.page_uid,
            "document_type": "page",
            "sync_version": sync_version,
            "last_synced_edit_time": normalize_time(max_edit_time) if max_edit_time is not None else None,
            "content_hash": content_hash,
        },
    )

    objects: List[Dict[str, Any]] = [
        {
            "uuid": deterministic_uuid(namespace, "page", snapshot.page_uid),
            "properties": page_properties,
        }
    ]

    chunk_objects: List[Dict[str, Any]] = []

    for index, chunk in enumerate(chunk_results):
        text = chunk.get("text", "")
        start = chunk.get("start_index", 0)
        end = chunk.get("end_index", 0)
        token_count = chunk.get("token_count")

        source_uids = _uids_for_span(snapshot.uid_map, start, end) or [snapshot.page_uid]
        non_page_uids = [uid for uid in source_uids if uid != snapshot.page_uid]
        primary_uid = non_page_uids[0] if non_page_uids else snapshot.page_uid

        if _is_page_only_chunk(text, snapshot.page_title, primary_uid, source_uids, snapshot.page_uid):
            continue

        chunk_texts.append(text)

        chunk_props = select_values(
            notnone,
            {
                "chunk_text_preview": text,
                "primary_uid": primary_uid,
                "page_title": snapshot.page_title,
                "page_uid": snapshot.page_uid,
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
                "uuid": deterministic_uuid(namespace, "chunk", snapshot.page_uid, str(index)),
                "properties": chunk_props,
            }
        )

    objects.extend(chunk_objects)

    return WeaviateObjectSet(
        page_object=objects[0],
        chunk_objects=chunk_objects,
        all_objects=objects,
        chunk_texts=chunk_texts,
        content_hash=content_hash,
    )

