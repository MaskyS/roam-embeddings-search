# Roam Semantic Search Extension

A Roam Depot–compatible extension that lets you run hybrid semantic search inside Roam by connecting to the backend in this repository. It provides a search modal, sync controls, reranking toggles, and status visibility directly from Roam's UI.

## Prerequisites

Before loading the extension, make sure you have:
- **Semantic backend running** – Follow `../README.md` to launch Weaviate, the chunker service, and `backend/main_semantic.py`. The default local endpoint is `http://localhost:8002`.
- **Initial sync completed** – Trigger `/sync/start` with `mode: "full"` (and optionally `recreate_collection: true`) so Weaviate has your graph content. New installs must finish at least one successful sync.
- **Browser access to the backend** – If Roam is accessed over HTTPS, expose the backend through HTTPS (reverse proxy) or a trusted tunnel. CORS is already configured server-side for Roam domains and `localhost`.

## Installation options

### 1. Inline `roam/js`
1. Open `roam-semantic-search/extension.js` and copy the file contents.
2. In Roam, create a block containing `{{[[roam/js]]}}`.
3. Add a child code block (\`\`\`javascript) and paste the script.
4. Click "Yes, I know what I'm doing" when prompted and refresh the page if necessary.

### 2. Hosted script (e.g., GitHub Gist)
1. Upload `extension.js` to a public location that serves a raw JavaScript file.
2. In Roam, create a `{{[[roam/js]]}}` block.
3. In a child block, add:
   ```javascript
   var s = document.createElement("script");
   s.src = "https://your-hosted-extension.js";
   document.head.appendChild(s);
   ```
4. Reload Roam so the script initializes.

Once the code is loaded, the extension registers in Roam Depot settings and command palette automatically.

## Configuration

Open the command palette (`Cmd/Ctrl+P`) → "Semantic Search: Open Settings" or use the Roam Depot settings drawer. Key settings:
- **Backend URL** – Point this to your deployment (e.g., `http://localhost:8002` or `https://search.example.com`). Changing it updates the API client immediately.
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

For end-to-end setup details, see the repository root `README.md`.
