# Quick Start

Get semantic search running in your Roam graph.

## One-Click Deploy (Render Free Tier)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/MaskyS/roam-embeddings-search)

**Prerequisites:** Get these keys first, you'll enter them during deploy:
- **Roam API token**: Settings → Graph → API Tokens
- **VoyageAI API key**: [voyageai.com](https://www.voyageai.com)
- **Weaviate Cloud**: [console.weaviate.cloud](https://console.weaviate.cloud) (free tier available)

Then skip to [Install the Extension](#install-the-extension).

---

## Self-Hosted (Docker Compose)

### 1. Get API Keys

- **Roam API token**: Settings → Graph → API Tokens (read-only scope is fine)
- **VoyageAI API key**: [voyageai.com](https://www.voyageai.com) (needs `voyage-context-3` access)
- **Optional**: [Weaviate Cloud](https://console.weaviate.cloud) account (if you want managed hosting)

### 2. Start the Backend

```bash
# Clone and configure
git clone https://github.com/MaskyS/roam-embeddings-search.git
cd roam-embeddings-search
cp .env.example .env
```

Edit `.env`:
```bash
ROAM_GRAPH_NAME=your-graph-slug
ROAM_API_TOKEN=roam-graph-token-xxx
VOYAGEAI_API_KEY=sk-xxx
```

### Choose Your Vector Database

| Local Weaviate | Weaviate Cloud |
|----------------|----------------|
| Runs in Docker on your machine | Managed service, no infrastructure |
| Uses ~2GB RAM + disk | Requires account + API key |
| Good for personal use | Better for production/teams |

**Local Weaviate** (default - no extra config needed):
```bash
docker compose -f docker-compose.prod.yml --profile local-weaviate up -d
```

**Weaviate Cloud** (add these to `.env` first):
```bash
WEAVIATE_CLOUD_URL=https://your-cluster.weaviate.network
WEAVIATE_CLOUD_API_KEY=your-api-key
```
Then:
```bash
docker compose -f docker-compose.prod.yml up -d
```

Wait ~1-2 minutes for the chunker to download ML models, then verify:
```bash
curl http://localhost:8002/   # Should show {"graph": "your-graph", ...}
```

## Install the Extension

1. Open [`roam-semantic-search/extension.js`](roam-semantic-search/extension.js) and copy its contents
2. In Roam, create a block: `{{[[roam/js]]}}`
3. Add a child code block and paste the script
4. Click "Yes, I know what I'm doing"

The extension registers automatically in Roam Depot settings.

## Configure & Sync

1. **Open settings**: Command Palette (`Cmd/Ctrl+P`) → "Semantic Search: Open Settings"
2. **Set Backend URL**: `http://localhost:8002` (or your production URL)
3. **Test connection**: Click "Test Connection" - should show document count
4. **Run initial sync**: Click "Full Sync (All Pages)"
   - Progress displays in the status field
   - First sync takes 5-15 minutes depending on graph size

## Search

1. Command Palette → "Semantic Search"
2. Type your query - results appear after a short delay
3. Navigate with ↑/↓ arrows
4. Press `Enter` to open block, `Shift+Enter` for sidebar

### Search Tips

- Finds content by meaning, not just keywords
- Use the **Alpha slider** to balance keyword (0) vs semantic (1) matching
- Enable **VoyageAI Rerank** for better result ordering
- Toggle **Hide Page Results** to show only blocks

## Keeping in Sync

- **Incremental sync**: Click "Sync Recently Edited Pages" - only processes changes
- **Auto-sync**: Set `AUTO_SYNC_ENABLED=true` and `AUTO_SYNC_TIME=02:00` in `.env`

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Can't connect to backend | Check backend URL in settings; ensure Docker is running |
| No search results | Verify sync completed; check status shows documents |
| Mixed-content error | Roam (HTTPS) requires backend on HTTPS too - use a reverse proxy |
| Sync fails immediately | Check Docker logs: `docker compose logs backend-semantic` |

For detailed configuration options, see the main [README.md](README.md).
