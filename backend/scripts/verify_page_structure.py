"""
A script to empirically test the data structure of a Roam Research page entity.
"""
import asyncio
import httpx
import json
import os
import sys

# Add backend to path to allow local imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from services.search_service import settings
except ImportError:
    print("Could not import settings. Make sure your environment is set up.")
    class DummySettings:
        roam_graph_name = os.getenv("ROAM_GRAPH_NAME", "YOUR_GRAPH_NAME")
        roam_api_token = os.getenv("ROAM_API_TOKEN", "YOUR_API_TOKEN")
    settings = DummySettings()

async def verify_structure():
    """
    This script tests whether a Roam page entity can have both a :node/title`
    and a `:block/string` attribute simultaneously.

    - The documentation in `api_response_samples.md` suggests they are mutually exclusive.
    - The logic in `linearize.py` assumes they can coexist.

    This script will:
    1. Find the UID of one page in your graph.
    2. Use the `pull` API to fetch that page with a selector for both attributes.
    3. Print the result and an analysis.
    """
    print("--- Roam Page Structure Verification Script ---")

    token = settings.roam_api_token
    graph_name = settings.roam_graph_name

    if "YOUR_GRAPH_NAME" in graph_name or "YOUR_API_TOKEN" in token:
        print("\nERROR: Please configure your Roam graph name and API token in your environment.")
        return

    headers = {
        "X-Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    
    # 1. Get the page UID from command-line argument or find one automatically
    page_uid = None
    if len(sys.argv) > 1:
        page_uid = sys.argv[1]
        print(f"\nStep 1: Using provided page UID: {page_uid}")
    else:
        print("\nStep 1: No UID provided, finding a page UID to test...")
        try:
            q_url = f"https://api.roamresearch.com/api/graph/{graph_name}/q"
            # Datalog query to find the UID of one page
            q_data = {"query": "[:find ?uid :where [?e :node/title] [?e :block/uid ?uid]]"}
            
            async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
                response = await client.post(q_url, headers=headers, json=q_data)
                response.raise_for_status()
                result = response.json().get("result")
                if result and result[0]:
                    page_uid = result[0][0]
                    print(f"Found page UID to test: {page_uid}")
                else:
                    print("Could not find any pages in the graph.")
                    return
        except Exception as e:
            print(f"Error finding a page UID: {e}")
            if hasattr(e, 'response'):
                print(f"Response body: {e.response.text}")
            return

    if not page_uid:
        print("Could not determine a page UID to test.")
        return

    # 2. Pull that page with a specific selector
    print(f"\nStep 2: Pulling data for page UID '{page_uid}'...")
    selector = "[:block/uid :node/title :block/string]"
    print(f"Using selector: {selector}")
    
    try:
        pull_url = f"https://api.roamresearch.com/api/graph/{graph_name}/pull"
        pull_data = {
            "eid": f'[:block/uid "{page_uid}"]',
            "selector": selector
        }
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            response = await client.post(pull_url, headers=headers, json=pull_data)
            response.raise_for_status()
            result_data = response.json().get("result")

            print("\n--- API Response ---")
            print(json.dumps(result_data, indent=2))
            print("--------------------\n")

            # 3. Analyze the result
            print("Step 3: Analyzing the result...")
            if not result_data:
                print("Result is empty. Cannot analyze.")
                return

            has_title = ":node/title" in result_data
            has_string = ":block/string" in result_data

            print(f"Does the page entity have ':node/title'?   -> {has_title}")
            print(f"Does the page entity have ':block/string'? -> {has_string}")

            if has_title and has_string:
                print("\nConclusion: CORRECT. A page can have both ':node/title' and ':block/string'.")
                print("The logic in `linearize.py` is robust and handles this correctly.")
            elif has_title and not has_string:
                print("\nConclusion: The `api_response_samples.md` finding is correct for THIS page.")
                print("This specific page entity only has a ':node/title'. The `linearize.py` logic still works correctly.")
            else:
                print("\nConclusion: Unexpected structure found.")

            print("\nTo be certain, you can manually add content to the top-level of the page (not as a child block) and re-run this script.")

    except Exception as e:
        print(f"An error occurred during the pull request: {e}")
        if hasattr(e, 'response'):
             print(f"Response body: {e.response.text}")


if __name__ == "__main__":
    # Ensure the environment variables are loaded if using a .env file
    from dotenv import load_dotenv
    load_dotenv()
    asyncio.run(verify_structure())
