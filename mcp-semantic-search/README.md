# Roam Semantic Search MCP Server

A query-only MCP server that enables semantic search across your Roam Research graph using the Model Context Protocol.

## Overview

- Exposes a single MCP tool `semantic_search` that calls your existing FastAPI backend `/search`
- Works with MCP hosts like Claude Desktop via stdio transport
- No sync tools are exposed; this is read/query-only

## Requirements

- Python 3.10+
- Backend running (default `http://localhost:8002`) with `/search` route

## Installation

Using `uv` (recommended):

```bash
cd mcp-semantic-search
uv venv && source .venv/bin/activate
uv sync
```

## Configuration

Create a `.env` file or set environment variables:

- `SEMANTIC_BACKEND_URL` - Backend URL (e.g., `http://localhost:8002`)
- `SEMANTIC_BACKEND_API_KEY` - Optional API key if your backend requires authentication
- `GRAPH_SLUG` - For deep links (e.g., `my-graph`)

## Development

Run with MCP Inspector for testing:

```bash
uv run mcp dev server.py
```

## Claude Desktop Integration

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` and add:

```json
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
```

### Using uvx (after PyPI publish)

After publishing this server to PyPI as `roam-semantic-mcp`, you can run it without cloning using `uvx`:

```json
{
  "mcpServers": {
    "roam-semantic-search": {
      "command": "uvx",
      "args": ["roam-semantic-mcp"],
      "env": {
        "SEMANTIC_BACKEND_URL": "http://localhost:8002",
        "GRAPH_SLUG": "your-graph-slug",
        "SEMANTIC_BACKEND_API_KEY": "optional"
      }
    }
  }
}
```

### Using pipx (alternative)

```json
{
  "mcpServers": {
    "roam-semantic-search": {
      "command": "pipx",
      "args": ["run", "roam-semantic-mcp"],
      "env": {
        "SEMANTIC_BACKEND_URL": "http://localhost:8002",
        "GRAPH_SLUG": "your-graph-slug",
        "SEMANTIC_BACKEND_API_KEY": "optional"
      }
    }
  }
}
```

## Tool Schema

### `semantic_search`

Performs semantic search across your Roam graph.

**Parameters:**
- `query` (str): Search query
- `limit` (int, default=10): Maximum number of results
- `rerank` (bool, default=True): Use VoyageAI reranking for improved relevance
- `exclude_pages` (bool, default=False): Exclude page-level results
- `alpha` (float, default=0.5): Hybrid search balance (0=keyword only, 1=vector only)

**Returns:**
- `List[SearchResult]` with properties:
  - `page_title`: Title of the page
  - `page_uid`: Unique identifier for the page
  - `block_uid`: Block identifier (optional, for block results)
  - `block_text`: Block content (optional, for block results)
  - `score`: Relevance score
  - `url`: Deep link to Roam (optional, when `GRAPH_SLUG` is set)
  - `highlights`: Query match highlights (optional)

## Complementary Tools

This server focuses exclusively on semantic search. For direct Roam API access (creating/updating pages and blocks, structured queries, Datomic queries), consider using [roam-research-mcp](https://github.com/2b3pro/roam-research-mcp) alongside this server. The two MCP servers serve different purposes:

- **This server**: AI-powered semantic search using VoyageAI embeddings and vector similarity
- **roam-research-mcp**: Direct CRUD operations and structured queries against Roam's API

Both can be installed together in Claude Desktop for complementary functionality.

## Notes

- Logging goes to stderr; no stdout prints to keep stdio transport stable
- Per-result deep links are generated when `GRAPH_SLUG` is set
