# Backend Scripts

## setup_chunker_url.sh

Generates the correct `CHUNKER_SERVICE_URL` from `CHUNKER_HOSTPORT` for Render deployments.

### Usage

This script is automatically executed in the render.yaml startCommand:

```bash
source backend/scripts/setup_chunker_url.sh && uvicorn services.search_service:app --host 0.0.0.0 --port 8000
```

### How it Works

**On Render:**
- Input: `CHUNKER_HOSTPORT=roam-semantic-chunker-xyz123:8000` (provided by Render's `fromService`)
- Output: `CHUNKER_SERVICE_URL=https://roam-semantic-chunker-xyz123.onrender.com`

The script:
1. Checks if `CHUNKER_HOSTPORT` is set
2. Extracts the hostname (part before the colon)
3. Constructs the full HTTPS URL with `.onrender.com` suffix
4. Exports `CHUNKER_SERVICE_URL` for use by the backend

**For local development:**
- If `CHUNKER_HOSTPORT` is not set, defaults to `http://chunker:8003` (Docker Compose service name)
- If already a full URL (starts with `http`), uses it as-is

### Environment Variables

**Input:**
- `CHUNKER_HOSTPORT` - Format: `hostname:port` (e.g., `roam-semantic-chunker-xyz123:8000`)

**Output:**
- `CHUNKER_SERVICE_URL` - Full URL to chunker service (e.g., `https://roam-semantic-chunker-xyz123.onrender.com`)

### Why This Is Needed

On Render, services communicate via public HTTPS endpoints, not internal Docker networking. The backend needs to know the full HTTPS URL of the chunker service, but Render only provides the `hostport` (hostname and port).

This script bridges that gap by:
1. Taking Render's `hostport` format
2. Converting it to a full HTTPS URL with the `.onrender.com` domain
3. Making it available as `CHUNKER_SERVICE_URL` environment variable

### Testing

```bash
# Test with Render format
CHUNKER_HOSTPORT="roam-semantic-chunker-xyz123:8000" source backend/scripts/setup_chunker_url.sh
echo $CHUNKER_SERVICE_URL
# Expected: https://roam-semantic-chunker-xyz123.onrender.com

# Test with full URL
CHUNKER_HOSTPORT="https://custom-service.com:8000" source backend/scripts/setup_chunker_url.sh
echo $CHUNKER_SERVICE_URL
# Expected: https://custom-service.com

# Test without CHUNKER_HOSTPORT
unset CHUNKER_HOSTPORT
source backend/scripts/setup_chunker_url.sh
echo $CHUNKER_SERVICE_URL
# Expected: http://chunker:8003 (local default)
```
