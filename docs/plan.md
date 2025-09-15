
# Project Plan: Semantic Search for Roam Research

## 1. Project Overview

This document outlines the plan to build a semantic (embeddings-based) search engine for a Roam Research graph.

The system will consist of three main components:
1.  A **Backend Service** to ingest data from Roam, generate embeddings, and serve search requests.
2.  A **Vector Database** (ChromaDB) to store and query the embeddings.
3.  A **Roam Extension** (client-side) to provide the user interface for searching.

Syncing will be handled on-demand by the backend, not in real-time from the client.

---

## 2. The Criticality of a Sophisticated Embedding Strategy

A naive embedding of raw block text is insufficient because it fails to capture what makes Roam powerful: context. A block's meaning is a composite of its own text, its hierarchical ancestors, its siblings, and its linked neighbors.

### 2.1. Analysis of Roam Writing Scenarios

To build an effective strategy, we must consider how users structure information:

-   **Scenario 1: A Pro/Con List**
    -   `Decision on ChromaDB:`
        -   `Pros:`
            -   `- Open source`
            -   `- Runs locally`
        -   `Cons:`
            -   `- Requires self-hosting`
    *Implication:* The block `- Open source` is only a "Pro" because of its parent and grandparent. Sibling context matters for understanding the list, but the parent context (`Pros`) is what defines the topic.

-   **Scenario 2: Sequential Arguments**
    -   `Argument Flow:`
        -   `1. First, we establish the user need.`
        -   `2. Second, we demonstrate that keyword search is insufficient.`
        -   `3. Finally, we propose semantic search as the solution.`
    *Implication:* The meaning of block #2 is clarified by its preceding sibling, block #1. Simple parent context is not enough.

### 2.2. Recommended Strategy: "Adaptive Context"

Given these scenarios, we must use a strategy that adapts to the block's role. We will treat "parent" blocks differently from "leaf" blocks.

1.  **For "Parent Blocks" (blocks with children):**
    -   **Strategy:** Treat the block and its immediate children as a single, coherent "chunk".
    -   **Document Construction:** Concatenate the parent's text with the text of all its children (up to a token limit). Example: `"Pros: - Open source - Runs locally"`.
    -   **Embedding:** Generate **one single embedding** for this entire chunk and associate it with the **Parent Block's UID**. The children are not embedded individually.
    -   *Benefit:* This creates a highly relevant, topic-focused document and is very efficient.

2.  **For "Leaf Blocks" (blocks with no children):**
    -   **Strategy:** Capture context from parents and immediate siblings using a "sliding window".
    -   **Document Construction:** Create a document combining parent/grandparent context with the text of the previous sibling, the current block, and the next sibling. Example: `"Decision on ChromaDB > Pros > - Open source - Runs locally - Good Python client"`.
    -   **Embedding:** This constructed document is embedded and stored with the **Leaf Block's UID**.

### 2.3. Consideration of Technical Constraints & Future Advances

-   **Context Length Limits:** Standard embedding models have context limits (~8,000 tokens). This is a hard constraint that makes our intelligent chunking and budgeting logic mandatory.
-   **Future Advances:** While future tech like Structure-Aware Models would be a perfect fit, they are not yet commodity tools. Our "Adaptive Context" strategy is a state-of-the-art *practical* approach that simulates what those models do by manually formatting structure into text.

---

## 3. System Architecture

```
+-----------------+      +----------------------+      +------------------------+
|                 |      |                      |      |                        |
|  Roam Research  |      |    Backend Service   |      |      Roam Extension    |
|  (User Client)  |----->|  (Python + FastAPI)  |<---->| (JavaScript Alpha API) |
|                 |      |                      |      |                        |
+-----------------+      +-----------+----------+      +------------------------+
       ^                             |
       |                             | (Sync Data)
(Backend API Calls)                  |
       |                             |
       v                             v
+-----------------+      +----------------------+
|                 |      |                      |
| Roam Backend API|      |   Vector Database    |
|                 |<-----|      (ChromaDB)      |
|                 |      |                      |
+-----------------+      +----------------------+
```

## 4. Technology Stack & Deployment

-   **Backend Service:** **Python 3.10+** with the **FastAPI** web framework.
-   **Vector Database:** **ChromaDB**.
-   **Embedding Model:** **Google Generative AI** (Gemini).
-   **Roam Extension:** **JavaScript**.
-   **Deployment:** **Docker Compose**.

### Docker Architecture:
- **ChromaDB Container:** Runs on port 8000, persists data in `./chroma_data`
- **Backend Container:** Python/FastAPI on port 8001, hot-reloads with mounted `./backend` volume
- **Environment:** Uses `.env` file for secrets (Roam API token, Google API key)
- **Package Management:** Uses `uv` for fast Python dependency installation
- **Development:** Containers support hot-reload for rapid iteration

## 5. Development Philosophy: REPL Approach

We use a REPL (Read-Eval-Print-Loop) methodology for iterative development:

### **Observe** - Learn from real data
- Test each enhancement against actual Roam data
- Measure concrete improvements (e.g., search quality)
- Identify patterns and edge cases

### **Orient** - Understand implications
- Analyze what the observations mean
- Identify the next most impactful improvement
- Consider technical constraints

### **Decide** - Choose minimal change
- Select the smallest change that addresses a real limitation
- Build on proven infrastructure
- Define clear success metrics

### **Act** - Implement and measure
- Make the change
- Test with real data
- Document learnings

This approach ensures:
- **Small failures** - Easy to rollback or fix
- **Testable iterations** - Clear success metrics
- **Compounding knowledge** - Each version informs the next
- **Early value delivery** - Improvements are usable immediately

## 6. Technical Specifications

### Core Parameters:
- **Embedding Model:** `models/gemini-embedding-001` (3072 dimensions)
- **Context Limit:** 8000 characters (configurable as `MAX_CONTEXT_LENGTH`)
- **Batch Size:** 50 blocks per pull-many request (optional, adjustable for rate limiting)
- **Rate Limit:** 50 requests/minute/graph (Roam API constraint)
- **Query Timeout:** 20 seconds (Roam API constraint)
- **Search Results Limit:** 50 maximum (configurable)
- **Query Length Limit:** 1000 characters (prevent token overflow)
- **Max Siblings in Context:** 4 siblings (2 before, 2 after current block)
- **Min Sibling Space:** 50 characters (siblings excluded if less space available)

## 7. Technical Implementation Details

### Key Discoveries:

1. **Roam's Data Model:**
   - Pages have `:node/title` attribute
   - Blocks have `:block/string` attribute
   - Both can be parents, requiring different handling

2. **Pull API Capabilities:**
   - Supports reverse lookups: `{:block/_children [...]}` gets parent info
   - Supports nested patterns for fetching related data in one request
   - More efficient than multiple separate queries

3. **Enhanced Pull Selectors:**
   ```clojure
   [:block/uid :block/string
    {:block/children [:block/uid :block/string :block/order]}
    {:block/_children [:block/uid :block/string :node/title
                      {:block/children [:block/uid :block/string :block/order]}]}]
   ```
   This single selector gets:
   - Current block's data
   - Its children (if any)
   - Its parent
   - Its siblings (parent's children)

4. **Context Building Patterns:**
   - **Parent blocks:** Concatenate with children as bullet points
   - **Leaf blocks:** Smart allocation with multi-sibling support:
     - Parent gets up to 1/3 of total space (2666 chars)
     - Unused parent space redistributed to current block and siblings
     - Up to 6 siblings included using middle-out selection
     - Distance-weighted space allocation (closer siblings get more space)
     - Format: `Parent > sib1 → sib2 → [[current]] → sib3 → sib4`
   - **Page children:** `Page Title > block text`

### Important Gotchas:

- The parent from reverse lookup doesn't automatically include its children
- Must explicitly request parent's children for sibling context
- Pages don't have sibling relationships (only blocks do)

## 7. Detailed Implementation Plan

### Current Implementation Status:

✅ **Completed:**
- Docker environment with ChromaDB and FastAPI backend
- Connection to Roam Backend API with proper authentication
- Enhanced pull selectors with parent and sibling context
- Adaptive context building with smart allocation:
  - Dynamic parent space redistribution
  - Multi-sibling support (up to 6 siblings)
  - Middle-out sibling selection
  - Distance-weighted space allocation
- Full graph sync with paginated batching (`sync_full.py`)
- Command-line arguments for sync control (`--clear`, `--test N`)
- Google Gemini embeddings integration (models/gemini-embedding-001)
- Semantic search API with block enrichment
- Highlight generation for search matches
- Multi-sibling context tracking and statistics

🚧 **In Progress:**
- Performance optimization for large graphs

📋 **Future Work:**
- Block reference resolution (((uid)) expansion)
- Incremental sync with cascade effects
- Roam Extension UI
- Related blocks endpoint

### Phase 2: Full Graph Sync (`sync_full.py`)
- **Paginated Strategy:** Due to 20-second timeout on Roam API
  1. Get all UIDs with lightweight query (no text/children)
  2. Use `pull-many` in batches of 50 blocks
  3. Build adaptive context for each block with smart allocation
  4. Pass context as documents to ChromaDB
- **Command-line Options:**
  - `--clear`: Clear existing embeddings before sync (default: incremental)
  - `--test N`: Limit sync to first N blocks for testing
- **Smart Context Allocation:**
  - Parent blocks: Concatenate with all children until space limit
  - Leaf blocks: Dynamic allocation based on content needs
  - Redistributes unused parent space to current block and siblings
  - Includes up to 4 siblings using middle-out selection
  - Distance-weighted space distribution (closer = more space)
- **Rate Limiting:** 50 requests/minute - configurable delay between batches
- **Context Limits:** Truncate to 8000 characters (configurable constant)
- **Page Handling:** Pages appear as parents with `:node/title` - format as "Page Title > child text"
- **Progress Tracking:** Log progress for large graphs with statistics
- **Save timestamp** for future incremental syncs

### Phase 3: Incremental Sync Strategy (FUTURE)

**Why Complex:** Our Adaptive Context strategy creates dependencies between blocks. When one block changes, multiple embeddings become stale.

#### Cascade Effects Problem

When a block is modified, the following embeddings need updates:

```
Modified Block (B)
├─ Parent (P)        → If B is a child, P's context includes B's text
├─ Siblings (S1, S2) → Their sliding windows include B
└─ Children (C1, C2) → If B is parent, their context includes B

Total affected: 1 modified + potentially 5+ related blocks
```

**Example Scenario:**
1. User edits "Open source" to "Free and open source"
2. Must re-embed:
   - The block itself (text changed)
   - Parent block "Pros:" (its children context changed)
   - Sibling "Runs locally" (its sliding window changed)
   - Sibling "Good Python client" (its sliding window changed)

#### Query Strategy

```clojure
; Find all blocks edited since last sync
[:find ?uid ?edit-time
 :where
 [?b :block/uid ?uid]
 [?b :block/edit-time ?edit-time]
 [(> ?edit-time LAST_SYNC_TIMESTAMP)]]
```

Then for each modified block:
1. Pull the block with full context selector
2. Identify all affected blocks (parent, siblings, children)
3. Build set of UIDs needing re-embedding
4. Process entire set (avoiding duplicates)

#### Deletion Handling Challenge

Roam API doesn't provide deletion events, leading to four possible approaches:

1. **Ignore for MVP**
   - Stale embeddings remain in ChromaDB
   - Won't match new searches well
   - Simplest approach, acceptable for MVP

2. **Full Comparison**
   - Query all UIDs from Roam
   - Compare with ChromaDB collection
   - Delete missing UIDs
   - Expensive but thorough

3. **Track Block Count**
   - Monitor total block count
   - If significant decrease, trigger full resync
   - Heuristic approach, may miss some deletions

4. **Event Log (Future)**
   - If Roam adds deletion events to API
   - Would be the ideal solution
   - Not currently available

**Recommendation:** Start with approach #1 (ignore), implement #2 when needed.

#### Implementation Complexity

- Must track last sync timestamp persistently
- Need efficient set operations for affected blocks
- Careful handling of cascading updates
- Consider rate limits when processing affected blocks
- May need to batch updates for large changes

**Note:** Due to cascade complexity, implement only after full sync is battle-tested

### Phase 4: Roam Extension
- Add "Semantic Search" command to command palette
- Create search UI with real-time results
- Use `window.roamAlphaAPI.ui.components.renderBlock` for display
- Add "Sync Now" button to trigger backend sync

## 8. Search Design Decisions

### Why Semantic Search
- **Goal:** Find blocks by meaning, not just keyword matching
- **Benefit:** Discovers conceptually related content even with different wording
- **Trade-off:** Requires embedding generation and vector storage

### Enrichment Strategy
- **Decision:** Pull latest block data from Roam after ChromaDB query
- **Rationale:** Ensures search results show current content, not stale cached data
- **Cost:** Additional API call but guarantees accuracy

### Distance vs Similarity Conversion
- **ChromaDB:** Returns distance (0-2 range, lower is better)
- **User-facing:** Convert to similarity (0-1 range, higher is better)
- **Formula:** `similarity = 1 - (distance / 2)`

### Highlight Generation
- **Approach:** Case-insensitive word matching in both original text and context
- **Smart Snippets:** Centers around first match with configurable window
- **Limitation:** Simple word matching, not semantic highlighting

### Query Processing
- **Decision:** Use raw query without expansion
- **Rationale:** Predictable results, no unexpected matches
- **Alternative considered:** Query expansion with synonyms (too unpredictable)

### Result Filtering
- **Pre-filter:** Use ChromaDB's `where` clause for block_type filtering (efficient)
- **Post-filter:** Apply similarity threshold after retrieval (flexible)
- **Limit:** Hard cap at 50 results to manage pull-many performance

### Empty Block Handling
- **Discovery:** Some blocks have no `:block/string` or `:node/title`
- **Decision:** Skip these during sync (likely queries, embeds, buttons)
- **Benefit:** Improves search relevance by excluding non-text content

## 9. API Endpoints

### GET /
- **Description:** Health check and status
- **Response:** Graph name, collection document count

### GET /search
- **Description:** Semantic search across Roam blocks
- **Parameters:**
  - `q` (required): Search query text
  - `limit` (optional): Number of results (1-50, default 10)
  - `threshold` (optional): Similarity threshold (0-1, filters results)
  - `block_type` (optional): Filter by "parent" or "leaf"
- **Response Structure:**
  ```json
  {
    "query": "search text",
    "results": [{
      "uid": "block-uid",
      "similarity": 0.95,
      "distance": 0.1,
      "block": {
        "text": "current block text",
        "text_preview": { "text": "snippet", "highlights": [...] },
        "parent_text": "parent block text",
        "type": "leaf|parent",
        "is_page": false,
        "has_children": true
      },
      "context": {
        "used_for_embedding": "full context text",
        "preview": { "text": "snippet", "highlights": [...] }
      },
      "metadata": { ... }
    }],
    "count": 10,
    "execution_time": 3.2
  }
  ```
- **Error Handling:**
  - 400: Empty query
  - 500: Service unavailable

### POST /sync
- **Description:** Trigger full graph sync (currently placeholder)
- **Response:** Success message with UIDs processed

### GET /health-check
- **Description:** Check Roam API connectivity
- **Response:** Status and total block count in graph

## 10. Configuration

A `.env` file will be used for secrets:
```
# .env
ROAM_GRAPH_NAME="my-graph"
ROAM_API_TOKEN="roam-graph-token-..."
GOOGLE_API_KEY="AIza..."
```

## 9. Expected Context Output Examples

**Sequential List:**
```
Pros: > Open source → Runs locally → Good Python client
```

**Isolated Block:**
```
Decision on ChromaDB > Evaluate vector database options
```

**Page Child:**
```
Project Plan > Overview of the semantic search system
```

## 10. Known Issues and Limitations

### Current Limitations

1. **Block References Not Resolved**
   - `((block-uid))` references remain as UIDs in context
   - Page references `[[page-name]]` are preserved but not expanded
   - Impact: Reduced context quality for blocks with many references
   - Solution: Implement batch-local + on-demand reference resolution

2. **Special Blocks Not Supported**
   - Query blocks, embeds, and buttons have no text content
   - Currently skipped during sync
   - Could potentially index their configuration/query text

3. **No Incremental Sync**
   - Must run full sync to capture changes
   - Becomes inefficient for large graphs with frequent updates
   - Solution outlined in Phase 3 (complex due to cascade effects)

4. **Character-Based Truncation**
   - Using character count instead of token count for limits
   - May occasionally exceed model token limits for non-ASCII text
   - Solution: Implement proper tokenization

5. **Simple Highlight Matching**
   - Only matches exact words, not semantic concepts
   - Case-insensitive but doesn't handle stemming
   - Solution: Would require NLP processing

### Performance Considerations

- Full sync takes ~1-2 seconds per block (including embeddings)
- Search enrichment adds ~3-5 seconds for pull-many
- Large graphs (>10,000 blocks) may hit rate limits

### API Constraints

- Roam API: 20-second timeout, 50 requests/minute
- Google Gemini: Context limit of ~8000 tokens
- ChromaDB: Collection dimension fixed after creation

## 11. Open Questions

1.  **Handling Deletions:** Currently ignoring (see Phase 3 for options)
2.  **Sync Trigger:** Manual trigger vs scheduled vs webhook
3.  **Reference Expansion Depth:** How deep to follow block references?
4.  **Context Budget Allocation:** How to split 8000 chars between parent/siblings/children?
