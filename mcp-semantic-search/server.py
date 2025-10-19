from __future__ import annotations

import asyncio
import logging
import os
from typing import List

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP, Context
from mcp.server.session import ServerSession

from .client_backend import BackendClient, from_env
from .models import SearchInput, SearchResult


# Configure logging to stderr (stdout must remain clean for stdio transport)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("semantic-mcp")

# Eagerly load env from a local .env if present (non-fatal if missing)
load_dotenv(override=False)


mcp = FastMCP(
    name="roam-semantic-search",
    instructions=(
        "Expose a single tool to query the Roam Semantic Search backend. "
        "Use semantic_search to retrieve relevant page and block results."
    ),
)


def _client() -> BackendClient:
    return from_env()


@mcp.tool(structured_output=True)
async def semantic_search(
    query: str,
    limit: int = 10,
    rerank: bool = True,
    exclude_pages: bool = False,
    alpha: float = 0.5,
    ctx: Context[ServerSession, None] | None = None,
) -> List[SearchResult]:
    """Search Roam Semantic index.

    Args:
        query: Search query string.
        limit: Max results to return (default 10).
        rerank: Whether to apply Voyage rerank in backend (default true).
        exclude_pages: If true, return only block/chunk results.
        alpha: Hybrid search balance (0=keyword, 1=vector). Default 0.5.
    Returns:
        List of SearchResult items (structured output).
    """
    # Validate inputs conservatively
    limit = max(1, min(50, int(limit)))
    alpha = 0.0 if alpha < 0.0 else 1.0 if alpha > 1.0 else float(alpha)

    if ctx:
        await ctx.info(f"semantic_search: q='{query[:64]}' limit={limit} rerank={rerank} exclude_pages={exclude_pages} alpha={alpha}")

    params = SearchInput(query=query, limit=limit, rerank=rerank, exclude_pages=exclude_pages, alpha=alpha)
    try:
        results = await _client().search(params)
        return results
    except Exception as e:
        # Surface as a tool error message while keeping stdout clean
        msg = f"Search failed: {e}"
        logger.error(msg)
        # Returning an empty list keeps schema stable while signalling failure via logs
        return []


@mcp.tool()
async def health(ctx: Context[ServerSession, None] | None = None) -> str:
    """Check backend health."""
    try:
        data = await _client().health()
        return str(data)
    except Exception as e:
        if ctx:
            await ctx.warning(f"Health check failed: {e}")
        return "unhealthy"


def main() -> None:
    transport = os.getenv("MCP_TRANSPORT", "stdio").lower()
    if transport not in {"stdio", "streamable-http"}:
        transport = "stdio"
    mcp.run(transport=transport)


if __name__ == "__main__":
    main()

