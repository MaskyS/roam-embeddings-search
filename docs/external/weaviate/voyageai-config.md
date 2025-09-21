Weaviate's integration with Voyage AI's APIs allows you to access their models' capabilities directly from Weaviate.

[Configure a Weaviate vector index](https://docs.weaviate.io/weaviate/model-providers/voyageai/embeddings#configure-the-vectorizer) to use an Voyage AI embedding model, and Weaviate will generate embeddings for various operations using the specified model and your Voyage AI API key. This feature is called the _vectorizer_.

At [import time](https://docs.weaviate.io/weaviate/model-providers/voyageai/embeddings#data-import), Weaviate generates text object embeddings and saves them into the index. For [vector](https://docs.weaviate.io/weaviate/model-providers/voyageai/embeddings#vector-near-text-search) and [hybrid](https://docs.weaviate.io/weaviate/model-providers/voyageai/embeddings#hybrid-search) search operations, Weaviate converts text queries into embeddings.

![Embedding integration illustration](https://docs.weaviate.io/assets/images/integration_voyageai_embedding-fd6763f557ed7fab652bca45682fa741.png)

## Requirements [​](https://docs.weaviate.io/weaviate/model-providers/voyageai/embeddings\#requirements "Direct link to Requirements")

### Weaviate configuration [​](https://docs.weaviate.io/weaviate/model-providers/voyageai/embeddings\#weaviate-configuration "Direct link to Weaviate configuration")

Your Weaviate instance must be configured with the Voyage AI vectorizer integration ( `text2vec-voyageai`) module.

For Weaviate Cloud (WCD) users

This integration is enabled by default on Weaviate Cloud (WCD) serverless instances.

For self-hosted users

- Check the [cluster metadata](https://docs.weaviate.io/deploy/configuration/meta) to verify if the module is enabled.
- Follow the [how-to configure modules](https://docs.weaviate.io/weaviate/configuration/modules) guide to enable the module in Weaviate.

### API credentials [​](https://docs.weaviate.io/weaviate/model-providers/voyageai/embeddings\#api-credentials "Direct link to API credentials")

You must provide a valid Voyage AI API key to Weaviate for this integration. Go to [Voyage AI](https://www.voyageai.com/) to sign up and obtain an API key.

Provide the API key to Weaviate using one of the following methods:

- Set the `VOYAGEAI_APIKEY` environment variable that is available to Weaviate.
- Provide the API key at runtime, as shown in the examples below.

- Python API v4
- JS/TS API v3
- Go

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

## Configure the vectorizer [​](https://docs.weaviate.io/weaviate/model-providers/voyageai/embeddings\#configure-the-vectorizer "Direct link to Configure the vectorizer")

[Configure a Weaviate index](https://docs.weaviate.io/weaviate/manage-collections/vector-config#specify-a-vectorizer) as follows to use a Voyage AI embedding model:

- Python API v4
- JS/TS API v3
- Go

```codeBlockLines_e6Vv
from weaviate.classes.config import Configure

client.collections.create(
    "DemoCollection",
    vector_config=[\
        Configure.Vectors.text2vec_voyageai(\
            name="title_vector",\
            source_properties=["title"]\
        )\
    ],
    # Additional parameters not shown
)

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

### Select a model [​](https://docs.weaviate.io/weaviate/model-providers/voyageai/embeddings\#select-a-model "Direct link to Select a model")

You can specify one of the [available models](https://docs.weaviate.io/weaviate/model-providers/voyageai/embeddings#available-models) for the vectorizer to use, as shown in the following configuration example.

- Python API v4
- JS/TS API v3
- Go

```codeBlockLines_e6Vv
from weaviate.classes.config import Configure

client.collections.create(
    "DemoCollection",
    vector_config=[\
        Configure.Vectors.text2vec_voyageai(\
            name="title_vector",\
            source_properties=["title"],\
            model="voyage-3-lite"\
        )\
    ],
    # Additional parameters not shown
)

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

You can [specify](https://docs.weaviate.io/weaviate/model-providers/voyageai/embeddings#vectorizer-parameters) one of the [available models](https://docs.weaviate.io/weaviate/model-providers/voyageai/embeddings#available-models) for Weaviate to use. The [default model](https://docs.weaviate.io/weaviate/model-providers/voyageai/embeddings#available-models) is used if no model is specified.

Vectorization behavior

Weaviate follows the collection configuration and a set of predetermined rules to vectorize objects.

Unless specified otherwise in the collection definition, the default behavior is to:

- Only vectorize properties that use the `text` or `text[]` data type (unless [skipped](https://docs.weaviate.io/weaviate/manage-collections/vector-config#property-level-settings))
- Sort properties in alphabetical (a-z) order before concatenating values
- If `vectorizePropertyName` is `true` ( `false` by default) prepend the property name to each property value
- Join the (prepended) property values with spaces
- Prepend the class name (unless `vectorizeClassName` is `false`)
- Convert the produced string to lowercase

### Vectorizer parameters [​](https://docs.weaviate.io/weaviate/model-providers/voyageai/embeddings\#vectorizer-parameters "Direct link to Vectorizer parameters")

The following examples show how to configure Voyage AI-specific options.

- Python API v4
- JS/TS API v3
- Go

```codeBlockLines_e6Vv
from weaviate.classes.config import Configure

client.collections.create(
    "DemoCollection",
    vector_config=[\
        Configure.Vectors.text2vec_voyageai(\
            name="title_vector",\
            source_properties=["title"],\
            # Further options\
            # model="voyage-large-2"\
            # base_url="<custom_voyageai_url>",\
            # truncate=True,\
        )\
    ],
    # Additional parameters not shown
)

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

For further details on model parameters, see the [Voyage AI Embedding API documentation](https://docs.voyageai.com/docs/embeddings).

## Header parameters [​](https://docs.weaviate.io/weaviate/model-providers/voyageai/embeddings\#header-parameters "Direct link to Header parameters")

You can provide the API key as well as some optional parameters at runtime through additional headers in the request. The following headers are available:

- `X-VoyageAI-Api-Key`: The Voyage AI API key.
- `X-VoyageAI-Baseurl`: The base URL to use (e.g. a proxy) instead of the default Voyage AI URL.

Any additional headers provided at runtime will override the existing Weaviate configuration.

Provide the headers as shown in the [API credentials examples](https://docs.weaviate.io/weaviate/model-providers/voyageai/embeddings#api-credentials) above.

## Data import [​](https://docs.weaviate.io/weaviate/model-providers/voyageai/embeddings\#data-import "Direct link to Data import")

After configuring the vectorizer, [import data](https://docs.weaviate.io/weaviate/manage-objects/import) into Weaviate. Weaviate generates embeddings for text objects using the specified model.

- Python API v4
- JS/TS API v3
- Go

```codeBlockLines_e6Vv
source_objects = [\
    {"title": "The Shawshank Redemption", "description": "A wrongfully imprisoned man forms an inspiring friendship while finding hope and redemption in the darkest of places."},\
    {"title": "The Godfather", "description": "A powerful mafia family struggles to balance loyalty, power, and betrayal in this iconic crime saga."},\
    {"title": "The Dark Knight", "description": "Batman faces his greatest challenge as he battles the chaos unleashed by the Joker in Gotham City."},\
    {"title": "Jingle All the Way", "description": "A desperate father goes to hilarious lengths to secure the season's hottest toy for his son on Christmas Eve."},\
    {"title": "A Christmas Carol", "description": "A miserly old man is transformed after being visited by three ghosts on Christmas Eve in this timeless tale of redemption."}\
]

collection = client.collections.use("DemoCollection")

with collection.batch.fixed_size(batch_size=200) as batch:
    for src_obj in source_objects:
        # The model provider integration will automatically vectorize the object
        batch.add_object(
            properties={
                "title": src_obj["title"],
                "description": src_obj["description"],
            },
            # vector=vector  # Optionally provide a pre-obtained vector
        )
        if batch.number_errors > 10:
            print("Batch import stopped due to excessive errors.")
            break

failed_objects = collection.batch.failed_objects
if failed_objects:
    print(f"Number of failed imports: {len(failed_objects)}")
    print(f"First failed object: {failed_objects[0]}")

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

Re-use existing vectors

If you already have a compatible model vector available, you can provide it directly to Weaviate. This can be useful if you have already generated embeddings using the same model and want to use them in Weaviate, such as when migrating data from another system.

## Searches [​](https://docs.weaviate.io/weaviate/model-providers/voyageai/embeddings\#searches "Direct link to Searches")

Once the vectorizer is configured, Weaviate will perform vector and hybrid search operations using the specified Voyage AI model.

![Embedding integration at search illustration](https://docs.weaviate.io/assets/images/integration_voyageai_embedding_search-5de9fd1fd2b419985c4d4d3bb2b3f83f.png)

### Vector (near text) search [​](https://docs.weaviate.io/weaviate/model-providers/voyageai/embeddings\#vector-near-text-search "Direct link to Vector (near text) search")

When you perform a [vector search](https://docs.weaviate.io/weaviate/search/similarity#search-with-text), Weaviate converts the text query into an embedding using the specified model and returns the most similar objects from the database.

The query below returns the `n` most similar objects from the database, set by `limit`.

- Python API v4
- JS/TS API v3
- Go

```codeBlockLines_e6Vv
collection = client.collections.use("DemoCollection")

response = collection.query.near_text(
    query="A holiday film",  # The model provider integration will automatically vectorize the query
    limit=2
)

for obj in response.objects:
    print(obj.properties["title"])

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

### Hybrid search [​](https://docs.weaviate.io/weaviate/model-providers/voyageai/embeddings\#hybrid-search "Direct link to Hybrid search")

What is a hybrid search?

A hybrid search performs a vector search and a keyword (BM25) search, before [combining the results](https://docs.weaviate.io/weaviate/search/hybrid) to return the best matching objects from the database.

When you perform a [hybrid search](https://docs.weaviate.io/weaviate/search/hybrid), Weaviate converts the text query into an embedding using the specified model and returns the best scoring objects from the database.

The query below returns the `n` best scoring objects from the database, set by `limit`.

- Python API v4
- JS/TS API v3
- Go

```codeBlockLines_e6Vv
collection = client.collections.use("DemoCollection")

response = collection.query.hybrid(
    query="A holiday film",  # The model provider integration will automatically vectorize the query
    limit=2
)

for obj in response.objects:
    print(obj.properties["title"])

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

## References [​](https://docs.weaviate.io/weaviate/model-providers/voyageai/embeddings\#references "Direct link to References")

### Available models [​](https://docs.weaviate.io/weaviate/model-providers/voyageai/embeddings\#available-models "Direct link to Available models")

- voyage-3.5
- voyage-3.5-lite
- voyage-3-large
- voyage-3 (default)
- voyage-3-lite
- voyage-large-2 (default for <= `v1.24.24`, `v1.25.17`, `v1.26.4`)
- voyage-code-2
- voyage-2
- voyage-law-2
- voyage-large-2-instruct
- voyage-finance-2
- voyage-multilingual-2

Model support history

- `v1.24.25`, `v1.25.18`, `v1.26.5`:
  - Added `voyage-3`, `voyage-3-lite`
  - Default model changed to `voyage-3` from `voyage-large-2`
- `v1.24.14`, `v1.25.1`:
  - Added `voyage-large-2-instruct`
  - Removed `voyage-lite-02-instruct`
- `v1.24.9`:
  - Added `voyage-law-2`, `voyage-lite-02-instruct`
- `v1.24.2`:
  - Introduced `text2vec-voyage`, with `voyage-large-2`, `voyage-code-2`, `voyage-2` support

## Further resources [​](https://docs.weaviate.io/weaviate/model-providers/voyageai/embeddings\#further-resources "Direct link to Further resources")

### Other integrations [​](https://docs.weaviate.io/weaviate/model-providers/voyageai/embeddings\#other-integrations "Direct link to Other integrations")

- [Voyage AI multimodal embedding embeddings models + Weaviate](https://docs.weaviate.io/weaviate/model-providers/voyageai/embeddings-multimodal)
- [Voyage AI reranker models + Weaviate](https://docs.weaviate.io/weaviate/model-providers/voyageai/embeddings).

### Code examples [​](https://docs.weaviate.io/weaviate/model-providers/voyageai/embeddings\#code-examples "Direct link to Code examples")

Once the integrations are configured at the collection, the data management and search operations in Weaviate work identically to any other collection. See the following model-agnostic examples:

- The [How-to: Manage collections](https://docs.weaviate.io/weaviate/manage-collections) and [How-to: Manage objects](https://docs.weaviate.io/weaviate/manage-objects) guides show how to perform data operations (i.e. create, read, update, delete collections and objects within them).
- The [How-to: Query & Search](https://docs.weaviate.io/weaviate/search) guides show how to perform search operations (i.e. vector, keyword, hybrid) as well as retrieval augmented generation.

### External resources [​](https://docs.weaviate.io/weaviate/model-providers/voyageai/embeddings\#external-resources "Direct link to External resources")

- Voyage AI [Embeddings API documentation](https://docs.voyageai.com/docs/embeddings)
