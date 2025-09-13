"""
Sync v1: Minimal viable sync - process 20 blocks with basic context
"""
print("[sync_v1] Starting imports...")
import asyncio
import json
from typing import List, Dict, Optional
import httpx
print("[sync_v1] Importing from roam...")
from roam import query_roam
print("[sync_v1] Importing from main...")
from main import settings, get_collection
print("[sync_v1] All imports complete")
# chromadb imported from main.py

async def pull_block(uid: str) -> Optional[Dict]:
    """Pull a single block with its children"""
    print(f"  [DEBUG] Pulling block {uid}...")
    url = f"https://api.roamresearch.com/api/graph/{settings.roam_graph_name}/pull"
    headers = {
        "X-Authorization": f"Bearer {settings.roam_api_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    
    pull_data = {
        "eid": f'[:block/uid "{uid}"]',
        "selector": '''[:block/uid :block/string :block/order
                       {:block/children [:block/uid :block/string :block/order]}
                       {:block/parents [:block/uid :block/string]}]'''
    }
    
    print(f"  [DEBUG] Making pull request...")
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        response = await client.post(url, headers=headers, json=pull_data)
        print(f"  [DEBUG] Pull response status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            result = data.get('result')
            print(f"  [DEBUG] Pull result exists: {result is not None}")
            return result
    return None

async def build_parent_block_context(block_data: Dict) -> str:
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

async def build_leaf_block_context(block_data: Dict) -> str:
    """Build context for a leaf block: include parent context"""
    block_text = block_data.get(':block/string', '')
    parents = block_data.get(':block/parents', [])
    
    # For now, just prepend parent text
    if parents:
        parent_text = parents[0].get(':block/string', '')
        if parent_text:
            return f"{parent_text} > {block_text}"
    
    return block_text

async def sync_batch():
    """Sync a small batch of blocks to test our approach"""
    print("=== Starting Sync v1 ===")
    print("[DEBUG] Inside sync_batch function")
    
    # Step 1: Get 20 blocks (mix of parents and leaves)
    query = """[:find ?uid ?string 
               :where 
               [?b :block/uid ?uid] 
               [?b :block/string ?string]
               :limit 20]"""
    
    print("[DEBUG] About to query Roam for blocks...")
    result = await query_roam(
        token=settings.roam_api_token,
        graph_name=settings.roam_graph_name,
        query=query
    )
    print("[DEBUG] Query completed")
    print(f"[DEBUG] Query result received: {result is not None}")
    
    if not result or not result.get('result'):
        print("Failed to get blocks")
        return
    
    blocks = result['result']
    print(f"Processing {len(blocks)} blocks...")
    
    # Step 2: Process each block
    documents = []
    ids = []
    metadatas = []
    
    for i, (uid, string) in enumerate(blocks):
        print(f"\nProcessing block {i+1}/{len(blocks)}: {uid}")
        
        # Pull full block data
        block_data = await pull_block(uid)
        if not block_data:
            print(f"  ⚠️  Failed to pull block data")
            continue
        
        # Determine if it's a parent or leaf block
        has_children = bool(block_data.get(':block/children'))
        
        # Build context based on block type
        if has_children:
            print(f"  → Parent block with {len(block_data.get(':block/children', []))} children")
            context = await build_parent_block_context(block_data)
            block_type = "parent"
        else:
            print(f"  → Leaf block")
            context = await build_leaf_block_context(block_data)
            block_type = "leaf"
        
        # Prepare for ChromaDB
        documents.append(context)
        ids.append(uid)
        metadatas.append({
            "block_type": block_type,
            "original_text": string[:500],  # Store first 500 chars
            "has_children": str(has_children),
            "context_length": str(len(context))
        })
        
        print(f"  ✓ Context built ({len(context)} chars)")
    
    # Step 3: Store in ChromaDB
    if documents:
        print(f"\n[DEBUG] About to store {len(documents)} blocks in ChromaDB...")
        print(f"[DEBUG] First document preview: {documents[0][:100]}...")
        print(f"[DEBUG] IDs: {ids[:3]}...")
        try:
            print("[DEBUG] Calling collection.add()...")
            get_collection().add(
                documents=documents,
                ids=ids,
                metadatas=metadatas
            )
            print(f"✓ Successfully stored {len(documents)} blocks")
        except Exception as e:
            print(f"✗ Error storing in ChromaDB: {e}")
            print(f"[DEBUG] Exception type: {type(e)}")
    
    # Step 4: Test with a simple query
    print("\n=== Testing Search ===")
    test_query = "builder"
    print(f"Searching for: '{test_query}'")
    
    try:
        results = get_collection().query(
            query_texts=[test_query],
            n_results=3
        )
        
        if results['ids'][0]:
            print(f"Found {len(results['ids'][0])} results:")
            for i, (doc_id, distance) in enumerate(zip(results['ids'][0], results['distances'][0])):
                metadata = results['metadatas'][0][i]
                print(f"\n  Result {i+1}:")
                print(f"    Block UID: {doc_id}")
                print(f"    Distance: {distance:.4f}")
                print(f"    Type: {metadata.get('block_type', 'unknown')}")
                print(f"    Original: {metadata.get('original_text', '')[:100]}...")
    except Exception as e:
        print(f"Search error: {e}")
    
    print("\n=== Sync v1 Complete ===")

if __name__ == "__main__":
    print("[SYNC_V1] Starting main execution...")
    asyncio.run(sync_batch())
    print("[SYNC_V1] Main execution completed")