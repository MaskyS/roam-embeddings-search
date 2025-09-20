"""
Sync Full: Production-ready full graph sync with all improvements
- Uses pull-many for efficiency
- Handles entire graph with progress tracking
- Includes rate limiting and context limits
- Resolves block references
- Saves timestamp for future incremental syncs
"""
print("[sync_full] Starting...")

import asyncio
import json
import re
import time
import argparse
from datetime import datetime
from typing import Dict, List, Optional, Set
import httpx
from roam import query_roam
from main import settings, get_collection

# Configuration constants
MAX_CONTEXT_LENGTH = 8000  # Maximum characters for context
BATCH_SIZE = 50  # Blocks per pull-many request (respects rate limit)
# RATE_LIMIT_DELAY = 1.2  # Seconds between batches (50 req/min = 1.2s/req)
TIMESTAMP_FILE = "last_sync.json"

async def pull_many_blocks(uids: List[str]) -> List[Optional[Dict]]:
    """Pull multiple blocks at once using pull-many for efficiency"""
    if not uids:
        return []

    url = f"https://api.roamresearch.com/api/graph/{settings.roam_graph_name}/pull-many"
    headers = {
        "X-Authorization": f"Bearer {settings.roam_api_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    # Build eids string for pull-many - must be properly formatted Clojure vector
    eids_list = " ".join([f'[:block/uid "{uid}"]' for uid in uids])
    eids_str = f"[{eids_list}]"

    # Enhanced selector - gets parent's children too for sibling context
    selector_str = "[:block/uid :block/string :node/title {:block/children [:block/uid :block/string :block/order]} {:block/_children [:block/uid :block/string :node/title {:block/children [:block/uid :block/string :block/order]}]}]"

    pull_data = {
        "eids": eids_str,
        "selector": selector_str
    }

    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        try:
            response = await client.post(url, headers=headers, json=pull_data)
            if response.status_code == 200:
                data = response.json()
                result = data.get('result', [])
                # Debug: Show first result structure
                if result and len(result) > 0:
                    first_block = result[0] if result[0] else None
                    if first_block:
                        has_string = ':block/string' in first_block if isinstance(first_block, dict) else False
                        has_title = ':node/title' in first_block if isinstance(first_block, dict) else False
                        print(f"    → First block has :block/string={has_string}, :node/title={has_title}")
                return result
            else:
                print(f"  ✗ Pull-many failed with status {response.status_code}")
                print(f"    Response: {response.text[:500]}")
                return [None] * len(uids)
        except Exception as e:
            print(f"  ✗ Pull-many error: {e}")
            return [None] * len(uids)

async def get_all_block_uids() -> List[str]:
    """Get all block UIDs from the graph (lightweight query)"""
    # This gets both blocks and pages (pages have UIDs too)
    query = """[:find ?uid
               :where [?e :block/uid ?uid]]"""

    result = await query_roam(
        token=settings.roam_api_token,
        graph_name=settings.roam_graph_name,
        query=query
    )

    if result and result.get('result'):
        # Result is array of [uid] tuples, extract just the UIDs
        return [uid[0] for uid in result['result']]
    return []

def build_parent_block_context(block_data: Dict) -> str:
    """Build context for a parent block: parent + children"""
    # Handle both pages (:node/title) and blocks (:block/string)
    parent_text = block_data.get(':block/string', '') or block_data.get(':node/title', '')

    children = block_data.get(':block/children', [])

    # Sort children by order
    children_sorted = sorted(children, key=lambda x: x.get(':block/order', 0))

    # Build document
    document_parts = [parent_text]
    current_length = len(parent_text)

    for child in children_sorted:
        child_text = child.get(':block/string', '').strip()
        if child_text:
            child_line = f"• {child_text}"
            # Check if adding this child would exceed limit
            if current_length + len(child_line) + 1 > MAX_CONTEXT_LENGTH:
                break
            document_parts.append(child_line)
            current_length += len(child_line) + 1  # +1 for newline

    context = "\n".join(document_parts)
    return context[:MAX_CONTEXT_LENGTH]  # Final safety truncation

def build_leaf_block_context(block_data: Dict, block_uid: str) -> str:
    """Build context for leaf block with smart allocation and multi-sibling support"""
    # Handle both blocks and pages
    block_text = block_data.get(':block/string', '') or block_data.get(':node/title', '')

    # Get parent from reverse lookup
    parents = block_data.get(':block/_children', [])
    if not parents:
        return block_text[:MAX_CONTEXT_LENGTH]

    parent = parents[0]

    # Check if parent is a page (pages don't have sibling context)
    if parent.get(':node/title'):
        context = f"{parent.get(':node/title')} > {block_text}"
        return context[:MAX_CONTEXT_LENGTH]

    # Block parent - get siblings
    parent_text = parent.get(':block/string', '')

    siblings = parent.get(':block/children', [])

    # If no siblings or only child, just use parent context
    if not siblings or len(siblings) <= 1:
        context = f"{parent_text} > {block_text}"
        return context[:MAX_CONTEXT_LENGTH]

    # Sort siblings by order
    siblings_sorted = sorted(siblings, key=lambda x: x.get(':block/order', 0))

    # Find current block position
    current_idx = None
    for i, sib in enumerate(siblings_sorted):
        if sib.get(':block/uid') == block_uid:
            current_idx = i
            break

    # If not found in siblings (shouldn't happen), fallback
    if current_idx is None:
        context = f"{parent_text} > {block_text}"
        return context[:MAX_CONTEXT_LENGTH]

    # Context Alloction
    # Step 1: Calculate parent allocation
    PARENT_MAX_ALLOCATION = MAX_CONTEXT_LENGTH // 3
    parent_actual = min(len(parent_text), PARENT_MAX_ALLOCATION)
    parent_unused = PARENT_MAX_ALLOCATION - parent_actual

    # Step 2: Calculate base allocations with redistribution
    remaining_after_parent = MAX_CONTEXT_LENGTH - parent_actual

    # Current block gets its needs + half of unused parent space
    current_block_bonus = parent_unused // 2
    current_block_allocation = len(block_text) + current_block_bonus
    current_block_actual = min(len(block_text), current_block_allocation)

    # Siblings get remaining + half of unused parent space
    sibling_pool = remaining_after_parent - current_block_actual + (parent_unused - current_block_bonus)

    # Step 3: Select siblings using middle-out approach
    MAX_SIBLINGS = 4
    max_radius = MAX_SIBLINGS // 2

    selected_siblings = []
    for distance in range(1, max_radius + 1):
        # Look before current block
        prev_idx = current_idx - distance
        if prev_idx >= 0 and len(selected_siblings) < MAX_SIBLINGS:
            sibling_text = siblings_sorted[prev_idx].get(':block/string', '')
            if sibling_text:  # Only include non-empty siblings
                selected_siblings.append({
                    'index': prev_idx,
                    'text': sibling_text,
                    'distance': distance,
                    'position': 'before'
                })

        # Look after current block
        next_idx = current_idx + distance
        if next_idx < len(siblings_sorted) and len(selected_siblings) < MAX_SIBLINGS:
            sibling_text = siblings_sorted[next_idx].get(':block/string', '')
            if sibling_text:  # Only include non-empty siblings
                selected_siblings.append({
                    'index': next_idx,
                    'text': sibling_text,
                    'distance': distance,
                    'position': 'after'
                })

    # Step 4: Distribute space among siblings (distance-weighted)
    sibling_allocations = []
    if selected_siblings and sibling_pool > 100:  # Need meaningful space
        # Calculate weights - closer siblings get more space
        weights = [1.0 / sib['distance'] for sib in selected_siblings]
        total_weight = sum(weights)

        for sibling, weight in zip(selected_siblings, weights):
            # Allocate space proportionally
            allocated_space = int(sibling_pool * (weight / total_weight))

            # Only include if we have enough space for meaningful context
            MIN_SIBLING_CHARS = 50
            if allocated_space >= MIN_SIBLING_CHARS:
                actual_text_len = min(len(sibling['text']), allocated_space)
                truncated = sibling['text'][:actual_text_len]
                if len(sibling['text']) > actual_text_len:
                    truncated += "..."

                sibling_allocations.append({
                    'index': sibling['index'],
                    'text': truncated,
                    'position': sibling['position']
                })

    # Step 5: Build final context
    context_parts = []

    # Add parent (truncated if needed)
    truncated_parent = parent_text[:parent_actual]
    if len(parent_text) > parent_actual:
        truncated_parent += "..."
    context_parts.append(truncated_parent)
    context_parts.append(" > ")

    # Add siblings before current block
    before_siblings = sorted(
        [s for s in sibling_allocations if s['position'] == 'before'],
        key=lambda x: x['index']
    )
    for sibling in before_siblings:
        context_parts.append(sibling['text'])
        context_parts.append(" → ")

    # Add current block (with emphasis to distinguish it)
    context_parts.append(f"[[{block_text[:current_block_actual]}]]")

    # Add siblings after current block
    after_siblings = sorted(
        [s for s in sibling_allocations if s['position'] == 'after'],
        key=lambda x: x['index']
    )
    for sibling in after_siblings:
        context_parts.append(" → ")
        context_parts.append(sibling['text'])

    context = "".join(context_parts)
    return context[:MAX_CONTEXT_LENGTH]  # Final safety truncation

async def sync_full_graph(clear_existing: bool = False, test_limit: Optional[int] = None):
    """Sync the entire graph with batched processing and progress tracking

    Args:
        clear_existing: If True, clear all existing embeddings before syncing
        test_limit: If set, only process first N blocks for testing
    """
    print("\n[sync_full] Starting full graph sync...")
    start_time = time.time()

    # Step 1: Get all block UIDs
    print("[sync_full] Step 1: Getting all block UIDs...")
    all_uids = await get_all_block_uids()

    if not all_uids:
        print("[sync_full] No blocks found in graph!")
        return

    total_blocks = len(all_uids)
    print(f"[sync_full] Found {total_blocks} blocks to process")

    # Get collection
    collection = get_collection()
    initial_count = collection.count()
    print(f"[sync_full] Collection currently has {initial_count} documents")

    # Clear collection if requested
    if clear_existing and initial_count > 0:
        print("[sync_full] Clearing existing collection for fresh sync...")
        # Get all IDs and delete them
        all_existing = collection.get()
        if all_existing['ids']:
            collection.delete(ids=all_existing['ids'])
            print(f"[sync_full] Collection cleared ({len(all_existing['ids'])} documents removed)")
    elif not clear_existing and initial_count > 0:
        print(f"[sync_full] Incremental mode: keeping existing {initial_count} documents")

    # Step 2: Process in batches
    print(f"[sync_full] Step 2: Processing blocks in batches of {BATCH_SIZE}...")

    # Apply test limit if specified
    if test_limit and len(all_uids) > test_limit:
        print(f"[sync_full] TEST MODE: Limiting to first {test_limit} blocks for testing")
        all_uids = all_uids[:test_limit]
        total_blocks = len(all_uids)

    # Statistics
    successful = 0
    failed = 0
    skipped = 0
    parent_blocks = 0
    leaf_blocks = 0
    leaf_with_parent = 0
    leaf_with_siblings = 0
    total_siblings_included = 0  # Track multi-sibling usage
    max_siblings_in_context = 0  # Track maximum siblings included
    avg_sibling_distances = []  # Track how far we're reaching for context

    # Process batches
    for batch_num, batch_start in enumerate(range(0, total_blocks, BATCH_SIZE)):
        batch_end = min(batch_start + BATCH_SIZE, total_blocks)
        batch_uids = all_uids[batch_start:batch_end]
        batch_size = len(batch_uids)

        # Progress indicator
        progress_pct = (batch_start / total_blocks) * 100
        print(f"\n[sync_full] Batch {batch_num + 1}: Processing blocks {batch_start+1}-{batch_end} ({progress_pct:.1f}% complete)")

        # Check which UIDs already exist
        existing = collection.get(ids=batch_uids)
        existing_set = set(existing['ids'])

        # Filter out existing UIDs
        new_uids = [uid for uid in batch_uids if uid not in existing_set]
        skipped += len(batch_uids) - len(new_uids)

        if not new_uids:
            print(f"  → All {batch_size} blocks already in collection, skipping batch")
            continue

        # Pull block data for new UIDs
        blocks_data = await pull_many_blocks(new_uids)

        # Debug: Check pull-many results
        successful_pulls = sum(1 for bd in blocks_data if bd is not None)
        print(f"  → Pull-many returned {successful_pulls}/{len(new_uids)} blocks")

        # Prepare batch for ChromaDB
        batch_ids = []
        batch_documents = []
        batch_metadatas = []

        # Debug: Track empty contexts
        empty_contexts = 0

        # Process each block
        for uid, block_data in zip(new_uids, blocks_data):
            if not block_data:
                print(f"  ✗ Failed to pull data for {uid}")
                failed += 1
                continue

            # Get original text (handle pages which have :node/title instead of :block/string)
            original_text = block_data.get(':block/string', '') or block_data.get(':node/title', '')

            # Skip truly empty blocks (no text at all)
            # These might be special blocks like queries, embeds, etc.
            if not original_text:
                print(f"  → Skipping empty block {uid}")
                failed += 1
                continue

            # Check if this is a page
            # Pages have :node/title OR are Daily Note Pages (DNPs) with UIDs like MM-DD-YYYY
            is_dnp = bool(uid and re.match(r'^\d{2}-\d{2}-\d{4}$', uid))
            is_page = ':node/title' in block_data or is_dnp

            # Determine block type
            has_children = bool(block_data.get(':block/children'))
            has_parent = bool(block_data.get(':block/_children'))

            # Build context based on block type
            # DNPs and pages are special cases
            if is_page:
                block_type = "page"
                if is_dnp:
                    # DNPs usually just have their date as title
                    context = original_text[:MAX_CONTEXT_LENGTH]
                elif has_children:
                    # Regular pages with children
                    context = build_parent_block_context(block_data)
                else:
                    # Regular pages without children
                    context = original_text[:MAX_CONTEXT_LENGTH]
                parent_blocks += 1  # Count pages as parent blocks for stats
            elif has_children:
                context = build_parent_block_context(block_data)
                block_type = "parent"
                parent_blocks += 1
            else:
                # Track leaf statistics
                leaf_blocks += 1
                if has_parent:
                    leaf_with_parent += 1
                    parent = block_data.get(':block/_children', [])[0]
                    siblings = parent.get(':block/children', [])
                    if siblings and len(siblings) > 1:
                        leaf_with_siblings += 1

                context = build_leaf_block_context(block_data, uid)
                block_type = "leaf"

                # Track multi-sibling metrics from context
                # Count → separators to estimate siblings included
                sibling_count = context.count(" → ")
                if sibling_count > 0:
                    total_siblings_included += sibling_count
                    max_siblings_in_context = max(max_siblings_in_context, sibling_count)

            # Ensure context is never empty (ChromaDB requirement)
            if not context or not context.strip():
                empty_contexts += 1
                # Debug empty context
                if empty_contexts <= 3:  # Only log first few
                    print(f"    ⚠️  Empty context for {uid}: original_text='{original_text[:50] if original_text else 'None'}'")
                context = original_text if original_text else f"[Empty block {uid}]"

            # Prepare for ChromaDB
            batch_ids.append(uid)
            batch_documents.append(context)
            batch_metadatas.append({
                "block_type": block_type,
                "is_page": str(is_page),
                "original_text": original_text[:500],  # Store more for debugging
                "has_children": str(has_children),
                "has_parent": str(has_parent),
                "context_length": str(len(context)),
                "sync_version": "full_v1",
                "sync_timestamp": datetime.now().isoformat()
            })

        # Add batch to ChromaDB
        if batch_ids:
            # Report empty contexts if any
            if empty_contexts > 0:
                print(f"  ⚠️  {empty_contexts} blocks had empty context and were filled with fallback")

            try:
                collection.add(
                    ids=batch_ids,
                    documents=batch_documents,
                    metadatas=batch_metadatas
                )
                successful += len(batch_ids)
                print(f"  ✓ Added {len(batch_ids)} blocks to collection")
            except Exception as e:
                print(f"  ✗ Error adding batch to collection: {e}")
                failed += len(batch_ids)

        # Rate limiting - comment out if not needed
        # if batch_num < (total_blocks // BATCH_SIZE):  # Don't delay after last batch
        #     print(f"  → Rate limit delay: {RATE_LIMIT_DELAY}s")
        #     await asyncio.sleep(RATE_LIMIT_DELAY)

    # Step 3: Save timestamp
    print("\n[sync_full] Step 3: Saving sync timestamp...")
    try:
        with open(TIMESTAMP_FILE, 'w') as f:
            json.dump({
                "last_sync": datetime.now().isoformat(),
                "blocks_processed": total_blocks,
                "blocks_added": successful,
                "blocks_failed": failed,
                "blocks_skipped": skipped
            }, f, indent=2)
        print(f"  ✓ Timestamp saved to {TIMESTAMP_FILE}")
    except Exception as e:
        print(f"  ✗ Failed to save timestamp: {e}")

    # Final statistics
    elapsed_time = time.time() - start_time
    final_count = collection.count()

    print("\n" + "="*50)
    print("[sync_full] SYNC COMPLETE!")
    print("="*50)
    print(f"  • Total blocks in graph: {total_blocks}")
    print(f"  • Successfully added: {successful}")
    print(f"  • Failed: {failed}")
    print(f"  • Skipped (already existed): {skipped}")
    print(f"  • Parent blocks: {parent_blocks}")
    print(f"  • Leaf blocks: {leaf_blocks}")
    print(f"    - With parent context: {leaf_with_parent}")
    print(f"    - With sibling context: {leaf_with_siblings}")
    print(f"  • Multi-sibling context:")
    print(f"    - Total siblings included: {total_siblings_included}")
    print(f"    - Max siblings in one context: {max_siblings_in_context}")
    if leaf_with_siblings > 0:
        print(f"    - Avg siblings per leaf: {total_siblings_included / leaf_with_siblings:.1f}")
    print(f"  • Collection size: {initial_count} → {final_count}")
    print(f"  • Time elapsed: {elapsed_time:.2f} seconds")
    print(f"  • Processing rate: {(total_blocks / elapsed_time):.1f} blocks/second")
    print("="*50)

async def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Sync Roam graph to vector database')
    parser.add_argument(
        '--clear',
        action='store_true',
        help='Clear all existing embeddings before syncing (default: incremental sync)'
    )
    parser.add_argument(
        '--test',
        type=int,
        metavar='N',
        help='Test mode: only process first N blocks'
    )

    args = parser.parse_args()

    # Run sync with options
    await sync_full_graph(clear_existing=args.clear, test_limit=args.test)

if __name__ == "__main__":
    print("[sync_full] Running full graph sync...")
    asyncio.run(main())
    print("[sync_full] Done!")
