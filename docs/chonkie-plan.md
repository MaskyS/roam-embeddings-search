# Chonkie Integration Plan for Roam Semantic Search

## Meta-Principles (How We Build)

### 1. REPL-Driven Development
- Build small, immediately testable pieces
- Get feedback from each component before composing
- No component larger than what can be understood in one sitting

### 2. OODA Loop
- **Observe**: Test with real data, measure actual behavior
- **Orient**: Understand what the data tells us
- **Decide**: Choose simplest path forward based on evidence
- **Act**: Implement minimal change, then loop back

### 3. Rich Hickey's Principles
- **Simple > Easy**: Each function does ONE thing
- **Avoid complecting**: Don't mix concerns (e.g., linearization ≠ chunking ≠ storage)
- **Constraints over Planning**: Define what we MUST have, not folder structures
- **Data > Functions > Macros**: Work with plain data structures first

## Known Constraints (What We Know)

1. **Data Structure**
   - Roam provides hierarchical JSON with UIDs
   - Pages have `:node/title`, blocks have `:block/string`
   - Daily notes identified by UID pattern (MM-DD-YYYY), may lack `:node/title`
   - Block references exist as `((uid))` in text
   - We'll be pulling blocks page by page (natural grouping)

2. **Chonkie Requirements**
   - Expects linear text input
   - Returns chunks with start/end indices
   - Configurable semantic similarity threshold and skip-window

3. **Search Requirements**  
   - Must map chunks back to at least one block UID for navigation
   - Prefer most contributing block or parent block for click-through
   - Non-destructive to existing system

4. **Scale**
   - 50K-100K blocks typical
   - Batch sync acceptable
   - Page-by-page processing natural fit

## Open Questions (To Be Answered Empirically)

### Question 1: UID Tracking Method
**We need to see**:
- How Chonkie chunks hierarchical text
- The tree structure after linearization
- Which blocks end up in which chunks

**Options to test**:
```python
# Option A: Block-Set Tracking
chunk_metadata = {
    'source_uids': ['uid1', 'uid2', 'uid3'],  # All contributing blocks
    'primary_uid': 'uid1'  # For navigation
}

# Option B: Delimiter-Based
text = f"[{uid}]{block_text}"  # Insert markers
# Parse after chunking

# Option C: Parallel Arrays
texts = ["text1", "text2", "text3"]
uids = ["uid1", "uid2", "uid3"]
# Map chunks back via index ranges
```

**How we'll decide**: Run all three on sample data, compare complexity vs accuracy

### Question 2: Page Processing Strategy
Since we're pulling page by page, we need to test:
- Feed entire page as one document to Chonkie?
- Pre-process page into logical sections?
- How to handle daily notes vs topic pages?

## Phase 1: Empirical Exploration (See the Data First)

### 1.1 Document Roam API Behavior
**File**: `experiments/test_roam_api.py`
**Purpose**: Get ground truth on API responses
**Output**: `docs/external/roam_research/api_response_samples.md`

Key tests:
- Pull a complete page with all children
- Pull a daily note page (test the UID quirk)
- Pull-many with different batch sizes
- Document exact JSON structure returned
- Save 3-5 real response examples

### 1.2 Visualize Page Structure
**File**: `experiments/visualize_page_structure.py`
**Purpose**: Understand the tree structure we're working with

Output:
- Text representation of page hierarchy
- Count of blocks at each level
- Identify natural breaking points
- Show where block references appear

### 1.3 Test Chonkie with Roam Pages
**File**: `experiments/test_chonkie_basic.py`
**Purpose**: See how Chonkie actually chunks Roam content

Tests to run:
```python
# Test 1: Raw page linearization
page_text = linearize_page_simple(page_data)
chunks = chunker.chunk(page_text)
# Analyze: How many chunks? Where are boundaries?

# Test 2: With hierarchy markers
page_text_with_markers = linearize_with_indentation(page_data)
chunks = chunker.chunk(page_text_with_markers)
# Analyze: Does structure help or hurt?

# Test 3: Different skip-window values
for skip in [0, 1, 2]:
    chunker = SemanticChunker(skip_window=skip)
    # Test with daily note that has interleaved topics
```

### 1.4 Test UID Tracking Approaches
**File**: `experiments/test_uid_tracking.py`
**Purpose**: Try all three tracking methods with real data

For each approach:
1. Linearize a page with the method
2. Chunk it
3. Try to map chunks back to UIDs
4. Measure:
   - Accuracy (can we find all source UIDs?)
   - Complexity (lines of code, edge cases)
   - Performance (speed)

### 1.5 End-to-End Proof
**File**: `experiments/test_pipeline.py`
**Purpose**: Verify complete flow with best approach from above

Steps:
1. Pull 3 different pages (topic page, daily note, page with many children)
2. Process each with winning approach from 1.4
3. Store in test collection
4. Query and verify navigation works
5. Document what we learned

## Phase 2: Component Development (Based on Phase 1 Learnings)

### 2.1 Chosen Linearizer
**File**: `backend/roam_linearizer.py`
**Implementation**: Based on what worked best in Phase 1

Likely structure:
```python
def linearize_page(page_data: Dict) -> Tuple[str, List[Dict]]:
    """
    Linearize a Roam page for chunking.
    Returns (text, metadata) where metadata helps map chunks back.
    """
    # Implementation chosen from experiments
```

### 2.2 Chunking Wrapper
**File**: `backend/semantic_chunker_wrapper.py`
**Purpose**: Configure Chonkie for Roam's specific needs

```python
class RoamChunker:
    def __init__(self, threshold=0.7, skip_window=?):  # Values from experiments
        self.chunker = SemanticChunker(...)
    
    def chunk_page(self, page_data: Dict) -> List[ChunkWithMetadata]:
        # Linearize, chunk, add metadata
```

### 2.3 Full Sync Script
**File**: `backend/sync_chonkie.py`
**Purpose**: Process entire graph with proven approach

Key differences from sync_full.py:
- Process page by page (natural grouping)
- Use Chonkie for semantic chunking
- Store in "roam_blocks_semantic" collection

## Phase 3: Integration & Comparison

### 3.1 Non-Destructive Search Update
**File**: `backend/main.py` (minimal changes)

```python
@app.get("/search")
async def search(q: str, strategy: str = "adaptive"):
    """
    strategy: 'adaptive' (original) or 'semantic' (Chonkie-based)
    """
    collection_name = {
        "adaptive": "roam_blocks",  # sync_full.py
        "semantic": "roam_blocks_semantic"  # sync_chonkie.py
    }.get(strategy, "roam_blocks")
    # Rest of search logic unchanged
```

### 3.2 A/B Testing Framework
**File**: `experiments/compare_strategies.py`
**Purpose**: Empirically compare approaches

Test queries:
- Interleaved topics from daily notes
- Specific project information
- Cross-referenced concepts
- Measure: relevance, result quality, performance

## Success Metrics

1. **Correctness**: Every chunk maps to valid source UIDs
2. **Quality**: Better handling of interleaved topics
3. **Simplicity**: Fewer lines of code than complex context windows
4. **Non-destructive**: Original system untouched

## What We're NOT Planning (Yet)

- Complex semantic island algorithms (let Chonkie handle it)
- Frontend changes (separate concern)
- Incremental sync (separate concern)
- Performance optimizations (measure first)
- Final folder structure (let it emerge)

## Decision Points (After Each Phase)

### After Phase 1:
- Which UID tracking method is simplest and sufficient?
- What Chonkie parameters work best for Roam content?
- Should we pre-process pages or feed them raw?

### After Phase 2:
- Is the semantic chunking actually better for search?
- What edge cases did we discover?
- Is the added complexity worth it?

### After Phase 3:
- Should this replace the adaptive approach?
- What queries work better with which approach?
- What did we learn for future improvements?

## First Action

Create `experiments/test_roam_api.py` to:
1. Pull several complete pages
2. Document exact structure
3. Save real examples for testing

---

*This plan is designed to evolve based on what we learn. Each experiment informs the next step.*