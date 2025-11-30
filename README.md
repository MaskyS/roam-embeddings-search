# Roam Semantic Search

Add powerful semantic search to your Roam Research graph. This system ingests your Roam pages into a vector database using AI embeddings, letting you find relevant notes by meaning rather than just keywords. Includes a FastAPI backend, optional auto-sync, and a Roam extension for in-app search.

## Before You Begin

### System Requirements Checklist

Verify you have these tools installed:

**1. Docker**
   - Check: `docker --version` (should show v24.0 or higher)
   - Check: `docker compose version` (should show v2.x)
   - If not installed: [Get Docker](https://docs.docker.com/get-docker/) (includes Docker Compose)

**2. Git** (for downloading the code)
   - Check: `git --version`
   - If not installed: [Install Git](https://git-scm.com/downloads)

**3. curl** (for API testing)
   - Check: `curl --version`
   - Usually pre-installed on Mac/Linux
   - Windows users: Use PowerShell (built-in) or [install curl](https://curl.se/download.html)

### Get the Code

Clone this repository and navigate into it:

```bash
git clone https://github.com/MaskyS/roam-embeddings-search.git
cd roam-embeddings-search
```

> **Troubleshooting**: If `git clone` fails, verify git is installed and you have network access. All following commands assume you're in the `roam-embeddings-search` directory.

---

## Quick Start

Get running in **5-10 minutes** (after completing setup above).

### API Keys & Accounts

You'll need these before starting:

1. **Roam graph token** – Generate under *Settings ▸ Graph ▸ API Tokens* (read-only or read+edit scope)
2. **VoyageAI API key** – Sign up at [voyageai.com](https://www.voyageai.com) and create a key with access to `voyage-context-3` and `rerank-2-lite`
3. **Optional: Weaviate Cloud account** – Only if you prefer managed hosting over local vector database ([console.weaviate.cloud](https://console.weaviate.cloud))

### Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and fill in your credentials:
   ```bash
   # Required
   ROAM_GRAPH_NAME=your-graph-slug
   ROAM_API_TOKEN=roam-graph-token-XXXXXXXX
   VOYAGEAI_API_KEY=sk-your-voyage-key
   ```

3. **Choose: Local Weaviate or Weaviate Cloud**

   | **Local Weaviate** | **Weaviate Cloud** |
   |--------------------|--------------------|
   | ✅ No signup required | ✅ Managed, no infrastructure |
   | ✅ Runs in Docker on your machine | ✅ High availability + backups |
   | ✅ Good for development & personal use | ✅ Better for production teams |
   | ⚠️ Uses ~2GB RAM + disk space | ⚠️ Requires account + API key |

   **For Local Weaviate** (default): Your `.env` is already configured correctly. Skip to Deploy step.

   **For Weaviate Cloud**:
   - Sign up at [console.weaviate.cloud](https://console.weaviate.cloud) and create a cluster
   - Add these to your `.env` (replace cluster URL and key):
     ```bash
     WEAVIATE_CLOUD_URL=https://your-cluster.weaviate.network
     WEAVIATE_CLOUD_API_KEY=your-weaviate-cloud-api-key
     ```

### Deploy

**Option 1: Pre-built images (recommended)** – Instant startup, tested builds

```bash
# With local Weaviate
docker compose -f docker-compose.prod.yml --profile local-weaviate up -d

# With Weaviate Cloud (no local database)
docker compose -f docker-compose.prod.yml up -d
```

**Option 2: Build from source** – Only if you're modifying the code

```bash
# Build images (takes 5-10 minutes first time)
docker compose build chunker backend-semantic

# Launch with local Weaviate
docker compose --profile local-weaviate up -d

# Or with Weaviate Cloud
docker compose up -d chunker backend-semantic
```

### Verify Services

Check that everything is running:

```bash
# Health checks
curl http://localhost:8003/health          # chunker ready
curl http://localhost:8002/                # backend (shows graph + doc count)

# View logs
docker compose logs -f chunker backend-semantic

# Add 'weaviate' to logs command if using local Weaviate
docker compose logs -f chunker backend-semantic weaviate
```

Expected endpoints:
- Backend API: `http://localhost:8002`
- Chunker: `http://localhost:8003`
- Weaviate (local only): `http://localhost:8080`

> **Note**: First chunker startup downloads ML models (~1-2 minute delay).

### Initial Sync

Populate the vector database with your Roam graph:

```bash
# Trigger full sync (creates collection and indexes all pages)
curl -X POST http://localhost:8002/sync/start \
  -H 'Content-Type: application/json' \
  -d '{"mode": "full", "recreate_collection": true}'
```

Monitor progress:
```bash
# Watch sync status (press Ctrl+C to stop watching)
watch -n5 "curl -s http://localhost:8002/sync/status | jq"

# Or check recent runs
curl http://localhost:8002/sync/runs | jq
```

The sync will:
1. Fetch all page UIDs from your Roam graph
2. Pull page content and detect changes (skips unchanged pages on future syncs)
3. Break pages into semantic chunks
4. Generate embeddings with VoyageAI
5. Store in Weaviate for hybrid search

**Cancel if needed:**
```bash
curl -X POST http://localhost:8002/sync/cancel
```

### Install the Roam Extension

1. Open `roam-semantic-search/extension.js` and copy its contents

2. In Roam, paste the script:
   - **Option A**: Create a block with `{{[[roam/js]]}}` and paste code as a child block, or
   - **Option B**: Host on GitHub Gist/CDN and load via `<script src="...">` tag

3. Configure the extension:
   - Open Command Palette → "Semantic Search: Open Settings" (or use Roam Depot settings)
   - Set **Backend URL** to `http://localhost:8002` (or your production URL)
   - Adjust settings as needed:
     - Result limits (default: 10 blocks, 5 pages)
     - Enable/disable VoyageAI reranking
     - Search alpha (hybrid search balance)

4. Test the connection:
   - Click **Test Connection** button in settings
   - Should confirm collection exists and show document count

5. Start searching:
   - Command Palette → "Semantic Search"
   - Type your query and press Enter
   - Use ↑/↓ to navigate, Enter to open block in Roam

## Using the Extension

### Search Interface
- **Command Palette**: Type "Semantic Search" to open modal
- **Keyboard navigation**: ↑/↓ arrows to browse results, Enter to open
- **Filtering**: Toggle "Hide Page Results" to show only blocks
- **Reranking**: Enable "Use VoyageAI Rerank" for better relevance (uses more API calls)

### Sync Controls
Built-in buttons in extension settings:
- **Sync Recently Edited Pages** – Incremental sync (only changed pages)
- **Full Sync** – Re-index entire graph (use sparingly)
- **Clear Database** – Deletes all vectors (destructive, requires full sync after)

### Search Tips
- Searches find semantically similar content, not just keyword matches
- Better for concepts and questions than exact phrase matching
- Results show context (parent block) and link directly to Roam blocks

## Advanced

### Auto-Sync Scheduling

Run incremental syncs automatically at a scheduled time:

```bash
# In your .env
AUTO_SYNC_ENABLED=true
AUTO_SYNC_TIME=02:00          # 2 AM local time (24-hour format)
```

> **Note**: Uses the system's local timezone automatically. In Docker containers, this defaults to UTC unless you set the `TZ` environment variable (e.g., `TZ=America/Los_Angeles`).

Or trigger syncs via cron/automation:
```bash
# Incremental sync (uses last run's timestamp automatically)
curl -X POST http://localhost:8002/sync/start \
  -H 'Content-Type: application/json' \
  -d '{"mode": "since"}'
```

### Tuning Parameters

Advanced settings in `.env` (defaults work well for most graphs):

```bash
# Chunking behavior
CHUNKER_EMBEDDING_PROVIDER=voyageai     # or 'granite' (no API calls)
CHUNKER_VOYAGE_MODEL=voyage-3-lite
CHUNKER_THRESHOLD=0.6                   # semantic similarity threshold
CHUNKER_CHUNK_SIZE=800                  # target characters per chunk
CHUNKER_MIN_CHUNK_SIZE=50

# Pipeline concurrency
ROAM_MAX_REQUESTS_PER_MINUTE=50         # respect Roam rate limits
CHUNKER_CONCURRENCY=1
CHUNKER_GROUP_SIZE=16
VOYAGE_CONCURRENCY=4
WEAVIATE_WRITE_CONCURRENCY=1

# Persistence
SEMANTIC_SYNC_DB=/app/data/semantic_sync.db
SYNC_STATE_FILE=/app/data/sync_state.json
```

**Tip**: Persist `backend/data/` to keep incremental sync state across container restarts.

### Building from Source

For developers modifying the code:

```bash
# Build images (includes ML models, takes 5-10 minutes)
docker compose build chunker backend-semantic

# Launch (with local Weaviate)
docker compose --profile local-weaviate up -d

# Or use docker-compose.yml for development (hot reload)
docker compose up -d
```

> **Note**: If you haven't cloned the repository yet, see the "Before You Begin" section above.

Development compose file (`docker-compose.yml`) includes:
- Source code mounted for live editing
- Single-worker backend with reload
- Verbose logging

Production compose file (`docker-compose.prod.yml`) optimizes for:
- Multi-worker backend (4 workers)
- Healthchecks and auto-restart
- Pre-built images from GitHub Container Registry

### Production Deployment

#### Security
- **Reverse proxy**: Use nginx/Caddy/Traefik to terminate TLS and authenticate requests
- **Network isolation**: Restrict ports 8002, 8003, and 8080 to trusted networks
- **Secrets management**: Store API keys in a vault, not `.env` files in repos

#### TLS/HTTPS
- Terminate HTTPS in a reverse proxy
- Forward to backend on `localhost:8002`
- Update extension's **Backend URL** to your public HTTPS domain

#### Monitoring
- Watch container logs for errors: `docker compose logs -f`
- Common issues: VoyageAI quota exhausted, Roam rate limits, connection failures
- Consider scraping `/sync/status` endpoint for metrics

#### Backups
Snapshot these directories regularly:
- `weaviate_data/` – Vector database (local Weaviate only)
- `backend/data/` – Sync state and run history

#### Resource Sizing
- **CPU**: Embedding is CPU-intensive (especially for large graphs)
- **RAM**: ~4GB recommended (2GB for chunker, 2GB for backend/Weaviate)
- **Network**: Allow outbound HTTPS to:
  - `api.roamresearch.com` (graph data)
  - `api.voyageai.com` (embeddings)

## Troubleshooting

**401/403 from Roam API**
- Verify `ROAM_GRAPH_NAME` matches your graph slug (from Roam URL)
- Re-generate token under Settings ▸ Graph ▸ API Tokens
- Ensure token starts with `roam-graph-token-`

**VoyageAI errors (quota/rate limit)**
- Check your VoyageAI dashboard for quota usage
- Confirm key has access to `voyage-context-3` and `rerank-2-lite`
- For chunker, switch to `CHUNKER_EMBEDDING_PROVIDER=granite` to avoid VoyageAI calls

**Chunker not responding**
- First startup downloads models (~1-2 minutes)
- Check logs: `docker compose logs chunker`
- Ensure container has ~2GB RAM available

**Weaviate rejects writes**
- Confirm reranker module is enabled (automatic in our schema)
- Check that `X-VoyageAI-Api-Key` header is passed (logged in backend)
- Re-run sync with `"recreate_collection": true` if schema changed

**Extension can't reach backend**
- If Roam is HTTPS, backend must be HTTPS too (browser mixed-content policy)
- Check CORS: backend allows all origins by default
- Test backend directly: `curl http://localhost:8002/`

**Sync state not persisting**
- Ensure `backend/data/` is persisted (volume or bind mount)
- Without persistence, each restart requires full sync

**Empty or missing results**
- Verify sync completed: `curl http://localhost:8002/sync/runs`
- Check collection has documents: `curl http://localhost:8002/` (shows count)
- Try simple queries first: "test", "March", specific page titles

## How It Works

### Architecture Overview

The system has four main components:

1. **Search + Sync API** (`backend/services/search_service.py`)
   - FastAPI service that orchestrates semantic sync
   - Talks to chunker, embeds with VoyageAI, writes/queries Weaviate
   - Exposes `/sync/*` management endpoints and `/search` for the extension

2. **Chunker microservice** (`backend/services/chunker_service.py`)
   - Keeps a warm `chonkie` semantic chunker process
   - Breaks Roam pages into semantically coherent chunks
   - Avoids cold-start latency during sync

3. **Weaviate vector database**
   - Stores `RoamSemanticChunks` collection with embeddings
   - Hybrid search: vector similarity + BM25 keyword matching
   - VoyageAI reranker module for improved relevance

4. **Roam extension** (`roam-semantic-search/extension.js`)
   - Runs inside Roam browser environment
   - Provides search modal, sync controls, and settings UI
   - Communicates with backend API over HTTP

5. **Persistent state** (`backend/data/semantic_sync.db`)
   - SQLite cache backing incremental sync
   - Tracks page edit times and content hashes
   - Stores run history and sync cursors

### Request Flow

**Sync pipeline:**
1. List all page UIDs from Roam Backend API (uses your graph token)
2. Metadata prepass: fetch each page's max edit time and title
3. Filter unchanged pages (compares against cached edit times)
4. Pull full content for changed pages
5. Childless pages (title-only) bypass chunker and embed directly
6. Pages with children are chunked semantically, then embedded
7. Write embeddings + metadata to Weaviate with content hash
8. Delete stale objects from previous runs (hash mismatch)

**Search flow:**
1. Extension sends query to `/search` endpoint
2. Backend embeds query with VoyageAI
3. Weaviate runs hybrid search (vector + BM25)
4. Optional: Rerank results with VoyageAI reranker
5. Return formatted results with block context and highlights

### Change Detection Strategy

Roam pages don't update their `:edit/time` when children change, so we aggregate the maximum block edit timestamp while walking each page. Incremental syncs skip a page when its aggregated edit time hasn't increased. Content hashes prevent duplicates and safely delete stale chunks.

### Childless Page Optimization

For pages without children, all content lives in `:node/title`. The pipeline skips the second Roam pull and chunker entirely, embedding only the page object. This saves API calls and chunker latency for ~30-50% of typical graphs.

## Reference

- **Backend source**: `backend/` (see `services/`, `sync/`, `clients/`, `common/`)
- **CLI sync**: `backend/cli/sync.py` (run sync outside API)
- **Roam extension**: `roam-semantic-search/extension.js`
- **Roam API docs**: `docs/external/roam_research/roam-backend-api.md`
- **VoyageAI context models**: `docs/external/voyageai/context-model-guide.md`
- **Chunker config**: `backend/services/chunker_service.py`

---

**Contributing**: Open issues or PRs on GitHub. For questions, check existing issues or start a discussion.

**License**: [Add your license here]
