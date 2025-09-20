"""
Sync v4: Add parent context for leaf blocks using pull's reverse lookup
This builds on v3 by enhancing leaf blocks with their parent context.
"""
print("[sync_v4] Starting...")

import asyncio
from typing import Dict, List, Optional
import httpx
from roam import query_roam
from main import settings, get_collection

async def pull_block(uid: str) -> Optional[Dict]:
    """Pull a single block with its children AND parent info via reverse lookup"""
    url = f"https://api.roamresearch.com/api/graph/{settings.roam_graph_name}/pull"
    headers = {
        "X-Authorization": f"Bearer {settings.roam_api_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    # Enhanced selector with reverse parent lookup
    # :block/_children gets the parent that has this block as a child
    pull_data = {
        "eid": f'[:block/uid "{uid}"]',
        "selector": """[:block/uid :block/string
                       {:block/children [:block/uid :block/string :block/order]}
                       {:block/_children [:block/uid :block/string :node/title]}]"""
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

def build_leaf_block_context(block_data: Dict) -> str:
    """Build context for a leaf block with parent context"""
    block_text = block_data.get(':block/string', '')

    # Get parent from reverse lookup
    parents = block_data.get(':block/_children', [])
    if parents:
        parent = parents[0]  # Should only have one parent
        # Check if parent is a page (has :node/title) or block (has :block/string)
        parent_text = parent.get(':node/title') or parent.get(':block/string', '')
        if parent_text:
            # Format: "Parent Context > Block Text"
            return f"{parent_text} > {block_text}"

    # If no parent found, return just the block text
    return block_text

async def sync_blocks():
    """Sync a batch of blocks with enhanced context"""
    print("\n[sync_v4] Starting block sync with parent context...")

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
        print("[sync_v4] Failed to get blocks")
        return

    blocks = result['result']
    # Take blocks 35-45 to get fresh ones different from v3
    blocks = blocks[35:45] if len(blocks) > 45 else blocks[:10]
    print(f"[sync_v4] Processing {len(blocks)} blocks...")

    # Get collection
    collection = get_collection()

    # Process each block
    successful = 0
    leaf_with_parent = 0
    leaf_without_parent = 0

    for i, (uid, string) in enumerate(blocks):
        print(f"\n[sync_v4] Processing block {i+1}/{len(blocks)}: {uid}")
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
            else:
                print(f" (no parent found)")
                leaf_without_parent += 1

            context = build_leaf_block_context(block_data)
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
                    "version": "v4"
                }]
            )
            print(f"  ✓ Added to collection ({len(context)} chars)")
            if block_type == "leaf" and has_parent:
                print(f"  → Context: {context[:150]}...")
            successful += 1
        except Exception as e:
            print(f"  ✗ Error adding to collection: {e}")

    print(f"\n[sync_v4] Sync complete!")
    print(f"  • Added {successful} new blocks")
    print(f"  • Leaf blocks with parent context: {leaf_with_parent}")
    print(f"  • Leaf blocks without parent: {leaf_without_parent}")
    print(f"  • Collection now has {collection.count()} total documents")

async def main():
    await sync_blocks()

if __name__ == "__main__":
    print("[sync_v4] Running enhanced sync with parent context...")
    asyncio.run(main())
    print("[sync_v4] Done!")
