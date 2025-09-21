# Weaviate & Voyage AI Migration Plan

This document outlines the plan to migrate the vector backend from ChromaDB to Weaviate, integrating Voyage AI's contextual embedding models and enabling hybrid search.
This is a significant architectural change, moving from ChromaDB to Weaviate to enable more advanced features like hybrid search. I have carefully reviewed the documentation you
 provided and my own search results. Here is a detailed analysis, followed by a proposed plan and clarifying questions.

 Analysis of Weaviate Documentation

 Here is a ranking of the provided Weaviate documentation in terms of importance for this migration, along with my key takeaways:

  1. `collections-api-ref.md` (Most Important): This is the cornerstone document. It explains how to define a collection's schema.
      * Key Takeaway: The most critical piece of information is the ability to set the vectorizer to "none". This explicitly tells Weaviate not to generate vectors for the data,
        and to expect that I will provide them at import time. This is the fundamental requirement for integrating any external embedding model like Voyage.
      * Other Details: It also details how to define properties (title, chunk_text, etc.) and their data types, which is essential for creating the schema.

  2. `batch-import.md` (Very Important): Efficiency is key, and the current system uses batching. This document shows how to do the same with Weaviate.
      * Key Takeaway: The collection.batch.add_object() method accepts a vector parameter. This is the mechanism I will use to import the pre-computed contextual embeddings from
        Voyage alongside the text and metadata for each chunk.

  3. `hybrid-search.md` (Very Important): This directly addresses one of the primary motivations for this migration.
      * Key Takeaway: The collection.query.hybrid() method is the entry point for hybrid search. It allows for a query string (for the keyword part) and a vector (for the vector
        search part). The alpha parameter allows for tuning the balance between the two, which is a powerful feature.

  4. `vectorizers.md` (Important): This document confirms the "none" vectorizer strategy and shows how to configure Weaviate for various embedding models, which provides good
     context for how Weaviate thinks about vectorization.

  5. `python-sdk-ref-website.md/*` (Important): These files provide a good overview of the Python client's structure, classes (WeaviateClient, Collection, etc.), and methods. They
     serve as a good general reference for the implementation phase.

  6. `docker.md` (Important): Since we need to run Weaviate locally, this document is essential for setting up the docker-compose.yml file correctly, including defining services
     and environment variables.

  7. `async-client.md` (Important): The existing main_semantic.py uses asyncio and FastAPI. This document confirms that Weaviate has a WeaviateAsyncClient, which will be necessary
     to integrate cleanly into the existing async web server.

  8. `filters-metadata.md` & `datatypes.md` (Useful Reference): These are good for understanding the full capabilities of Weaviate's querying and data modeling, but are less
     critical for the initial migration plan, which will focus on replicating the existing metadata structure and search functionality.

 Deep Plan for Weaviate Migration

 This is a comprehensive plan to replace ChromaDB with Weaviate.

 Phase 1: Environment & Setup

  1. Docker Configuration:
      * I will create a new docker-compose.weaviate.yml file to define the Weaviate service. This keeps it separate from the existing application services for clarity.
      * The service will use a recent, stable cr.weaviate.io/semitechnologies/weaviate image.
      * I will configure a persistent volume to ensure the Weaviate data is not lost between restarts.
      * The AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED environment variable will be set to true for local development simplicity.
      * The DEFAULT_VECTORIZER_MODULE will be set to none to make it the default for new collections, although I will also specify this explicitly in the collection schema.

 Phase 2: Code Migration and Refactoring

 This phase involves modifying main_semantic.py and sync_semantic.py.

  1. Client Connection:
      * Replace all instances of chromadb.HttpClient with weaviate.Client (for the sync script) and weaviate.WeaviateAsyncClient (for the async FastAPI app).
      * The client will be configured to connect to localhost on the ports defined in the new Docker Compose file.

  2. Schema Definition (`sync_semantic.py`):
      * I will create a new function, ensure_weaviate_schema(client), that will be called at the start of the sync process.
      * This function will check if the RoamSemanticChunks collection exists. If not, it will create it.
      * The collection will be created using client.collections.create().
      * The vector_config will be set using Configure.Vectors.self_provided() (or by setting vectorizer='none'), explicitly telling Weaviate that we will provide the vectors.
      * The properties will be defined to match the existing metadata fields: primary_uid, page_title, page_uid, document_type, chunk_text_preview, etc., using appropriate
        DataType enums (e.g., DataType.TEXT, DataType.UUID).

  3. Data Ingestion (`sync_semantic.py`):
      * The logic for fetching data from Roam and chunking it with chonkie will remain unchanged.
      * The logic for generating contextual embeddings with Voyage AI will also remain.
      * The core change will be in the batching loop. Instead of appending to ChromaDB lists, I will use Weaviate's batching context manager: with client.batch.fixed_size(...) as
        batch:.
      * For each chunk, I will call batch.add_object(), passing the chunk's text and metadata to the properties argument and the pre-computed Voyage vector to the vector argument.


  4. Search Endpoint (`main_semantic.py`):
      * The /search endpoint will be refactored to use the WeaviateAsyncClient.
      * The core search logic will use collection.query.hybrid().
      * The user's text query (q) will be passed to the query parameter of the hybrid() method for the keyword search component.
      * A vector for the query q will be generated using the standard (non-contextual) Voyage embed function and passed to the vector parameter of the hybrid() method.
      * The alpha parameter will be used to balance the two search methods.
      * The existing logic for fetching parent context from Roam after the search will be preserved.


## 1. Current ChromaDB Connection Points

The following is an exhaustive list of all points in the codebase that currently interact with ChromaDB and will need to be replaced.

### `main_semantic.py`

-   **Global Variables**: The `_collections` dictionary and `_chroma_client` global variable will be removed.
-   **`get_collection()` function**: This entire function, which handles ChromaDB client initialization, embedding function selection, and collection creation/retrieval, will be replaced with a Weaviate equivalent.
-   **`delete_collection()` function**: This function, used for clearing data, will be replaced with a Weaviate alternative (`client.collections.delete`).
-   **`/search` endpoint**:
    -   The call to `get_collection(COLLECTION_NAME)` will be replaced.
    -   The `collection.query()` method call is the primary search mechanism and will be replaced with Weaviate's `collection.query.hybrid()` method.
    -   The construction of the `where_filter` for excluding pages will be replaced with Weaviate's `Filter` class.

### `sync_semantic.py`

-   **`get_collection()` import**: The import from `main_semantic` will be removed.
-   **Collection Handling**:
    -   The call to `delete_collection(COLLECTION_NAME)` when `--clear` is used will be replaced.
    -   The call to `get_collection(COLLECTION_NAME)` will be replaced with Weaviate client initialization and schema creation logic.
-   **Data Ingestion**:
    -   The primary point of contact is the `collection.add()` call within the batch processing loop. This is where embeddings are currently generated by ChromaDB's embedding function. This entire block will be refactored to use Weaviate's batch import mechanism with pre-computed vectors.

## 2. VoyageAI Implementation Details

The core logic of using VoyageAI will be preserved and enhanced to fit the new data flow.

### Data Ingestion (`sync_semantic.py`)

1.  **Model**: `voyage-context-3` will be used.
2.  **Function**: `voyageai.Client.contextualized_embed()` is the key function.
3.  **Input Formatting**: For each batch of pages fetched from Roam, the chunked texts will be organized into a `List[List[str]]`. Each inner list will contain all the non-overlapping text chunks from a single Roam page, in order.
4.  **API Call**: A single API call to `contextualized_embed()` will be made per batch of documents, with `input_type="document"`.
5.  **Output Handling**: The nested list of embedding vectors returned by Voyage will be flattened to correspond with the flattened list of all chunks from the batch, ensuring a 1:1 mapping between a chunk and its contextualized vector.

### Querying (`main_semantic.py`)

1.  **Model**: A standard, non-contextual Voyage model like `voyage-3-large` will be used for embedding the user's search query.
2.  **Function**: The standard `voyageai.Client.embed()` function will be used.
3.  **API Call**: A single API call will be made for each incoming search request `q`, with `input_type="query"`.
4.  **Output**: This will produce a single vector representing the query, which will be used in the `vector` parameter of Weaviate's hybrid search.

## 3. Weaviate Implementation Details

This section details the end-to-end integration of Weaviate.

### A. Docker Compose (`docker-compose.yml`)

The existing `docker-compose.yml` will be modified to include a new `weaviate` service:

```yaml
services:
  # ... existing services (ollama, chromadb, backend)
  weaviate:
    image: cr.weaviate.io/semitechnologies/weaviate:1.25.4
    ports:
      - "8080:8080"
      - "50051:50051"
    volumes:
      - ./weaviate_data:/var/lib/weaviate
    restart: on-failure:0
    environment:
      QUERY_DEFAULTS_LIMIT: 25
      AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: 'true'
      PERSISTENCE_DATA_PATH: '/var/lib/weaviate'
      DEFAULT_VECTORIZER_MODULE: 'none'
      ENABLE_MODULES: ''
      CLUSTER_HOSTNAME: 'node1'
```
*(Note: The ChromaDB service can be removed from this file once the migration is complete and verified.)*

### B. Client Connection

-   **Sync (`sync_semantic.py`)**: A sync client will be initialized:
    ```python
    import weaviate
    client = weaviate.connect_to_local()
    ```
-   **Async (`main_semantic.py`)**: An async client will be initialized for the FastAPI app:
    ```python
    import weaviate
    async_client = weaviate.use_async_with_local()
    # await async_client.connect() will be called on app startup
    ```

### C. Schema (Collection) Definition

A function `ensure_weaviate_schema(client)` will be implemented in `sync_semantic.py`.

-   It will use `client.collections.create()` to define the `RoamSemanticChunks` collection.
-   **`vectorizer_config`**: This will be set to `Configure.Vectorizer.none()`. This is the most critical step, ensuring Weaviate does not attempt to vectorize the data itself.
-   **`properties`**: The schema will be defined as follows:
    ```python
    from weaviate.classes.config import Property, DataType

    properties = [
        Property(name="chunk_text_preview", data_type=DataType.TEXT),
        Property(name="primary_uid", data_type=DataType.TEXT),
        Property(name="page_title", data_type=DataType.TEXT),
        Property(name="page_uid", data_type=DataType.TEXT),
        Property(name="document_type", data_type=DataType.TEXT, tokenization=Tokenization.FIELD), # For exact match filtering
        Property(name="source_uids_json", data_type=DataType.TEXT, skip_vectorization=True),
        Property(name="chunk_token_count", data_type=DataType.INT),
        Property(name="sync_version", data_type=DataType.TEXT, skip_vectorization=True),
    ]
    ```

### D. Data Ingestion (`sync_semantic.py`)

The batch processing loop will be entirely refactored.

1.  **Preparation**: Before the loop, initialize lists to hold data for the batch: `batch_page_chunks = []` and `batch_objects_to_add = []`.
2.  **Page Processing**: Inside the loop over pages, after linearizing and chunking a page, append the list of its chunk texts to `batch_page_chunks`. Also, create corresponding data objects (without vectors yet) and append them to `batch_objects_to_add`.
3.  **Vectorization**: After the page loop, call `voyageai.Client.contextualized_embed(inputs=batch_page_chunks, ...)` once.
4.  **Batch Import**:
    ```python
    with client.batch.fixed_size(batch_size=100) as batch:
        for i, data_object in enumerate(batch_objects_to_add):
            data_object["vector"] = voyage_embeddings[i] # Add the pre-computed vector
            batch.add_object(
                collection="RoamSemanticChunks",
                properties=data_object["properties"],
                uuid=data_object["uuid"],
                vector=data_object["vector"]
            )
    # Error handling
    if len(batch.failed_objects) > 0:
        print(f"Failed to import {len(batch.failed_objects)} objects.")
    ```

### E. Search Endpoint (`main_semantic.py`)

The `/search` endpoint will be updated.

1.  **Query Vectorization**: Embed the incoming query `q` using `voyageai.Client.embed([q], input_type="query")`.
2.  **Filtering**: If `exclude_pages` is true, a filter will be constructed:
    ```python
    from weaviate.classes.query import Filter
    filters = Filter.by_property("document_type").equal("chunk")
    ```
3.  **Hybrid Search**: The core query will be:
    ```python
    response = await collection.query.hybrid(
        query=q,
        vector=query_vector,
        alpha=0.5, # As decided
        limit=limit,
        filters=filters # if applicable
    )
    ```
4.  **Result Processing**: The `response.objects` will be iterated through to format the final API response, similar to the current implementation.

### F. Error Handling

-   **Connection Errors**: `weaviate.connect_to_local()` and `async_client.connect()` calls will be wrapped in `try...except WeaviateConnectionError`.
-   **Embedding Errors**: All calls to Voyage AI's API will be wrapped in a `try...except` block to catch potential API errors or network issues.
-   **Query/Deletion Errors**: All Weaviate CUD and query operations (`.add_object`, `.delete`, `.hybrid`, etc.) will be wrapped to catch `WeaviateQueryError` and other relevant exceptions, providing informative log messages.
