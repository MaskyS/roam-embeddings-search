
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

## 4. Technology Stack

-   **Backend Service:** **Python 3.10+** with the **FastAPI** web framework.
-   **Vector Database:** **ChromaDB**.
-   **Embedding Model:** **Google Generative AI** (Gemini).
-   **Roam Extension:** **JavaScript**.
-   **Deployment:** **Docker Compose**.

## 5. Detailed Implementation Plan

### Phase 1: Backend Setup & Initial Indexing

1.  **Environment Setup:** Create `docker-compose.yml`, `backend/Dockerfile`, and `.env` files.
2.  **Initial Indexing Script (`sync.py`):** Connects to ChromaDB, fetches the full graph from Roam, applies the **"Adaptive Context"** logic to each block, generates embeddings, and saves them to ChromaDB. Saves a timestamp upon completion.

### Phase 2: Incremental Syncing Strategy

1.  **Modify Sync Script:** Use a Datalog query to fetch only blocks edited since the last sync timestamp, along with their required context (parents, siblings).
2.  **Create Sync API Endpoint:** Expose a `POST /sync` endpoint in FastAPI to trigger the sync script.

### Phase 3: Search API Endpoint

1.  **Create Search Endpoint:** Define `GET /search?q=...`. This will embed the query `q` and return the top `k` most similar `block_uid`s from ChromaDB.

### Phase 4: Roam Extension Frontend

1.  **Setup:** Add a "Semantic Search" command to the command palette.
2.  **UI:** Create a search input and a "Sync Now" button. The button calls `POST /sync`; the search input calls `GET /search`.
3.  **Display Results:** Use `window.roamAlphaAPI.ui.components.renderBlock` to display the returned `block_uid`s interactively.

## 6. Configuration

A `.env` file will be used for secrets:
```
# .env
ROAM_GRAPH_NAME="my-graph"
ROAM_API_TOKEN="roam-graph-token-..."
GOOGLE_API_KEY="AIza..."
```

## 7. Open Questions

1.  **Handling Deletions:** For the MVP, we will ignore deleted blocks.
2.  **Sync Trigger:** The MVP will have a manual "Sync Now" button.
