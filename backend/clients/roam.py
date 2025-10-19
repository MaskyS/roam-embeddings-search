"""Roam Research API client + helpers."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Sequence

import httpx
from aiolimiter import AsyncLimiter
from tenacity import AsyncRetrying, stop_after_attempt, wait_exponential


async def query_roam(token: str, graph_name: str, query: str, args: list = None):
    """Execute a Datalog query against the Roam Research backend API."""
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
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            # Keep stderr minimal in production; callers should handle None
            print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            return None
        except httpx.RequestError as e:
            print(f"An error occurred while requesting {e.request.url!r}.")
            return None

# We dont use :create/time.
METADATA_SELECTOR = (
    "[:block/uid :node/title  :edit/time "
    "{:block/children [:block/uid :edit/time {:block/children ...}]}]"
)

# Previous (broader) selector kept for reference:
# FULL_PAGE_SELECTOR = (
#     "[:block/uid :block/string :node/title :block/order :create/time :edit/time "
#     "{:create/user [:user/uid]} {:edit/user [:user/uid]} {:block/refs [:block/uid :node/title :block/string]} "
#     "{:block/children ...}]"
# )

# Lean recursive selector with only the fields needed for linearization, ordering,
# and aggregated edit times.
FULL_PAGE_SELECTOR = (
    "[:block/uid :node/title :block/string :block/order :edit/time "
    "{:block/children [:block/uid :block/string :block/order :edit/time {:block/children ...}]}]"
)


@dataclass
class RoamClient:
    graph_name: str
    token: str
    requests_per_minute: int

    def __post_init__(self) -> None:
        self.base_url = f"https://api.roamresearch.com/api/graph/{self.graph_name}/"
        self.headers = {
            "X-Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self._limiter = AsyncLimiter(self.requests_per_minute, time_period=60)

    async def get_all_page_uids(self) -> List[str]:
        query = """[:find ?uid
                   :where [?e :node/title]
                          [?e :block/uid ?uid]]"""
        result = await query_roam(
            token=self.token,
            graph_name=self.graph_name,
            query=query,
        )
        if not result or not result.get("result"):
            return []
        return [item[0] for item in result["result"]]

    async def pull_many_pages(
        self,
        uids: Iterable[str],
        selector: str = FULL_PAGE_SELECTOR,
        *,
        timeout: float = 60.0,
    ) -> List[Optional[Dict[str, Any]]]:
        batch = list(uids)
        if not batch:
            return []
        payload = self._build_payload(batch, selector)
        response = await self._post("pull-many", payload, timeout=timeout)
        if response.status_code == 200:
            return response.json().get("result", [])
        return [None] * len(batch)

    async def pull_many_metadata(
        self,
        uids: Iterable[str],
        selector: str = METADATA_SELECTOR,
        *,
        timeout: float = 30.0,
    ) -> List[Optional[Dict[str, Any]]]:
        batch = list(uids)
        if not batch:
            return []
        payload = self._build_payload(batch, selector)
        response = await self._post("pull-many", payload, timeout=timeout)
        if response.status_code == 200:
            return response.json().get("result", [])
        return [None] * len(batch)

    def _build_payload(self, uids: Sequence[str], selector: str) -> Dict[str, str]:
        eids_list = " ".join([f'[:block/uid "{uid}"]' for uid in uids])
        return {"eids": f"[{eids_list}]", "selector": selector}

    async def _post(self, endpoint: str, payload: Dict[str, Any], *, timeout: float) -> httpx.Response:
        async for attempt in AsyncRetrying(
            stop=stop_after_attempt(3),
            wait=wait_exponential(max=4),
            reraise=True,
        ):
            with attempt:
                async with self._limiter:
                    async with httpx.AsyncClient(
                        base_url=self.base_url,
                        headers=self.headers,
                        follow_redirects=True,
                        timeout=timeout,
                    ) as client:
                        response = await client.post(endpoint, json=payload)
                if response.status_code >= 500 or response.status_code == 429:
                    response.raise_for_status()
                return response
        raise RuntimeError("Roam API retry loop exhausted")
