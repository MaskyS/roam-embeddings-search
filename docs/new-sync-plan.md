Here is a comprehensive plan that addresses the architectural shift, incorporates the research on ChromaDB, and outlines a clear path forward.

  Guiding Principles for the New Approach

   1. Replace, Don't Patch: The new semantic sync process is a fundamental replacement for the manual context-building logic in sync_full.py, not an addition to it.
   2. Page as the Source Unit: We will process the graph on a page-by-page basis. Each page is treated as a single "document" that we linearize and then chunk.
   3. Chunks are the Indexed Unit: The items stored and searched in our ChromaDB collection will be semantically-defined chunks, not Roam blocks.
   4. Metadata is for Context, Not Primary Filtering: Given ChromaDB's limitations on metadata indexing, our primary retrieval method will be vector search on chunk
      content. Metadata will provide the crucial link back to the Roam graph and add context to search results.

  ---

  The Plan: `sync_semantic.py` Architecture

  I will create a new script, backend/sync_semantic.py, that is purpose-built for this new workflow.

  Phase 1: Project Scaffolding

   1. Create New Files:
       * backend/sync_semantic.py: The main script for the new sync process.
       * backend/linearize.py: A new module to house the linearize_page_markdown_style function, keeping the code clean and reusable.
   2. Establish New ChromaDB Collection: The script will be hardcoded to use a new collection, roam_semantic_chunks, to ensure zero impact on the existing search
      system.

  Phase 2: Data Ingestion and Processing

  This will be the core logic loop within sync_semantic.py.

   1. Fetch All Pages:
       * Implement a get_all_page_uids() function in the script.
       * This function will use query_roam to get a list of all page UIDs.
       * Decision: We will initially exclude Daily Note Pages to focus on processing more structured, evergreen content.
   2. Process Pages in Batches:
       * The script will iterate through the list of page UIDs.
       * It will use a batched pull_many_blocks call to efficiently fetch the full, recursive content of multiple pages at once.
   3. For Each Page, Execute the Pipeline:
       * Step 3.1: Linearize. Use the linearize_page_markdown_style function from the new linearize.py module. This function's output will be a tuple containing the
         single linearized text string and the crucial character-to-UID map.
       * Step 3.2: Chunk. Feed the linearized text into chonkie.SemanticChunker.
           * Initial Parameters: We will start with empirically-driven settings: threshold=0.6 (to group related sentences without being overly aggressive),
             skip_window=1 (to catch closely related but non-consecutive ideas), and a min_chunk_size of 50 tokens to prevent uselessly small chunks.
       * Step 3.3: Structure for ChromaDB. For each chunk returned by Chonkie, create a dictionary that represents the document to be indexed. This addresses the
         "lots of questions" about the data structure.
           * ID Generation: The document ID will be a new UUID: str(uuid.uuid4()). This is necessary because chunks are generated and have no inherent stable ID.
           * Metadata Schema: The metadata will be structured as follows:

   1             {
   2               "source_uids_json": "[\"uid1\", \"uid2\"]",
   3               "primary_uid": "uid1",
   4               "page_title": "Free Hierarchy",
   5               "page_uid": "d5-M3x7wX",
   6               "chunk_token_count": 128,
   7               "sync_version": "semantic_v1"
   8             }
           * Rationale for Metadata Fields:
               * source_uids_json: This will be a JSON-serialized string of all block UIDs that contributed to the chunk. This is a workaround for ChromaDB's lack of
                 native list support.
               * primary_uid: This will be the first UID found in the chunk. It serves as the direct link for user navigation, providing a simple and predictable
                 click-through target.
               * page_title and page_uid: Provide essential context in the search UI, showing the user where the result came from.

  Phase 3: Integration

   1. Update Search Endpoint: The /search endpoint in main.py will be modified. A strategy query parameter will be used to select which ChromaDB collection to query
      (roam_blocks for the old method, roam_semantic_chunks for the new one). This ensures a non-destructive A/B testing capability.

  First Action

  The first concrete step is to create the new file backend/linearize.py and implement the linearize_page_markdown_style function within it. This component is a
  foundational dependency for the entire pipeline.
