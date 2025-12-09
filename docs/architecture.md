# Roam Semantic Search Architecture

## System Overview

```
┌────────────────────────────────────────────────────────────┐
│                     FastAPI Backend                        │
│                                                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Search    │  │    Sync     │  │  Scheduler  │         │
│  │  Service    │  │   Service   │  │   Service   │         │
│  │             │  │             │  │             │         │
│  │ GET /search │  │ POST /sync  │  │ APScheduler │         │
│  │ GET /       │  │ GET /status │  │ daily cron  │         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │
│         │                │                │                │
└─────────┼────────────────┼────────────────┼────────────────┘
          │                │                │
          │    ┌───────────┴────────────────┘
          │    │
          ▼    ▼
┌─────────────────────┐    ┌─────────────────────┐
│   VoyageAI API      │    │   Roam Research     │
│ (voyage-context-3)  │    │      API            │
│                     │    │                     │
│ • Query embeddings  │    │ • Page metadata     │
│ • Doc embeddings    │    │ • Full page pulls   │
│ • Reranking         │    │ • Block structure   │
└─────────────────────┘    └─────────────────────┘
          │
          ▼
┌─────────────────────┐    ┌─────────────────────┐
│   Weaviate          │    │   Chunker Service   │
│   (Vector DB)       │    │   (Chonkie)         │
│                     │    │                     │
│ • Hybrid search     │    │ • Semantic chunking │
│ • BM25 + vector     │    │ • VoyageAI context  │
│ • Reranker module   │    │ • Token-aware       │
└─────────────────────┘    └─────────────────────┘
```

## Sync Pipeline Flow

The sync pipeline processes pages through multiple phases:

```
1. METADATA PHASE
   ┌──────────────────────────────────────────────────────────┐
   │                                                          │
   │  Fetch all page UIDs from Roam                           │
   │           │                                              │
   │           ▼                                              │
   │  Pull metadata (edit times, has_children)                │
   │           │                                              │
   │           ▼                                              │
   │  Filter: skip pages where                                │
   │    - edit_time <= last_synced_edit_time                  │
   │    - content_hash matches stored hash                    │
   │    - page exists in Weaviate                             │
   │           │                                              │
   │           ▼                                              │
   │  Output: remaining_uids (pages that need sync)           │
   │                                                          │
   └──────────────────────────────────────────────────────────┘
                            │
                            ▼
2. BATCH PHASE (per batch of pages)
   ┌──────────────────────────────────────────────────────────┐
   │                                                          │
   │  For each batch (default: 50 pages):                     │
   │                                                          │
   │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐         │
   │  │  CHUNK  │→│ PAYLOAD │→│  EMBED  │→│  WRITE  │         │
   │  │ (async) │ │ (sync)  │ │ (async) │ │ (async) │         │
   │  └─────────┘ └─────────┘ └─────────┘ └─────────┘         │
   │                                                          │
   │  CHUNK: Send to Chonkie for semantic splitting           │
   │  PAYLOAD: Build Weaviate objects with UUIDs              │
   │  EMBED: VoyageAI contextualized embeddings               │
   │  WRITE: Insert to Weaviate, delete old versions          │
   │                                                          │
   └──────────────────────────────────────────────────────────┘
                            │
                            ▼
3. STATE PERSISTENCE
   ┌──────────────────────────────────────────────────────────┐
   │                                                          │
   │  SQLite: page_state table                                │
   │    - page_uid                                            │
   │    - last_synced_edit_time                               │
   │    - content_hash                                        │
   │                                                          │
   │  File: sync_state.json (for resume on failure)           │
   │    - pending_page_uids                                   │
   │    - processed_count                                     │
   │    - since timestamp                                     │
   │                                                          │
   └──────────────────────────────────────────────────────────┘
```

## Token Budget Algorithm

VoyageAI has strict token limits. The pipeline handles this via segmentation:

```
Input: Pages with varying sizes (some > 32K tokens)

Per-Document Limit: 32,000 tokens (we use 31,040 with 3% margin)
Per-Request Limit: 120,000 tokens (we use 110,400 with 8% margin)

Algorithm:
1. SEGMENT: Split each page into segments that fit 32K budget
   Page A: 45K tokens → [Segment A1 (31K), Segment A2 (14K)]
   Page B: 10K tokens → [Segment B1 (10K)]

2. BATCH: Process segments round-robin across pages
   Round 0: [A1, B1] → 41K tokens → 1 API call
   Round 1: [A2]     → 14K tokens → 1 API call

3. ACCUMULATE: Collect embeddings back to source pages
   Page A embeddings: [A1_embeddings..., A2_embeddings...]
   Page B embeddings: [B1_embeddings...]

Benefits:
- Large pages don't block small pages
- Maximizes segments per API call
- Respects all Voyage limits
```

## Search Flow

```
Query: "machine learning papers"
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. EMBED QUERY                                              │
│    VoyageAI embed(query, input_type="query")                │
│    → query_vector (1024 dims)                               │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. HYBRID SEARCH                                            │
│    Weaviate hybrid query:                                   │
│    - BM25 keyword matching on chunk_text_preview            │
│    - Vector similarity on embeddings                        │
│    - alpha=0.5 (equal weight by default)                    │
│    → top-K results with scores                              │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. OPTIONAL RERANKING                                       │
│    VoyageAI rerank-2-lite on chunk_text_preview             │
│    → reordered results with better relevance                │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. ENRICHMENT                                               │
│    Roam API pull-many for primary_uids                      │
│    → current block text, parent context                     │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. RESPONSE                                                 │
│    Format results with:                                     │
│    - uid, parent_uid, page_uid                              │
│    - similarity score                                       │
│    - highlighted chunk_text_preview                         │
│    - page_title, parent_text                                │
└─────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
backend/
├── services/
│   ├── search_service.py    # FastAPI app + search endpoint
│   ├── sync_service.py      # Sync API router (/sync/*)
│   └── scheduler.py         # Auto-sync scheduling
│
├── sync/
│   ├── orchestrator.py      # High-level sync coordination
│   ├── context.py           # SyncContext dataclass
│   ├── resources.py         # Resource management (clients, semaphores)
│   │
│   ├── pipeline/
│   │   ├── batch_phase.py   # Batch processing loop
│   │   ├── metadata_phase.py# Incremental sync filtering
│   │   └── stages/          # Individual pipeline stages
│   │       ├── chunk_stage.py
│   │       ├── payload_stage.py
│   │       ├── embed_stage.py
│   │       ├── validate_stage.py
│   │       └── write_stage.py
│   │
│   ├── data/
│   │   ├── models.py        # Data classes (PageWorkItem, etc.)
│   │   ├── results.py       # Stage result types
│   │   └── transform.py     # Pure functions (linearize, hash)
│   │
│   └── state/
│       ├── run_state.py     # SyncRunState, StatusEmitter
│       ├── db_persistence.py# SQLite operations
│       └── file_persistence.py # JSON checkpoint
│
├── clients/
│   ├── roam.py              # Roam Research API client
│   ├── voyage.py            # VoyageAI embedding client
│   ├── weaviate.py          # Weaviate adapter
│   └── chunker.py           # Chunker service client
│
├── common/
│   ├── config.py            # SyncConfig, environment vars
│   ├── retry.py             # Retry decorators
│   ├── errors.py            # Error hierarchy
│   └── logging.py           # Structlog configuration
│
└── data/
    ├── semantic_sync.db     # SQLite state database
    └── sync_state.json      # Resume checkpoint
```

## Concurrency Model

```
┌─────────────────────────────────────────────────────────────┐
│                    Semaphore Guards                         │
│                                                             │
│  chunk_semaphore (1)   ─── Rate limit chunker service       │
│  embed_semaphore (1)   ─── Rate limit VoyageAI API          │
│  weaviate_semaphore (1)─── Rate limit Weaviate writes       │
│                                                             │
│  sync_lock (1)         ─── Prevent concurrent sync jobs     │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Within a batch:
- Groups processed in parallel via asyncio.TaskGroup
- Each group acquires semaphores sequentially (chunk → embed → write)
- No more than one operation per external service at a time

Roam API:
- AsyncLimiter (50 requests/minute)
- Applied to both metadata and full page pulls
```

## Error Handling Strategy

```
Transient Errors (retry):
- Network timeouts
- Rate limit (429)
- Server errors (5xx)

Permanent Errors (fail fast):
- Invalid credentials
- Missing required fields
- Schema validation failures

Stage Failures:
- Chunk failure → Fail entire group
- Payload failure → Skip page, continue others
- Embed failure → Fail entire group
- Write failure → Fail entire group
- Validation mismatch → Skip page, continue others

Result types capture errors explicitly:
  ChunkStageResult.errors: List[str]
  EmbedStageResult.errors: List[str]
  etc.
```
