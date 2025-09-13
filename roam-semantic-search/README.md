# Roam Semantic Search Extension

A Roam Research extension that adds semantic (AI-powered) search capabilities to your graph using embeddings.

## Prerequisites

1. **Backend must be running** on `http://localhost:8001`
   - Make sure Docker containers are up: `docker-compose up -d`
   - Verify by visiting http://localhost:8001 in your browser

2. **Graph must be synced** with embeddings
   - Run sync: `docker exec roam-test-backend-1 python sync_full.py`
   - This needs to be done at least once to populate the vector database

## Installation

### Method 1: Copy & Paste (Quickest)

1. Copy the entire contents of `extension.js`
2. In Roam, create a new block with `{{[[roam/js]]}}`
3. Create a code block underneath (```) 
4. Paste the extension code
5. Click "Yes, I know what I'm doing" when prompted

### Method 2: GitHub Gist

1. Create a new GitHub Gist with the contents of `extension.js`
2. Get the raw URL of the gist
3. In Roam, create a block with:
   ```
   {{[[roam/js]]}}
   ```
4. In a child block, add:
   ```javascript
   var s = document.createElement("script");
   s.src = "YOUR_GIST_RAW_URL";
   document.head.appendChild(s);
   ```

## Usage

### Testing Connection (v0.1)
1. Open Command Palette (Cmd/Ctrl + P)
2. Type "Semantic Search: Test Connection"
3. You should see a success message with your graph name and document count

### Testing Search (v0.2)
1. Open Command Palette (Cmd/Ctrl + P)
2. Type "Semantic Search: Test Query"
3. Enter a search query
4. Check the browser console for detailed results

### Full Search Interface (v0.3)
1. Open Command Palette (Cmd/Ctrl + P)
2. Type "Semantic Search"
3. The search modal will appear
4. Start typing to search (300ms debounce)
5. Click on a result to navigate to that block
6. Shift+Click to open in sidebar
7. Press Escape to close

## Features

- **Real-time search** - Results update as you type
- **Similarity scores** - Visual bars show how relevant each result is
- **Parent context** - See the parent block for context
- **Keyboard navigation** - Use Escape to close
- **Smart navigation** - Click to go to block, Shift+Click for sidebar

## Troubleshooting

### "Cannot connect to backend"
- Make sure Docker is running: `docker ps`
- Check backend is accessible: `curl http://localhost:8001`
- Verify containers are up: `docker-compose up -d`
- CORS is now configured automatically - no additional setup needed

### "No results found"
- Ensure sync has been run: `docker exec roam-test-backend-1 python sync_full.py`
- Try a simpler query
- Check if ChromaDB has documents: `curl http://localhost:8001`

### Modal doesn't appear
- Check browser console for errors
- Make sure roam/js is enabled in your graph
- Try refreshing the page

### CORS Configuration
- **CORS is handled automatically** by the backend
- The backend allows requests from:
  - `https://roamresearch.com` (production)
  - `https://*.roamresearch.com` (subdomains)
  - `https://relemma-git-roam-app-store.roamresearch.com` (Roam Depot dev)
  - `http://localhost:*` (local development)
- If you still get CORS errors, check backend logs: `docker logs roam-test-backend-1`

## Development

### Current Version: v0.3
- ✅ v0.1: Test connection command
- ✅ v0.2: Basic search with console output
- ✅ v0.3: Floating modal with results display
- ⏳ v0.4: Keyboard navigation (arrow keys)
- ⏳ v0.5: Dark mode support
- ⏳ v0.6: Settings panel

### Project Structure
```
roam-semantic-search/
├── extension.js    # Main extension code
├── extension.css   # Styles (future)
└── README.md      # This file
```

### Testing Workflow
1. Make changes to `extension.js`
2. Copy updated code to Roam
3. Refresh the page or re-run the roam/js block
4. Test the changes

## Notes

- The extension currently connects to `localhost:8001` (hardcoded)
- Search limit is set to 20 results
- Debounce delay is 300ms
- No data is stored locally (stateless)