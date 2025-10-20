from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

import httpx
from pydantic import AnyUrl

from models import SearchInput, SearchResult


class BackendClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None, graph_slug: Optional[str] = None) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.graph_slug = graph_slug

    def _headers(self) -> Dict[str, str]:
        headers: Dict[str, str] = {"Accept": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _build_roam_url(self, page_uid: Optional[str], block_uid: Optional[str]) -> Optional[AnyUrl]:
        try:
            if not self.graph_slug or not page_uid:
                return None
            base = f"https://roamresearch.com/#/app/{self.graph_slug}/page/{page_uid}"
            if block_uid:
                base = f"{base}?block={block_uid}"
            return AnyUrl(base)
        except Exception:
            return None

    async def health(self) -> Dict[str, Any]:
        url = f"{self.base_url}/"
        async with httpx.AsyncClient(timeout=15.0) as client:
            r = await client.get(url, headers=self._headers())
            r.raise_for_status()
            return r.json()

    async def search(self, params: SearchInput) -> List[SearchResult]:
        query_params = {
            "q": params.query,
            "limit": params.limit,
            "alpha": params.alpha,
            "exclude_pages": str(params.exclude_pages).lower(),
            "rerank": str(params.rerank).lower(),
        }
        url = f"{self.base_url}/search"
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.get(url, params=query_params, headers=self._headers())
            r.raise_for_status()
            data = r.json() or {}

        results_raw = data.get("results", []) or []
        out: List[SearchResult] = []
        for item in results_raw:
            page_title = item.get("page_title") or ""
            page_uid = item.get("page_uid") or None
            primary_uid = item.get("uid") or None
            document_type = item.get("document_type") or "chunk"
            # Treat chunks as blocks; pages have no block uid
            block_uid = primary_uid if document_type != "page" else None
            block_text = item.get("chunk_text_preview") or item.get("parent_text") or None
            score = float(item.get("similarity") or 0.0)
            url_val = self._build_roam_url(page_uid, block_uid)

            out.append(
                SearchResult(
                    page_title=page_title,
                    page_uid=page_uid or "",
                    block_uid=block_uid,
                    block_text=block_text,
                    score=score,
                    url=url_val,
                    highlights=None,
                )
            )
        return out


def from_env() -> BackendClient:
    base = os.getenv("SEMANTIC_BACKEND_URL", "http://localhost:8002").strip()
    key = os.getenv("SEMANTIC_BACKEND_API_KEY")
    graph = os.getenv("GRAPH_SLUG")
    return BackendClient(base_url=base, api_key=key, graph_slug=graph)
