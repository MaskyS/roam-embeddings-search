# Roam Semantic Search Project Context

## Project Overview
Building a semantic search system for Roam Research using VoyageAI embeddings, Weaviate vector database, and hybrid search (BM25 + vector similarity).

## Current Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     FastAPI Backend                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Search    │  │    Sync     │  │  Scheduler  │         │
│  │  Service    │  │   Service   │  │   Service   │         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │
└─────────┼────────────────┼────────────────┼─────────────────┘
          │                │                │
          ▼                ▼                ▼
┌─────────────────────┐    ┌─────────────────────┐
│   VoyageAI API      │    │   Roam Research     │
│ (voyage-context-3)  │    │      API            │
└─────────────────────┘    └─────────────────────┘
          │
          ▼
┌─────────────────────┐    ┌─────────────────────┐
│   Weaviate          │    │   Chunker Service   │
│   (Vector DB)       │    │   (Chonkie)         │
└─────────────────────┘    └─────────────────────┘
```

## How to Get Oriented

### 1. Read Core Documentation First
- `/docs/external/roam_research/roam-backend-api.md` - Official Roam Backend API
- `/docs/external/roam_research/roam-frontend-api.md` - Official Roam Frontend API
- `/docs/external/voyageai/` - VoyageAI contextualized embeddings guide
- `/docs/architecture.md` - System architecture diagrams
- `/docs/sync-state-machine.md` - Sync job state transitions

### 2. Understand the Sync Pipeline
The sync pipeline has evolved significantly. Current implementation:
- `/backend/sync/orchestrator.py` - High-level sync coordination
- `/backend/sync/pipeline/batch_phase.py` - Token-aware batch processing
- `/backend/sync/pipeline/metadata_phase.py` - Incremental sync filtering
- `/backend/sync/pipeline/stages/` - Individual pipeline stages (chunk, embed, write)

### 3. Check Current Implementation
- `/backend/services/search_service.py` - FastAPI app with search + sync endpoints
- `/backend/services/sync_service.py` - Sync management API router
- `/backend/services/scheduler.py` - Auto-sync scheduling
- `/backend/clients/` - External service clients (Roam, VoyageAI, Weaviate, Chunker)
- `/docker-compose.yml` - Container orchestration (backend, chunker, weaviate)

## Key Design Principles

### Adaptive Context Strategy
- **Parent blocks**: Concatenated with children as single embedding
- **Leaf blocks**: Include parent context and sibling sliding window
- This is THE core innovation - Roam's power comes from context, not isolated text

### Token-Aware Segmentation
The sync pipeline automatically handles VoyageAI token limits:
- **Per-document**: 32K tokens max (with 3% safety margin)
- **Per-request**: 120K tokens max (with 8% safety margin)
- Large pages are segmented and processed in round-robin order

### API Usage Patterns
- **Pull-many over individual pulls** for efficiency
- **30-second timeout** on Roam API calls
- **50 requests/minute** rate limit per graph
- **String format for eids** in pull-many (Clojure syntax)

### Data Quality
- **Skip empty blocks** (no :block/string or :node/title)
- **Handle pages differently** (they have :node/title, not :block/string)
- **Content hashing** for incremental sync

## Development Workflow

### To Run the System
1. Ensure Docker is running
2. Check `.env` has required keys:
   - `ROAM_API_TOKEN` - Roam graph token
   - `ROAM_GRAPH_NAME` - Your graph name
   - `VOYAGEAI_API_KEY` - VoyageAI API key
   - Optional: `WEAVIATE_CLOUD_URL` and `WEAVIATE_CLOUD_API_KEY` for cloud deployment
3. `docker-compose up -d` to start services
4. Trigger sync via API: `curl -X POST http://localhost:8002/sync/start`
5. Test search: `curl "http://localhost:8002/search?q=your+query"`

### To Understand Search Implementation
1. Read the search endpoint in `/backend/services/search_service.py`
2. Note the hybrid search (alpha parameter: 0=keyword, 1=vector)
3. Understand result enrichment (pulls fresh data after vector search)
4. VoyageAI reranking for improved relevance

### To Debug Issues
- Check sync status: `curl http://localhost:8002/sync/status`
- View sync history: `curl http://localhost:8002/sync/runs`
- Check health: `curl http://localhost:8002/`
- Logs are in JSON format via structlog

## Current State

### Completed
- ✅ Full graph sync with adaptive context
- ✅ VoyageAI contextualized embeddings (voyage-context-3)
- ✅ Hybrid search (BM25 + vector) via Weaviate
- ✅ VoyageAI reranking for result quality
- ✅ Auto-sync scheduler with timezone support
- ✅ Incremental sync (metadata phase filtering)
- ✅ Token-aware segmentation for large pages
- ✅ Result enrichment from Roam API
- ✅ Structured logging with structlog

### Known Limitations
- Block references `((uid))` not resolved in embeddings
- Character-based truncation (token estimation is heuristic)
- Single point of failure (chunker service)

## Important Implementation Details

### Weaviate Collection
- Name: `RoamSemanticChunks` (configurable)
- Hybrid search: BM25 + vector similarity
- Reranker: VoyageAI `rerank-2-lite`
- Properties: chunk_text_preview, primary_uid, page_uid, document_type, etc.

### Search Response Structure
- Returns enriched blocks with current text from Roam
- Includes similarity scores (0-1, higher is better)
- Provides highlight markers (`^^text^^`) for query matches
- Contains page context and parent information

### Sync State Persistence
- SQLite: `backend/data/semantic_sync.db` - page state (edit times, content hashes)
- File: `backend/data/sync_state.json` - checkpoint for resume on failure

## Key Files Reference

| File | Purpose |
|------|---------|
| `backend/sync/orchestrator.py` | Main sync coordination |
| `backend/sync/pipeline/batch_phase.py` | Token-aware batch processing |
| `backend/sync/pipeline/stages/` | Individual pipeline stages |
| `backend/services/search_service.py` | Search API + app host |
| `backend/common/config.py` | Configuration management |
| `backend/clients/roam.py` | Roam API client |
| `backend/clients/voyage.py` | VoyageAI embedding client |

## Where to Find Answers
- **Roam API specifics**: Check `/docs/external/roam_research/`
- **VoyageAI usage**: Check `/docs/external/voyageai/`
- **Architecture decisions**: See `/docs/architecture.md`
- **Sync state machine**: See `/docs/sync-state-machine.md`
