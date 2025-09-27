"""
This module contains functions for linearizing Roam Research page data
into a flat text format suitable for semantic chunking.
"""
from typing import Dict, List, Tuple


def linearize_page_markdown_style(page_data: Dict) -> Tuple[str, List[Dict], Dict]:
    """
    Linearize a Roam page into a markdown-style string and track UIDs at a character level.

    This function traverses the hierarchical block structure of a Roam page and flattens it
    into a single text document. It uses markdown headings for the page title and bullet
    points for blocks to preserve structural context.

    It simultaneously generates a character-level map that links every part of the
    linearized text back to its source block UID.

    Args:
        page_data: A dictionary representing a single Roam page, including its children.

    Returns:
        A tuple containing:
        - A single string representing the linearized page content.
        - A list of mapping dictionaries, where each dict is {'start': int, 'end': int, 'uid': str, ...}.
        - A dictionary of metadata (page UID, max edit time, max create time).
    """
    text_parts: List[str] = []
    uid_map: List[Dict] = []
    current_pos = 0
    page_meta = {
        "page_uid": page_data.get(":block/uid"),
        "max_edit_time": None,
        "max_create_time": None,
    }

    def process_block(block: Dict, level: int = 0):
        nonlocal current_pos

        text = block.get(':block/string') or block.get(':node/title', '')
        uid = block.get(':block/uid')
        edit_time = block.get(':edit/time')
        create_time = block.get(':create/time')

        if edit_time is not None:
            if page_meta['max_edit_time'] is None or edit_time > page_meta['max_edit_time']:
                page_meta['max_edit_time'] = edit_time
        if create_time is not None:
            if page_meta['max_create_time'] is None or create_time > page_meta['max_create_time']:
                page_meta['max_create_time'] = create_time

        if not uid:
            # Skip blocks without a UID, as they cannot be referenced.
            return

        if text:
            if level > 0:
                indent = "    " * (level - 1)
                full_line = f"{indent}- {text}"
            else:
                full_line = f"# {text}"

            start_pos = current_pos
            end_pos = start_pos + len(full_line)

            text_parts.append(full_line)
            mapping_entry = {
                'start': start_pos,
                'end': end_pos,
                'uid': uid,
            }

            if edit_time is not None:
                mapping_entry['edit_time'] = edit_time
            if create_time is not None:
                mapping_entry['create_time'] = create_time

            uid_map.append(mapping_entry)

            # Update position for the next line, including the newline character
            current_pos = end_pos + 1

        children = block.get(':block/children', [])
        if children:
            # Sort children by their display order
            sorted_children = sorted(children, key=lambda x: x.get(':block/order', 0))
            for child in sorted_children:
                process_block(child, level + 1)

    process_block(page_data)

    full_text = "\n".join(text_parts)
    return full_text, uid_map, page_meta
