import asyncio
import json
from roam import query_roam
from main import settings
import httpx

async def test_connection():
    """Test basic connection to Roam API"""
    print("=== Testing Roam API Connection ===")
    query = "[:find (count ?b) . :where [?b :block/uid]]"
    result = await query_roam(
        token=settings.roam_api_token,
        graph_name=settings.roam_graph_name,
        query=query
    )
    if result:
        print(f"✓ Connected! Total blocks in graph: {result['result']}")
    else:
        print("✗ Connection failed")
    return result is not None

async def explore_block_structure():
    """Step 1: Get a few blocks to see their structure"""
    print("\n=== Exploring Block Structure ===")
    query = """[:find ?uid ?string 
               :where 
               [?b :block/uid ?uid] 
               [?b :block/string ?string]
               :limit 5]"""
    
    result = await query_roam(
        token=settings.roam_api_token,
        graph_name=settings.roam_graph_name,
        query=query
    )
    
    if result and result.get('result'):
        print(f"Found {len(result['result'])} blocks:")
        for uid, string in result['result']:
            print(f"  - UID: {uid}")
            print(f"    Text: {string[:50]}..." if len(string) > 50 else f"    Text: {string}")
    return result

async def find_parent_blocks():
    """Step 2: Find blocks that have children"""
    print("\n=== Finding Parent Blocks ===")
    query = """[:find ?uid ?string (count ?child)
               :where 
               [?b :block/uid ?uid]
               [?b :block/string ?string]
               [?b :block/children ?child]
               :limit 5]"""
    
    result = await query_roam(
        token=settings.roam_api_token,
        graph_name=settings.roam_graph_name,
        query=query
    )
    
    if result and result.get('result'):
        print(f"Found {len(result['result'])} parent blocks:")
        for uid, string, child_count in result['result']:
            print(f"  - UID: {uid}")
            print(f"    Text: {string[:50]}..." if len(string) > 50 else f"    Text: {string}")
            print(f"    Children: {child_count}")
        return result['result'][0][0] if result['result'] else None
    return None

async def explore_block_hierarchy(parent_uid):
    """Step 3: Use pull API to get full block hierarchy"""
    print(f"\n=== Exploring Block Hierarchy for {parent_uid} ===")
    
    # Create a simple pull endpoint helper
    url = f"https://api.roamresearch.com/api/graph/{settings.roam_graph_name}/pull"
    headers = {
        "X-Authorization": f"Bearer {settings.roam_api_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    
    pull_data = {
        "eid": f'[:block/uid "{parent_uid}"]',
        "selector": '[:block/uid :block/string {:block/children [:block/uid :block/string :block/order]}]'
    }
    
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        response = await client.post(url, headers=headers, json=pull_data)
        if response.status_code == 200:
            data = response.json()
            result = data.get('result')
            if result:
                print(f"Parent block: {result.get(':block/string', '')[:100]}...")
                children = result.get(':block/children', [])
                print(f"Number of children: {len(children)}")
                for i, child in enumerate(children[:3]):  # Show first 3 children
                    print(f"  Child {i+1}: {child.get(':block/string', '')[:50]}...")
            return result
    return None

async def test_context_building(block_data):
    """Step 4: Build context for a parent block"""
    print("\n=== Testing Context Building ===")
    
    if not block_data:
        print("No block data provided")
        return
    
    # Build context: parent + children
    parent_text = block_data.get(':block/string', '')
    children = block_data.get(':block/children', [])
    
    # Sort children by order
    children_sorted = sorted(children, key=lambda x: x.get(':block/order', 0))
    
    # Build document
    document_parts = [parent_text]
    for child in children_sorted[:5]:  # Limit to first 5 children for testing
        child_text = child.get(':block/string', '')
        if child_text:
            document_parts.append(f"- {child_text}")
    
    context_document = "\n".join(document_parts)
    print(f"Built context document ({len(context_document)} chars):")
    print("-" * 50)
    print(context_document[:500] + "..." if len(context_document) > 500 else context_document)
    print("-" * 50)
    
    return context_document

async def test_leaf_block_context():
    """Step 5: Find and build context for a leaf block"""
    print("\n=== Testing Leaf Block Context ===")
    
    # Find a leaf block (block without children)
    query = """[:find ?uid ?string ?parent_uid
               :where 
               [?b :block/uid ?uid]
               [?b :block/string ?string]
               [?parent :block/children ?b]
               [?parent :block/uid ?parent_uid]
               (not [?b :block/children])
               :limit 1]"""
    
    result = await query_roam(
        token=settings.roam_api_token,
        graph_name=settings.roam_graph_name,
        query=query
    )
    
    if result and result.get('result'):
        uid, string, parent_uid = result['result'][0]
        print(f"Found leaf block: {uid}")
        print(f"Text: {string[:100]}...")
        print(f"Parent: {parent_uid}")
        
        # TODO: Get siblings and build sliding window context
        # This would be the next iteration
        
    return result

async def main():
    """Run all tests in sequence"""
    print("Starting Roam Sync Testing...\n")
    
    # Test 1: Connection
    if not await test_connection():
        print("Connection failed, stopping tests")
        return
    
    # Test 2: Explore blocks
    await explore_block_structure()
    
    # Test 3: Find parent blocks
    parent_uid = await find_parent_blocks()
    
    # Test 4: Explore hierarchy
    if parent_uid:
        block_data = await explore_block_hierarchy(parent_uid)
        
        # Test 5: Build context
        if block_data:
            await test_context_building(block_data)
    
    # Test 6: Leaf block context
    await test_leaf_block_context()
    
    print("\n=== Testing Complete ===")

if __name__ == "__main__":
    asyncio.run(main())