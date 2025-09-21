---
url: "https://weaviate-python-client.readthedocs.io/en/stable/changelog.html"
title: "Changelog — Weaviate Python Client 4.16.10 documentation"
---

- [Home](https://weaviate-python-client.readthedocs.io/en/stable/index.html)
- Changelog
- [View page source](https://weaviate-python-client.readthedocs.io/en/stable/_sources/changelog.rst.txt)

* * *

# Changelog [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#changelog "Link to this heading")

## Version 4.16.10 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-16-10 "Link to this heading")

This patch version includes:

- Addition of helper to create an uncompressed quantizer for use when not using default compression

- Support for `overwrite_alias` option to backup create/restore

- Support for OIDC groups

- Addition of `multi2vec-aws` and `text2vec-morph` modules

- Support for `alias.exists` method

- Update to `weaviate-agents-client` dependency for GA release of agents


## Version 4.16.9 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-16-9 "Link to this heading")

This patch version includes:

- Explicitly depend on protobuf package


## Version 4.16.8 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-16-8 "Link to this heading")

This patch version includes:

- Further attempted fixes for `protobuf` compatability issues

- Introduction of the `backups.list()` method


## Version 4.16.7 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-16-7 "Link to this heading")

This patch version includes:

- Fixes compatability issues between the built gRPC stubs and differing protobuf versions depending on the version of `grpcio` used to build the stubs

- Add `text2vec-model2vec` module to `Configure.NamedVectors`

- Deprecated `min_occurrences` in `Metrics.text` in favour of `limit`


## Version 4.16.6 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-16-6 "Link to this heading")

This patch version includes:

- Add `dimensions` property to `text2vec-transformers` vectorizers in `Configure.Vectors`

- Add `text2vec-model2vec` vectorizer in `Configure.Vectors`

- Deprecate `text2vec-contextionary` vectorizer


## Version 4.16.5 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-16-5 "Link to this heading")

This patch version includes:

- Add `dimensions` property to Google vectorizers in `Configure.Vectors`


## Version 4.16.4 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-16-4 "Link to this heading")

This patch version includes:

- Changes default value for `vectorize_collection_name` to `True` in new methods of `Configure.Vectors` and `Configure.MultiVectors`
\- This is a short-term fix to implicit default behaviour that is caused by an server-side issue
\- Once that is resolved, then this default will be changed back to `False` in a future release


## Version 4.16.3 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-16-3 "Link to this heading")

This patch version includes:

- Fix for dates with nananosecond precision

- Relax requirements for grcp dependencies and support protobuf 4, 5 and 6


## Version 4.16.2 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-16-2 "Link to this heading")

This patch version includes:

- Renames `model_id` to `model` in `Configure.Vectors`


## Version 4.16.1 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-16-1 "Link to this heading")

This patch version includes:

- Fixes capitalization of alias permissions

- Changes default value for `vectorize_collection_name` back to `True` in deprecated methods `Configure.Vectorizer` and `Configure.NamedVectors`

- Add `rescore_limit` to RQ configuration


## Version 4.16.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-16-0 "Link to this heading")

This minor version includes:

- Support for new 1.32 features:

- collection aliasing

- replica movement

- RQ configuration

- Restoring of users and RBAC roles from backups

- Support for the new `multi2multivec-jinaai` module


- Introduction of `Configure.Vectors` and `Configure.MultiVectors` and deprecation of legacy `Configure.Vectorizer` and `Configure.NamedVectors`

- Usage of `Configure.MultiVectors` is reserved for modules like `text2multivec-jinaai`, which was previously known as `text2colbert-jinaai`


- Addition of helper methods for updating tenant activity statuses: `collection.tenants.activate()`, `collection.tenants.deactivate()` and `collection.tenants.offload()`


## Version 4.15.4 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-15-4 "Link to this heading")

This patch version includes:

- Adds deprecation warning for connecting to Weaviate Cloud (WCD) using OIDC. Support for this will be removed in early August, please switch to using API keys instead.


## Version 4.15.3 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-15-3 "Link to this heading")

This patch version includes:

- Allows newer versions of authlib as dependency


## Version 4.15.2 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-15-2 "Link to this heading")

This patch version includes:

- Fixes adding the original weaviate error message to our exceptions for async client


## Version 4.15.1 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-15-1 "Link to this heading")

This patch version includes:

- Adds the original weaviate error message to our exceptions


## Version 4.15.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-15-0 "Link to this heading")

This minor version includes:

- Support for new 1.31 features:
\- Adding new named vectors to existing collections
\- Support for bm25 operators
\- Mueva configuration

- Fixes config.get() for multivector collections

- Copy context to ensure open telemetry makes it to batch requests

- Update cohere models

- Update voyageai models

- Update embedded version to 1.30.5

- Fix storage location for embedded mode

- Add agents docs to the readthedocs page


## Version 4.14.4 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-14-4 "Link to this heading")

This patch version includes:

- Fixes interfaces for user.db/oidc

- If a string is passed into auth= we assume that it is an api-key

- Fix extracting nested array properties from data models


## Version 4.14.3 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-14-3 "Link to this heading")

This patch version includes:

- Fixes return type for aggregate with group\_by and zero results

- Fix multi-vector with hybrid search


## Version 4.14.2 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-14-2 "Link to this heading")

not released

## Version 4.14.1 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-14-1 "Link to this heading")

This patch version includes:

- Fixes a missing `typing.overload` specification for the `query.bm25` method


## Version 4.14.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-14-0 "Link to this heading")

This minor version includes a major update to the docstrings and documentation of the client.

- All docstrings have been aligned with Google’s style format

- The read-the-docs page has been streamlined and improved for ease of use: [https://weaviate-python-client.readthedocs.io/en/stable/](https://weaviate-python-client.readthedocs.io/en/stable/)

- Fixes a bug when adding a property to a collection configured with both named vectors and a generative module

- Potential fixes for race conditions when instantiating async clients

- A number of minor fixes to the public .pyi stub files found by developing a stub auto-generating tool for the codebase


## Version 4.13.2 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-13-2 "Link to this heading")

This patch version includes:

- Fixes a parsing bug when providing URLs with `GenerativeConfig` for runtime generate queries


## Version 4.13.1 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-13-1 "Link to this heading")

This patch version includes:

- Fixes `generative.near_text()` to not require `generative_provider`


## Version 4.13.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-13-0 "Link to this heading")

This minor version provides a complete top-down refactor of the underlying transport for the sync and async clients.

- Introduction of a dependency injection system whereby the sync/async connections are injected into each client independently thereby removing their cross-dependency.

- Removal of the `event_loop.py` file and all logic surrounding its usage by the sync client.

- Refactoring of the batching algorithm to use blocking threads with a sync connection, rather than the event loop sidecar thread.


## Version 4.12.1 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-12-1 "Link to this heading")

This patch version includes:

- Renames `GenerativeConfig.openai_azure` to `GenerativeConfig.azure_openai` to align with the convention of `Configure.Generative.azure_openai`


## Version 4.12.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-12-0 "Link to this heading")

This minor version includes:

- Support for new 1.30 features:

- Dynamic user management of OIDC and native DB users

- Improved multi-dimensional/colBERT vectors

- Query-time configuration of generative modules

- Tenant-based filtering of data permissions in RBAC

- The new `generative-xai` module


## Version 4.11.3 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-11-3 "Link to this heading")

This patch version includes:

- Fixes a rare bug when the batching algorithm waits for async indexing to complete far beyond the maximum number of allowed retries

- Removes the sync-in-async warning emitted by the sync client when used in an async context due to the warning being erroneously emitted in notebooks


## Version 4.11.2 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-11-2 "Link to this heading")

This patch version includes:

- Adds exponential backoff on the UNAVAILABLE gRPC error code for the BatchObjects method

- This is used in the batching algorithm and in `data.insert_many`

- Max number of retries is configurable using the `WEAVIATE_BATCH_MAX_RETRIES` env var


- Adds support for OIDC when using the `text2vec-weaviate` module

- Adds support for updating descriptions of properties in collections (needs compatible server version)

- Adds warning recommending to refactor to use AsyncClient if the SyncClient is used in an async context

- Fixes bugs when importing/exporting collection configurations with respect to property module configs

- Fixes bug when exporting config with multivector enabled between versions


## Version 4.11.1 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-11-1 "Link to this heading")

This patch version incldues:

- Fixes exporting of named vector collections

- Support for upcoming weaviate agents. User `pip install weaviate-client[agents]` to try it out

- Raise error if a header with value None\` has been added

- Introduce `collections.use` as an alias for `collections.get`

- `collections.use` is the preferred method to create an in-memory collection object

- `collections.get` will be deprecated in the future and should not be used in new code


## Version 4.11.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-11-0 "Link to this heading")

This minor version includes:

- Support for new 1.29 features:

- RBAC is ready for production

- Multi-dimensional/COLBert vectors experimental, breaking changes are expected

- Aggregations are using GRPC now


- Improved exception handling for errors returned by Weaviate

- Add support for NVIDIA modules:

- multi2vec-nvidia

- text2vec-nvidia

- generative-nvidia


## Version 4.10.4 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-10-4 "Link to this heading")

This patch version incldues:

- Fix missing dimensions parameter in text2vec-azure-openai


## Version 4.10.3 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-10-3 "Link to this heading")

This patch version includes:

- Add experimental debug namespace

- Add support for dynamic backup location

- Fix potential deadlock in batching

- Fix backup and restore for embedded mode

- Add extra method for text2vec\_google\_aistudio


## Version 4.10.2 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-10-2 "Link to this heading")

This patch version includes:

- Fixes issue with query parameters in `cluster.nodes` method due to dependence on bugged behaviour of `httpx` that was fixed in `0.28.0`


## Version 4.10.1 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-10-1 "Link to this heading")

This patch version includes:

- Fixes compatibility with `httpx` to 0.28.X which requires updating the minimum required version to 0.26.0

- Remove outdated docs


## Version 4.10.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-10-0 "Link to this heading")

This minor version includes:

- Support for new 1.28 features:

- RBAC (experimental, breaking changes are expected)


- Add VoyageAI’s new multimodal embedding model

- Remove copy of v3-client. If you are still using v4 code please either:

- Update your code to v4: [https://weaviate.io/developers/weaviate/client-libraries/python/v3\_v4\_migration](https://weaviate.io/developers/weaviate/client-libraries/python/v3_v4_migration)

- Use the v3-client directly: weaviate-client>=3.26.7;<4.0.0


- Upgrade protobuf to v5

- Add support for python 3.13

- Weaviate v1.23 and v1.24 are NOT supported anymore


## Version 4.9.6 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-9-6 "Link to this heading")

This release is the last release that supports weaviate v1.23 and v1.24

This patch version includes:

- Add support for the new `Kagame_JA` tokenizer


## Version 4.9.5 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-9-5 "Link to this heading")

This patch version includes:

- Add support for the new `text2vec-weaviate` module

- Wrap `tenant.get` `AioRpcError` in a specific exception


## Version 4.9.4 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-9-4 "Link to this heading")

This patch version includes:

- Add support for `multi2vec-jinaai`

- Add support for `multi2vec-cohere`

- Add support for time-based deletion strategy

- Fix type restriction on include\_vector in QueryReference


## Version 4.9.3 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-9-3 "Link to this heading")

This patch version includes:

- Fixes interface for updating generative and reranker collection settings


## Version 4.9.2 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-9-2 "Link to this heading")

This patch version includes:

- Suppress gRPC library warnings for each event loop used in each process


## Version 4.9.1 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-9-1 "Link to this heading")

This patch version includes:

- Fix event loop being used from multiple processes

- Add updating generative and reranker collection settings

- Add experimental backoff for GRPC UNAVAILABLE error codes

- Automatically pick up GRPC message size from Weaviate

- Remove octoai vectorizer and generative methods. They are shutting down


## Version 4.9.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-9-0 "Link to this heading")

This minor version includes:

- Support for new 1.27 features:

- Multi vector search for near\_vector and hybrid

- Backup cancellation

- Vector search filter strategy (acorn)


- Renaming `*-palm` to `*-google` for generative and vectorization modules.

- Typing fixes

- Bump of default embedded version to 1.26.6

- Allow `return_properties={True, False}` as equivalents to `{None, []}`

- Dependency updates


## Version 4.8.1 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-8-1 "Link to this heading")

This patch version includes:

- Suppresses warning emitted by `protobuf` library in relation to obsolate generated stubs

- Fixes the `authlib` to `<1.32.2` while a potential bug is investigated

- Updates the `validators` dependency


## Version 4.8.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-8-0 "Link to this heading")

This minor version includes:

- Support for new modules:

- Mistral text2vec module

- Friendli generative module

- Databricks text2vec and generative modules


- New `fetch_objects_by_ids` method

- Support for hybrid search with vector distance

- Fixes issue with adding a property on a vectorized collection

- Bumps `requests`, `importlib-metadata`, ``pytest` ``, `pytest-asyncio`, `types-requests`, `litestar` and `typing-extensions` libs to newest versions


## Version 4.7.1 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-7-1 "Link to this heading")

This patch version includes:

- Fixes log noise due to value of deprecated `GRPC_VERBOSITY` flag in underlying `grpc` library

- Bumps `requests` and `authlib` versions to avoid security issues

- Adds support for configuring the new `reranker-jinaai` module when creating collections

- Fixes parsing of the timeout configuration on client instantiation

- The `query` timeout now modifies the `read=` timeout in the `httpx` client for all `GET`, `HEAD`, and `gql` query requests

- The `insert` timeout now modifies the `read=` timeout in the `httpx` client for all `DELETE`, `POST`, `PATCH`, and `PUT` requests

- The `init` timeout now only modifies the timeouts in the `httpx` client for requests involved in the `client.connect()` method


## Version 4.7.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-7-0 "Link to this heading")

This minor version includes:

- The introduction of the `WeaviateAsyncClient` class to support I/O requests to Weaviate using the `async/await` syntax with asyncio <https://docs.python.org/3/library/asyncio.html>

- All methods that perform CRUD and search actions are now `async def` functions

- To instantiate a client quickly, use the `weaviate.use_async_with_x` methods in an async context manager pattern, e.g.:





```
async with weaviate.use_async_with_local() as client:
      # Your code

```

- Note, you cannot do `await weaviate.use_async_with_x` if not using the context manager pattern. You have to create the client first and then connect manually:





```
client = weaviate.use_async_with_local()
await client.connect()
# Your code
await client.close()

```


- A refactoring of the underlying implementation of the `WeaviateClient` to use the `WeaviateAsyncClient` under-the-hood scheduling the necessary coroutines to run in a side-car event-loop thread

- Support for new core Weaviate features in both the sync and async clients:

- Multi-vector search in the `.near_x` and `.hybrid` methods within the `.generate` and `.query` collection namespaces

- Scalar Quantization (SQ) vector index configuration

- Async replication configuration for multi-node Weaviate deployments

- Tenant offloading to S3 cloud storage using the newly intrduced `OFFLOADED` tenant activity status

- Renaming of `HOT` to `ACTIVE` and `COLD` to `INACTIVE` for tenant activity statuses

- NOTE: To use these features, you must have Weaviate version 1.26.0 or higher


## Version 4.6.7 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-6-7 "Link to this heading")

This patch version includes:

- Fix batching with references. Under some circumstances a reference could be added before its `to`-object and the reference would be lost.

- Fix node status for timed out nodes

- Fix parsing the year 0. While weaviate allows to add dates with year zero (“0000-01-30T00:00:00Z”), the datetime library is based on the gregorian calendar which does not have a year zero. The client will years with 0 as the minimum date that is possible in datetime ( `datetime.datetime(1, 1, 1, 0, 0)`) and emit a warning

- Support for custom rerankers and generative modules using `Configure.Generative.custom()` and `Configure.Reranker.custom()`

- Add support for kagome\_kr tokenizer. Requires Weaviate 1.25.8

- Increase default embedded version to 1.25.8


## Version 4.6.6 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-6-6 "Link to this heading")

This patch version includes:

- Log batch errors

- Only the last 100k successfully added UUIDs are kept in memory to prevent OOM situations.

- Fix tenant creation with string input


In the v3 copy that is part of v4:

- Fixes GraphQL query injection vulnerability caused by incorrect escaping of backslashes in plain text input builder methods. Many thanks to [@adamleko](https://github.com/adamleko), [@bismuthsalamander](https://github.com/bismuthsalamander), and [@tardigrade-9](https://github.com/tardigrade-9) for their help in fixing this issue

- Fixes batch retry with tenants


## Version 4.6.5 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-6-5 "Link to this heading")

This patch version includes:

- Addition of new voyageai embedding and rerank models as string literal types

- Added missing exports of submodules in `weaviate.outputs` to aid usage

- Updated ollama modules docstrings

- Added missing `py.typed` file for use by static type checkers


## Version 4.6.4 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-6-4 "Link to this heading")

This patch version includes:

- Add support for auto-tenant-activation (available in Weaviate 1.25.2)


## Version 4.6.3 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-6-3 "Link to this heading")

This patch version includes:

- Removal of top-level validation of `vector` in `data.insert`, `data.replace`, and `data.update`. This validation occurs within the `_get_vector_v4` method now instead.


## Version 4.6.2 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-6-2 "Link to this heading")

This patch version includes:

- Respect default vectorizer

- Wait for Weaviate 1.25 to be ready before starting the embedded client

- Add missing models for voyageai

- Rename WCS to Weaviate Cloud and add new helper function weaviate.connect\_to\_weaviate\_cloud


## Version 4.6.1 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-6-1 "Link to this heading")

This patch version includes:

- Fixes for `client.integrations.configure`


## Version 4.6.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-6-0 "Link to this heading")

This minor version includes:

- Support for Weaviate 1.25.0:

  - BM25/Hybrid support groupBy parameter

  - Hybrid supports MoveTo/MoveAwayFrom in near\_vector and near\_text through HybridVector class

  - Ollama text2vec and generative module

  - Octoai text2vec and generative module

  - multi2vev-palm module

  - dynamic vector index type

  - auto tenant creation

  - improved batching with vectorization

  - tenant exists endpoint

  - get tenant by name
- Added `client.integrations.configure` to configure api-keys and model provider parameters for integration/module-providers without setting headers.

- Improved error messages and deprecation warnings.


## Version 4.5.7 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-5-7 "Link to this heading")

This patch version includes:

- Deprecation of the `bit_compression` field in the `PQConfig` class

- Improvements to closing possibly open objects and connections

- Enhances the `WeaviateGRPCUnavailableError` message with added context relevant to the user’s environment

- Relaxes the `httpx` requirements to aid compatability with other packages


## Version 4.5.6 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-5-6 "Link to this heading")

This patch version includes:

- Support for configuring collections with the new `reranker-voyageai` module

- Providing an `alpha` parameter to `collection.iterator()` to control the beginning of the iteration

- Update the default `Timeout.init` value from `1s` to `2s`


## Version 4.5.5 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-5-5 "Link to this heading")

This patch version includes:

- Bugfix when parsing the result from `v1/nodes` API with `shards: null`

- Bugfix when parsing the result from `v1/schema` API with `class.properties.moduleConfig: null` and `class.vectoriser: !'none'`

- Dependency bumps


## Version 4.5.4 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-5-4 "Link to this heading")

This patch version includes:

- Fix parsing of creation/update time from old weaviate versions that write them in ns instead of ms

- Support `video_fields` in `multi2vec-palm` which was added in Weaviate 1.24.4:


## Version 4.5.3 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-5-3 "Link to this heading")

This patch version includes:

- Fix bug with hybrid searches without vector.

- Support for new modules in Weaviate 1.24.2:
\- `text2vec-voyageai`
\- `generative-mistral`
\- Support new parameters for inference URLs in `text2vec-transformers` and `multi2vec-clip`

- Support for new modules in Weaviate 1.24.3:
\- `multi2vec-palm`


## Version 4.5.2 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-5-2 "Link to this heading")

This patch version includes:

- Fixes endpoint parameter for `text2vec-palm`

- Adds support for GSE and TRIGRAM tokenizers


## Version 4.5.1 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-5-1 "Link to this heading")

This patch version includes:

- Implements an extension to the filtering syntax allowing to pass lists of filters

- `Filter.all_of([f1, f2]])` is a shortcut for `f1 & f2`

- `Filter.any_of([f1, f2]])` is a shortcut for `f1 | f2`

- Can all be chained and mixed together to create dynamic and complex filters


- Introduces `weaviate.classes.init.Timeout` class allowing to define the timeout used when performing client init checks, in addition to connect and query

- Fixes a bug when performing `contains_any/contains_all` filtering using an empty list

- Adds the ability to limit the `top_occurences` return when performing aggregation queries

- Allows for defining gRPC proxying of the client and fixes the parsing of `http` and `https` proxies

- Allow `None` as a query value in BM25 and hybrid queries

- Fix missing named vectors support in `data.update` and `data.replace`

- Reimplement support for updating named vector configurations alongside the patched `1.24.1` server version


## Version 4.5.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-5-0 "Link to this heading")

This minor version includes:

- Full support for the new named vectors feature available in the Weaviate `1.24` release.

- Bugfixes to passing of Weaviate schema objects as collection configurations in certain edge cases.

- Support use of Sagemaker when vectorizing with the `text2vec-aws` module.

- Allow creation of collections that use the `hnsw` index with the `bq` quantizing strategy.

- Allow specifying `dimensions` when vectorizing with the `text2vec-openai` module.

- Python in-memory performance improvements when making queries .


## Version 4.4.4 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-4-4 "Link to this heading")

This patch version includes:

- A fix to the validation logic of the `apiEndpoint` field of `GenerativePaLMConfig` object.


## Version 4.4.3 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-4-3 "Link to this heading")

This patch version includes

- Fixes batching with references. Under some circumstances a reference could be added before its `from`-object and the reference would be lost.

- Fixes readthedocs page

- Small performance improvements for queries


## Version 4.4.2 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-4-2 "Link to this heading")

This patch version includes

- Fixes client.is\_ready().

- Adds option to skip input parameter validation if you need to squeeze out some extra performance.

- All functions that accept vectors now also accept numpy arrays, tensorflow arrays and pandas/polars dataframes as input.

- Hybrid search accepts None as query for a pure vector search.

- Adds `FilterValue` to `weaviate.outputs`.

- Allows `group_by: str` in aggregation queries.


## Version 4.4.1 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-4-1 "Link to this heading")

This patch version includes

- Allows strings as input for `groupBy` arguments for aggregation.

- Fixes for rate limit batching.


## Version 4.4.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-4-0 "Link to this heading")

This version is the first full release for the Python v4 client and \_requires\_ weaviate versions >= 1.23.7.

Since the previous RC, there have been a number of improvements and final bug fixes.
\- The type of `object.vector` has changed from `Optional[Dict[str, List[float]]]` to `Dict[str, List[float]]` so that `object.vector` is never `None`.
\- Exporting and importing of collections has been tidied up and improved.
\- A number of methods have had input validation added to them.
\- Most exceptions are now unified under a few common classes.

For more information around the new client, see here: [https://weaviate.io/developers/weaviate/client-libraries/python](https://weaviate.io/developers/weaviate/client-libraries/python)

## Version 4.4.rc1 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-4-rc1 "Link to this heading")

This version is a release candidate for the python v4 client.

There is a significant breaking change in this version in anticipation of the named vectors functionality of future Weaviate versions.
\- The `vector` property of `Object` has had its type changed from `Optional[List[float]]` to `Optional[Dict[str, List[float]]]`.
\- Accessing of the vector property has changed from `object.vector` to `object.vector["default"]`.
\- When using the client with future releases, other named vectors will be accessible as `object.vector["name"]`.

Newly created (as of 15:00UTC 01/30/24) WCS sandbox instances are now capable of handling gRPC connections and so the client has been updated accordingly in its `connect_to_wcs` method.
If you are using an old sandbox, make a new one and use the new one instead.

Minor bugfixes are also included.

## Version 4.4.rc0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-4-rc0 "Link to this heading")

This version is a release candidate for the python v4 client.

All backward compatibility code is being removed and \_requires\_ weaviate versions >= 1.23.5.

All deprecated code has been removed. Check the migration guide ( [https://www.weaviate.io/developers/weaviate/client-libraries/python#migration-guides](https://www.weaviate.io/developers/weaviate/client-libraries/python#migration-guides)) how to update your code.

Improvements include:
\- Input validation
\- Embedded weaviate shows an error when the chosen port(s) are already occupied

Fixes include:
\- Filter chained references by reference count
\- Various bug with filtered aggregation
\- Aggregation with move to/away\_from objects
\- Timeouts also apply to GRPC calls

## Version 4.4.b9 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-4-b9 "Link to this heading")

This beta version has breaking changes, a migration guide is available at [https://www.weaviate.io/developers/weaviate/client-libraries/python#migration-guides](https://www.weaviate.io/developers/weaviate/client-libraries/python#migration-guides):

- The batching algorithm has been streamlined and improved in its implementation and API surface.

- There are now three types of batching that can be performed:

- `client.batch.dynamic()` where the algorithm will automatically determine the optimal batch size and number of concurrent requests.

- `client.batch.fixed_size()` where the user can specify the batch size and number of concurrent requests.

- `client.batch.rate_limit()` where the user specifies the number of requests per minute that their third-party vectorization API can support.


- If an exception is thrown in the background batching thread then this is surfaced to the main thread and re-raised in order to stop the batch.

- Previously, this would silently error.


- Enforces that all optional arguments to queries must be supplied as keyword arguments.

- Adds runtime validation to all queries.

- Renaming of `prop` to `name` in `Filter.by_property`.

- Moving of the `timeout` argument in `weaviate.connect_to_x` methods into new argument `additional_config: Optional[AdditionalConfig]`.


Improvements include:
\- Introduction of the `.by_ref_count()` method on `Filter` to filter on the number of references present in a reference property of an object.

> - This was previously achievable with `Filter([refProp]).greater_than(0)` but is now more explicit using the chaining syntax.

- The syntax for sorting now feels similar to the new filtering syntax.

- Supports method chaining like `Sort.by_property(prop).by_creation_time()` which will apply the sorting in the order they are chained, i.e.,
this chain is equivalent to the previous syntax of `[Sort(prop), Sort("_creationTimeUnix")]`.


Fixes include:
\- The potential for deadlocks and data races when batching has been reduced.
\- Fixes a number of missing properties and poor docstrings in `weaviate.connect_to_x` methods.
\- Adds the missing `offset` parameter to all queries.

## Version 4.4.b8 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-4-b8 "Link to this heading")

This beta version has breaking changes, a migration guide is available at [https://www.weaviate.io/developers/weaviate/client-libraries/python#migration-guides](https://www.weaviate.io/developers/weaviate/client-libraries/python#migration-guides):

- Filters have been reworked and have a new syntax.

- Coming from <=4.4.b6 you can replace:

- `Filter(path=property)` with `Filter.by_property(property)`

- `Filter(path=["ref","target_class", "target_property"])` with `Filter.by_ref("ref").by_property("target_property")`

- ```FilterMetadata.ByXX``with ``Filter.by_id/creation_time/update_time()```


- Coming from =4.4b7 you can replace:

- `Filter.by_ref().link_on("ref").by_property("target_property")` with `Filter.by_ref("ref").by_property("target_property")`


Bugfixes include:
\- Error message when creating the client directly without calling `connect_to_XXX`.
\- Fix deadlock in new batching algorithm.
\- Fix `skip_init_checks=True` resulting in compatibility with Weaviate 1.22 only.

## Version 4.4.b7 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-4-b7 "Link to this heading")

This beta version has breaking changes, a migration guide is available at [https://www.weaviate.io/developers/weaviate/client-libraries/python#migration-guides](https://www.weaviate.io/developers/weaviate/client-libraries/python#migration-guides):

- For `client.batch` the `add_reference` method was revised. The `to_object_collection` parameter was removed and the other parameters were harmonized with `collection.batch`. Available parameters are now: `from_uuid`, `from_collection`, `from_property`, `to` and `tenant`.

- It is no longer possible to use `client.batch` directly, you must use it as a context manager ( `with client.batch as batch`)

- Manual batch mode has been removed.

- Dynamic batching (for batch\_size and number of concurrent requests) is now default. Fixed-size batching can be configured with `batch.configure_fixed_size(..)`.

- Filters have been reworked and have a new syntax. You can replace:

- `Filter(path=property)` with `Filter.by_property(property)`

- `Filter(path=["ref","target_class", "target_property"])` with `Filter.by_ref().link_on("ref").by_property("target_property")`

- ```FilterMetadata.ByXX``with ``Filter.by_id/creation_time/update_time()```


- Importing directly from `weaviate` has been deprecated. Use `import weaviate.classes as wvc` instead and import from there.

- Multi-target references functions have been moved to:

- `ReferenceProperty.MultiTarget`

- `DataReference.MultiTarget`

- `QueryReference.MultiTarget`


- Exception names are now compatible with PEP8, old names are still available but deprecated.

- References can now be provided directly as `UUIDs`, `str` and `Reference.XXX()` has been deprecated. For multi-target references use `ReferenceToMulti`.


New functionality includes:
\- New batching algorithm that supports dynamic scaling of batch-size and number of concurrent requests.
\- New filter syntax that also supports structured filtering on references for normal properties and metadata.
\- All reference functions have unified input formats and now accept `UUID`, `str` and (where applicable) `List[str]`, `List[UUID]`.
\- Returned types are now available in `weaviate.output`.
\- Add missing classes to `weaviate.classes`.
\- Add missing parameters to `connect_to_XXX`, all functions should support skipping of init checks and auth.
\- The client can now be used in a context manager `with connect_to_XX(..) as client` and all connections will be closed when exiting the manager.
\- New close function `client.close()` that needs to be called when not using a context manager to avoid stale connections and potential memory leaks.
\- Support for `Phonenumber` datatype.
\- Referenced objects now contain the name of their collection.
\- Adds `collection.config.update_shards()`.

Bugfixes include:
\- object.reference is empty instead of None, if an object does not have a reference.
\- Fixes creating backups on weaviate master.
\- Add missing classes to `wvc`.

New client usage:
\- Client as a context manager:

> ```
> with weaviate.connect_to_local() as client:
>     # Your code
>
> ```

- Client without a context manager:


> ```
> try:
>     client = weaviate.connect_to_local()
>     # Your code
> finally:
>     client.close()
>
> ```


## Version 4.4.b6 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-4-b6 "Link to this heading")

This beta version includes:

- A fix to the `_Property` dataclass returned within `collection.config.get()` to include any `nested_properties` of `object` and `object[]` type properties

- Fix batch inserts with empty lists


## Version 4.4.b5 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-4-b5 "Link to this heading")

This beta version includes:

- fetch\_object\_by\_id with Weaviate 1.22 returned `None` for non-existing references

- empty strings in returned objects caused a panic with weaviate 1.22

- Support for nodes/cluster API

- Speed up client creation when connecting to WCS using `connect_to_wcs`

- Checks GRPC availability of Weaviate instance and return an error if it is not supported yet

- Adds `skip_init_checks` to `connect_to_wcs`


With the next Weaviate version (1.23.1) this beta version supports:
\- Blob properties
\- Reranker

## Version 4.4.b4 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-4-b4 "Link to this heading")

This beta version fixes an issue with being unable to disable PQ once enabled

## Version 4.4.b3 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-4-b3 "Link to this heading")

This beta version fixes a naming issue:
\- All instances of `quantitizer` have been renamed to `quantizer`

## Version 4.4.b2 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-4-b2 "Link to this heading")

This version works best with Weaviate 1.23 which was released on 2023-12-18.

This beta version has breaking changes, a migration guide is available at [https://www.weaviate.io/developers/weaviate/client-libraries/python#migration-guides](https://www.weaviate.io/developers/weaviate/client-libraries/python#migration-guides):

- Refactor `weaviate.classes` structure

- Rename various classes and methods:

- In all vectorizer configuration methods: `vectorize_class_name` =\> `vectorize_collection_name`

- `object.metadata.creation_time_unix` =\> `object.metadata.creation_time` which is now a datetime

- `object.metadata.last_update_time_unix` =\> `object.metadata.last_update_time` which is now a datetime

- `MetadataQuery(creation_time_unix=.., last_update_time_unix= ..)` =\> `MetadataQuery(creation_time=.., last_update_time=..)`

- `FromReference` =\> `QueryReference` when querying references


- Splits out references from properties when creating, changing and querying collections

- UUID and UUID\_ARRAY properties are now returned as typed UUID objects

- DATE and DATE\_ARRAY properties are now returned as typed datetime objects

- ```vector_index_type``has been remove from ``collection.create()``` and is now determined automatically

- `Configure.vector_index()` has been moved to `Configure.VectorIndex.hnsw()`

- PQ can now be configured using Configure.VectorIndex.hnsw(quantitizer=Configure.VectorIndex.Quantitizer.pq(..options..))

- `object.metadata.vector` was moved to `object.vector` and can be requested by using `include_vector=True/False` when querying

- `object.metadata.uuid` was moved to `object.uuid` and is always available

- Order of arguments in .data.update() and .replace() changed to accommodate not providing properties when updating.

- In .data.reference\_add, .reference\_delete and .reference\_replace the `ref` keyword was renamed to `to`

- In collections.create() and .get() the keyword to provide generics was renamed from `data_model` to `data_model_properties`


New functionality includes:

- Adds backup functionality to v4 client ( `client.backup`) and directly to the collection ( `collection.backup`)

- Adds support for FLAT vector index

- Adds binary quantization for FLAT vector index

- Adds `text2vec_jinaai` static method to `Configure.Vectorizer`

- Adds `anyscale` static method to `Configure.Generative`

- Adds collection.batch for uploading to a single collection in batches

- Adds methods for creating a collection from dict and exporting a collection config as dict

- Adds support for geo-coordinates

- Adds metadata filtering with `FilterMetadata`

- Adds `client.graphql_raw_query` to use Weaviate features that are not directly supported.

- Adds `DataReferenceOneToMany` which allows to add multiple references at once.

- Adds validation of input parameters for non-mypy users.

- Various performance improvements and bugfixes


## Version 4.4.b1 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-4-b1 "Link to this heading")

This patch beta version includes:

- Performance improvements when making queries


## Version 4.4.b0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-4-b0 "Link to this heading")

This minor beta version includes:

- Adds support for connecting to WCS using the `connect_to_wcs` helper function

- Changes default `num_workers` in `client.batch` from `1` to Python’s `ThreadPoolExecutor` default

- Adds `text2vec-aws` and `generative-aws` static methods to `Configure.Vectorizer` and `Configure.Generative`

- Tidy up stale docstrings

- Add missing class exports


## Version 4.3.b2 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-3-b2 "Link to this heading")

This patch beta version includes:

- Fixes to the `dataclass` types returned by aggregate queries


## Version 4.3.b1 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-3-b1 "Link to this heading")

This patch beta version includes:

- Bump default Weaviate embedded version


## Version 4.3.b0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-3-b0 "Link to this heading")

This minor beta version includes:

- Refactoring of the `_Object` class

- `_Object.metadata.uuid` moved to `_Object.uuid` and is not `Optional`

- `_Object.metadata.vector` moved to `_Object.vector`


- Addition of `include_vector` argument to all queries

- `include_vector` is `False` by default


- `return_metadata` in queries is now `Optional` and defaults to `None`

- `_Object.metadata` is now `Optional` as a result


- Addition of `include_vector` to `FromReference`

- Addition of `ReferenceAnnotation` for use when defining generic annotated cross references


## Version 4.2.b2 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-2-b2 "Link to this heading")

This patch beta version includes:

- Allow `None` when batch inserting using `DataObject` and `BatchObject`


## Version 4.2.b1 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-2-b1 "Link to this heading")

This patch beta version includes:

- Bug fix of the default `alpha` argument to `query.hybrid`

- Extend the `Configure.Vectorizer.multi2vec_` methods to accept lists of strings

- Correctly export `StopwordsPreset` from `weaviate.classes`

- Add `generative_config` and `vectorizer_config` to `_CollectionConfig`

- Add `skip_vectorization` and `vectorize_class_name` to `_PropertyConfig`


## Version 4.2.b0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-2-b0 "Link to this heading")

This minor beta version includes:

- A refactoring of the `collection.aggregate` namespace methods

- Change `Metrics` to no longer accept the `type_` argument

- Instead, `Metrics` has multiple methods, e.g. `.text()`, for each type of metric

- Allow `return_metrics` to be a single metric object or a list of metric objects in each aggregate query


## Version 4.1.b2 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-1-b2 "Link to this heading")

This patch beta version includes:

- Correctly exporting `weaviate.collections.classes.aggregate.Metrics` from `weaviate.classes`


## Version 4.1.b1 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-1-b1 "Link to this heading")

This patch beta version includes:

- Bumping the default embedded version to Weaviate latest

- Adding the `version` argument to `weaviate.connect_to_embedded` to allow users to specify the embedded version


## Version 4.1.b0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-1-b0 "Link to this heading")

This minor beta version includes:

- Makes `total_count=True` the default in aggregation queries to avoid unintentional GraphQL errors

- Catches empty GraphQL errors in aggregation queries in case of user error

- Renames `class_name` to `collections` within the `collections.batch` namespace

- Adds `get_vector` to the `collections.data` namespace so that users can supply numpy and pytorch vectors

- Adds `__str__` magic method to `Collections` class so that `print(collection)` outputs the collection’s schema as pretty JSON


## Version 4.0.b5 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-0-b5 "Link to this heading")

This patch beta version includes:

- Update changelog


## Version 4.0.b4 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-0-b4 "Link to this heading")

This patch beta version includes:

- A small bug fix to remove a redundant print

- Raising an exception from `connect_to_wcs` as gRPC support is not ready

- Making `_Collection` a public class as `Collection` to be used in type hinting


## Version 4.0.b3 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-0-b3 "Link to this heading")

This patch beta version includes:

- Addition of `batch_size` to `client.batch.configure` for users who want automatic non-dynamic batching

- Renaming of `ConfigureUpdate` to `Reconfigure`

- Fixing of missing arguments to `Configure.Vectorizer.text2vec_` methods


## Version 4.0.b2 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-0-b2 "Link to this heading")

This patch beta version includes:

- Fixes to the readthedocs documentation appearance


## Version 4.0.b1 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-4-0-b1 "Link to this heading")

This beta version includes:

- Introduction of the new beta Python collections client API

- Streamlined and simplified client API for mutating and querying your data

- Full support for gRPC batching and searching

- End-to-end generics support for type safety

- Python-native dataclasses for easy data manipulation

- No more builder methods or raw dictionaries


- Join the discussion and contribute your feedback [here](https://forum.weaviate.io/t/python-v4-client-feedback-megathread/892)


## Version 3.26.5 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-26-5 "Link to this heading")

This patch version includes

- Fixes GraphQL query injection vulnerability caused by incorrect escaping of backslashes in plain text input builder methods

- Many thanks to [@adamleko](https://github.com/adamleko), [@bismuthsalamander](https://github.com/bismuthsalamander), and [@tardigrade-9](https://github.com/tardigrade-9) for their help in fixing this issue


## Version 3.26.4 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-26-4 "Link to this heading")

This patch version includes

- Fixes batch retry with tenants


## Version 3.26.2 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-26-2 "Link to this heading")

This patch version includes

- Adds a timeout to wait\_for\_weaviate startup check


## Version 3.26.1 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-26-1 "Link to this heading")

This patch version includes

- Fix backup creation with current weaviate master


## Version 3.26.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-26-0 "Link to this heading")

This minor version includes:

- Support for Weaviate 1.23

- Bump of the default version for Weaviate Embedded DB to v1.23.0

- Adds support for nodes api verbosity option


## Version 3.25.3 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-25-3 "Link to this heading")

This patch version includes

- Bump of the default version for Weaviate Embedded DB to v1.22.3


## Version 3.25.2 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-25-2 "Link to this heading")

This patch version includes

- Fixes to the codebase naming convention and directory structure to prevent collision with Google’s proto-plus library

- Fixes to the build method so that readthedocs.io builds the documentation correctly again


## Version 3.25.1 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-25-1 "Link to this heading")

This patch version includes:

- Bump default embedded version to 1.22.0


## Version 3.25.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-25-0 "Link to this heading")

This minor version includes:

- Support for new Weaviate nested objects on insert and query

- `client.data_object.create()` now supports nested objects

- `client.query.get()` now supports nested objects


- Updates to use Weaviate’s v1 gRPC API

- Support for batching with Weaviate>1.22.0 version and async vector indexing

- Addition of the client.batch.wait\_for\_async\_indexing() method to force block until async indexing is complete

- Add tests for Python 3.12 to ensure compatibility


## Version 3.24.2 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-24-2 "Link to this heading")

This patch version includes:

- Small fix to the batching process to ensure that failed multi-tenant objects are re-added to the batch with their tenant attached


## Version 3.24.1 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-24-1 "Link to this heading")

This patch version updates the `changelog.rst` that became stale over the last few releases

## Version 3.24.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-24-0 "Link to this heading")

This minor version includes:

- Small fixes and improvements throughout the codebase:

- Catching and reraising of `JsonDecodeException` for users to catch

- Client-wide mypy error fixing and type hinting improvements

- Fix for where filter operands in `batch.delete_objects`

- Removal of buggy client-side schema validation

- Package dependency updates


## Version 3.23.2 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-23-2 "Link to this heading")

This patch version includes:

- Enforcing class name capitalization throughout the client

- Further fixes to where filtering with `ContainsAny/All`


## Version 3.23.1 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-23-1 "Link to this heading")

This patch version includes:

- Enabling of `rerank-cohere` module in `EmbeddedWeaviate`

- Fixes for where filtering between `query.get` over GraphQL and `batch.delete_objects` over REST


## Version 3.23.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-23-0 "Link to this heading")

This minor version updates the client to work with Weaviate’s 1.21 version and includes:

- Adds support for `near<Media>` filters when using the new `multi2vec-bind` module for neural searching on different media types

- `client.query.get().with_near_audio()`

- `client.query.get().with_near_depth()`

- `client.query.get().with_near_image()` (unchanged from previous versions but usable by the module)

- `client.query.get().with_near_imu()`

- `client.query.get().with_near_thermal()`

- `client.query.get().with_near_video()`


- Deprecates configuring `client.batch` using `client.batch()` in favour of using `client.batch.configure()`

- `client.batch()` will be removed in a future version

- `client.batch.configure()` will return `None` in a future version

- `with client.batch as batch` should be the standard way to initiate a batch


- Adds support for new `ContainsAny` and `ContainsAll` filters when using `.with_where`

- Adds support for updating individual tenants within a multi-tenancy class configuration: `client.schema.update_class_tenants`

- Improves `client.batch` algorithm to choose batch size dynamically maximizing throughput

- Provides sensible defaults to `client.batch` that do not cause unexpected damaging consequences like infinite batch sizes

- Fixes bugs when using `.with_where` with `valueText`, `valueString`, and `valueGeoRange` types


## Version 3.22.1 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-22-1 "Link to this heading")

This patch version includes:

- Fix “is client outdated”-check in air-gaped environments

- Add `tenant` to batch delete


## Version 3.22.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-22-0 "Link to this heading")

This minor version includes:

- Multi-tenancy

- Aggregate with limit

- Autocut

- Fusion type for hybrid search

- Client emits a warning when it is outdated (three minor version behind last release on pypi)

- Increase default embedded version to 1.19.12


## Version 3.21.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-21-0 "Link to this heading")

This minor version includes:
\- Weaviate Embedded supports MacOs

## Version 3.20.1 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-20-1 "Link to this heading")

This patch version includes:

- Fix imports without GRPC package

- Improve shutdown handling with Weaviate Embedded


## Version 3.20.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-20-0 "Link to this heading")

This minor version includes:

- Increase maximum version of request library to `2.31.0`. This also updates to urllib 2.0. This may contain minor breaking changes if you use urllib in other projects in the same virtual environment.

- Add licensing information to pypi package

- Increase default embedded version to 1.19.7


## Version 3.19.2 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-19-2 "Link to this heading")

This patch version includes:

- Add custom headers to all requests

- Support properties field in generative groupedResult field


## Version 3.19.1 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-19-1 "Link to this heading")

This patch version includes:

- Fixes imports of of `weaviate_pb2`.


## Version 3.19.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-19-0 "Link to this heading")

This minor version includes:

- Increases default embedded version to 1.19.3

- Clients emits warning if used weaviate version is too old (3 versions behind latest minor version)

- Adds native support for querying reference properties


> ```
> result = client.query.get(
>   "Article", ["title", "url", "wordCount", LinkTo(link_on="caller", linked_class="Person", properties=["name"])]
>      )
>
> ```

- Adds dataclasses to easier access to additional properties:


> ```
> query = client.query.get("Test").with_additional(
>             weaviate.AdditionalProperties(
>                 uuid=True,
>                 vector=True,
>                 creationTimeUnix=True,
>                 lastUpdateTimeUnix=True,
>                 distance=True,
>             )
>         )
>
> ```

- Typing fixes

- Expand support for _experimental_ GRPC API and add support for

- BM25 and hybrid search

- Additional properties (via dataclass shown above)

- Querying reference properties (via dataclass shown above)


## Version 3.18.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-18-0 "Link to this heading")

This minor version includes:

- Add support for properties with hybrid search

- Fixes documentation publishing on readthedocs


## Version 3.17.1 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-17-1 "Link to this heading")

This patch version includes:

- Fix schemas with new property keys indexFilterable and indexSearchable.


## Version 3.17.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-17-0 "Link to this heading")

This minor version includes:

- Add support for groupBy to group objects:


> ```
> .with_group_by(properties=["caller"], groups=2, objects_per_group=3)
>
> ```

- Add support for uuid and uuid\[\] datatypes.

- Add schema.exists(class).

- Add support for Support GQL Get{} tunable consistency:


> ```
> resp = (
>     client.query.get("Article", ["name"])
>     .with_additional("isConsistent")
>     .with_consistency_level(ConsistencyLevel.ALL)
>     .do()
> )
>
> ```


## Version 3.16.2 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-16-2 "Link to this heading")

This patch version includes:

- Fix url containing username and password.


## Version 3.16.1 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-16-1 "Link to this heading")

This patch version includes:

- Fixes timeout error in detection of grpc.


## Version 3.16.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-16-0 "Link to this heading")

This minor version includes:

- **Experimental** support for GRPC.

- Can by enabled by installing the client with pip install weaviate-client\[GRPC\] or install the grpcio package manually.

- To disable uninstall the grpcio package.

- This will speed up certain GraphQL queries: Get with NearObject or NearVector if only non-reference queries are retrieved and no other options are set.


- Removal of python 3.7 support. Minimum supported version is python 3.8

- Removal of the WCS module. Note that the module was used to administrate old WCS instances and does not work anymore.


## Version 3.15.6 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-15-6 "Link to this heading")

This patch version includes:

- Fix multi-line queries for BM25 and hybrid search.


## Version 3.15.5 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-15-5 "Link to this heading")

This patch version includes:

- EmbeddedDB now supports `latest` and versions (eg `1.18.3`) as `version` argument.

- Removed `cluster_hostname` from `EmbeddedOptions`. It can still be set by using `additional_env_vars`.

- Fix multi-line queries for generative search.


## Version 3.15.4 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-15-4 "Link to this heading")

This patch version includes:

- Fix imports of EmbeddedDB on Mac. It now properly raises an exception that MacOS is currently unsupported.


## Version 3.15.3 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-15-3 "Link to this heading")

This patch version includes:

- Improve embedded weaviate: Better folder structures, add support for env variables and support multiple versions.

- Fix edge case for timeout retries: When all objects have been added, no empty batch will be send.

- Fix authentication via additional\_headers


## Version 3.15.2 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-15-2 "Link to this heading")

This patch version includes:

- Fixes API keys with Weaviate setups that do not have OIDC enabled.


## Version 3.15.1 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-15-1 "Link to this heading")

This patch version includes:

- Fixes refreshing of OIDC tokens on unstable connections


## Version 3.15.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-15-0 "Link to this heading")

This minor version includes:

- GraphQL Multiple queries and aliases support:


> ```
> client.query.multi_get(
>         [\
>            client.query.get("Ship", ["name"]).with_alias("one"),\
>            client.query.get("Ship", ["size"]).with_alias("two"),\
>            client.query.get("Person", ["name"])\
>         ]
>
> ```

- Adds support for embedded weaviate version:


> ```
> from weaviate import Client
> from weaviate.embedded import EmbeddedOptions
>
> # Create the embedded client which automatically launches a Weaviate database in the background
> client = Client(embedded_options=EmbeddedOptions())
>
> ```


## Version 3.14.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-14-0 "Link to this heading")

This minor version includes:

- Support for API-Keys:


> ```
> client = weaviate.Client(url, auth_client_secret=AuthApiKey(api_key="my-secret-key"))
>
> ```


## Version 3.13.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-13-0 "Link to this heading")

This minor version includes:

- Extend CRUD operations for single data objects and reference with consistency level.

- Extend batch operations with consistency level.

- Add Cursor api.

- Add support for azure backup module.


## Version 3.12.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-12-0 "Link to this heading")

This minor version includes:

- Adds `with_generate()` in `GetBuilder` which allows to use the generative openai module. Needs Weaviate with version >=v1.17.3.

- Fix for empty OIDC scopes

- New startup\_period parameter in `Client`. The client will wait for the given timeout for
Weaviate to start. By default 5 seconds.

- Improved error messages for where filters and authentication.


## Version 3.11.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-11-0 "Link to this heading")

This minor version includes:

- New status code attribute for [`UnexpectedStatusCodeException`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.UnexpectedStatusCodeException "weaviate.exceptions.UnexpectedStatusCodeException") that can be accessed like this:


> ```
> try:
>     # your code
> except weaviate.UnexpectedStatusCodeException as err:
>     print(err.status_code)
>
> ```

- Fix for `get_meta()`.

- Caches server version at `Client` initialization. This improves batch reference creation performance.

- Changes accepted data types for arguments `from_object_uuid` and `to_object_uuid` of the method `add_reference()` to `str` and `uuid.UUID`.

- Adds automatic retry for failed objects. It can be configured using the `weaviate_error_retries` argument for the `configure()` or
`__call__()`, and should be an instance of `WeaviateErrorRetryConf`. It can be used like this:




> - All errors:
>
>
> > ```
> > from weaviate import WeaviateErrorRetryConf
> >
> > with client.batch(
> >     weaviate_error_retries=WeaviateErrorRetryConf(number_retries=3),
> > ) as batch:
> >     # Your code
> >
> > ```
>
> - Exclude errors, all the other errors will be retried:
>
>
> > ```
> > from weaviate import WeaviateErrorRetryConf
> >
> > with client.batch(
> >     weaviate_error_retries=WeaviateErrorRetryConf(number_retries=3, errors_to_exclude=["Ignore me", "other error to ignore"]),
> > ) as batch:
> >     # Your code
> >
> > ```
>
> - Include errors, all the other errors will be ignored:
>
>
> > ```
> > from weaviate import WeaviateErrorRetryConf
> >
> > with client.batch(
> >     weaviate_error_retries=WeaviateErrorRetryConf(number_retries=3, errors_to_include=["error to retry", "other error to test again"]),
> > ) as batch:
> >     # Your code
> >
> > ```

- Adds new arguments `sort` and `offset` for `get()`.


## Version 3.10.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-10-0 "Link to this heading")

This minor version includes:

- Improves error message for error `"413: Payload Too Large"`

- Adds new `Client` credential OIDC flow method:




> ```
> client_credentials_config = weaviate.AuthClientCredentials(
>     client_secret = "client_secret",
>     scope = "scope1 scope2" # optional, depends on the configuration of your identity provider
> )
> client = weaviate.Client("https://localhost:8080", auth_client_secret=client_credentials_config)
>
> ```

- Improves size of batches on dynamic batching.

- New `limit` argument to `get()` method of the `DataObject` client attribute.

- Bump minimum version of request to `2.28.0`

- Adds support for `node_name` and `consistency_level` for both `get()` and `get_by_id()`
of the `DataObject` client attribute.
This can be used ONLY with Weaviate Server `v1.17.0` or later.

- Adds support for replication factor in schema. This can be used ONLY with Weaviate Server `v1.17.0` or later. This can be configured in class schema like this:




> ```
> my_class = {
>     "class": "MyClass",
>     ...,
>     "replicationConfig": {
>         "factor": 1
>     }
> }
>
> ```

- Adds support for `Bm25` for `Get` queries, `with_bm25()`. This can be used ONLY with Weaviate Server `v1.17.0` or later.

- Adds support for `with_hybrid` for `Get` queries, `with_hybrid()`. This can be used ONLY with Weaviate Server `v1.17.0` or later.


## Version 3.9.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-9-0 "Link to this heading")

This minor version includes:

- Authentication using Bearer token, by adding `additional_headers` to the `Client` initialization:





```
client = weaviate.Client(
      url='http://localhost:8080',
      additional_headers={
          {"authorization": "Bearer <MY_TOKEN>"}
      }
)

```

- Multi-threading `Batch` import:

- Now it is possible to import data using multi-threading. The number of threads can be set using the new argument `num_workers` in
`configure()` and `__call__()`, defaults to 1 ( Use with care to not overload your weaviate instance.).

- New argument `connection_error_retries` to retry on `ConnectionError` that can be set in `configure()` and `__call__()`
or using the property getter/setter: `client.batch.connection_error_retries` to get the value and `client.batch.connection_error_retries = 5` to set the value.

- New method `start()` to create a `BatchExecutor` ( `ThreadExecutor`). This method does NOT need to be called if using the
`Batch` in a context manager ( `with`). Also it is idempotent.

- New method `shutdown()` to shutdown the existing `BatchExecutor` ( `ThreadExecutor`) to release any resources that it is holding once the
batch import is done. This method does NOT need to be called if using the `Batch` in a context manager ( `with`). Also it is idempotent.


- New `Client` attribute `Cluster` to check the status of the cluster nodes.

- The method `get_nodes_status()` returns the status of each node as a list of dictionaries.





```
client.cluster.get_nodes_status()

```


- Fix for `replace()` and `update()` when using with Weaviate server `>=v1.14.0`.

- New default `timeout_config`: `(10, 60)`.


## Version 3.8.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-8-0 "Link to this heading")

This minor version includes:

- Backup functionalities ( `Backup`):

- `create()` method to create backups (all/subset of classes).

- `get_create_status()` method to get the status of the created backup.

- `restore()` method to restore Weaviate from a backup (all/subset of classes).

- `get_restore_status()` method to get the status of the restored backup.


- New `Client` attribute: `backup` to `create`, `restore` and `get status` of the backups. All backup operations MUST be done through `Client.backup`.

- Added return value for `add_data_object()`, it now returns the UUID of the added object, if one was not set then an UUIDv4 will be generated.


## Version 3.7.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-7-0 "Link to this heading")

This minor version includes:

- Adds rolling average (last 5 batches) for batch creation time used by Dynamic Batching method.

- Adds ability to use `get()` without specifying any properties IF Additional Properties ( `with_additional()`) are set before executing the query.

- Adds base Weaviate Exception [`WeaviateBaseError`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.exceptions.html#weaviate.exceptions.WeaviateBaseError "weaviate.exceptions.WeaviateBaseError").

- Adds ability to set proxies. Can be set at `Client` initialization by using the new `proxies` or `trust_env` arguments.

- `Batch` creates UUIDs (UUIDv4) for all added objects that do not have one at client side (fixes data duplication on Batch retries).

- Adds new methods for `WCS` for instances that have authentication enabled:

- `get_users_of_cluster()` to get users (emails) for all the users that have access to the created Weaviate instance.

- `add_user_to_cluster()` to add users (email) to the created Weaviate instance.

- `remove_user_from_cluster()` to remove user (email) from the created Weaviate instance.


## Version 3.6.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-6-0 "Link to this heading")

This minor version includes:

- New function in `check_batch_result()` used to print errors from batch creation.

- New function argument `class_name` for `generate_local_beacon()`, used ONLY with Weaviate Server version >= `1.14.0`

(defaults to `None` for backwards compatibility).

- `check_batch_result()` is the default `callback` function for `Batch`
( `configure()` and `__call__()`) (instead of `None`).

- New method argument `to_object_class_name` for `add_reference()`, used ONLY with Weaviate Server version >= `1.14.0`
(defaults to `None` for backwards compatibility).

- Support for `distance` in GraphQL filters (only with Weaviate server >= `1.14.0`).

- For `DataObject`:

- New method argument `class_name` for `get_by_id()`, `get()`, `delete()` `exists()`, used ONLY with Weaviate Server version >= `1.14.0` (defaults to `None` for backwards compatibility).

- Deprecation Warning if Weaviate Server version >= 1.14.0 and `class_name` is `None` OR if Weaviate Server version < 1.14.0 and `class_name` is NOT `None`.


- For `Reference`:

- New method arguments `from_class_name` and `to_class_name` ( `to_class_names` for `update()`) for
`add()`, `delete()`,
`update()`, used ONLY with Weaviate Server version >= `1.14.0` (defaults to `None` for backwards compatibility).

- Deprecation Warning if Weaviate Server version >= 1.14.0 and `class_name` is `None` OR if Weaviate Server version < 1.14.0 and `class_name` is NOT `None`.


## Version 3.5.1 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-5-1 "Link to this heading")

This patch version fixes:

- the rerank not being set bug in `with_ask()`.

- the bug when using double quotes(”) in question field in `with_ask()`.

- the bug where nearText filter checks for objects in moveXXX clause but never sets it.


## Version 3.5.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-5-0 "Link to this heading")

This minor version contains functionality for the new features introduced in Weaviate `v1.13.0`.

- New `Batch` method `delete_objects()` to delete all objects that match a particular expression ( `where` filter).

- New `GetBuilder` method `with_sort()` that allows sorting data on a particular field/s.

- New [`AggregateBuilder`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder "weaviate.gql.aggregate.AggregateBuilder") method [`with_near_text()`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder.with_near_text "weaviate.gql.aggregate.AggregateBuilder.with_near_text") that allows to
aggregate data that is matching `nearText` filter.

- New [`AggregateBuilder`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder "weaviate.gql.aggregate.AggregateBuilder") method [`with_near_object()`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder.with_near_object "weaviate.gql.aggregate.AggregateBuilder.with_near_object") that allows to
aggregate data that is matching `nearObject` filter.

- New [`AggregateBuilder`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder "weaviate.gql.aggregate.AggregateBuilder") method [`with_near_vector()`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.aggregate.AggregateBuilder.with_near_vector "weaviate.gql.aggregate.AggregateBuilder.with_near_vector") that allows to
aggregate data that is matching `nearVector` filter.


## Version 3.4.2 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-4-2 "Link to this heading")

This patch version fixes another bug in `exists()`.

## Version 3.4.1 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-4-1 "Link to this heading")

This patch version fixes bug in `exists()`.

## Version 3.4.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-4-0 "Link to this heading")

This minor version fixes the bug in setting the Schema’s `invertedIndexConfig` field.

New method `get_class_shards()` to get all shards configuration of a particular class.

New method `update_class_shard()` to update one/all shard/s configuration of a particular class.

Support for new Property field: `tokenization`.

## Version 3.3.3 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-3-3 "Link to this heading")

This patch version fixes the nearImage filter requests.

## Version 3.3.2 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-3-2 "Link to this heading")

This patch version allows using UUIDs in hex format for `DataObject` too i.e. UUIDs without hyphens.

## Version 3.3.1 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-3-1 "Link to this heading")

This patch version allows using UUIDs in hex format too i.e. UUIDs without hyphens.

## Version 3.3.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-3-0 "Link to this heading")

This minor version adds a new `with_offset()` for the `Get` queries. This method should be used
with the `with_limit()`. This new feature (introduced in weaviate version `1.8.0`) allows to
use pagination functionality with the `Get` queries. The `offset` represents the start index of the objects to be returned,
and the number of objects is specified by the `with_limit()` method.

For example, to list the
first ten results, set `limit: 10`. Then, to “display the second page of 10”, set `offset: 10, limit: 10` and so on. E.g.
to show the 9th page of 10 results, set `offset: 80, limit: 10` to effectively display results 81-90.

## Version 3.2.5 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-2-5 "Link to this heading")

This patch fixes the `'Batch' object is not callable` error.

## Version 3.2.4 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-2-4 "Link to this heading")

All `class_name` and cross-refs `dataType` are implicitly capitalized. (This functionality is added because if `class_name` is not capitalized
then Weaviate server does it for you, and this was leading to errors where the client and server have different configurations.)

Fixes/updates in `Schema` class:

- This patch fixes the `contains()` to accept separate class schemas as argument
i.e. it does not expect to have only this format: `{"classes": [CLASS_1, CLASS_2, ...]}`; now it is possible to pass just `CLASS_X` as well.


## Version 3.2.3 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-2-3 "Link to this heading")

This patch fixes the `with_near_object()`. It uses now explicit string literals for `id`/ `beacon` in nearoOject clauses.

## Version 3.2.2 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-2-2 "Link to this heading")

This patch adds support for array data types: `boolean[]`, `date[]`.

## Version 3.2.1 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-2-1 "Link to this heading")

This patch adds support for array data types: `int[]`, `number[]`, `text[]`, `string[]`.

## Version 3.2.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-2-0 "Link to this heading")

Fixes/updates in `WCS` class:

- Fixed progress bar for `create()`, it is being updated in Notebooks too, instead of printing each iteration on new line.

- Method `create()` now prints the creation status above the bar.


Updates in [`gql`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#module-weaviate.gql "weaviate.gql") sub-package:

- New key-value `autocorrect: <bool>` introduced for the [`NearText`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.NearText "weaviate.gql.filter.NearText") and [`Ask`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.gql.html#weaviate.gql.filter.Ask "weaviate.gql.filter.Ask") filters.
The `autocorrect` is enabled only if Weaviate server has the `text-spellcheck` module enabled. If `autocorrect` is `True` the query is
corrected before the query is made. Usage example:


```
# with 'nearText' filter
client.query\
    .get('Article', ['title', 'author'])\
    .near_text(
        {
            'concepts': ['Ecconomy'],
            'autocorrect': True
        }
    )
    # the concept should be corrected to 'Economy'
# with 'ask' filter
client.query\
    .get('Article', ['title', 'author'])\
    .with_ask(
        {
            'question': 'When was the last financial crysis?',
            'autocorrect': True
        }
    )
    # the question should be corrected to 'When was the last financial crisis?'

```

- New method `with_additional()` is added to GET the \_additional properties. Usage example:


```
# single additional property with this GraphQL query
'''
{
    Get {
        Article {
            title
            author
            _additional {
                id
            }
        }
    }
}
'''
client.query\
    .get('Article', ['title', 'author'])\
    .with_additional('id') # argument as `str`

# multiple additional property with this GraphQL query
'''
{
    Get {
        Article {
            title
            author
            _additional {
                id
                certainty
            }
        }
    }
}
'''
client.query\
    .get('Article', ['title', 'author'])\
    .with_additional(['id', 'certainty']) # argument as `List[str]`

# additional properties as clause with this GraphQL query
'''
{
    Get {
        Article {
            title
            author
            _additional {
                classification {
                    basedOn
                    classifiedFields
                    completed
                    id
                    scope
                }
            }
        }
    }
}
'''
client.query\
    .get('Article', ['title', 'author'])\
    .with_additional(
        {
            'classification' : [\
                'basedOn',\
                'classifiedFields',\
                'completed',\
                'id',\
                'scope'\
            ]
        }
    ) # argument as `Dict[str, List[str]]`

# or with this GraphQL query
'''
{
    Get {
        Article {
            title
            author
            _additional {
                classification {
                    completed
                }
            }
        }
    }
}
'''
client.query\
    .get('Article', ['title', 'author'])\
    .with_additional(
        {
            'classification' : 'completed'
        }
    ) # argument as `Dict[str, str]`

# additional properties as clause and clause settings with this GraphQL query
'''
{
    Get {
        Article {
            title
            author
            _additional {
                token (
                    properties: ["content"]
                    limit: 10
                    certainty: 0.8
                ) {
                    certainty
                    endPosition
                    entity
                    property
                    startPosition
                    word
                }
            }
        }
    }
}
'''
clause = {
    'token': [\
        'certainty',\
        'endPosition',\
        'entity',\
        'property',\
        'startPosition',\
        'word',\
    ]
}
settings = {
    'properties': ["content"],  # is required
    'limit': 10,                # optional, int
    'certainty': 0.8            # optional, float
}
client.query\
    .get('Article', ['title', 'author'])\
    .with_additional(
        (clause, settings)
    ) # argument as `Tuple[Dict[str, List[str]], Dict[str, Any]]`

# if the desired clause does not match any example above, then the clause can always
# be converted to string before passing it to the `.with_additional` method

```

## Version 3.1.1 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-1-1 "Link to this heading")

- Fixes in `WCS` class:

- Make `WCS`’s methods’ argument `cluster_name` case insensitive (lowercased inside the method) to match Weaviate Cloud Service’
naming convention, this fixes the error when Weaviate Cloud Service lowercases the `cluster_name` but the users are not aware of this and get the exception
KeyError.


## Version 3.1.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-1-0 "Link to this heading")

- New `Batch` methods:

- `pop_object()` / `pop_reference()` to remove and return an added object/reference
from the `Batch` at position `index` (by default `-1`).

- `empty_objects()` / `empty_references()` to remove all the existing objects/references
from the `Batch` instance.

- `is_empty_objects()` / `is_empty_references()` to check there are any objects/references
in the `Batch` instance.


- Fixes in `WCS` class:

- Authentication only with [`AuthClientPassword`](https://weaviate-python-client.readthedocs.io/en/stable/weaviate.html#weaviate.auth.AuthClientPassword "weaviate.auth.AuthClientPassword").

- The `create()` argument `module` is renamed to `modules` and can also be a list of modules to enable for the WCS cluster.
The argument can be used on the [PROD](https://console.semi.technology/) WCS too.

- The `get_cluster_config()` does not raise an exception if the cluster does not exist but returns a empty configuration.

- The `delete_cluster()` does not raise an exception if the cluster does not exist.


- Add `phoneNumber` to the Weaviate’s primitive types. Thanks to GitHub user [@cdpierse](https://github.com/cdpierse).

- Bug fix in `Connection`.

- Fix `ConnectionError` handling.

- Optimization in `weaviate.batch.requests` and `weaviate.connect.connection`.


## Version 3.0.0 [](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html\#version-3-0-0 "Link to this heading")

- `weaviate.tools` module is REMOVED.

- `Batcher` class is REMOVED.

- `WCS` class is moved from the `weaviate.tools` to the new module `weaviate.wcs`

- `weaviate.tools.generate_uuid` is REMOVED.


- `weaviate.util.generate_uuid5()` is ADDED.

- New `Batch` class implementation to replace the old one. This implementation uses the `BatchRequest`
objects under the hood, which means that there is no need to create `BatchRequest`’s anymore. This new class implementation
allows 3 different batch creations methods: manual, auto-create and auto-create with dynamic batching.
See the `Batch` documentation for more information.

- `BatchRequest` classes ( `ObjectsBatchRequest` and `ReferenceBatchRequest`) are hidden from the user and should not be
used anymore. This is due to the new `Batch` class implementation.

- New `Schema` field is ADDED, “shardingConfig”. It can bu used with Weaviate version >= 1.6.0.

- New method `update_config()` used to update mutable schema configuration (like efConstruction, …).


Versions[latest](https://weaviate-python-client.readthedocs.io/en/latest/changelog.html)**[stable](https://weaviate-python-client.readthedocs.io/en/stable/changelog.html)**[v4.16.10](https://weaviate-python-client.readthedocs.io/en/v4.16.10/changelog.html)[v4.16.9](https://weaviate-python-client.readthedocs.io/en/v4.16.9/changelog.html)[v4.16.8](https://weaviate-python-client.readthedocs.io/en/v4.16.8/changelog.html)[v4.16.7](https://weaviate-python-client.readthedocs.io/en/v4.16.7/changelog.html)[v4.16.6](https://weaviate-python-client.readthedocs.io/en/v4.16.6/changelog.html)[v4.16.5](https://weaviate-python-client.readthedocs.io/en/v4.16.5/changelog.html)[v4.16.4](https://weaviate-python-client.readthedocs.io/en/v4.16.4/changelog.html)[v4.16.3](https://weaviate-python-client.readthedocs.io/en/v4.16.3/changelog.html)[v4.16.2](https://weaviate-python-client.readthedocs.io/en/v4.16.2/changelog.html)[v4.16.1](https://weaviate-python-client.readthedocs.io/en/v4.16.1/changelog.html)[v4.16.0](https://weaviate-python-client.readthedocs.io/en/v4.16.0/changelog.html)[v4.15.4](https://weaviate-python-client.readthedocs.io/en/v4.15.4/changelog.html)[v4.15.3](https://weaviate-python-client.readthedocs.io/en/v4.15.3/changelog.html)[v4.15.2](https://weaviate-python-client.readthedocs.io/en/v4.15.2/changelog.html)[v4.15.1](https://weaviate-python-client.readthedocs.io/en/v4.15.1/changelog.html)[v4.15.0](https://weaviate-python-client.readthedocs.io/en/v4.15.0/changelog.html)[v4.14.4](https://weaviate-python-client.readthedocs.io/en/v4.14.4/changelog.html)[v4.14.3](https://weaviate-python-client.readthedocs.io/en/v4.14.3/changelog.html)[v4.14.2](https://weaviate-python-client.readthedocs.io/en/v4.14.2/changelog.html)[v4.14.1](https://weaviate-python-client.readthedocs.io/en/v4.14.1/changelog.html)[v4.14.0](https://weaviate-python-client.readthedocs.io/en/v4.14.0/changelog.html)[v4.13.2](https://weaviate-python-client.readthedocs.io/en/v4.13.2/changelog.html)[v4.13.1](https://weaviate-python-client.readthedocs.io/en/v4.13.1/changelog.html)[v4.13.0](https://weaviate-python-client.readthedocs.io/en/v4.13.0/changelog.html)[v4.12.1](https://weaviate-python-client.readthedocs.io/en/v4.12.1/changelog.html)[v4.12.0](https://weaviate-python-client.readthedocs.io/en/v4.12.0/changelog.html)[v4.11.3](https://weaviate-python-client.readthedocs.io/en/v4.11.3/changelog.html)[v4.11.2](https://weaviate-python-client.readthedocs.io/en/v4.11.2/changelog.html)[v4.11.1](https://weaviate-python-client.readthedocs.io/en/v4.11.1/changelog.html)[v4.11.0](https://weaviate-python-client.readthedocs.io/en/v4.11.0/changelog.html)[v4.10.4](https://weaviate-python-client.readthedocs.io/en/v4.10.4/changelog.html)[v4.10.3](https://weaviate-python-client.readthedocs.io/en/v4.10.3/changelog.html)[v4.10.2](https://weaviate-python-client.readthedocs.io/en/v4.10.2/changelog.html)[v4.10.0](https://weaviate-python-client.readthedocs.io/en/v4.10.0/changelog.html)[v4.9.6](https://weaviate-python-client.readthedocs.io/en/v4.9.6/changelog.html)[v4.9.5](https://weaviate-python-client.readthedocs.io/en/v4.9.5/changelog.html)[v4.9.4](https://weaviate-python-client.readthedocs.io/en/v4.9.4/changelog.html)[v4.9.3](https://weaviate-python-client.readthedocs.io/en/v4.9.3/changelog.html)[v4.9.2](https://weaviate-python-client.readthedocs.io/en/v4.9.2/changelog.html)[v4.9.1](https://weaviate-python-client.readthedocs.io/en/v4.9.1/changelog.html)[v4.9.0](https://weaviate-python-client.readthedocs.io/en/v4.9.0/changelog.html)[v4.8.1](https://weaviate-python-client.readthedocs.io/en/v4.8.1/changelog.html)[v4.8.0](https://weaviate-python-client.readthedocs.io/en/v4.8.0/changelog.html)[v4.7.1](https://weaviate-python-client.readthedocs.io/en/v4.7.1/changelog.html)[v4.7.0](https://weaviate-python-client.readthedocs.io/en/v4.7.0/changelog.html)[v4.6.7](https://weaviate-python-client.readthedocs.io/en/v4.6.7/changelog.html)[v4.6.6](https://weaviate-python-client.readthedocs.io/en/v4.6.6/changelog.html)[v4.6.5](https://weaviate-python-client.readthedocs.io/en/v4.6.5/changelog.html)[v4.6.4](https://weaviate-python-client.readthedocs.io/en/v4.6.4/changelog.html)[v4.6.3](https://weaviate-python-client.readthedocs.io/en/v4.6.3/changelog.html)[v4.6.2](https://weaviate-python-client.readthedocs.io/en/v4.6.2/changelog.html)[v4.6.1](https://weaviate-python-client.readthedocs.io/en/v4.6.1/changelog.html)[v4.6.0](https://weaviate-python-client.readthedocs.io/en/v4.6.0/changelog.html)[v4.5.7](https://weaviate-python-client.readthedocs.io/en/v4.5.7/changelog.html)[v4.5.6](https://weaviate-python-client.readthedocs.io/en/v4.5.6/changelog.html)[v4.5.5](https://weaviate-python-client.readthedocs.io/en/v4.5.5/changelog.html)[v4.5.4](https://weaviate-python-client.readthedocs.io/en/v4.5.4/changelog.html)[v4.5.3](https://weaviate-python-client.readthedocs.io/en/v4.5.3/changelog.html)[v4.5.2](https://weaviate-python-client.readthedocs.io/en/v4.5.2/changelog.html)[v4.5.1](https://weaviate-python-client.readthedocs.io/en/v4.5.1/changelog.html)[v4.5.0](https://weaviate-python-client.readthedocs.io/en/v4.5.0/changelog.html)[v4.4.4](https://weaviate-python-client.readthedocs.io/en/v4.4.4/changelog.html)[v4.4.3](https://weaviate-python-client.readthedocs.io/en/v4.4.3/changelog.html)[v4.4.2](https://weaviate-python-client.readthedocs.io/en/v4.4.2/changelog.html)[v4.4.1](https://weaviate-python-client.readthedocs.io/en/v4.4.1/changelog.html)[v4.4.0](https://weaviate-python-client.readthedocs.io/en/v4.4.0/changelog.html)[v3.26.2](https://weaviate-python-client.readthedocs.io/en/v3.26.2/changelog.html)[v3.26.1](https://weaviate-python-client.readthedocs.io/en/v3.26.1/changelog.html)[v3.26.0](https://weaviate-python-client.readthedocs.io/en/v3.26.0/changelog.html)[v3.25.3](https://weaviate-python-client.readthedocs.io/en/v3.25.3/changelog.html)[v3.25.2](https://weaviate-python-client.readthedocs.io/en/v3.25.2/changelog.html)[v3.23.0](https://weaviate-python-client.readthedocs.io/en/v3.23.0/changelog.html)[v3.22.1](https://weaviate-python-client.readthedocs.io/en/v3.22.1/changelog.html)[v3.22.0](https://weaviate-python-client.readthedocs.io/en/v3.22.0/changelog.html)[v3.21.0](https://weaviate-python-client.readthedocs.io/en/v3.21.0/changelog.html)[v3.20.1](https://weaviate-python-client.readthedocs.io/en/v3.20.1/changelog.html)[v3.20.0](https://weaviate-python-client.readthedocs.io/en/v3.20.0/changelog.html)[v3.19.2](https://weaviate-python-client.readthedocs.io/en/v3.19.2/changelog.html)[v3.19.1](https://weaviate-python-client.readthedocs.io/en/v3.19.1/changelog.html)[v3.19.0](https://weaviate-python-client.readthedocs.io/en/v3.19.0/changelog.html)[v3.18.0](https://weaviate-python-client.readthedocs.io/en/v3.18.0/changelog.html)[v3.15.6](https://weaviate-python-client.readthedocs.io/en/v3.15.6/changelog.html)[v3.15.5](https://weaviate-python-client.readthedocs.io/en/v3.15.5/changelog.html)[v3.15.4](https://weaviate-python-client.readthedocs.io/en/v3.15.4/changelog.html)[v3.15.3](https://weaviate-python-client.readthedocs.io/en/v3.15.3/changelog.html)[v3.15.2](https://weaviate-python-client.readthedocs.io/en/v3.15.2/changelog.html)[v3.15.1](https://weaviate-python-client.readthedocs.io/en/v3.15.1/changelog.html)[v3.15.0](https://weaviate-python-client.readthedocs.io/en/v3.15.0/changelog.html)[v3.14.0](https://weaviate-python-client.readthedocs.io/en/v3.14.0/changelog.html)[v3.13.0](https://weaviate-python-client.readthedocs.io/en/v3.13.0/changelog.html)[v3.12.0\_a](https://weaviate-python-client.readthedocs.io/en/v3.12.0_a/changelog.html)[v3.11.0](https://weaviate-python-client.readthedocs.io/en/v3.11.0/changelog.html)[v3.10.0](https://weaviate-python-client.readthedocs.io/en/v3.10.0/changelog.html)[v3.9.0](https://weaviate-python-client.readthedocs.io/en/v3.9.0/changelog.html)[v3.8.0](https://weaviate-python-client.readthedocs.io/en/v3.8.0/changelog.html)[v3.7.0](https://weaviate-python-client.readthedocs.io/en/v3.7.0/changelog.html)[v3.6.0](https://weaviate-python-client.readthedocs.io/en/v3.6.0/changelog.html)[v3.5.1](https://weaviate-python-client.readthedocs.io/en/v3.5.1/changelog.html)[v3.5.0](https://weaviate-python-client.readthedocs.io/en/v3.5.0/changelog.html)[v3.4.1](https://weaviate-python-client.readthedocs.io/en/v3.4.1/changelog.html)[v3.4.0](https://weaviate-python-client.readthedocs.io/en/v3.4.0/changelog.html)[v3.3.3](https://weaviate-python-client.readthedocs.io/en/v3.3.3/changelog.html)[v3.3.2](https://weaviate-python-client.readthedocs.io/en/v3.3.2/changelog.html)[v3.3.1](https://weaviate-python-client.readthedocs.io/en/v3.3.1/changelog.html)[v3.3.0](https://weaviate-python-client.readthedocs.io/en/v3.3.0/changelog.html)[v3.2.5](https://weaviate-python-client.readthedocs.io/en/v3.2.5/changelog.html)[v3.2.4](https://weaviate-python-client.readthedocs.io/en/v3.2.4/changelog.html)[v3.2.3](https://weaviate-python-client.readthedocs.io/en/v3.2.3/changelog.html)[v3.2.2](https://weaviate-python-client.readthedocs.io/en/v3.2.2/changelog.html)[v3.2.1](https://weaviate-python-client.readthedocs.io/en/v3.2.1/changelog.html)[v3.2.0](https://weaviate-python-client.readthedocs.io/en/v3.2.0/changelog.html)[v3.1.1](https://weaviate-python-client.readthedocs.io/en/v3.1.1/changelog.html)[v3.1.0](https://weaviate-python-client.readthedocs.io/en/v3.1.0/changelog.html)[v3.0.0](https://weaviate-python-client.readthedocs.io/en/v3.0.0/changelog.html)On Read the Docs[Project Home](https://app.readthedocs.org/projects/weaviate-python-client/?utm_source=weaviate-python-client&utm_content=flyout)[Builds](https://app.readthedocs.org/projects/weaviate-python-client/builds/?utm_source=weaviate-python-client&utm_content=flyout)Search

* * *

[Addons documentation](https://docs.readthedocs.io/page/addons.html?utm_source=weaviate-python-client&utm_content=flyout) ― Hosted by
[Read the Docs](https://about.readthedocs.com/?utm_source=weaviate-python-client&utm_content=flyout)