# Roam Semantic Search Project Context

## Project Overview
Building a semantic search system for Roam Research using embeddings and vector similarity.

## How to Get Oriented

### 1. Read Core Documentation First
- `/docs/roam-backend-api.md` - Official Roam Backend API (source of truth)
- `/docs/roam-frontend-api.md` - Official Roam Frontend API (source of truth)
- `/docs/plan.md` - Project architecture, design decisions, and roadmap

### 2. Understand the Implementation Evolution
Read the sync files in order to understand how the solution evolved:
- `/backend/sync_v1.py` - Basic implementation
- `/backend/sync_v5.py` - Full adaptive context with sibling windows
- `/backend/sync_full.py` - Production implementation

### 3. Check Current Implementation
- `/backend/main.py` - FastAPI backend with search endpoint
- `/backend/roam.py` - Roam API communication utilities
- `/docker-compose.yml` - Container orchestration
- `/.env` - Configuration (API keys, graph name)

## Key Design Principles

### Adaptive Context Strategy
- **Parent blocks**: Concatenate with children as single embedding
- **Leaf blocks**: Include parent context and sibling sliding window
- This is THE core innovation - Roam's power comes from context, not isolated text

### API Usage Patterns
- **Pull-many over individual pulls** for efficiency
- **20-second timeout** on all Roam API calls
- **50 requests/minute** rate limit per graph
- **String format for eids** in pull-many (Clojure syntax, not JSON)

### Data Quality
- **Skip empty blocks** (no :block/string or :node/title)
- **Handle pages differently** (they have :node/title, not :block/string)
- **8000 character context limit** for embeddings

## Development Workflow

### To Run the System
1. Ensure Docker is running
2. Check `.env` has required keys (ROAM_API_TOKEN, GOOGLE_API_KEY, ROAM_GRAPH_NAME)
3. `docker-compose up -d` to start services
4. Run sync: `docker exec roam-test-backend-1 python sync_full.py`
5. Test search: `curl "http://localhost:8001/search?q=your+query"`

### To Understand Search Implementation
1. Read the search endpoint in `/backend/main.py` (around line 192)
2. Note the enrichment strategy (pull-many after ChromaDB query)
3. Understand distance vs similarity conversion

### To Debug Issues
- Check sync output for empty block warnings
- Verify ChromaDB collection has documents
- Test with simple queries first ("March", "test")

## Current State & Next Steps

### Completed
- ✅ Full graph sync with adaptive context
- ✅ Google Gemini embeddings (models/gemini-embedding-001)
- ✅ Semantic search API with block enrichment
- ✅ Highlight generation for matches

### In Progress
- Frontend integration planning (see end of conversation)
- Considering Command Palette + Custom Modal approach

### Known Limitations
- Block references ((uid)) not resolved
- No incremental sync (complex due to cascade effects)
- Character-based truncation (not token-based)

## Important Implementation Details

### ChromaDB Collection
- Name: "roam_blocks"
- Embedding dimension: 3072 (Gemini)
- Stores context as documents, not raw block text

### Search Response Structure
- Returns enriched blocks with current text from Roam
- Includes similarity scores (0-1, higher is better)
- Provides highlight positions for query matches
- Contains both original text and embedding context

## Questions to Consider for Frontend Integration

1. **Result Display**: Show just blocks or include parent context?
2. **Interaction**: Navigate on click or open in sidebar?
3. **Authentication**: How to pass Roam token to backend?
4. **CORS**: Use Roam's proxy or configure headers?

## Testing Approach
- Start with 100-block test runs before full graph
- Check for empty blocks in sync output
- Verify search returns relevant results
- Test different block types (parent/leaf filtering)

## Where to Find Answers
- **Roam API specifics**: Check the official docs in `/docs/`
- **Implementation decisions**: Read `/docs/plan.md`
- **Current bugs/issues**: Check Known Issues section in plan.md
- **Sync strategies**: Compare sync_v*.py files for evolution