"""
Sync v2: Debug version - start with minimal imports
"""
print("[sync_v2] Script starting...")

# Step 1: Test basic imports
print("[sync_v2] Step 1: Testing basic imports...")
import asyncio
print("[sync_v2] - asyncio imported")

# Step 2: Test roam import
print("[sync_v2] Step 2: Testing roam import...")
from roam import query_roam
print("[sync_v2] - roam imported successfully")

# Step 2b: Test httpx import (used in v1)
print("[sync_v2] Step 2b: Testing httpx import...")
import httpx
print("[sync_v2] - httpx imported successfully")

# Step 3: Test settings import only
print("[sync_v2] Step 3: Testing settings import from main...")
from main import settings
print(f"[sync_v2] - settings imported: graph={settings.roam_graph_name}")

# Step 4: Test get_collection import
print("[sync_v2] Step 4: Testing get_collection import...")
from main import get_collection
print("[sync_v2] - get_collection imported successfully")

# Add pull_block function from v1
async def pull_block(uid: str):
    """Pull a single block with its children"""
    print(f"[sync_v2] Pulling block {uid}...")
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

async def test_minimal():
    print("\n[sync_v2] Running minimal test...")
    
    # Test 1: Just query Roam
    print("[sync_v2] Test 1: Query Roam for count...")
    query = "[:find (count ?b) . :where [?b :block/uid]]"
    result = await query_roam(
        token=settings.roam_api_token,
        graph_name=settings.roam_graph_name,
        query=query
    )
    if result:
        print(f"[sync_v2] ✓ Roam query successful: {result['result']} blocks")
    else:
        print("[sync_v2] ✗ Roam query failed")
    
    # Test 2: Try to get ChromaDB collection
    print("\n[sync_v2] Test 2: Getting ChromaDB collection...")
    try:
        print("[sync_v2] Calling get_collection()...")
        collection = get_collection()
        print(f"[sync_v2] ✓ Collection retrieved: {collection.count()} documents")
        
        # Test 3: Try adding a simple document
        print("\n[sync_v2] Test 3: Adding a test document...")
        test_id = "test_block_v2"
        test_doc = "This is a test document from sync v2"
        
        # Check if it already exists
        existing = collection.get(ids=[test_id])
        if existing['ids']:
            print(f"[sync_v2] Document {test_id} already exists, skipping...")
        else:
            print(f"[sync_v2] Adding document: {test_id}")
            collection.add(
                ids=[test_id],
                documents=[test_doc],
                metadatas=[{"source": "sync_v2", "type": "test"}]
            )
            print(f"[sync_v2] ✓ Document added. Collection now has {collection.count()} documents")
        
        # Test 4: Try pulling a block
        print("\n[sync_v2] Test 4: Testing pull_block function...")
        # Use the UID we found in test_sync.py
        test_uid = "7-A3nufzR"
        block_data = await pull_block(test_uid)
        if block_data:
            print(f"[sync_v2] ✓ Block pulled successfully")
            print(f"[sync_v2] Block text: {block_data.get(':block/string', '')[:50]}...")
            print(f"[sync_v2] Has children: {bool(block_data.get(':block/children'))}")
        else:
            print(f"[sync_v2] ✗ Failed to pull block")
            
    except Exception as e:
        print(f"[sync_v2] ✗ Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n[sync_v2] Minimal test complete!")

if __name__ == "__main__":
    print("[sync_v2] Starting async run...")
    asyncio.run(test_minimal())
    print("[sync_v2] Script complete!")