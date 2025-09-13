"""
Sync v3: Actually sync some blocks with proper context building
"""
print("[sync_v3] Starting...")

import asyncio
from typing import Dict, List, Optional
import httpx
from roam import query_roam
from main import settings, get_collection

async def pull_block(uid: str) -> Optional[Dict]:
    """Pull a single block with its children"""
    url = f"https://api.roamresearch.com/api/graph/{settings.roam_graph_name}/pull"
    headers = {
        "X-Authorization": f"Bearer {settings.roam_api_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    
    pull_data = {
        "eid": f'[:block/uid "{uid}"]',
        "selector": '[:block/uid :block/string {:block/children [:block/uid :block/string :block/order]}]'
    }
    
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        response = await client.post(url, headers=headers, json=pull_data)
        if response.status_code == 200:
            data = response.json()
            return data.get('result')
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

async def sync_blocks():
    """Sync a batch of blocks"""
    print("\n[sync_v3] Starting block sync...")
    
    # Get a small batch of blocks to process
    # Skip some to get fresh ones
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
        print("[sync_v3] Failed to get blocks")
        return
    
    blocks = result['result']
    # Take blocks 25-35 to get fresh ones
    blocks = blocks[25:35] if len(blocks) > 35 else blocks[:10]
    print(f"[sync_v3] Processing {len(blocks)} blocks...")
    
    # Get collection
    collection = get_collection()
    
    # Process each block
    successful = 0
    for i, (uid, string) in enumerate(blocks):
        print(f"\n[sync_v3] Processing block {i+1}/{len(blocks)}: {uid}")
        
        # Check if already processed
        existing = collection.get(ids=[uid])
        if existing['ids']:
            print(f"  → Already in collection, skipping")
            continue
        
        # Pull full block data
        block_data = await pull_block(uid)
        if not block_data:
            print(f"  ✗ Failed to pull block data")
            continue
        
        # Determine if it's a parent or leaf block
        has_children = bool(block_data.get(':block/children'))
        
        # Build context
        if has_children:
            print(f"  → Parent block with {len(block_data.get(':block/children', []))} children")
            context = build_parent_block_context(block_data)
            block_type = "parent"
        else:
            print(f"  → Leaf block")
            context = block_data.get(':block/string', '')
            block_type = "leaf"
        
        # Add to collection
        try:
            collection.add(
                ids=[uid],
                documents=[context],
                metadatas=[{
                    "block_type": block_type,
                    "original_text": string[:200],
                    "has_children": str(has_children),
                    "context_length": str(len(context))
                }]
            )
            print(f"  ✓ Added to collection ({len(context)} chars)")
            successful += 1
        except Exception as e:
            print(f"  ✗ Error adding to collection: {e}")
    
    print(f"\n[sync_v3] Sync complete! Added {successful} new blocks")
    print(f"[sync_v3] Collection now has {collection.count()} total documents")

async def main():
    await sync_blocks()

if __name__ == "__main__":
    print("[sync_v3] Running...")
    asyncio.run(main())
    print("[sync_v3] Done!")