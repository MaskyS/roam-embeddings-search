# Roam Semantic Search Extension

An extension that lets you run hybrid semantic search inside Roam. It provides a search modal, sync controls, reranking toggles, and status visibility directly from Roam's UI.

![Semantic Search Settings](https://raw.githubusercontent.com/MaskyS/roam-embeddings-search/main/roam-semantic-search/search-settings.png)

![Semantic Search in Action](https://raw.githubusercontent.com/MaskyS/roam-embeddings-search/main/roam-semantic-search/search-results.png)

*The semantic search modal showing results with highlighted matches, similarity scores, and parent context.*

## Main Features

- **Semantic Search Modal** – Find blocks by meaning, not just keywords. Search using natural language queries to discover relevant content across your entire graph.
- **Hybrid Search** – Combines vector similarity with BM25 keyword matching for best-of-both-worlds results. Adjust the alpha slider to balance semantic vs. keyword search.
- **VoyageAI Reranking** – Optional server-side reranking for improved result relevance using state-of-the-art reranking models.
- **In-Roam Sync Controls** – Trigger full syncs, incremental syncs, or limited test syncs directly from the extension settings panel.
- **Real-time Status** – View sync progress, success/failure states, and collection statistics without leaving Roam.
- **Keyboard Navigation** – Fast result browsing with arrow keys, Enter to open in main pane, Shift+Enter for sidebar.
- **Contextual Results** – Each result shows the block text with highlighted matches, parent context, similarity score, and source page.
- **Flexible Configuration** – Customize result limits, search debounce, hybrid search balance, and more from the settings panel.

## Prerequisites

Before loading the extension, make sure you have:
- **Semantic backend running** – See the Installation section below for server setup instructions.
- **Initial sync completed** – Trigger `/sync/start` with `mode: "full"` (and optionally `recreate_collection: true`) so Weaviate has your graph content. New installs must finish at least one successful sync.
- **Browser access to the backend** – If Roam is accessed over HTTPS, expose the backend through HTTPS (reverse proxy) or a trusted tunnel. CORS is already configured server-side for Roam domains and `localhost`.

## Installation

### Step 1: Set Up the Backend Server

You need a running backend server to use this extension. You have two options:

**Option A: Cloud Deployment (Recommended)**
- Quick setup with Render and Weaviate Cloud (~10-15 minutes)
- No local infrastructure required
- **Cost**: ~$60/month (Render + Weaviate Cloud)
- [Follow the Quick Start guide](https://github.com/MaskyS/roam-embeddings-search#quick-start-cloud-deployment) in the main repository

**Option B: Local Development**
- Run everything on your machine using Docker
- Free to run, but requires Docker setup
- Good for development and testing
- [Follow the Local Development guide](https://github.com/MaskyS/roam-embeddings-search#local-development) in the main repository

Once your backend is running, you'll have a URL (e.g., `https://roam-semantic-backend-XXXX.onrender.com` for cloud or `http://localhost:8002` for local).

### Step 2: Install the Extension in Roam

1. Sign in to your Roam Research graph
2. Go to **Settings** → **Roam Depot** → **Installed Extensions**
3. Enable **Developer Mode**
4. Click **Add Extension by URL**
5. Paste this URL: `https://raw.githubusercontent.com/MaskyS/roam-embeddings-search/refs/heads/main/roam-semantic-search/`
6. Click **Add** to install

### Step 3: Configure the Extension

1. Go to **Settings** → **Extension Settings** → **Semantic Search (dev)**
2. Set **Backend URL** to your server URL:
   - Cloud: `https://roam-semantic-backend-XXXX.onrender.com`
   - Local: `http://localhost:8002`
3. Click **Test Connection** to verify it works

You're ready to search! Open the Command Palette (Cmd/Ctrl + P) and type "Semantic Search".

---

**For more information, check out our docs at https://github.com/MaskyS/roam-embeddings-search**

---

## Configuration

Open the command palette (`Cmd/Ctrl+P`) → "Semantic Search: Open Settings" or use the Roam Depot settings drawer. Key settings:
- **Backend URL** – Point this to your deployment (e.g., `http://localhost:8002` or `https://search.example.com`). Changing it updates the API client immediately.
- **Auto-Ping (Render Keep-Alive)** – Automatically pings the backend every 14 minutes when the backend URL is from Render (contains `onrender.com`). This prevents Render's free tier from spinning down after 15 minutes of inactivity. **Disabled by default**. Enable this if you're using Render's free tier.
- **Result Limit** – Maximum rows the modal renders (1–100).
- **Search Delay (ms)** – Debounce between keystrokes and API calls (100–1000ms).
- **Sync Test Page Limit** – Default `limit` used when running "Sync Test Page Limit" mode from the panel.
- **Hide Page Results** – Filters out top-level page hits, returning only block chunks.
- **Hybrid Alpha** – Balance between keyword (0) and semantic vector (1) results.
- **Use VoyageAI Rerank** – Toggles server-side reranking for higher-precision ordering.

The settings panel also displays the current sync status in real time.

## Running searches

1. Open the command palette and choose **Semantic Search** (or use the registered hotkey if you configure one).
2. Type your query; results update after the configured debounce delay.
3. Navigate results with the mouse or arrow keys.
   - `Enter` opens the block in the main pane.
   - `Shift+Enter` opens it in the sidebar.
   - `Esc` closes the modal.
4. Use the in-modal toggles to hide page entries, tweak the hybrid alpha slider, or enable reranking per session.

Each result shows the block text with highlighted matches, the parent context, similarity score, and the source page title.

## Managing sync jobs from Roam

The settings panel exposes backend actions that map to REST endpoints:
- **Test Connection** → `GET /`
- **Sync Recently Edited Pages** → `POST /sync/start` with `mode: "since"`
- **Full Sync (All Pages)** → `POST /sync/start` with `mode: "full"`
- **Run Limited Sync** → `POST /sync/start` with `mode: "limit"` and the configured page count
- **Cancel Sync** → `POST /sync/cancel`
- **Clear Database** → `POST /sync/clear` (drops the Weaviate collection; destructive)

Status updates poll `/sync/status` and display progress, including failures.

## Troubleshooting

- **"Cannot connect to backend"** – Confirm the backend URL in settings, ensure the service is reachable from the browser (`curl -I https://your-backend/`), and check Docker logs for FastAPI startup errors.
- **No search results** – Verify a sync has completed and Weaviate contains data (`GET /` should show a non-zero `collection_count`). Hybrid alpha of `1.0` with no embeddings can also produce empty output; lower it temporarily.
- **Sync jobs fail immediately** – Usually caused by invalid Roam or VoyageAI credentials. Review backend logs for `401` or quota errors.
- **Chunker not ready** – The backend waits for `http://chunker:8003/health`. Make sure the chunker container is healthy before starting a sync.
- **Mixed-content warnings** – Serve the backend over HTTPS when Roam is loaded via HTTPS.

## Development notes

- The extension exports `onload`/`onunload` for Depot compatibility; use `extension.old.js` for prior experiments.
- When iterating locally, keep the backend running with `uvicorn main_semantic:app --reload` on port 8002 so requests succeed.
- Inspect the browser console (`Cmd/Ctrl+Shift+J`) for diagnostic logs prefixed with `[Semantic Search]`.
- **Auto-ping logs**: When auto-ping is enabled, you'll see `[Semantic Search] Auto-ping: <url>` and `[Semantic Search] Ping successful: <data>` messages in the console every 14 minutes. This helps verify the keep-alive mechanism is working.
