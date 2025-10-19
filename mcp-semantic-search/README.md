Roam Semantic Search MCP Server (Query-only)

Overview
- Exposes a single MCP tool `semantic_search` that calls your existing FastAPI backend `/search`.
- Works with MCP hosts like Claude Desktop via stdio transport.
- No sync tools are exposed; this is read/query-only.

Requirements
- Python 3.10+
- Backend running (default http://localhost:8002) with `/search` route

Install (uv recommended)
1) cd mcp-semantic-search
2) uv venv && source .venv/bin/activate
3) uv sync

Config
- Create `.env` or set env vars:
  - `SEMANTIC_BACKEND_URL` (e.g., http://localhost:8002)
  - `SEMANTIC_BACKEND_API_KEY` (optional, if your backend requires it)
  - `GRAPH_SLUG` (for deep links, e.g., my-graph)

Run with MCP Inspector
  uv run mcp dev server.py

Claude Desktop Integration
Edit `~/Library/Application Support/Claude/claude_desktop_config.json` and add:

{
  "mcpServers": {
    "roam-semantic-search": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/REPO/mcp-semantic-search",
        "run",
        "server.py"
      ],
      "env": {
        "SEMANTIC_BACKEND_URL": "http://localhost:8002",
        "GRAPH_SLUG": "your-graph-slug"
      }
    }
  }
}

Tool Schema
- `semantic_search(query: str, limit: int=10, rerank: bool=True, exclude_pages: bool=False, alpha: float=0.5) -> List[SearchResult]`
- SearchResult: { page_title, page_uid, block_uid?, block_text?, score, url?, highlights?[] }

Notes
- Logging goes to stderr; no stdout prints to keep stdio transport stable.
- Per-result deep links are generated when `GRAPH_SLUG` is set.

