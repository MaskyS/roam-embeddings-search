
import httpx

async def query_roam(token: str, graph_name: str, query: str, args: list = None):
    """Executes a Datalog query against the Roam Research backend API."""
    url = f"https://api.roamresearch.com/api/graph/{graph_name}/q"
    headers = {
        "X-Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    json_body = {"query": query}
    if args is not None:
        json_body["args"] = args

    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        try:
            response = await client.post(url, headers=headers, json=json_body)
            response.raise_for_status()  # Raises an exception for 4XX or 5XX status codes
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            return None
        except httpx.RequestError as e:
            print(f"An error occurred while requesting {e.request.url!r}.")
            return None
