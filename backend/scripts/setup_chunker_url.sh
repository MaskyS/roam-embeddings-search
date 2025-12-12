#!/bin/bash
# Script to generate CHUNKER_SERVICE_URL from CHUNKER_HOSTPORT for Render deployment
# CHUNKER_HOSTPORT format: roam-semantic-chunker-t4b0:8000
# CHUNKER_SERVICE_URL format: https://roam-semantic-chunker-t4b0.onrender.com

set -e

if [ -n "$CHUNKER_HOSTPORT" ]; then
    # Check if it already looks like a full URL
    if [[ "$CHUNKER_HOSTPORT" == http* ]]; then
        echo "CHUNKER_HOSTPORT already contains a URL scheme, using as-is"
        # Remove port if present (everything after last colon)
        export CHUNKER_SERVICE_URL="${CHUNKER_HOSTPORT%:*}"
    else
        # Extract hostname (everything before the colon)
        CHUNKER_HOST="${CHUNKER_HOSTPORT%%:*}"
        # Construct the Render URL
        export CHUNKER_SERVICE_URL="https://${CHUNKER_HOST}.onrender.com"
        echo "Generated CHUNKER_SERVICE_URL: $CHUNKER_SERVICE_URL"
    fi
else
    echo "CHUNKER_HOSTPORT not set, using default CHUNKER_SERVICE_URL if available"
fi

# If CHUNKER_SERVICE_URL is still not set, check if we have a default in environment
# Otherwise use localhost for local development
if [ -z "$CHUNKER_SERVICE_URL" ]; then
    # Default to localhost for local development
    export CHUNKER_SERVICE_URL="${CHUNKER_SERVICE_URL:-http://127.0.0.1:8003}"
    echo "Using default CHUNKER_SERVICE_URL: $CHUNKER_SERVICE_URL"
fi

echo "Final CHUNKER_SERVICE_URL: $CHUNKER_SERVICE_URL"
