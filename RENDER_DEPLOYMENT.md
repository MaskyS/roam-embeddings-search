# Render Deployment Guide

This guide covers manual deployment of the Roam Semantic Search services to Render.

## Prerequisites

- Render account
- Weaviate Cloud instance
- VoyageAI API key
- Roam Research API token

## Architecture on Render

You'll deploy two services:

1. **chunker** - Text chunking service (internal dependency)
2. **backend-semantic** - Main search and sync API

## Deployment Order

Deploy in this order due to service dependencies:

### 1. Deploy Chunker Service

**Service Configuration:**
- **Name:** `roam-chunker`
- **Environment:** `Docker`
- **Region:** Choose closest to your users
- **Branch:** `main` (or your production branch)
- **Root Directory:** `backend`

**Start Command:**
```bash
uvicorn services.chunker_service:app --host 0.0.0.0 --port 8000
```

**Environment Variables:**
```bash
PYTHONUNBUFFERED=1
# Use VoyageAI for low memory footprint (~150-250MB vs ~600-900MB with local model)
CHUNKER_EMBEDDING_PROVIDER=voyageai
CHUNKER_VOYAGE_MODEL=voyage-3-lite
VOYAGE_API_KEY=<your-voyageai-api-key>
CHUNKER_THRESHOLD=0.6
CHUNKER_CHUNK_SIZE=800
CHUNKER_SKIP_WINDOW=1
CHUNKER_MIN_CHUNK_SIZE=50
```

**Note:** Using `voyageai` provider significantly reduces memory usage. For local model alternative (requires 1GB+ RAM), use:
```bash
CHUNKER_EMBEDDING_PROVIDER=granite
CHUNKER_MODEL=ibm-granite/granite-embedding-small-english-r2
```

**Health Check:**
- Path: `/health`
- Port: `8000`

**Note the internal service URL** after deployment . Click on Connect > Internal to view the internal service URL (e.g., `roam-chunker:8000`).

---

### 2. Deploy Backend Semantic Service

**Service Configuration:**
- **Name:** `roam-backend-semantic`
- **Environment:** `Docker`
- **Region:** Same as chunker
- **Branch:** `main`
- **Root Directory:** `backend`

**Start Command:**
```bash
uvicorn services.search_service:app --host 0.0.0.0 --port 8000 --workers 2
```

**Environment Variables:**
```bash
# Python
PYTHONUNBUFFERED=1

# Roam API
ROAM_API_TOKEN=<your-roam-api-token>
ROAM_GRAPH_NAME=<your-graph-name>

# VoyageAI
VOYAGEAI_API_KEY=<your-voyageai-api-key>

# Weaviate (use Weaviate Cloud)
WEAVIATE_CLOUD_URL=<your-weaviate-cloud-url>
WEAVIATE_CLOUD_API_KEY=<your-weaviate-api-key>
WEAVIATE_COLLECTION_NAME=RoamSemanticChunks

# Chunker Service (use Render internal URL)
CHUNKER_SERVICE_URL=http://roam-chunker:8000
```

**Health Check:**
- Path: `/health`
- Port: `8000`

**Persistent Storage (Disk):**
- **Mount Path:** `/app/data`
- **Size:** 1 GB (or more depending on your graph size)
- This stores sync state and SQLite database

---

## Important Notes

### Service Communication
- Use Render's internal service URLs for inter-service communication
- Format: `http://service-name:8000`
- The backend service needs to reach the chunker via `CHUNKER_SERVICE_URL`

### Port Configuration
- Both services run on port `8000` internally
- Render automatically handles external port mapping
- Don't use `PORT` environment variable unless you need dynamic ports

### Data Persistence
- **CRITICAL:** Add a Render Disk to the backend service at `/app/data`
- Without this, sync state will be lost on every deployment
- Recommended size: 1-5 GB depending on graph size

### Weaviate Configuration
- **Do NOT** deploy Weaviate on Render (use Weaviate Cloud instead)
- Local Weaviate in docker-compose is only for development
- Set `WEAVIATE_CLOUD_URL` and `WEAVIATE_CLOUD_API_KEY` in backend environment

### Workers
- Backend service uses `--workers 2` for better performance
- Chunker uses single worker (default) as it's less critical path
- Adjust based on your plan and load

### Memory Requirements
- **Chunker service with VoyageAI (recommended):** ~150-250MB
- **Chunker service with local Granite model:** ~600-900MB
- **Backend service:** ~300-500MB base + ~100-200MB per worker
- **Recommendation:** Use VoyageAI for chunker on free tier or small instances

### Deployment from Git
- Render will automatically build the Docker image from your repository
- Dockerfile is optimized with `uv` for fast builds
- Build cache is used for dependencies (faster rebuilds)

## Testing Deployment

After deployment, test the services:

### 1. Test Chunker Health
```bash
curl https://your-chunker-url.onrender.com/health
```

### 2. Test Backend Health
```bash
curl https://your-backend-url.onrender.com/
```

### 3. Trigger a Sync
```bash
curl -X POST https://your-backend-url.onrender.com/sync/start
```

### 4. Check Sync Status
```bash
curl https://your-backend-url.onrender.com/sync/status
```

### 5. Test Search
```bash
curl "https://your-backend-url.onrender.com/search?q=test+query"
```

## Troubleshooting

### Build Failures
- Check that `backend/Dockerfile` exists and is correct
- Verify `pyproject.toml` and `uv.lock` are present
- Check Render build logs for specific errors

### Runtime Errors
- Check environment variables are set correctly
- Verify chunker URL is using internal Render URL format
- Check Render logs for both services
- Ensure Weaviate Cloud is accessible

### Sync Issues
- Verify Roam API token and graph name
- Check that persistent disk is mounted at `/app/data`
- Review sync logs: `curl https://your-backend-url/sync/runs`

### Connection Timeouts
- Ensure services are in the same region
- Verify internal service URLs are correct
- Check that services are fully started (health checks passing)

## Cost Optimization

### Free Tier Considerations
- Services spin down after 15 minutes of inactivity
- First request after spin-down will be slow (cold start)
- Consider upgrading for production use

### Paid Plans
- Use smallest instance type that handles your load
- Backend service needs more resources than chunker
- Monitor memory usage and CPU usage in Render dashboard

### Scaling
- Increase workers for backend if needed
- Consider adding more instances for high availability
- Use Render's autoscaling if traffic is variable

## Monitoring

### Built-in Health Checks
Both services have health check endpoints:
- Chunker: `GET /health`
- Backend: `GET /`

### Logs
- View logs in Render dashboard
- Structured JSON logs via `structlog`
- Filter by service name and severity

### Metrics
- Check Render dashboard for CPU, memory, and request metrics
- Monitor sync job duration via `/sync/runs` endpoint
- Track search latency in logs

## Environment-Specific Configuration

### Development vs Production
The same Dockerfile works for both:
- Development: Use docker-compose.yml with hot-reload
- Production: Render builds from Dockerfile with CMD

### Multiple Environments
To deploy staging and production:
1. Create separate Render services for each environment
2. Use different branches or tags
3. Use environment-specific variable values
4. Consider separate Weaviate Cloud instances

## Security

### API Keys
- Store all secrets in Render environment variables
- Never commit API keys to the repository
- Rotate keys periodically

### Network Security
- Use Render's internal networking for service-to-service communication
- Don't expose chunker service publicly (internal only)
- Consider adding authentication to backend endpoints if needed

### Data Security
- Weaviate Cloud handles data encryption
- Render disks are encrypted at rest
- Use HTTPS for all external communication (automatic on Render)
