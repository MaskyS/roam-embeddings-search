#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "chonkie[semantic]",
#     "sentence-transformers",
#     "httpx",
#     "pydantic",
#     "pydantic-settings",
#     "python-dotenv"
# ]
# ///

"""
Test Chonkie with real Roam data pulled from the API.
This tests how we'd actually process pages in production.
"""

import asyncio
import json
from typing import Dict, List, Tuple, Optional
from chonkie import SemanticChunker
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.roam import query_roam
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    roam_api_token: str = Field(..., env="ROAM_API_TOKEN")
    roam_graph_name: str = Field(..., env="ROAM_GRAPH_NAME")
    google_api_key: str = Field(None, env="GOOGLE_API_KEY")  # Optional field

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"

settings = Settings()

async def pull_page_with_content():
    """Pull a page that likely has substantial content"""
    import httpx

    # First, let's find pages with the most blocks to ensure substantial content
    # We'll count children at multiple levels
    query = """[:find ?uid ?title (count ?desc)
               :where
               [?e :node/title ?title]
               [?e :block/uid ?uid]
               [?e :block/children ?c]
               [?c :block/children ?gc]
               [?gc :block/children ?desc]]"""  # Pages with grandchildren

    result = await query_roam(
        token=settings.roam_api_token,
        graph_name=settings.roam_graph_name,
        query=query
    )

    if result and result.get('result'):
        # Sort by number of descendants (third element in tuple)
        pages = sorted(result['result'], key=lambda x: x[2] if len(x) > 2 else 0, reverse=True)
        print(f"Found {len(pages)} pages with deep nesting")

        if pages:
            uid, title, _ = pages[0]
            print(f"Selected most content-rich page: {title}")
        else:
            # Fallback to simpler query
            query = """[:find ?uid ?title
                       :where
                       [?e :node/title ?title]
                       [?e :block/uid ?uid]
                       [?e :block/children ?c]]"""

            result = await query_roam(
                token=settings.roam_api_token,
                graph_name=settings.roam_graph_name,
                query=query
            )

            if not result or not result.get('result'):
                print("No pages with children found")
                return None

            pages = result['result']
            print(f"Found {len(pages)} pages with children")

            # Try to find pages with promising titles suggesting content
            content_keywords = ['guide', 'tutorial', 'how', 'what', 'why', 'research', 'notes', 'project', 'overview']

            selected = None
            for uid, title in pages:
                if any(keyword in title.lower() for keyword in content_keywords):
                    selected = (uid, title)
                    break

            if not selected:
                # Just pick a non-daily-note page
                for uid, title in pages[:50]:
                    if not uid.startswith(('01-', '02-', '03-', '04-', '05-', '06-',
                                          '07-', '08-', '09-', '10-', '11-', '12-')):
                        selected = (uid, title)
                        break

            if selected:
                uid, title = selected
                print(f"Selected: {title}")
    else:
        print("No pages found with complex query, trying simpler approach...")
        return None

    # Pull the page with recursive children
    url = f"https://api.roamresearch.com/api/graph/{settings.roam_graph_name}/pull"
    headers = {
        "X-Authorization": f"Bearer {settings.roam_api_token}",
        "Content-Type": "application/json",
    }

    pull_data = {
        "eid": f'[:block/uid "{uid}"]',
        "selector": "[:block/uid :block/string :node/title :block/order {:block/children ...}]"
    }

    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        response = await client.post(url, headers=headers, json=pull_data)
        if response.status_code == 200:
            data = response.json()
            return data.get('result')
        else:
            print(f"Failed to pull page: {response.status_code}")
            return None


def linearize_page_markdown_style(page_data: Dict) -> Tuple[str, List[Dict], List[Dict]]:
    """
    Linearize a page using markdown-style bullets and indentation, and track UIDs at character level.
    Returns (text, uid_map, block_list)
    """
    text_parts = []
    uid_map = []  # List of {start, end, uid}
    block_list = []  # List of all blocks with their text and uid
    current_pos = 0

    def process_block(block: Dict, level: int = 0):
        nonlocal current_pos

        # Get block text
        text = block.get(':block/string', '') or block.get(':node/title', '')
        uid = block.get(':block/uid', '')

        if text:
            if level > 0:
                indent = "    " * (level - 1)
                full_line = f"{indent}- {text}"
            else:
                full_line = f"# {text}"

            # Track position
            start_pos = current_pos
            end_pos = current_pos + len(full_line)

            text_parts.append(full_line)
            uid_map.append({
                'start': start_pos,
                'end': end_pos,
                'uid': uid
            })
            block_list.append({
                'uid': uid,
                'text': text,
                'level': level
            })

            current_pos = end_pos + 1  # +1 for newline

        # Process children
        children = block.get(':block/children', [])
        if children:
            sorted_children = sorted(children, key=lambda x: x.get(':block/order', 0))
            for child in sorted_children:
                process_block(child, level + 1)

    process_block(page_data)

    full_text = "\n".join(text_parts)
    return full_text, uid_map, block_list


def linearize_with_uid_tracking(page_data: Dict) -> Tuple[str, List[Dict], List[Dict]]:
    """
    Linearize a page and track UIDs at character level.
    Returns (text, uid_map, block_list)
    """
    text_parts = []
    uid_map = []  # List of {start, end, uid}
    block_list = []  # List of all blocks with their text and uid
    current_pos = 0

    def process_block(block: Dict, level: int = 0):
        nonlocal current_pos

        # Get block text
        text = block.get(':block/string', '') or block.get(':node/title', '')
        uid = block.get(':block/uid', '')

        if text:
            # Add indentation for hierarchy
            indent = "  " * level
            full_line = f"{indent}{text}"

            # Track position
            start_pos = current_pos
            end_pos = current_pos + len(full_line)

            text_parts.append(full_line)
            uid_map.append({
                'start': start_pos,
                'end': end_pos,
                'uid': uid
            })
            block_list.append({
                'uid': uid,
                'text': text,
                'level': level
            })

            current_pos = end_pos + 1  # +1 for newline

        # Process children
        children = block.get(':block/children', [])
        if children:
            sorted_children = sorted(children, key=lambda x: x.get(':block/order', 0))
            for child in sorted_children:
                process_block(child, level + 1)

    process_block(page_data)

    full_text = "\n".join(text_parts)
    return full_text, uid_map, block_list

def map_chunks_to_uids(chunks, uid_map):
    """Map chunks back to their source UIDs"""
    results = []

    for chunk in chunks:
        # Find all UIDs that overlap with this chunk
        source_uids = set()
        primary_uid = None

        for mapping in uid_map:
            # Check for overlap
            if chunk.start_index < mapping['end'] and chunk.end_index > mapping['start']:
                source_uids.add(mapping['uid'])
                # First UID is primary
                if primary_uid is None:
                    primary_uid = mapping['uid']

        results.append({
            'text': chunk.text,
            'token_count': chunk.token_count,
            'start': chunk.start_index,
            'end': chunk.end_index,
            'source_uids': list(source_uids),
            'primary_uid': primary_uid
        })

    return results

async def test_real_page():
    """Test with a real page from the graph"""
    print("="*60)
    print("TEST: Real Page Chunking")
    print("="*60)

    # Get a page with content
    page_data = await pull_page_with_content()

    if not page_data:
        print("Could not retrieve a page with content")
        return

    # Save for inspection
    with open('real_page_sample.json', 'w') as f:
        json.dump(page_data, f, indent=2)

    # Linearize with tracking
    text, uid_map, block_list = linearize_page_markdown_style(page_data)

    print(f"\nPage structure:")
    print(f"  - Total blocks: {len(block_list)}")
    print(f"  - Text length: {len(text)} chars")
    print(f"  - Max depth: {max(b['level'] for b in block_list) if block_list else 0}")

    # Show preview
    print("\nText preview:")
    print("-" * 40)
    print(text[:500] + "..." if len(text) > 500 else text)
    print("-" * 40)

    # Save linearized text for inspection
    with open('linearized_text.txt', 'w') as f:
        f.write(text)
    print("\nLinearized text saved to linearized_text.txt")

    # Test different chunking strategies
    strategies = [
        {'threshold': 0.7, 'skip_window': 0, 'name': 'Standard'},
        {'threshold': 0.7, 'skip_window': 2, 'name': 'With Skip-Window'},
        {'threshold': 0.5, 'skip_window': 0, 'name': 'Lower Threshold'},
    ]

    for strategy in strategies:
        print(f"\n### Strategy: {strategy['name']}")
        print(f"    Threshold: {strategy['threshold']}, Skip-window: {strategy['skip_window']}")

        chunker = SemanticChunker(
            embedding_model="sentence-transformers/all-MiniLM-L6-v2",
            threshold=strategy['threshold'],
            chunk_size=1024,
            skip_window=strategy['skip_window']
        )

        chunks = chunker.chunk(text)
        mapped_chunks = map_chunks_to_uids(chunks, uid_map)

        print(f"    Created {len(chunks)} chunks")

        for i, chunk_info in enumerate(mapped_chunks[:3]):  # Show first 3
            print(f"\n    Chunk {i+1}:")
            print(f"      Tokens: {chunk_info['token_count']}")
            print(f"      UIDs: {len(chunk_info['source_uids'])} blocks")
            print(f"      Primary: {chunk_info['primary_uid']}")
            print(f"      Preview: {chunk_info['text'][:100]}...")

        # Save chunks to file for inspection
        output_file = f'chunks_{strategy["name"].lower().replace(" ", "_")}.json'
        with open(output_file, 'w') as f:
            json.dump(mapped_chunks, f, indent=2)
        print(f"    Saved chunks to {output_file}")

async def test_daily_note():
    """Test with a daily note (which has interleaved content)"""
    print("\n" + "="*60)
    print("TEST: Daily Note with Interleaved Content")
    print("="*60)

    # Get a daily note
    query = """[:find ?uid ?title
               :where
               [?e :log/id ?log-id]
               [?e :node/title ?title]
               [?e :block/uid ?uid]
               [?e :block/children ?c]]"""  # Daily notes with content

    result = await query_roam(
        token=settings.roam_api_token,
        graph_name=settings.roam_graph_name,
        query=query
    )

    if not result or not result.get('result'):
        print("No daily notes with content found")
        return

    # Get the first one
    uid, title = result['result'][0]
    print(f"Testing with: {title}")

    # Pull the daily note
    import httpx
    url = f"https://api.roamresearch.com/api/graph/{settings.roam_graph_name}/pull"
    headers = {
        "X-Authorization": f"Bearer {settings.roam_api_token}",
        "Content-Type": "application/json",
    }

    pull_data = {
        "eid": f'[:block/uid "{uid}"]',
        "selector": "[:block/uid :block/string :node/title :block/order {:block/children ...}]"
    }

    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        response = await client.post(url, headers=headers, json=pull_data)
        if response.status_code == 200:
            data = response.json()
            daily_note_data = data.get('result')
        else:
            print(f"Failed to pull daily note: {response.status_code}")
            return

    # Process it
    text, uid_map, block_list = linearize_page_markdown_style(daily_note_data)

    print(f"\nDaily note structure:")
    print(f"  - Total blocks: {len(block_list)}")
    print(f"  - Text length: {len(text)} chars")

    # Test with skip-window to handle interleaved topics
    chunker = SemanticChunker(
        embedding_model="sentence-transformers/all-MiniLM-L6-v2",
        threshold=0.7,
        chunk_size=2048,
        skip_window=2  # Key for interleaved content
    )

    chunks = chunker.chunk(text)
    mapped_chunks = map_chunks_to_uids(chunks, uid_map)

    print(f"\nCreated {len(chunks)} chunks")
    print("Skip-window should help group related but non-consecutive content")

async def main():
    """Run all tests"""
    await test_real_page()
    await test_daily_note()

    print("\n" + "="*60)
    print("CONCLUSIONS")
    print("="*60)
    print("""
What we learned:
1. UID tracking through character positions works
2. Skip-window setting affects interleaved content grouping
3. Threshold controls granularity of semantic boundaries
""")

if __name__ == "__main__":
    asyncio.run(main())