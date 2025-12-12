#!/bin/bash
# Startup script for Render deployment
# Generates CHUNKER_SERVICE_URL from CHUNKER_HOSTPORT and starts the backend

set -e

echo "Starting backend service..."

# Generate CHUNKER_SERVICE_URL from CHUNKER_HOSTPORT
if [ -n "$CHUNKER_HOSTPORT" ]; then
    # Extract hostname (everything before the colon)
    CHUNKER_HOST="${CHUNKER_HOSTPORT%%:*}"
    export CHUNKER_SERVICE_URL="https://${CHUNKER_HOST}.onrender.com"
    echo "Generated CHUNKER_SERVICE_URL: $CHUNKER_SERVICE_URL"
else
    echo "WARNING: CHUNKER_HOSTPORT not set, using default"
    export CHUNKER_SERVICE_URL="${CHUNKER_SERVICE_URL:-http://127.0.0.1:8003}"
fi

echo "Starting uvicorn with CHUNKER_SERVICE_URL=$CHUNKER_SERVICE_URL"

# Execute uvicorn (replace the shell process)
exec uvicorn services.search_service:app --host 0.0.0.0 --port 8000
