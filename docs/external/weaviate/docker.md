Weaviate supports deployment with Docker.

You can [run Weaviate with default settings from a command line](https://docs.weaviate.io/deploy/installation-guides/docker-installation#run-weaviate-with-default-settings), or [customize your configuration](https://docs.weaviate.io/deploy/installation-guides/docker-installation#customize-your-weaviate-configuration) by creating your own `docker-compose.yml` file.

## Run Weaviate with default settings [​](https://docs.weaviate.io/deploy/installation-guides/docker-installation\#run-weaviate-with-default-settings "Direct link to Run Weaviate with default settings")

Added in v1.24.1

To run Weaviate with Docker using default settings, run this command from from your shell:

```codeBlockLines_e6Vv
docker run -p 8080:8080 -p 50051:50051 cr.weaviate.io/semitechnologies/weaviate:1.33.0

```

The command sets the following default [environment variables](https://docs.weaviate.io/deploy/installation-guides/docker-installation#environment-variables) in the container:

- `PERSISTENCE_DATA_PATH` defaults to `./data`
- `AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED` defaults to `true`.
- `QUERY_DEFAULTS_LIMIT` defaults to `10`.

## Customize your Weaviate configuration [​](https://docs.weaviate.io/deploy/installation-guides/docker-installation\#customize-your-weaviate-configuration "Direct link to Customize your Weaviate configuration")

You can customize your Weaviate configuration by creating a `docker-compose.yml` file. Start from our [sample Docker Compose file](https://docs.weaviate.io/deploy/installation-guides/docker-installation#sample-docker-compose-file), or use the interactive [Configurator](https://docs.weaviate.io/deploy/installation-guides/docker-installation#configurator) to generate a `docker-compose.yml` file.

## Sample Docker Compose file [​](https://docs.weaviate.io/deploy/installation-guides/docker-installation\#sample-docker-compose-file "Direct link to Sample Docker Compose file")

This starter Docker Compose file allows:

- Use of any [API-based model provider integrations](https://docs.weaviate.io/weaviate/model-providers) (e.g. `OpenAI`, `Cohere`, `Google`, and `Anthropic`).
  - This includes the relevant embedding model, generative, and reranker [integrations](https://docs.weaviate.io/weaviate/model-providers).
- Searching pre-vectorized data (without a vectorizer).
- Mounts a persistent volume called `weaviate_data` to `/var/lib/weaviate` in the container to store data.

### Download and run [​](https://docs.weaviate.io/deploy/installation-guides/docker-installation\#download-and-run "Direct link to Download and run")

- Anonymous access
- With authentication and authorization enabled

Save the code below as `docker-compose.yml` to download and run Weaviate with anonymous access enabled:

```codeBlockLines_e6Vv
---
services:
  weaviate:
    command:
    - --host
    - 0.0.0.0
    - --port
    - '8080'
    - --scheme
    - http
    image: cr.weaviate.io/semitechnologies/weaviate:1.33.0
    ports:
    - 8080:8080
    - 50051:50051
    volumes:
    - weaviate_data:/var/lib/weaviate
    restart: on-failure:0
    environment:
      QUERY_DEFAULTS_LIMIT: 25
      AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: 'true'
      PERSISTENCE_DATA_PATH: '/var/lib/weaviate'
      ENABLE_API_BASED_MODULES: 'true'
      CLUSTER_HOSTNAME: 'node1'
volumes:
  weaviate_data:
...

```

caution

Anonymous access is strongly discouraged except for development or evaluation purposes.

Edit the `docker-compose.yml` file to suit your needs. You can add or remove [environment variables](https://docs.weaviate.io/deploy/installation-guides/docker-installation#environment-variables), change the port mappings, or add additional [model provider integrations](https://docs.weaviate.io/weaviate/model-providers), such as [Ollama](https://docs.weaviate.io/weaviate/model-providers/ollama), or [Hugging Face Transformers](https://docs.weaviate.io/weaviate/model-providers/transformers).

To start your Weaviate instance, run this command from your shell:

```codeBlockLines_e6Vv
docker compose up -d

```

## Configurator [​](https://docs.weaviate.io/deploy/installation-guides/docker-installation\#configurator "Direct link to Configurator")

The Configurator can generate a `docker-compose.yml` file for you. Use the Configurator to select specific Weaviate modules, including vectorizers that run locally (i.e. `text2vec-transformers`, or `multi2vec-clip`)

Weaviate Version

v1.30.0

It is recommended to always use the latest version. You can also select an older version for compatibility sake, but not all features might be available on an older version. If you are running on arm64 hardware, please select v1.4.0 or newer.

v1.30.0

#### v1.30.0

Runtime config management, Dynamic user management, Dynamic RAG model selection, Multi-value vector support, BlockMax WAND-based BM25

#### v1.29.2

Async replication initialization improvements

#### v1.29.1

BlockMax Wand tombstone handling Fix, Binary quantization Improvement, Backup subdirectories Fix, Schema V2 Fixes

#### v1.29.0

RBAC, Async Replication, ACORN improvements, ColBERT, Blazing Fast BM25

#### v1.28.11

BlockMax Wand tombstone handling Fix, RBAC tenants check Fix

#### v1.28.10

Schema V2 related Fixes

#### v1.28.9

Binary quantization Improvement, Backup subdirectories Fix

#### v1.28.8

Shard loading concurrency limit improvement, Concurrent rangeable map writes Fix

#### v1.28.7

Cycle manager configurable goroutines improvement

#### v1.28.6

RBAC batch permissions Fix, Async replication Fix, GraphQL schema load improvement

#### v1.28.5

RBAC improvements, New NVIDIA modules, NotEqual filter performance improvements, Schema metrics improvements

#### v1.28.4

gRPC max message size Fix, RBAC improvements

#### v1.28.3

RBAC Fixes, Hybrid search Fix, Async replication Fixes

#### v1.28.2

Async replication improvements

#### v1.28.1

Async queue improvements

#### v1.28.0

RBAC preview, Replication delete repairs, Experimental BlockMax WAND, Async indexing improvements

#### v1.27.16

Batch rate limiter improvements

#### v1.27.15

Binary quantization Improvement, Backup subdirectories Fix, Schema V2 Fixes

#### v1.27.14

Shard loading concurrency limit improvement, Concurrent rangeable map writes Fix

#### v1.27.13

Schema concurrent updates improvement

#### v1.27.12

Merging documents with allow list fix, shard search improvements

#### v1.27.11

Schema metrics improvements, Async replication disable flag improvement

#### v1.27.10

gRPC max message size Fix, Async replication Fixes

#### v1.27.9

Async replication improvements

#### v1.27.8

New VoyageAI multimodal module

#### v1.27.7

Schema V2 redundant retries Fix, Added support for X-Goog-\* headers, Backup Azure module configurable blocksize / concurrency improvement

#### v1.27.6

LSM store compaction process improvements

#### v1.27.5

New multi2vec-jinaai module, Replication object time-based deletion improvement

#### v1.27.4

Filtered search performance improvements

#### v1.27.3

LSM store improvements, Data filtering Fix

#### v1.27.2

Dynamic backup locations feature, New multi2vec-cohere module, Range filters setting Fix

#### v1.27.1

Compressed vector cache parallel prefill and Non-blocking segment drop in compaction improvements, Auto Schema array type check Fix

#### v1.27.0

Improved HNSW Filters (ACORN-based Minority Filters), Multi-target Vector Search, Cancel Stuck Backups

#### v1.26.17

Shard loading concurrency limit improvement

#### v1.26.16

Cycle manager configurable goroutines improvement

#### v1.26.15

Schema concurrent updates improvement

#### v1.26.14

Schema metrics improvements

#### v1.26.13

Async replication improvements

#### v1.26.12

New VoyageAI multimodal module, LSM store compaction/flush synchronization Fix, Schema V2 redundant retries Fix, Added support for X-Goog-\* headers

#### v1.26.11

New multi2vec-jinaai module, Replication object time-based deletion improvement

#### v1.26.10

LSM store improvements, Data filtering Fix

#### v1.26.9

New multi2vec-cohere module, Range filters setting Fix

#### v1.26.8

Compressed vector cache parallel prefill and Non-blocking segment drop in compaction improvements

#### v1.26.7

LSM store segments cleanup feature, PaLM to Google modules renaming, Raft bootstrap timeout increase Fix

#### v1.26.6

Schema V2 recovering single node Fix, Ready and Live probes improvements, New batch related metrics

#### v1.26.5

New backup list and cancel endpoints, BM25 parallel search improvement, LSM compaction optimizations, HNSW deleted nodes condensing Fix, Raft Fixes, Support for New JinaAI and VoyageAI models

#### v1.26.4

BM25 performance improvements, Vector index ghost nodes and SQ distance calculation Fix, New text2vec modules metrics

#### v1.26.3

New Databricks text2vec and generative modules, New FriendliAI generative module, Hybrid cutoff Feature, Default replicas factor Fix

#### v1.26.2

Flat BQ index performance improvements, New text2vec-mistral module, HNSW index tombstone cleanup Fixes, Schema V2 RAFT Fixes, Sentry & Profiling Improvements

#### v1.26.1

Hybrid search performance Fix, Tenants create API Fix, New JinaAI Reranker module

#### v1.26.0

Tenant Offloading, Multi-Target Vector Search, Scalar Quantization, Async Replication, Improved Range Queries

#### v1.25.34

Backup subdirectories Fix

#### v1.25.33

Shard loading concurrency limit improvement

#### v1.25.32

Cycle manager configurable goroutines improvement

#### v1.25.31

Schema concurrent updates improvement

#### v1.25.30

Schema metrics improvements

#### v1.25.29

Security updates

#### v1.25.28

New VoyageAI multimodal module

#### v1.25.27

LSM store compaction/flush synchronization Fix, Schema V2 redundant retries Fix, Backup Azure module configurable blocksize / concurrency improvement

#### v1.25.26

New multi2vec-jinaai module, Replication object time-based deletion improvement

#### v1.25.25

New multi2vec-cohere module, LSM store improvements, Data filtering Fix

#### v1.25.24

Non-blocking segment drop in compaction improvement

#### v1.25.23

HNSW vector index improvements

#### v1.25.22

Compressed vector cache parallel prefill and Segments cleanup process improvements, Invalid replication factor validation

#### v1.25.21

LSM store segments cleanup feature, PaLM to Google modules renaming, Raft bootstrap timeout increase Fix

#### v1.25.20

Schema V2 recovering single node Fix, Ready and Live probes improvements, New batch related metrics

#### v1.25.19

Tombstone cleanup process long locking Fix

#### v1.25.18

Added support for new JinaAI V3 embeddings and VoyageAI models, maintenance mode, Raft Fixes

#### v1.25.17

New backup list and cancel endpoints, BM25 parallel search improvement, Brute force search setting, Hybrid & Bloom files compaction Fixes

#### v1.25.16

LSM store compaction optimizations, New tombstone cycles related metrics

#### v1.25.15

HNSW deleted nodes condensing Fix, Raft FQDN resolver support

#### v1.25.14

BM25 performance improvements, Default replicas factor Fix, Vector index ghost nodes Fix, New text2vec modules metrics

#### v1.25.13

New text2vec-mistral module, Module batch concurrent vectorization Support, Schema V2 Raft Fixes

#### v1.25.12

RAFT fixes, Bm25 speedups and experimental repair endpoint

#### v1.25.11

Flat index improvements, Shard initialization and Raft Fixes

#### v1.25.10

BM25 performance improvements, Vector index tombostone cleanup Fix, Sentry monitoring improvements

#### v1.25.9

Hybrid search and Object store retrevial performance Fix, Updates with empty arrays and lists Fix, Sentry configuration improvements

#### v1.25.8

Tombstone panic prevention Fix, HNSW PQ Fixes, GraphQL with primitive type named classes Fix, Schema V2 loading in metadata only mode Fix, Sentry logging integration

#### v1.25.7

DB blocking on failure Fix, Shards lazy loading Fix, PQ rescoring Fix, New Korean tokenizer

#### v1.25.6

Optional forced compaction for flat index, Improved panic handling, Rate limiting and HNSW race condition fixes

#### v1.25.5

Empty map during compaction Fix, GraphQL rebuild schema Fix

#### v1.25.4

Async indexing Fixes, Prevent deleted objects retrieval Fix

#### v1.25.3

Batch delete concurrency limitation, Dimension tracking Fix, Search with scores Fix, Google Auth support

#### v1.25.2

Property Length Tracker Fix, Context-aware wand Fix, Replication and HNSW tombstone deletion Fixes, Google, OpenAI and OctoAI module headers Fixes

#### v1.25.1

Schema V2 Fixes, AWS modules Fixes, Google Gemini 1.5 models support, Overwriting an object which is locally deleted Fix

#### v1.25.0

RAFT-based Schema, Batch Vectorization, Hybrid Search Improvements, Implicit Tenant Creation, Dynamic Index Switching

#### v1.24.26

Backup cancel endpoint and BM25 search improvements

#### v1.24.25

New backup list and cancel endpoints, BM25 parallel search improvement, LSM compaction optimizations, HNSW deleted nodes condensing Fix

#### v1.24.24

BM25 performance improvements, Vector index ghost nodes Fix

#### v1.24.23

HNSW index tombstone cleanup Fixes

#### v1.24.22

Replication with PATCH requests Fix, Vector index tombstone cleanup process Fix, Sentry & Profiling Improvements

#### v1.24.21

Tombstone panic prevention Fix, GraphQL with primitive type named classes Fix, Sentry logging integration

#### v1.24.20

Search all replicas setting, HNSW PQ rescoring Fix

#### v1.24.19

Async indexing Fixes, Prevent deleted objects retrieval Fix

#### v1.24.18

Replicated objects deletion Fix

#### v1.24.17

Batch delete concurrency limitation, Dimension tracking fix, improved error messages

#### v1.24.16

HNSW index visited list leak Fix, LSM store compaction Fixes, Search with scores Fix, Google Auth support

#### v1.24.15

Property Length Tracker Fix, Context-aware wand Fix, Replication and HNSW tombstone deletion Fixes

#### v1.24.14

Overwriting an object which is locally deleted Fix, Google Studio and Vertex separate headers support

#### v1.24.13

Empty segment generation Fix, Bedrock generative and Gemini 1.5 models support

#### v1.24.12

LSM Segment Size limit setting, text2vec-aws module Bedrock models support Fix

#### v1.24.11

Vector search with named vectors Fix, improved validation when using nearObject and nearVector searches

#### v1.24.10

HNSW performance regression Fix

#### v1.24.9

Added support for new Google models and Cohere V3 reranking models, Added memory guardrails, MTTR improvement Fix

#### v1.24.8

Minimal schema metrics, Prevent deadlock when goroutine panics Fix

#### v1.24.7

New VoyageAI reranker module, Fix for Azure OpenAI Api Version in text2vec-openai module

#### v1.24.6

Backup of nodes without data Fix, Reference types endless recursion Fix

#### v1.24.5

Keyword search display scores Fix, Default target vector in hybrid Fix, Module parameters values Fix, Allow setting AdvertiseAddr in memberlist Improvement

#### v1.24.4

Add video modality support to multi2vec-palm module

#### v1.24.3

New mutli2vec-palm module, restoring backup for pre v1.23 releases Fix

#### v1.24.2

New text2vec-voyageai and generative-mistral module, Cyclemanager not resetting Fix, Named vectors certainty param validation Fix, Stability and Performance Fixes

#### v1.24.1

Fixes for vector index compression, Tombstone cleanup, Multiple vectors, Schema deadlock

#### v1.24.0

High Frequency Updates, HNSW Binary Quantization, Support for Multiple Vectors per Class, Durability Improvements, Japanese & Chinese Tokenizers, Improved NotEqual Operator, Telemetry

#### v1.23.16

Replication and Backup related Fixes

#### v1.23.15

Overwriting an object which is locally deleted Fix

#### v1.23.14

Backup of nodes without data Fix, Reference types endless recursion Fix

#### v1.23.13

Fix for restoring backup for pre v1.23 releases

#### v1.23.12

Fix cardinality issues for backup-related metrics

#### v1.23.11

Fixes for Pread segments, Vector index compression, BM25 stability, Schema deadlocks

#### v1.23.10

Tokenizer optimizations, More efficient nodes API, Metrics and logging improvements

#### v1.23.9

Added support for gemini-ultra model in generative-palm module, added error checks for generative results in gRPC API

#### v1.23.8

Nodes API improvements, support for baseURL setting for Azure OpenAI endpoints in generative-openai module, CREF panic on invalid payload Fix

#### v1.23.7

BM25/WAND internal errors logic improvement, gRPC API groupby Fix

#### v1.23.6

Support for OpenAI's V3 embedding models, gRPC nested objects missing value and shard and replica selection Fixes

#### v1.23.5

AWS module gRPC headers, OpenAI error response, Hybrid vector search and Keyword search with special characters Fixes

#### v1.23.4

gRPC API Fixes, Added support for SageMaker in text2ve-aws module, Sharded locks lock contention Fix

#### v1.23.3

gRPC API improvements

#### v1.23.2

gRPC API generative search Fix, support for baseURL in Azure OpenAI endpoints in text2vec-openai module

#### v1.23.1

gRPC API enhancements, PQ stability Fixes, Cycle Manager Improvements

#### v1.23.0

Binary quantization support, Startup time improvements, New Generative Anyscale module, gRPC API performance improvements

#### v1.22.13

Fix cardinality issues for backup-related metrics

#### v1.22.12

Fixes for Pread segments, BM25 stability, Schema deadlocks

#### v1.22.11

Regex error in keyword search when passing special characters Fix

#### v1.22.10

Sharded locks lock contention Fix

#### v1.22.9

PQ stability Fixes, Cycle Manager Improvements

#### v1.22.8

Support for Google's latest Gecko embedding models, Batch deletions with enabled replication Fix

#### v1.22.7

Added support for Google's Gemini model in generative-palm module

#### v1.22.6

Performance optimizations, gRPC API and other Fixes

#### v1.22.5

New text2vec-aws and generative-aws modules, HNSW locking improvements, gRPC TLS support, hybrid score and other Fixes

#### v1.22.4

Added support for Google MakerSuite API in PaLM modules, gRPC API and PQ-enabled backup Fixes

#### v1.22.3

New text2vec-jinaai module, added support for new AI models in OpenAI and Cohere modules, gRPC API Fixes

#### v1.22.2

ContainsAny / All operator error in cluster environment Fix

#### v1.22.1

Import performance improvements, New vector\_segments\_metric metric, Cluster API communications Fix

#### v1.22.0

Async Indexing, Nested Object Support, gRPC API Support, Schema Repair, OIDC Group Auth, and many other improvements & fixes

#### v1.21.9

ContainsAny / All operator error in cluster environment Fix

#### v1.21.8

Multi-Tenancy startup and shutdown initialization improvements, added support for text\[\] property vectorization in bind and clip modules

#### v1.21.7

Metrics clean up on class/shard delete Fix

#### v1.21.6

Configurable CORS settings, multi tenancy backup Fix

#### v1.21.5

BM25 search no results in some situations Fix and text2vec-huggingface response parsing Fix

#### v1.21.4

New baseURL setting in all OpenAI modules, gRPC API improvements and other Fixes

#### v1.21.3

Improved schema resiliency, backup locking, PaLM module and gRPC API improvements

#### v1.21.2

Cluster API authentication, gRPC improvements, deadlock between backup and replication fix and other Fixes

#### v1.21.1

Fix vulnerability, support for OpenAI-Organization header and other Fixes

#### v1.21.0

Contains Operators, pread, backup compression, Import Performance, Inactive Tenants, and much more!

#### v1.20.6

Fix vulnerability, improve stability

#### v1.20.5

PQ related Fixes

#### v1.20.4

Hybrid oversearch, improved remote node repair and disallowance of restoring backup from higher version Fixes

#### v1.20.3

Multi-Tenancy search using cross-reference and proper vector sync to target nodes during read repair Fixes

#### v1.20.2

Multi-Tenancy validation during update, support for consistency level check in nearVector queries, hybrid and reranker-cohere module Fixes

#### v1.20.1

Multi-Tenancy error handling improvements and explainScore and single results with relativeScoreFusion fixes

#### v1.20.0

Multi-Tenancy, Rerankers, PQ General Availability, & more

#### v1.19.13

Fix vulnerability

#### v1.19.12

Combined Query Dimensions Metric and Unbounded concurrency, Weaviate blocking at startup Fixes

#### v1.19.11

Fix query vectorizer in text2vec-openai module

#### v1.19.10

Fix unbounded connections spike, add schema cluster status debugging insights

#### v1.19.9

RoaringSet metric grouping Fix

#### v1.19.8

Metrics, Auto Schema, Batch and Hybrid Fixes

#### v1.19.7

PQ Rescore, Group Metrics, Data Corruption Fixes

#### v1.19.6

Fixes for cycle manager, gRPC API, PQ performance improvements and more

#### v1.19.5

Fix for including an argument to a class with multiple modules enabled

#### v1.19.4

Fixes for Google PaLM modules, hybrid search limit in gRPC calls

#### v1.19.3

Fixes for many classes + grpc, memory leaks, and more

#### v1.19.2

Fix for multiple enabled modules

#### v1.19.1

Google PaLM text2vec-palm and generative-palm modules

#### v1.19.0

Grouping API, Text Bitmap Filters & better tokenization, Generative Cohere Module & more

#### v1.18.6

Fix vulnerability

#### v1.18.5

Fixes for BM25 filter, class name casing permutations, backups and more

#### v1.18.4

Various Fixes, Support Azure in all OpenAI modules

#### v1.18.3

Peformance and Reliability Fixes for Cross-Refs, Modules, Many-Class-Situations, and others

#### v1.18.2

Fix filter bugs, Autoschema casing, Filesystem Backups, and others

#### v1.18.1

Faster Cross-Ref Filtering, Fixes for Many-Class-Setups, BM25/Hybrid, Replication, and more

#### v1.18.0

Bitmap Indexing, HNSW-PQ, Hybrid Filters, Cursors, Tunable Consistency, Repairs, Azure Backups

#### v1.17.6

Reliability and Performances Fixes for Backups, Hybrid, Bm25, References

#### v1.17.5

Various fixes (Validation, BM25 Multi Node, Error Handling)

#### v1.17.4

Reliability Fixes

#### v1.17.3

Various Fixes for Backups, Cluster config, Support new Generative Modules

#### v1.17.2

Fixes for Hybrid Search with References, Geo Props, and more

#### v1.17.1

Fixes for Hybrid Search, Replication, and others

#### v1.17.0

Introduces Replication, Hybrid Search, and BM25(F)

#### v1.16.9

Fix text2vec-openai model version in query, node api object count

#### v1.16.8

Autoschema fixes, support different model versions in text2vec-openai

#### v1.16.7

Fixes Group/nearVector, adds better defaults for Cohere t2v module

#### v1.16.6

Adds OpenAI QnA as alternative for deprecated "Answers", adds skip re-vectorize

#### v1.16.5

Fixes potential security vulnerabilities

#### v1.16.4

Fixes for null-state filtering

#### v1.16.3

Another fix for a potential SEGFAULT crash

#### v1.16.2

Fixes for a potential SEGFAULT crash, and a stuck API (deadlock)

#### v1.16.1

Fixes for a concurrent import/query performance issue, and len() filter

#### v1.16.0

Distributed Backups, Null Prop Indexing, New & Improved Modules, and much more.

#### v1.15.5

Fixes around patching empty arrays, vectors inside refs, OIDC Well-known path.

#### v1.15.4

Fixes for Aggregations, AWS Backup IAM, and others.

#### v1.15.3

Fix for issue with vector cache limit (introduced in v1.15.1).

#### v1.15.2

Fix for an aggregation edge case.

#### v1.15.1

Fixes around Indexing, Sorting, Aggregation, UX, and more.

#### v1.15.0

Backups, faster aggregations, lower memory consumption, GOMEMLIMIT, various fixes, new modules, and new distance metrics.

#### v1.14.1

Fix for a startup issue that could result in a nil-pointer panic

#### v1.14.0

Critical reliability fixes (potential data loss, MTTR, API namespacing...), observability, non-cosine distances.

#### v1.13.2

L2 distance (preview), bug fixes

#### v1.13.1

Fixes a Delete Performance Degredation

#### v1.13.0

Includes Sorting, Faceted Search, Timestamp filters and Batch-delete-by-query

#### v1.12.2

Fixes a crash-recovery issue, as well as other smaller issues.

#### v1.12.1

Fixes a critical bug that was introduced in v1.12.0 (out of range panic)

#### v1.12.0

More control over inverted indexing: tokenization, stopwords. Reliability and performance fixes. Contains a bug, use v1.12.2 instead.

#### v1.11.0

Plenty of reliability fixes. Allows setting API Key in Open AI module at query time.

#### v1.10.1

Fixes bug around group/merge in Get.

#### v1.10.0

Adds support for text2vec-openai, qna reranking, several quality-of-life improvements.

#### v1.9.1

Contains a total of 9 bugfixes over the previous version. Allows running multiple modules for the same media type without conflicts.

#### v1.9.0

Adds support for multi2vec modules and adds several bugfixes.

#### v1.8.0

Previous release including support for Horizontal Scaling and various fixes around resiliency. Also adds Pagination and filter improvements, such as flat search cut-off and partial caching.

#### v1.7.2

Previous release including multiple bug fixes around prop name validation and array types.

#### v1.7.1

Bugfix release including a bugfix when array types are used with text2vec-contextionary.

#### v1.7.0

Support for various new modules, including ner and spellcheck. Bugfixes.

#### v1.6.0

Introducing zeroshot classifications.

#### v1.5.2

Includes an important bug fix.

#### v1.5.1

Includes various bug fixes.

#### v1.5.0

The release introducing LSM-tree storage and Auto-Schema.

#### v1.4.1

The last version using a B+Tree based storage.

v1.4.0

v1.3.0

v1.2.1

v1.2.0

v1.1.0

v1.0.4

v1.0.3

v1.0.2

v1.0.1

v1.0.0

PreviousNext

## Environment variables [​](https://docs.weaviate.io/deploy/installation-guides/docker-installation\#environment-variables "Direct link to Environment variables")

You can use environment variables to control your Weaviate setup, authentication and authorization, module settings, and data storage settings.

List of environment variables

A comprehensive of list environment variables [can be found on this page](https://docs.weaviate.io/deploy/configuration/env-vars).

## Example configurations [​](https://docs.weaviate.io/deploy/installation-guides/docker-installation\#example-configurations "Direct link to Example configurations")

Here are some examples of how to configure `docker-compose.yml`.

### Persistent volume [​](https://docs.weaviate.io/deploy/installation-guides/docker-installation\#persistent-volume "Direct link to Persistent volume")

We recommended setting a persistent volume to avoid data loss as well as to improve reading and writing speeds.

Make sure to run `docker compose down` when shutting down. This writes all the files from memory to disk.

**With named volume**

```codeBlockLines_e6Vv
services:
  weaviate:
    volumes:
        - weaviate_data:/var/lib/weaviate
    # etc

volumes:
    weaviate_data:

```

After running a `docker compose up -d`, Docker will create a named volume `weaviate_data` and mount it to the `PERSISTENCE_DATA_PATH` inside the container.

**With host binding**

```codeBlockLines_e6Vv
services:
  weaviate:
    volumes:
      - /var/weaviate:/var/lib/weaviate
    # etc

```

After running a `docker compose up -d`, Docker will mount `/var/weaviate` on the host to the `PERSISTENCE_DATA_PATH` inside the container.

### Weaviate without any modules [​](https://docs.weaviate.io/deploy/installation-guides/docker-installation\#weaviate-without-any-modules "Direct link to Weaviate without any modules")

An example Docker Compose setup for Weaviate without any modules can be found below. In this case, no model inference is performed at either import or search time. You will need to provide your own vectors (e.g. from an outside ML model) at import and search time:

```codeBlockLines_e6Vv
services:
  weaviate:
    image: cr.weaviate.io/semitechnologies/weaviate:1.33.0
    ports:
    - 8080:8080
    - 50051:50051
    restart: on-failure:0
    environment:
      QUERY_DEFAULTS_LIMIT: 25
      AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: 'true'
      PERSISTENCE_DATA_PATH: '/var/lib/weaviate'
      CLUSTER_HOSTNAME: 'node1'

```

### Weaviate with the `text2vec-transformers` module [​](https://docs.weaviate.io/deploy/installation-guides/docker-installation\#weaviate-with-the-text2vec-transformers-module "Direct link to weaviate-with-the-text2vec-transformers-module")

An example Docker Compose file with the transformers model [`sentence-transformers/multi-qa-MiniLM-L6-cos-v1`](https://huggingface.co/sentence-transformers/multi-qa-MiniLM-L6-cos-v1) is:

```codeBlockLines_e6Vv
services:
  weaviate:
    image: cr.weaviate.io/semitechnologies/weaviate:1.33.0
    restart: on-failure:0
    ports:
    - 8080:8080
    - 50051:50051
    environment:
      QUERY_DEFAULTS_LIMIT: 20
      AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: 'true'
      PERSISTENCE_DATA_PATH: "./data"
      DEFAULT_VECTORIZER_MODULE: text2vec-transformers
      ENABLE_MODULES: text2vec-transformers
      TRANSFORMERS_INFERENCE_API: http://text2vec-transformers:8080
      CLUSTER_HOSTNAME: 'node1'
  text2vec-transformers:
    image: cr.weaviate.io/semitechnologies/transformers-inference:sentence-transformers-multi-qa-MiniLM-L6-cos-v1
    environment:
      ENABLE_CUDA: 0 # set to 1 to enable
      # NVIDIA_VISIBLE_DEVICES: all # enable if running with CUDA

```

Note that transformer models are neural networks built to run on GPUs. Running Weaviate with the `text2vec-transformers` module and without GPU is possible, but it will be slower. Enable CUDA with `ENABLE_CUDA=1` if you have a GPU available.

For more information on how to set up the environment with the
`text2vec-transformers` integration, see [this\\
page](https://docs.weaviate.io/weaviate/model-providers/transformers/embeddings).

The `text2vec-transformers` module requires at least Weaviate version `v1.2.0`.

### Unreleased versions [​](https://docs.weaviate.io/deploy/installation-guides/docker-installation\#unreleased-versions "Direct link to Unreleased versions")

Unreleased software

DISCLAIMER: Release candidate images and other unreleased software are not supported.

Unreleased software and images may contain bugs. APIs may change. Features under development may be withdrawn or modified. Do not use unreleased software in production.

To run an unreleased version of Weaviate, edit your configuration file to use the unreleased image instead of a generally available image. The [GitHub releases page](https://github.com/weaviate/weaviate/releases/) lists generally available and release candidate builds.

For example, to run a Docker image for a release candidate, edit your `docker-config.yaml` to import the release candidate image.

```codeBlockLines_e6Vv
image: cr.weaviate.io/semitechnologies/weaviate:1.23.0-rc.1

```

## Multi-node configuration [​](https://docs.weaviate.io/deploy/installation-guides/docker-installation\#multi-node-configuration "Direct link to Multi-node configuration")

To configure Weaviate to use multiple host nodes, follow these steps:

- Configure one node as a "founding" member
- Set the `CLUSTER_JOIN` variable for the other nodes in the cluster.
- Set the `CLUSTER_GOSSIP_BIND_PORT` for each node.
- Set the `CLUSTER_DATA_BIND_PORT` for each node.
- Set the `RAFT_JOIN` each node.
- Set the `RAFT_BOOTSTRAP_EXPECT` for each node with the number of voters.
- Optionally, set the hostname for each node using `CLUSTER_HOSTNAME`.

(Read more about [horizontal replication in Weaviate](https://docs.weaviate.io/weaviate/concepts/cluster).)

So, the Docker Compose file includes environment variables for the "founding" member that look like this:

```codeBlockLines_e6Vv
  weaviate-node-1:  # Founding member service name
    ...  # truncated for brevity
    environment:
      CLUSTER_HOSTNAME: 'node1'
      CLUSTER_GOSSIP_BIND_PORT: '7100'
      CLUSTER_DATA_BIND_PORT: '7101'
      RAFT_JOIN: 'node1,node2,node3'
      RAFT_BOOTSTRAP_EXPECT: 3

```

And the other members' configurations may look like this:

```codeBlockLines_e6Vv
  weaviate-node-2:
    ...  # truncated for brevity
    environment:
      CLUSTER_HOSTNAME: 'node2'
      CLUSTER_GOSSIP_BIND_PORT: '7102'
      CLUSTER_DATA_BIND_PORT: '7103'
      CLUSTER_JOIN: 'weaviate-node-1:7100'  # This must be the service name of the "founding" member node.
      RAFT_JOIN: 'node1,node2,node3'
      RAFT_BOOTSTRAP_EXPECT: 3

```

Below is an example configuration for a 3-node setup. You may be able to test [replication](https://docs.weaviate.io/deploy/configuration/replication) examples locally using this configuration.

Docker Compose file for a replication setup with 3 nodes

```codeBlockLines_e6Vv
services:
  weaviate-node-1:
    init: true
    command:
    - --host
    - 0.0.0.0
    - --port
    - '8080'
    - --scheme
    - http
    image: cr.weaviate.io/semitechnologies/weaviate:1.33.0
    ports:
    - 8080:8080
    - 6060:6060
    - 50051:50051
    restart: on-failure:0
    volumes:
      - ./data-node-1:/var/lib/weaviate
    environment:
      LOG_LEVEL: 'debug'
      QUERY_DEFAULTS_LIMIT: 25
      AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: 'true'
      PERSISTENCE_DATA_PATH: '/var/lib/weaviate'
      ENABLE_API_BASED_MODULES: 'true'
      CLUSTER_HOSTNAME: 'node1'
      CLUSTER_GOSSIP_BIND_PORT: '7100'
      CLUSTER_DATA_BIND_PORT: '7101'
      RAFT_JOIN: 'node1,node2,node3'
      RAFT_BOOTSTRAP_EXPECT: 3

  weaviate-node-2:
    init: true
    command:
    - --host
    - 0.0.0.0
    - --port
    - '8080'
    - --scheme
    - http
    image: cr.weaviate.io/semitechnologies/weaviate:1.33.0
    ports:
    - 8081:8080
    - 6061:6060
    - 50052:50051
    restart: on-failure:0
    volumes:
      - ./data-node-2:/var/lib/weaviate
    environment:
      LOG_LEVEL: 'debug'
      QUERY_DEFAULTS_LIMIT: 25
      AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: 'true'
      PERSISTENCE_DATA_PATH: '/var/lib/weaviate'
      ENABLE_API_BASED_MODULES: 'true'
      CLUSTER_HOSTNAME: 'node2'
      CLUSTER_GOSSIP_BIND_PORT: '7102'
      CLUSTER_DATA_BIND_PORT: '7103'
      CLUSTER_JOIN: 'weaviate-node-1:7100'
      RAFT_JOIN: 'node1,node2,node3'
      RAFT_BOOTSTRAP_EXPECT: 3

  weaviate-node-3:
    init: true
    command:
    - --host
    - 0.0.0.0
    - --port
    - '8080'
    - --scheme
    - http
    image: cr.weaviate.io/semitechnologies/weaviate:1.33.0
    ports:
    - 8082:8080
    - 6062:6060
    - 50053:50051
    restart: on-failure:0
    volumes:
      - ./data-node-3:/var/lib/weaviate
    environment:
      LOG_LEVEL: 'debug'
      QUERY_DEFAULTS_LIMIT: 25
      AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: 'true'
      PERSISTENCE_DATA_PATH: '/var/lib/weaviate'
      ENABLE_API_BASED_MODULES: 'true'
      CLUSTER_HOSTNAME: 'node3'
      CLUSTER_GOSSIP_BIND_PORT: '7104'
      CLUSTER_DATA_BIND_PORT: '7105'
      CLUSTER_JOIN: 'weaviate-node-1:7100'
      RAFT_JOIN: 'node1,node2,node3'
      RAFT_BOOTSTRAP_EXPECT: 3

```

Port number conventions

It is a Weaviate convention to set the `CLUSTER_DATA_BIND_PORT` to 1 higher than `CLUSTER_GOSSIP_BIND_PORT`.

## Shell attachment options [​](https://docs.weaviate.io/deploy/installation-guides/docker-installation\#shell-attachment-options "Direct link to Shell attachment options")

The output of `docker compose up` is quite verbose as it attaches to the logs of all containers.

You can attach the logs only to Weaviate itself, for example, by running the following command instead of `docker compose up`:

```codeBlockLines_e6Vv
# Run Docker Compose
docker compose up -d && docker compose logs -f weaviate

```

Alternatively you can run docker compose entirely detached with `docker compose up -d` _and_ then poll `{bindaddress}:{port}/v1/meta` until you receive a status `200 OK`.

## Troubleshooting [​](https://docs.weaviate.io/deploy/installation-guides/docker-installation\#troubleshooting "Direct link to Troubleshooting")

### Set `CLUSTER_HOSTNAME` if it may change over time [​](https://docs.weaviate.io/deploy/installation-guides/docker-installation\#set-cluster_hostname-if-it-may-change-over-time "Direct link to set-cluster_hostname-if-it-may-change-over-time")

In some systems, the cluster hostname may change over time. This is known to create issues with a single-node Weaviate deployment. To avoid this, set the `CLUSTER_HOSTNAME` environment variable in the `values.yaml` file to the cluster hostname.

```codeBlockLines_e6Vv
---
services:
  weaviate:
    # ...
    environment:
      CLUSTER_HOSTNAME: 'node1'
...

```

## Related pages [​](https://docs.weaviate.io/deploy/installation-guides/docker-installation\#related-pages "Direct link to Related pages")

- If you are new to Docker, see [Docker Introduction for Weaviate Users](https://weaviate.io/blog/docker-and-containers-with-weaviate).
