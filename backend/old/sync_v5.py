"""
Sync v5: Add sibling context for leaf blocks using enhanced pull selector
This builds on v4 by adding sibling awareness through a sliding window approach.
"""
print("[sync_v5] Starting...")

import asyncio
from typing import Dict, List, Optional
import httpx
from roam import query_roam
from main import settings, get_collection

async def pull_block(uid: str) -> Optional[Dict]:
    """Pull block with children AND parent with ITS children (siblings)"""
    url = f"https://api.roamresearch.com/api/graph/{settings.roam_graph_name}/pull"
    headers = {
        "X-Authorization": f"Bearer {settings.roam_api_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    # Enhanced selector - gets parent's children too for sibling context
    pull_data = {
        "eid": f'[:block/uid "{uid}"]',
        "selector": """[:block/uid :block/string
                       {:block/children [:block/uid :block/string :block/order]}
                       {:block/_children [:block/uid :block/string :node/title 
                                         {:block/children [:block/uid :block/string :block/order]}]}]"""
    }

    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        response = await client.post(url, headers=headers, json=pull_data)
        if response.status_code == 200:
            data = response.json()
            return data.get('result')
        else:
            print(f"  ✗ Pull failed with status {response.status_code}: {response.text}")
    return None

def build_parent_block_context(block_data: Dict) -> str:
    """Build context for a parent block: parent + children"""
    parent_text = block_data.get(':block/string', '')
    children = block_data.get(':block/children', [])

    # Sort children by order
    children_sorted = sorted(children, key=lambda x: x.get(':block/order', 0))

    # Build document
    document_parts = [parent_text]
    for child in children_sorted[:10]:  # Limit to first 10 children
        child_text = child.get(':block/string', '').strip()
        if child_text:
            document_parts.append(f"• {child_text}")

    return "\n".join(document_parts)

def build_leaf_block_context(block_data: Dict, block_uid: str) -> str:
    """Build context for leaf block with parent AND sibling context"""
    block_text = block_data.get(':block/string', '')
    
    # Get parent from reverse lookup
    parents = block_data.get(':block/_children', [])
    if not parents:
        return block_text
    
    parent = parents[0]
    
    # Check if parent is a page (pages don't have sibling context)
    if parent.get(':node/title'):
        return f"{parent.get(':node/title')} > {block_text}"
    
    # Block parent - get siblings
    parent_text = parent.get(':block/string', '')
    siblings = parent.get(':block/children', [])
    
    # If no siblings or only child, just use parent context
    if not siblings or len(siblings) <= 1:
        return f"{parent_text} > {block_text}"
    
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
        return f"{parent_text} > {block_text}"
    
    # Build context with sliding window
    context_parts = []
    
    # Add parent
    context_parts.append(parent_text)
    context_parts.append(">")
    
    # Add previous sibling (if exists)
    if current_idx > 0:
        prev_text = siblings_sorted[current_idx - 1].get(':block/string', '')
        if prev_text:
            context_parts.append(prev_text)
            context_parts.append("→")
    
    # Add current block
    context_parts.append(block_text)
    
    # Add next sibling (if exists)
    if current_idx < len(siblings_sorted) - 1:
        next_text = siblings_sorted[current_idx + 1].get(':block/string', '')
        if next_text:
            context_parts.append("→")
            context_parts.append(next_text)
    
    return " ".join(context_parts)

async def sync_blocks():
    """Sync a batch of blocks with enhanced sibling context"""
    print("\n[sync_v5] Starting block sync with sibling context...")

    # Get a small batch of blocks to process
    query = """[:find ?uid ?string
               :where
               [?b :block/uid ?uid]
               [?b :block/string ?string]]"""

    result = await query_roam(
        token=settings.roam_api_token,
        graph_name=settings.roam_graph_name,
        query=query
    )

    if not result or not result.get('result'):
        print("[sync_v5] Failed to get blocks")
        return

    blocks = result['result']
    # Take blocks 45-55 to get fresh ones different from v4
    blocks = blocks[45:55] if len(blocks) > 55 else blocks[:10]
    print(f"[sync_v5] Processing {len(blocks)} blocks...")

    # Get collection
    collection = get_collection()

    # Process each block
    successful = 0
    leaf_with_parent = 0
    leaf_without_parent = 0
    leaf_with_siblings = 0

    for i, (uid, string) in enumerate(blocks):
        print(f"\n[sync_v5] Processing block {i+1}/{len(blocks)}: {uid}")
        print(f"  Original text: {string[:100]}...")

        # Check if already processed
        existing = collection.get(ids=[uid])
        if existing['ids']:
            print(f"  → Already in collection, skipping")
            continue

        # Pull full block data with parent info
        block_data = await pull_block(uid)
        if not block_data:
            print(f"  ✗ Failed to pull block data")
            continue

        # Determine if it's a parent or leaf block
        has_children = bool(block_data.get(':block/children'))
        has_parent = bool(block_data.get(':block/_children'))

        # Build context based on block type
        if has_children:
            print(f"  → Parent block with {len(block_data.get(':block/children', []))} children")
            context = build_parent_block_context(block_data)
            block_type = "parent"
        else:
            print(f"  → Leaf block", end="")
            if has_parent:
                parent = block_data.get(':block/_children', [])[0]
                parent_text = parent.get(':node/title') or parent.get(':block/string', '')[:50]
                print(f" with parent: '{parent_text}...'")
                leaf_with_parent += 1
                
                # Check if it has siblings
                siblings = parent.get(':block/children', [])
                if siblings and len(siblings) > 1:
                    print(f"    Found {len(siblings)} siblings")
                    leaf_with_siblings += 1
            else:
                print(f" (no parent found)")
                leaf_without_parent += 1

            context = build_leaf_block_context(block_data, uid)
            block_type = "leaf"

        # Add to collection with enhanced metadata
        try:
            collection.add(
                ids=[uid],
                documents=[context],
                metadatas=[{
                    "block_type": block_type,
                    "original_text": string[:200],
                    "has_children": str(has_children),
                    "has_parent": str(has_parent),
                    "context_length": str(len(context)),
                    "version": "v5"
                }]
            )
            print(f"  ✓ Added to collection ({len(context)} chars)")
            if block_type == "leaf" and has_parent:
                print(f"  → Context: {context[:150]}...")
            successful += 1
        except Exception as e:
            print(f"  ✗ Error adding to collection: {e}")

    print(f"\n[sync_v5] Sync complete!")
    print(f"  • Added {successful} new blocks")
    print(f"  • Leaf blocks with parent context: {leaf_with_parent}")
    print(f"  • Leaf blocks with sibling context: {leaf_with_siblings}")
    print(f"  • Leaf blocks without parent: {leaf_without_parent}")
    print(f"  • Collection now has {collection.count()} total documents")

async def main():
    await sync_blocks()

if __name__ == "__main__":
    print("[sync_v5] Running enhanced sync with sibling context...")
    asyncio.run(main())
    print("[sync_v5] Done!")
