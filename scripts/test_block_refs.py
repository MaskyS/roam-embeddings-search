"""
Test script to understand how :block/refs works in Roam's pull API
"""
import asyncio
import json
import httpx
from services.search_service import settings

async def test_pull_with_refs():
    """Test what :block/refs returns in a pull query"""
    
    # First, let's find a block that likely has references
    # We'll search for blocks containing "((" 
    query_url = f"https://api.roamresearch.com/api/graph/{settings.roam_graph_name}/q"
    headers = {
        "X-Authorization": f"Bearer {settings.roam_api_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    
    # Find blocks with block references
    query = """[:find ?uid ?str
               :where 
               [?b :block/uid ?uid]
               [?b :block/string ?str]
               [(clojure.string/includes? ?str "((")]]"""
    
    query_data = {"query": query}
    
    print("Step 1: Finding blocks with references...")
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        response = await client.post(query_url, headers=headers, json=query_data)
        if response.status_code == 200:
            results = response.json().get('result', [])
            print(f"Found {len(results)} blocks with potential references")
            
            if results:
                # Take first block with references
                test_uid = results[0][0]
                test_string = results[0][1]
                print(f"\nTest block UID: {test_uid}")
                print(f"Test block string: {test_string[:200]}...")
                
                # Now pull this block with different selectors to compare
                pull_url = f"https://api.roamresearch.com/api/graph/{settings.roam_graph_name}/pull"
                
                # Test 1: Pull WITHOUT :block/refs
                print("\n" + "="*60)
                print("Test 1: Pull WITHOUT :block/refs")
                print("="*60)
                
                selector_without = '[:block/uid :block/string]'
                pull_data = {
                    "eid": f'[:block/uid "{test_uid}"]',
                    "selector": selector_without
                }
                
                response = await client.post(pull_url, headers=headers, json=pull_data)
                if response.status_code == 200:
                    result = response.json().get('result')
                    print("Result:")
                    print(json.dumps(result, indent=2))
                
                # Test 2: Pull WITH :block/refs (flat)
                print("\n" + "="*60)
                print("Test 2: Pull WITH :block/refs (flat)")
                print("="*60)
                
                selector_with_refs_flat = '[:block/uid :block/string :block/refs]'
                pull_data = {
                    "eid": f'[:block/uid "{test_uid}"]',
                    "selector": selector_with_refs_flat
                }
                
                response = await client.post(pull_url, headers=headers, json=pull_data)
                if response.status_code == 200:
                    result = response.json().get('result')
                    print("Result:")
                    print(json.dumps(result, indent=2))
                
                # Test 3: Pull WITH :block/refs (nested - include ref block details)
                print("\n" + "="*60)
                print("Test 3: Pull WITH :block/refs (nested - with ref details)")
                print("="*60)
                
                selector_with_refs_nested = '[:block/uid :block/string {:block/refs [:block/uid :block/string :node/title]}]'
                pull_data = {
                    "eid": f'[:block/uid "{test_uid}"]',
                    "selector": selector_with_refs_nested
                }
                
                response = await client.post(pull_url, headers=headers, json=pull_data)
                if response.status_code == 200:
                    result = response.json().get('result')
                    print("Result:")
                    print(json.dumps(result, indent=2))
                    
                    # Analyze the refs
                    if result and ':block/refs' in result:
                        refs = result[':block/refs']
                        print(f"\nFound {len(refs)} resolved references:")
                        for ref in refs[:3]:  # Show first 3
                            ref_uid = ref.get(':block/uid', 'unknown')
                            ref_text = ref.get(':block/string', ref.get(':node/title', ''))
                            print(f"  - {ref_uid}: {ref_text[:100]}...")
                
                # Test 4: Check pull-many with refs
                print("\n" + "="*60)
                print("Test 4: Pull-many WITH :block/refs")
                print("="*60)
                
                # Get 2-3 blocks for pull-many test
                test_uids = [r[0] for r in results[:3]]
                
                pull_many_url = f"https://api.roamresearch.com/api/graph/{settings.roam_graph_name}/pull-many"
                
                eids_str = "[" + " ".join([f'[:block/uid "{uid}"]' for uid in test_uids]) + "]"
                selector_many = '[:block/uid :block/string {:block/refs [:block/uid :block/string :node/title]}]'
                
                pull_many_data = {
                    "eids": eids_str,
                    "selector": selector_many
                }
                
                response = await client.post(pull_many_url, headers=headers, json=pull_many_data)
                if response.status_code == 200:
                    results = response.json().get('result', [])
                    print(f"Pulled {len(results)} blocks")
                    
                    for i, result in enumerate(results[:2]):
                        if result and ':block/refs' in result:
                            uid = result.get(':block/uid')
                            refs = result[':block/refs']
                            print(f"\nBlock {i+1} ({uid}): {len(refs)} refs")
                
        else:
            print(f"Query failed: {response.status_code}")
            print(response.text)

async def test_specific_block():
    """Test with a specific block we know has references"""
    
    # You can put a specific UID here if you know one with refs
    test_uid = "avvpDZFYZ"  # From our earlier search results
    
    pull_url = f"https://api.roamresearch.com/api/graph/{settings.roam_graph_name}/pull"
    headers = {
        "X-Authorization": f"Bearer {settings.roam_api_token}",
        "Content-Type": "application/json",
    }
    
    selector = '[:block/uid :block/string {:block/refs [:block/uid :block/string :node/title]}]'
    pull_data = {
        "eid": f'[:block/uid "{test_uid}"]',
        "selector": selector
    }
    
    print(f"\nTesting specific block: {test_uid}")
    print("Selector:", selector)
    
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        response = await client.post(pull_url, headers=headers, json=pull_data)
        if response.status_code == 200:
            result = response.json().get('result')
            print("\nFull result:")
            print(json.dumps(result, indent=2))
        else:
            print(f"Failed: {response.status_code}")

if __name__ == "__main__":
    print("[test_block_refs] Testing :block/refs selector...")
    asyncio.run(test_pull_with_refs())
    # asyncio.run(test_specific_block())  # Uncomment to test specific block
    print("\n[test_block_refs] Done!")
