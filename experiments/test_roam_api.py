#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "httpx",
#     "pydantic",
#     "pydantic-settings",
#     "python-dotenv",
#     "chromadb",
#     "fastapi",
#     "uvicorn",
#     "google-generativeai"
# ]
# ///

"""
Test Roam API to document actual response structures.
This will help us understand exactly what data we're working with.
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.roam import query_roam
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    roam_api_token: str = Field(..., env="ROAM_API_TOKEN")
    roam_graph_name: str = Field(..., env="ROAM_GRAPH_NAME")
    google_api_key: str = Field(None, env="GOOGLE_API_KEY")

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"

settings = Settings()

async def pull_many_blocks_local(uids: List[str]) -> List[Optional[Dict]]:
    """Local version of pull_many_blocks for testing"""
    if not uids:
        return []

    import httpx

    url = f"https://api.roamresearch.com/api/graph/{settings.roam_graph_name}/pull-many"
    headers = {
        "X-Authorization": f"Bearer {settings.roam_api_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    # Build eids string for pull-many
    eids_list = " ".join([f'[:block/uid "{uid}"]' for uid in uids])
    eids_str = f"[{eids_list}]"

    # Enhanced selector - recursive to get all nested children
    # {:block/children ...} means recursively get all children
    selector_str = "[:block/uid :block/string :node/title {:block/children ...} {:block/_children [:block/uid :block/string :node/title {:block/children [:block/uid :block/string :block/order]}]}]"

    pull_data = {
        "eids": eids_str,
        "selector": selector_str
    }

    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        try:
            response = await client.post(url, headers=headers, json=pull_data)
            if response.status_code == 200:
                data = response.json()
                return data.get('result', [])
            else:
                print(f"  ✗ Pull-many failed with status {response.status_code}")
                return [None] * len(uids)
        except Exception as e:
            print(f"  ✗ Pull-many error: {e}")
            return [None] * len(uids)

async def test_pull_page():
    """Test pulling a complete page with all children"""
    print("\n" + "="*60)
    print("TEST 1: Pull Complete Page")
    print("="*60)

    # First, find a page to test with
    query = """[:find ?uid ?title
               :where
               [?e :node/title ?title]
               [?e :block/uid ?uid]]"""

    result = await query_roam(
        token=settings.roam_api_token,
        graph_name=settings.roam_graph_name,
        query=query
    )

    if not result or not result.get('result'):
        print("No pages found!")
        return None

    # Get first page
    pages = result['result']
    print(f"Found {len(pages)} pages")

    # Try to find a page with substantial content
    # Let's look for "Roam Research" or similar documentation pages
    test_page_uid = None
    test_page_title = None

    for uid, title in pages:
        # Look for likely documentation/content pages
        if any(keyword in title.lower() for keyword in ['roam', 'research', 'guide', 'how', 'tutorial', 'getting']):
            test_page_uid = uid
            test_page_title = title
            print(f"Found content page: {title}")
            break

    if not test_page_uid:
        # Pick a non-daily-note page if possible
        for uid, title in pages[:10]:  # Check first 10
            if not uid.startswith(('01-', '02-', '03-', '04-', '05-', '06-',
                                  '07-', '08-', '09-', '10-', '11-', '12-')):
                test_page_uid = uid
                test_page_title = title
                break

    if not test_page_uid:
        # Fallback to first page
        test_page_uid, test_page_title = pages[0]

    print(f"\nTesting with page: '{test_page_title}' (uid: {test_page_uid})")

    # Pull the page with full selector
    blocks = await pull_many_blocks_local([test_page_uid])

    if blocks and blocks[0]:
        page_data = blocks[0]

        # Save raw response
        with open('page_response_sample.json', 'w') as f:
            json.dump(page_data, f, indent=2)

        print(f"Page structure saved to page_response_sample.json")

        # Analyze structure
        print("\nPage structure analysis:")
        print(f"  - Has :node/title: {':node/title' in page_data}")
        print(f"  - Has :block/string: {':block/string' in page_data}")
        print(f"  - Number of children: {len(page_data.get(':block/children', []))}")
        print(f"  - Has parent info: {':block/_children' in page_data}")

        return page_data

    return None

async def test_pull_daily_note():
    """Test pulling a daily note page to check for quirks"""
    print("\n" + "="*60)
    print("TEST 2: Pull Daily Note Page")
    print("="*60)

    # Query for daily note pages - they have :log/id attribute
    query = """[:find ?uid
               :where
               [?e :block/uid ?uid]
               [?e :log/id ?log-id]]"""

    result = await query_roam(
        token=settings.roam_api_token,
        graph_name=settings.roam_graph_name,
        query=query
    )

    if not result or not result.get('result'):
        print("No daily notes found!")
        # Try to create a date-based UID
        from datetime import datetime, timedelta
        yesterday = datetime.now() - timedelta(days=1)
        test_uid = yesterday.strftime("%m-%d-%Y")
        print(f"Trying with constructed UID: {test_uid}")
    else:
        daily_notes = result['result']
        print(f"Found {len(daily_notes)} daily notes")
        # Try to find a daily note from 2025 (more likely to have content)
        test_uid = None
        for uid in daily_notes:
            if isinstance(uid, list):
                uid = uid[0]
            if "2025" in uid or "2024" in uid:
                test_uid = uid
                break
        if not test_uid:
            test_uid = daily_notes[0][0] if isinstance(daily_notes[0], list) else daily_notes[0]
        print(f"Testing with: {test_uid}")

    # Pull the daily note
    blocks = await pull_many_blocks_local([test_uid])

    if blocks and blocks[0]:
        dnp_data = blocks[0]

        # Save raw response
        with open('daily_note_response_sample.json', 'w') as f:
            json.dump(dnp_data, f, indent=2)

        print(f"Daily note structure saved to daily_note_response_sample.json")

        # Analyze structure
        print("\nDaily Note Page structure analysis:")
        print(f"  - UID: {dnp_data.get(':block/uid')}")
        print(f"  - Has :node/title: {':node/title' in dnp_data}")
        print(f"  - Has :block/string: {':block/string' in dnp_data}")
        print(f"  - Number of children: {len(dnp_data.get(':block/children', []))}")

        # Check if title exists or is generated
        if ':node/title' in dnp_data:
            print(f"  - Title: {dnp_data[':node/title']}")

        return dnp_data

    return None

async def test_pull_many_batch_sizes():
    """Test pull-many with different batch sizes"""
    print("\n" + "="*60)
    print("TEST 3: Pull-Many Batch Sizes")
    print("="*60)

    # Get a set of block UIDs
    query = """[:find ?uid
               :where
               [?e :block/uid ?uid]
               [?e :block/string ?s]]"""  # Only blocks with content

    result = await query_roam(
        token=settings.roam_api_token,
        graph_name=settings.roam_graph_name,
        query=query
    )

    if not result or not result.get('result'):
        print("No blocks found!")
        return

    all_uids = [uid[0] for uid in result['result']]
    print(f"Found {len(all_uids)} blocks with content")

    # Test different batch sizes
    batch_sizes = [1, 10, 50, 100]

    import time

    for batch_size in batch_sizes:
        if batch_size > len(all_uids):
            continue

        test_uids = all_uids[:batch_size]

        print(f"\nTesting batch size {batch_size}:")
        start_time = time.time()

        blocks = await pull_many_blocks_local(test_uids)

        elapsed = time.time() - start_time

        successful = sum(1 for b in blocks if b is not None)
        print(f"  - Success rate: {successful}/{batch_size}")
        print(f"  - Time: {elapsed:.2f}s")
        print(f"  - Per block: {elapsed/batch_size:.3f}s")

async def test_block_with_references():
    """Test pulling blocks that contain block references"""
    print("\n" + "="*60)
    print("TEST 4: Blocks with References")
    print("="*60)

    # Find blocks with references
    query = """[:find ?uid ?string
               :where
               [?e :block/uid ?uid]
               [?e :block/string ?string]
               [?e :block/refs ?ref]]"""

    result = await query_roam(
        token=settings.roam_api_token,
        graph_name=settings.roam_graph_name,
        query=query
    )

    if not result or not result.get('result'):
        print("No blocks with references found!")
        return None

    blocks_with_refs = result['result']
    print(f"Found {len(blocks_with_refs)} blocks with references")

    # Take first one
    test_uid, test_string = blocks_with_refs[0]
    print(f"\nTesting with block: {test_uid}")
    print(f"Block text: {test_string[:100]}...")

    # Pull with enhanced selector that includes refs
    blocks = await pull_many_blocks_local([test_uid])

    if blocks and blocks[0]:
        block_data = blocks[0]

        # Save raw response
        with open('block_with_refs_sample.json', 'w') as f:
            json.dump(block_data, f, indent=2)

        print(f"Block with refs saved to block_with_refs_sample.json")

        # Analyze references
        refs = block_data.get(':block/refs', [])
        print(f"\nReference analysis:")
        print(f"  - Number of refs: {len(refs)}")

        # Check for block reference pattern
        import re
        block_ref_pattern = r'\(\(([a-zA-Z0-9_-]+)\)\)'
        found_refs = re.findall(block_ref_pattern, test_string)
        print(f"  - Block refs in text: {found_refs}")

        return block_data

    return None

async def main():
    """Run all tests"""
    print("Starting Roam API Tests")
    print("=" * 60)

    # Test 1: Complete page
    page_data = await test_pull_page()

    # Test 2: Daily note
    dnp_data = await test_pull_daily_note()

    # Test 3: Batch sizes
    await test_pull_many_batch_sizes()

    # Test 4: Block references
    ref_data = await test_block_with_references()

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print("\nSample files created:")
    print("  - page_response_sample.json")
    print("  - daily_note_response_sample.json")
    print("  - block_with_refs_sample.json")
    print("\nNext step: Create markdown documentation of findings")

if __name__ == "__main__":
    asyncio.run(main())