# Roam Semantic Search

Add powerful semantic search to your Roam Research graph. This system ingests your Roam pages into a vector database using AI embeddings, letting you find relevant notes by meaning rather than just keywords. Includes a FastAPI backend, optional auto-sync, and a Roam extension for in-app search.

## Quick Start (Cloud Deployment)

Deploy to the cloud in **10-15 minutes** with no local setup required. This is the recommended approach for most users.

### What You'll Need

Before deploying, gather these API keys and accounts:

1. **Roam API token**
   - You must be an admin of your Roam graph
   - Generate under *Settings ▸ Graph ▸ API Tokens*
   - Use "read-only" or "read+edit" role
   - [Roam API documentation](https://roamresearch.com/#/app/developer-documentation/page/W4Po8pcHQ)

2. **VoyageAI API key**
   - Sign up at [voyageai.com](https://www.voyageai.com)
   - Create a key with access to `voyage-context-3` and `rerank-2-lite`

3. **Weaviate Cloud account** (required for cloud deployment)
   - Sign up at [console.weaviate.cloud](https://console.weaviate.cloud)
   - Create a cluster using the [Weaviate Cloud Quickstart](https://docs.weaviate.io/cloud/quickstart)
   - Create an API key with **Admin** role
   - Note your cluster's **REST URL** (e.g., `https://your-cluster.weaviate.network`)
   - **Cost**: Flex Plan starts at $45/month (free tier keeps database for 14 days only)

4. **Render account with billing**
   - Sign up at [render.com](https://render.com)
   - Add billing information (credit card required)
   - **Cost**: ~$15/month (2 Starter instances + 1GB disk)

**Total monthly cost**: ~$60 (Render + Weaviate Cloud)

### Deploy to Render

1. Click the deploy button below:

   [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/MaskyS/roam-embeddings-search)

2. Render will prompt for environment variables. Fill them in:
   - `ROAM_GRAPH_NAME` - Your Roam graph slug (from your graph URL)
   - `ROAM_API_TOKEN` - Your Roam API token (starts with `roam-graph-token-`)
   - `VOYAGEAI_API_KEY` - Your VoyageAI API key
   - `VOYAGE_API_KEY` - Same as `VOYAGEAI_API_KEY` (used by chunker)
   - `WEAVIATE_CLOUD_URL` - Your Weaviate cluster REST URL
   - `WEAVIATE_CLOUD_API_KEY` - Your Weaviate API key (admin role)

3. Click **Apply** to deploy both services:
   - `roam-semantic-chunker` - Text chunking service
   - `roam-semantic-backend` - Main search & sync API

4. Wait 5-10 minutes for deployment to complete
   - Both services should show "Live" status
   - Check logs if deployment fails

### Get Your Backend URL

Once deployed:

1. In your Render dashboard, click **roam-semantic-backend**
2. Copy the URL at the top (format: `https://roam-semantic-backend-XXXX.onrender.com`)
3. Save this URL - you'll need it for the Roam extension configuration

> **Detailed deployment guide:** [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)

### Trigger Initial Sync

Populate your vector database with your Roam graph:

```bash
# Replace <YOUR-BACKEND-URL> with your actual Render URL
curl -X POST https://roam-semantic-backend-XXXX.onrender.com/sync/start \
  -H 'Content-Type: application/json' \
  -d '{"mode": "full", "recreate_collection": true}'
```

Monitor sync progress:
```bash
# Check sync status
curl https://roam-semantic-backend-XXXX.onrender.com/sync/status

# View recent sync runs
curl https://roam-semantic-backend-XXXX.onrender.com/sync/runs
```

The sync will:
1. Fetch all page UIDs from your Roam graph
2. Pull page content and detect changes
3. Break pages into semantic chunks
4. Generate embeddings with VoyageAI
5. Store in Weaviate for hybrid search

**First sync timing**: Depends on your graph size (expect 5-20 minutes for most graphs)

**Cancel if needed:**
```bash
curl -X POST https://roam-semantic-backend-XXXX.onrender.com/sync/cancel
```

### Install the Roam Extension

#### Enable Developer Mode

1. Sign in to your Roam Research graph
2. Go to **Settings** → **Roam Depot** → **Installed Extensions**
3. Enable **Developer Mode**

#### Install the Extension

1. In Roam Depot, click **Add Extension by URL**
2. Paste this URL: `https://raw.githubusercontent.com/MaskyS/roam-embeddings-search/refs/heads/main/roam-semantic-search/`
3. Click **Add** to install the extension

> **Note**: This URL points to the latest version on the `main` branch. The extension will auto-update when you refresh Roam.

#### Configure the Extension

1. Go to **Settings** → **Extension Settings** → **Semantic Search (dev)**
2. Set **Backend URL** to your Render URL (e.g., `https://roam-semantic-backend-XXXX.onrender.com`)
   - For local development, use `http://localhost:8002` instead
3. Adjust settings as needed:
   - Result limits (default: 10 blocks, 5 pages)
   - Enable/disable VoyageAI reranking
   - Search alpha (hybrid search balance: 0=keyword only, 1=vector only)

#### Test the Connection

1. In the extension settings, click **Test Connection** button
2. Should confirm collection exists and show document count
3. If connection fails, verify the backend URL and check that services are running

#### Start Searching

1. Open Command Palette (Cmd/Ctrl + P)
2. Type "Semantic Search"
3. Enter your query and press Enter
4. Use ↑/↓ arrows to navigate results, Enter to open block in Roam

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
- **Auto-Ping (Render Keep-Alive)** – Enable this toggle if using Render's free tier. Automatically pings the backend every 14 minutes to prevent the service from spinning down after 15 minutes of inactivity. Only activates when the backend URL contains `onrender.com`. Disabled by default.

### Search Tips
- Searches find semantically similar content, not just keyword matches
- Better for concepts and questions than exact phrase matching
- Results show context (parent block) and link directly to Roam blocks

---

## Local Development

For developers who want to run the system locally or modify the code.

### System Requirements

**1. Docker**
   - Check: `docker --version` (should show v24.0 or higher)
   - Check: `docker compose version` (should show v2.x)
   - If not installed: [Get Docker](https://docs.docker.com/get-docker/)

**2. Git**
   - Check: `git --version`
   - If not installed: [Install Git](https://git-scm.com/downloads)

**3. curl** (for API testing)
   - Check: `curl --version`
   - Usually pre-installed on Mac/Linux
   - Windows: Use PowerShell or [install curl](https://curl.se/download.html)

### Get the Code

Clone this repository:

```bash
git clone https://github.com/MaskyS/roam-embeddings-search.git
cd roam-embeddings-search
```

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
   | ✅ No signup required | ✅ Managed hosting |
   | ✅ Runs in Docker | ✅ High availability |
   | ✅ Good for development | ✅ Better for production |
   | ⚠️ Uses ~2GB RAM + disk | ⚠️ Requires account ($45/mo) |

   **For Local Weaviate** (default): Skip to Deploy step.

   **For Weaviate Cloud**:
   - Create cluster at [console.weaviate.cloud](https://console.weaviate.cloud)
   - Add to `.env`:
     ```bash
     WEAVIATE_CLOUD_URL=https://your-cluster.weaviate.network
     WEAVIATE_CLOUD_API_KEY=your-weaviate-api-key
     ```

### Deploy Locally

**Option 1: Pre-built images (recommended)**

```bash
# With local Weaviate
docker compose -f docker-compose.prod.yml --profile local-weaviate up -d

# With Weaviate Cloud (no local database)
docker compose -f docker-compose.prod.yml up -d
```

**Option 2: Build from source** (for development)

```bash
# Build images (takes 5-10 minutes first time)
docker compose build chunker backend-semantic

# Launch with local Weaviate
docker compose --profile local-weaviate up -d

# Or with Weaviate Cloud
docker compose up -d chunker backend-semantic
```

### Verify Services

```bash
# Health checks
curl http://localhost:8003/health          # chunker
curl http://localhost:8002/                # backend

# View logs
docker compose logs -f chunker backend-semantic

# Add weaviate if using local
docker compose logs -f chunker backend-semantic weaviate
```

Expected endpoints:
- Backend API: `http://localhost:8002`
- Chunker: `http://localhost:8003`
- Weaviate (local only): `http://localhost:8080`

> **Note**: First chunker startup downloads ML models (~1-2 minute delay).

### Trigger Initial Sync

```bash
curl -X POST http://localhost:8002/sync/start \
  -H 'Content-Type: application/json' \
  -d '{"mode": "full", "recreate_collection": true}'
```

Monitor progress:
```bash
# Watch sync status
watch -n5 "curl -s http://localhost:8002/sync/status | jq"

# Or check recent runs
curl http://localhost:8002/sync/runs | jq
```

**Cancel if needed:**
```bash
curl -X POST http://localhost:8002/sync/cancel
```

### Development Tips

Development compose file (`docker-compose.yml`):
- Source code mounted for live editing
- Single-worker backend with auto-reload
- Verbose logging

Production compose file (`docker-compose.prod.yml`):
- Multi-worker backend (4 workers)
- Healthchecks and auto-restart
- Pre-built images from GitHub Container Registry

---

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

### Self-Hosted Production Deployment

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
- **Local**: Check logs with `docker compose logs chunker`
- **Render**: Check logs in Render dashboard for `roam-semantic-chunker`
- Ensure service has ~2GB RAM available (512MB minimum)

**Weaviate rejects writes**
- Confirm reranker module is enabled (automatic in our schema)
- Check that `X-VoyageAI-Api-Key` header is passed (logged in backend)
- Re-run sync with `"recreate_collection": true` if schema changed

**Extension can't reach backend**
- If Roam is HTTPS, backend must be HTTPS too (browser mixed-content policy)
  - Render URLs are HTTPS by default ✅
  - Local development requires reverse proxy for HTTPS
- Check CORS: backend allows all origins by default
- Test backend directly:
  - **Local**: `curl http://localhost:8002/`
  - **Render**: `curl https://roam-semantic-backend-XXXX.onrender.com/`

**Sync state not persisting** (Local deployments)
- Ensure `backend/data/` is persisted (volume or bind mount)
- Without persistence, each restart requires full sync
- **Render**: Persistent disk is configured automatically in `render.yaml`

**Empty or missing results**
- Verify sync completed: `curl <YOUR-BACKEND-URL>/sync/runs`
- Check collection has documents: `curl <YOUR-BACKEND-URL>/` (shows count)
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

### Backend API Endpoints

- **GET /ping** - Keep-alive endpoint that pings both backend and chunker service. Returns status of both services. Useful for preventing free tier services (like Render) from spinning down.
- **GET /health** - Simple health check for the backend service only.
- **GET /** - Returns backend status, Weaviate readiness, and collection statistics.
- **GET /search** - Hybrid semantic search (query parameters: `q`, `limit`, `alpha`, `exclude_pages`, `rerank`).
- **POST /sync/start** - Start a sync job (body: `mode`, `limit`, `recreate_collection`).
- **POST /sync/cancel** - Cancel a running sync job.
- **GET /sync/status** - Get current sync job status and progress.
- **GET /sync/runs** - List recent sync runs from database.
- **POST /sync/clear** - Clear all documents from Weaviate (destructive).
- **GET /sync/schedule** - Get auto-sync schedule configuration.
- **POST /sync/schedule** - Update auto-sync schedule (body: `enabled`, `schedule_time`, `timezone`).

### Source Code

- **Backend source**: `backend/` (see `services/`, `sync/`, `clients/`, `common/`)
- **CLI sync**: `backend/cli/sync.py` (run sync outside API)
- **Roam extension**: `roam-semantic-search/extension.js`
- **Roam API docs**: `docs/external/roam_research/roam-backend-api.md`
- **VoyageAI context models**: `docs/external/voyageai/context-model-guide.md`
- **Chunker config**: `backend/services/chunker_service.py`

---

**Contributing**: Open issues or PRs on GitHub. For questions, check existing issues or start a discussion.

**License**: [Add your license here]
