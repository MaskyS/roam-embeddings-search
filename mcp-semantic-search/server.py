from __future__ import annotations

import asyncio
import logging
import os
from typing import List

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP, Context
from mcp.server.session import ServerSession

from client_backend import BackendClient, from_env
from models import SearchInput, SearchResult


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


# Prompts
@mcp.prompt(
    name="semantic_qna_with_roam_context",
    description=(
        "Optionally use semantic_search to find relevant pages/blocks and, if the Roam MCP is available, "
        "pull a bit of hierarchy for top block hits before answering. Keeps the model in control."
    ),
)
def prompt_semantic_qna_with_roam_context(
    query: str,
    limit: int = 10,
    context_depth: int = 2,
):
    """Generate messages that guide the LLM to run semantic_search and (optionally) enrich with Roam context.

    Parameters:
      - query: User question to answer
      - limit: Number of semantic results to request (default 10)
      - context_depth: Children depth for roam_fetch_block_with_children (default 1)
    """
    sys_text = (
        "You can use tools to help answer the question. A common approach is:\n"
        "• Consider calling semantic_search with the user query (rerank=true, alpha≈0.5). Modest limits (e.g., {limit}) are often enough;\n"
        "  the backend accepts 1≤limit≤50 and 0.0≤alpha≤1.0.\n"
        "• From each hit, you may use: page_title, page_uid, similarity (treat as score), and when document_type≠'page',\n"
        "  uid (as block_uid), chunk_text_preview (as a snippet), and url (a deep link when available).\n"
        "• If a 'roam‑research' MCP server is available and structure would help, you may:\n"
        "  - Use roam_fetch_block_with_children(block_uid, depth≈{context_depth}) to see local children around a top block hit.\n"
        "  - If parent context matters, roam_search_hierarchy(child_uid=block_uid, max_depth≈1) can surface the parent node/page.\n"
        "  - Prefer UIDs over titles; keep actions read‑only (no write tools).\n"
        "  - For page‑only hits (no block_uid), if you're confident you know the exact page title, you may call roam_fetch_page_by_title(title, format='raw'|'markdown') to pull page‑level context. Titles are case‑sensitive; prefer UID‑based navigation elsewhere.\n"
        "• It's fine to group near‑duplicate hits (same page_uid or block_uid) to reduce repetition. If a hit looks like a daily note,\n"
        "  you can mention the date to help orientation.\n"
        "• It's okay to say there isn't enough evidence and suggest a narrower follow‑up. Keep the answer concise, and if you cite,\n"
        "  include: page_title — short snippet — score — url."
    ).format(limit=limit, context_depth=context_depth)

    user_text = f"Question: {query}"
    return [
        {"role": "system", "content": sys_text},
        {"role": "user", "content": user_text},
    ]


@mcp.prompt(
    name="semantic_hits_list",
    description=(
        "Return a compact, ordered list of semantic search hits for a query (page and/or chunk results)."
    ),
)
def prompt_semantic_hits_list(
    query: str,
    limit: int = 10,
    chunks_only: bool = False,
):
    """Generate messages that instruct the LLM to call semantic_search and return an ordered list of hits.

    Parameters:
      - query: Search query
      - limit: Number of results to request (default 10)
      - chunks_only: If true, exclude page-only hits (exclude_pages=true)
    """
    sys_text = (
        "Call semantic_search with: query={query}, rerank=true, alpha=0.5, limit={limit}, exclude_pages={chunks_only}.\n"
        "Return an ordered JSON array of hits with these fields (when present):\n"
        "  - page_title (string)\n"
        "  - page_uid (string)\n"
        "  - block_uid (string | null) — present when the hit is a chunk/block\n"
        "  - block_text (string | null) — snippet from chunk_text_preview\n"
        "  - score (number) — taken from 'similarity'\n"
        "  - url (string | null) — deep link built by this tool\n"
        "No commentary or extra prose; just the list."
    ).format(query=query, limit=limit, chunks_only=str(bool(chunks_only)).lower())

    user_text = f"Query: {query}"
    return [
        {"role": "system", "content": sys_text},
        {"role": "user", "content": user_text},
    ]


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
