from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl


class SearchResult(BaseModel):
    page_title: str = Field(default="", description="Title of the page")
    page_uid: str = Field(description="Roam page UID")
    block_uid: Optional[str] = Field(default=None, description="Block UID if result is a block")
    block_text: Optional[str] = Field(default=None, description="Block text preview, if available")
    score: float = Field(description="Similarity score or ranking score")
    url: Optional[HttpUrl] = Field(default=None, description="Deep link to Roam page or block")
    highlights: Optional[List[str]] = Field(default=None, description="Optional highlighted snippets")


class SearchInput(BaseModel):
    query: str
    limit: int = Field(default=10, ge=1, le=50)
    rerank: bool = True
    exclude_pages: bool = False
    alpha: float = Field(default=0.5, ge=0.0, le=1.0)

