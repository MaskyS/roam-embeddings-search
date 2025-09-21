Weaviate's integration with Voyage AI's APIs allows you to access their models' capabilities directly from Weaviate.

[Configure a Weaviate collection](https://docs.weaviate.io/weaviate/model-providers/voyageai/reranker#configure-the-reranker) to use a Voyage AI reranker model, and Weaviate will use the specified model and your Voyage AI API key to rerank search results.

This two-step process involves Weaviate first performing a search and then reranking the results using the specified model.

![Reranker integration illustration](https://docs.weaviate.io/assets/images/integration_voyageai_reranker-bdf0388838a7d14b47d4e0012114f601.png)

## Requirements [​](https://docs.weaviate.io/weaviate/model-providers/voyageai/reranker\#requirements "Direct link to Requirements")

### Weaviate configuration [​](https://docs.weaviate.io/weaviate/model-providers/voyageai/reranker\#weaviate-configuration "Direct link to Weaviate configuration")

Your Weaviate instance must be configured with the Voyage AI reranker integration ( `reranker-voyageai`) module.

For Weaviate Cloud (WCD) users

This integration is enabled by default on Weaviate Cloud (WCD) serverless instances.

For self-hosted users

- Check the [cluster metadata](https://docs.weaviate.io/deploy/configuration/meta) to verify if the module is enabled.
- Follow the [how-to configure modules](https://docs.weaviate.io/weaviate/configuration/modules) guide to enable the module in Weaviate.

### API credentials [​](https://docs.weaviate.io/weaviate/model-providers/voyageai/reranker\#api-credentials "Direct link to API credentials")

You must provide a valid Voyage AI API key to Weaviate for this integration. Go to [Voyage AI](https://www.voyageai.com/) to sign up and obtain an API key.

Provide the API key to Weaviate using one of the following methods:

- Set the `VOYAGEAI_APIKEY` environment variable that is available to Weaviate.
- Provide the API key at runtime, as shown in the examples below.

- Python API v4
- JS/TS API v3

```codeBlockLines_e6Vv
import weaviate
from weaviate.classes.init import Auth
import os

# Recommended: save sensitive data as environment variables
voyageai_key = os.getenv("VOYAGEAI_APIKEY")
headers = {
    "X-VoyageAI-Api-Key": voyageai_key,
}

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=weaviate_url,                       # `weaviate_url`: your Weaviate URL
    auth_credentials=Auth.api_key(weaviate_key),      # `weaviate_key`: your Weaviate API key
    headers=headers
)

# Work with Weaviate

client.close()

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

## Configure the reranker [​](https://docs.weaviate.io/weaviate/model-providers/voyageai/reranker\#configure-the-reranker "Direct link to Configure the reranker")

Reranker model integration mutable from `v1.25.23`, `v1.26.8` and `v1.27.1`

A collection's `reranker` model integration configuration is mutable from `v1.25.23`, `v1.26.8` and `v1.27.1`. See [this section](https://docs.weaviate.io/weaviate/manage-collections/generative-reranker-models#update-the-reranker-model-integration) for details on how to update the collection configuration.

Configure a Weaviate collection to use a Voyage AI reranker model as follows:

- Python API v4
- JS/TS API v3

```codeBlockLines_e6Vv
client.collections.create(
    "DemoCollection",
    reranker_config=Configure.Reranker.voyageai(
        # # This parameter is optional
        # model="rerank-lite-1"
    )
    # Additional parameters not shown
)

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

You can specify one of the [available models](https://docs.weaviate.io/weaviate/model-providers/voyageai/reranker#available-models) for the reranker to use.

The [default model](https://docs.weaviate.io/weaviate/model-providers/voyageai/reranker#available-models) is used if no model is specified.

## Header parameters [​](https://docs.weaviate.io/weaviate/model-providers/voyageai/reranker\#header-parameters "Direct link to Header parameters")

You can provide the API key as well as some optional parameters at runtime through additional headers in the request. The following headers are available:

- `X-VoyageAI-Api-Key`: The Voyage AI API key.
- `X-VoyageAI-Baseurl`: The base URL to use (e.g. a proxy) instead of the default Voyage AI URL.

Any additional headers provided at runtime will override the existing Weaviate configuration.

Provide the headers as shown in the [API credentials examples](https://docs.weaviate.io/weaviate/model-providers/voyageai/reranker#api-credentials) above.

## Reranking query [​](https://docs.weaviate.io/weaviate/model-providers/voyageai/reranker\#reranking-query "Direct link to Reranking query")

Once the reranker is configured, Weaviate performs [reranking operations](https://docs.weaviate.io/weaviate/search/rerank) using the specified Voyage AI model.

More specifically, Weaviate performs an initial search, then reranks the results using the specified model.

Any search in Weaviate can be combined with a reranker to perform reranking operations.

![Reranker integration illustration](https://docs.weaviate.io/assets/images/integration_voyageai_reranker-bdf0388838a7d14b47d4e0012114f601.png)

- Python API v4
- JS/TS API v3

```codeBlockLines_e6Vv
from weaviate.classes.query import Rerank

collection = client.collections.use("DemoCollection")

response = collection.query.near_text(
    query="A holiday film",  # The model provider integration will automatically vectorize the query
    limit=2,
    rerank=Rerank(
        prop="title",                   # The property to rerank on
        query="A melodic holiday film"  # If not provided, the original query will be used
    )
)

for obj in response.objects:
    print(obj.properties["title"])

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

## References [​](https://docs.weaviate.io/weaviate/model-providers/voyageai/reranker\#references "Direct link to References")

### Available models [​](https://docs.weaviate.io/weaviate/model-providers/voyageai/reranker\#available-models "Direct link to Available models")

- rerank-2
- rerank-2-lite
- rerank-1
- rerank-lite-1 (default)

Model support history

- `v1.24.25`, `v1.25.18`, `v1.26.5`:
  - Added `rerank-2`, `rerank-2-lite`
- `v1.24.18`, `v1.25.3`:
  - Added `rerank-1`
- `1.24.7`:
  - Introduced `reranker-voyageai`, with `rerank-lite-1` support

## Further resources [​](https://docs.weaviate.io/weaviate/model-providers/voyageai/reranker\#further-resources "Direct link to Further resources")

### Other integrations [​](https://docs.weaviate.io/weaviate/model-providers/voyageai/reranker\#other-integrations "Direct link to Other integrations")

- [Voyage AI embedding models + Weaviate](https://docs.weaviate.io/weaviate/model-providers/voyageai/embeddings).
- [Voyage AI multimodal embedding embeddings models + Weaviate](https://docs.weaviate.io/weaviate/model-providers/voyageai/embeddings-multimodal)

### Code examples [​](https://docs.weaviate.io/weaviate/model-providers/voyageai/reranker\#code-examples "Direct link to Code examples")

Once the integrations are configured at the collection, the data management and search operations in Weaviate work identically to any other collection. See the following model-agnostic examples:

- The [How-to: Manage collections](https://docs.weaviate.io/weaviate/manage-collections) and [How-to: Manage objects](https://docs.weaviate.io/weaviate/manage-objects) guides show how to perform data operations (i.e. create, read, update, delete collections and objects within them).
- The [How-to: Query & Search](https://docs.weaviate.io/weaviate/search) guides show how to perform search operations (i.e. vector, keyword, hybrid) as well as retrieval augmented generation.

### References [​](https://docs.weaviate.io/weaviate/model-providers/voyageai/reranker\#references-1 "Direct link to References")

- Voyage AI [Reranker API documentation](https://docs.voyageai.com/docs/reranker)
