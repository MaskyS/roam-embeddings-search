
Python and JS/TS client - Vectorizer Configuration API Changes

Starting with Weaviate Python client `v4.16.0`, the [vectorizer configuration API has been updated](https://docs.weaviate.io/weaviate/client-libraries/python#vectorizer-api-changes-v4160).

Starting with Weaviate JS/TS client `v3.8.0`, the [vectorizer configuration API has been updated](https://docs.weaviate.io/weaviate/client-libraries/typescript#vectorizer-api-changes-v380).

Action required: **Update to the latest client version** and migrate your code to use the [new vectorizer configuration API](https://docs.weaviate.io/weaviate/manage-collections/vector-config#specify-a-vectorizer).

## Specify a vectorizer [​](https://docs.weaviate.io/weaviate/manage-collections/vector-config\#specify-a-vectorizer "Direct link to Specify a vectorizer")

Specify a `vectorizer` for a collection.

Additional information

Collection level settings override default values and general configuration parameters such as [environment variables](https://docs.weaviate.io/deploy/configuration/env-vars).

- [Available model integrations](https://docs.weaviate.io/weaviate/model-providers)
- [Vectorizer configuration references](https://docs.weaviate.io/weaviate/config-refs/collections#vector-configuration)

- Python Client v4
- Python Client v3
- JS/TS Client v3
- JS/TS Client v2
- Java
- Go

```codeBlockLines_e6Vv
from weaviate.classes.config import Configure, Property, DataType

client.collections.create(
    "Article",
    vector_config=Configure.Vectors.text2vec_openai(),
    properties=[  # properties configuration is optional\
        Property(name="title", data_type=DataType.TEXT),\
        Property(name="body", data_type=DataType.TEXT),\
    ],
)

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

## Specify vectorizer settings [​](https://docs.weaviate.io/weaviate/manage-collections/vector-config\#specify-vectorizer-settings "Direct link to Specify vectorizer settings")

.Vectors.text2vec\_xxx with AutoSchema

Defining a collection with `Configure.Vectors.text2vec_xxx()` with Python client library `4.16.0`- `4.16.3` will throw an error if no properties are defined and `vectorize_collection_name` is not set to `True`.

This is addressed in `4.16.4` of the Weaviate Python client. See this FAQ entry for more details: [Invalid properties error in Python client versions 4.16.0 to 4.16.3](https://docs.weaviate.io/weaviate/more-resources/faq#q-invalid-properties-error-when-creating-a-collection-python-client-versions-4160-to-4163).

To configure how a vectorizer works (i.e. what model to use) with a specific collection, set the vectorizer parameters.

- Python Client v4
- Python Client v3
- JS/TS Client v3
- JS/TS Client v2
- Java
- Go

```codeBlockLines_e6Vv
from weaviate.classes.config import Configure

client.collections.create(
    "Article",
    vector_config=Configure.Vectors.text2vec_cohere(
        model="embed-multilingual-v2.0", vectorize_collection_name=True
    ),
)

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

## Define named vectors [​](https://docs.weaviate.io/weaviate/manage-collections/vector-config\#define-named-vectors "Direct link to Define named vectors")

Added in `v1.24`

You can define multiple [named vectors](https://docs.weaviate.io/weaviate/concepts/data#multiple-vector-embeddings-named-vectors) per collection. This allows each object to be represented by multiple vector embeddings, each with its own vector index.

As such, each named vector configuration can include its own vectorizer and vector index settings.

- Python Client v4
- Python Client v3
- JS/TS Client v3
- JS/TS Client v2
- Java
- Go

```codeBlockLines_e6Vv
from weaviate.classes.config import Configure, Property, DataType

client.collections.create(
    "ArticleNV",
    vector_config=[\
        # Set a named vector with the "text2vec-cohere" vectorizer\
        Configure.Vectors.text2vec_cohere(\
            name="title",\
            source_properties=["title"],  # (Optional) Set the source property(ies)\
            vector_index_config=Configure.VectorIndex.hnsw(),  # (Optional) Set vector index options\
        ),\
        # Set another named vector with the "text2vec-openai" vectorizer\
        Configure.Vectors.text2vec_openai(\
            name="title_country",\
            source_properties=[\
                "title",\
                "country",\
            ],  # (Optional) Set the source property(ies)\
            vector_index_config=Configure.VectorIndex.hnsw(),  # (Optional) Set vector index options\
        ),\
        # Set a named vector for your own uploaded vectors\
        Configure.Vectors.self_provided(\
            name="custom_vector",\
            vector_index_config=Configure.VectorIndex.hnsw(),  # (Optional) Set vector index options\
        ),\
    ],
    properties=[  # Define properties\
        Property(name="title", data_type=DataType.TEXT),\
        Property(name="country", data_type=DataType.TEXT),\
    ],
)

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

## Add new named vectors [​](https://docs.weaviate.io/weaviate/manage-collections/vector-config\#add-new-named-vectors "Direct link to Add new named vectors")

Added in `v1.31`

Named vectors can be added to existing collection definitions with named vectors. (This is not possible for collections without named vectors.)

- Python Client v4
- JS/TS Client v3
- Java
- Go

```codeBlockLines_e6Vv
from weaviate.classes.config import Configure

articles = client.collections.use("Article")

articles.config.add_vector(
    vector_config=Configure.Vectors.text2vec_cohere(
        name="body_vector",
        source_properties=["body"],
    )
)

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

Objects aren't automatically revectorized

Adding a new named vector to the collection definition [won't trigger vectorization for existing objects](https://docs.weaviate.io/weaviate/concepts/data#adding-a-named-vector-after-collection-creation). Only new or updated objects will receive embeddings for the newly added named vector definition.

## Define multi-vector embeddings (e.g. ColBERT, ColPali) [​](https://docs.weaviate.io/weaviate/manage-collections/vector-config\#define-multi-vector-embeddings-eg-colbert-colpali "Direct link to Define multi-vector embeddings (e.g. ColBERT, ColPali)")

Added in `v1.29`, `v1.30`

Multi-vector embeddings, also known as multi-vectors, represent a single object with multiple vectors, i.e. a 2-dimensional matrix. Multi-vectors are currently only available for HNSW indexes for named vectors. To use multi-vectors, enable it for the appropriate named vector.

- Python Client v4
- JS/TS Client v3
- Java

```codeBlockLines_e6Vv
from weaviate.classes.config import Configure, Property, DataType

client.collections.create(
    "DemoCollection",
    vector_config=[\
        # Example 1 - Use a model integration\
        # The factory function will automatically enable multi-vector support for the HNSW index\
        Configure.MultiVectors.text2vec_jinaai(\
            name="jina_colbert",\
            source_properties=["text"],\
        ),\
        # Example 2 - User-provided multi-vector representations\
        # Must explicitly enable multi-vector support for the HNSW index\
        Configure.MultiVectors.self_provided(\
            name="custom_multi_vector",\
        ),\
    ],
    properties=[Property(name="text", data_type=DataType.TEXT)],
    # Additional parameters not shown
)

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

Use quantization and encoding to compress your vectors

Multi-vector embeddings use up more memory than single vector embeddings. You can use [vector quantization](https://docs.weaviate.io/weaviate/configuration/compression) and [encoding](https://docs.weaviate.io/weaviate/configuration/compression/multi-vectors#muvera-encoding) to compress them and reduce memory usage.

## Set vector index type [​](https://docs.weaviate.io/weaviate/manage-collections/vector-config\#set-vector-index-type "Direct link to Set vector index type")

The vector index type can be set for each collection at creation time, between `hnsw`, `flat` and `dynamic` index types.

- Python Client v4
- Python Client v3
- JS/TS Client v3
- JS/TS Client v2
- Java
- Go

```codeBlockLines_e6Vv
from weaviate.classes.config import Configure, Property, DataType

client.collections.create(
    "Article",
    vector_config=Configure.Vectors.text2vec_openai(
        name="default",
        vector_index_config=Configure.VectorIndex.hnsw(),  # Use the HNSW index
        # vector_index_config=Configure.VectorIndex.flat(),  # Use the FLAT index
        # vector_index_config=Configure.VectorIndex.dynamic(),  # Use the DYNAMIC index
    ),
    properties=[\
        Property(name="title", data_type=DataType.TEXT),\
        Property(name="body", data_type=DataType.TEXT),\
    ],
)

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

Additional information

- Read more about index types & compression in [Concepts: Vector index](https://docs.weaviate.io/weaviate/concepts/vector-index).

## Set vector index parameters [​](https://docs.weaviate.io/weaviate/manage-collections/vector-config\#set-vector-index-parameters "Direct link to Set vector index parameters")

Set vector index parameters such as [compression](https://docs.weaviate.io/weaviate/configuration/compression) and [filter strategy](https://docs.weaviate.io/weaviate/concepts/filtering#filter-strategy) through collection configuration. Some parameters can be [updated later](https://docs.weaviate.io/weaviate/manage-collections/collection-operations#update-a-collection-definition) after collection creation.

Filter strategy parameter

Was added in `v1.27`

- Python Client v4
- Python Client v3
- JS/TS Client v3
- JS/TS Client v2
- Java
- Go

```codeBlockLines_e6Vv
from weaviate.classes.config import (
    Configure,
    Property,
    DataType,
    VectorDistances,
    VectorFilterStrategy,
)

client.collections.create(
    "Article",
    vector_config=Configure.Vectors.text2vec_openai(
        name="default",
        vector_index_config=Configure.VectorIndex.hnsw(
            ef_construction=300,
            distance_metric=VectorDistances.COSINE,
            filter_strategy=VectorFilterStrategy.SWEEPING,  # or ACORN (Available from Weaviate v1.27.0)
        ),
    ),
)

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

Additional information

- Read more about index types & compression in [Concepts: Vector index](https://docs.weaviate.io/weaviate/concepts/vector-index).

## Property-level settings [​](https://docs.weaviate.io/weaviate/manage-collections/vector-config\#property-level-settings "Direct link to Property-level settings")

Configure individual properties in a collection. Each property can have it's own configuration. Here are some common settings:

- Vectorize the property
- Vectorize the property name
- Set a [tokenization type](https://docs.weaviate.io/weaviate/config-refs/collections#tokenization)

- Python Client v4
- Python Client v3
- JS/TS Client v3
- JS/TS Client v2
- Java
- Go

```codeBlockLines_e6Vv
from weaviate.classes.config import Configure, Property, DataType, Tokenization

client.collections.create(
    "Article",
    vector_config=Configure.Vectors.text2vec_cohere(),
    properties=[\
        Property(\
            name="title",\
            data_type=DataType.TEXT,\
            vectorize_property_name=True,  # Use "title" as part of the value to vectorize\
            tokenization=Tokenization.LOWERCASE,  # Use "lowecase" tokenization\
            description="The title of the article.",  # Optional description\
        ),\
        Property(\
            name="body",\
            data_type=DataType.TEXT,\
            skip_vectorization=True,  # Don't vectorize this property\
            tokenization=Tokenization.WHITESPACE,  # Use "whitespace" tokenization\
        ),\
    ],
)

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

## Specify a distance metric [​](https://docs.weaviate.io/weaviate/manage-collections/vector-config\#specify-a-distance-metric "Direct link to Specify a distance metric")

If you choose to bring your own vectors, you should specify the `distance metric`.

- Python Client v4
- Python Client v3
- JS/TS Client v3
- JS/TS Client v2
- Java
- Go

```codeBlockLines_e6Vv
from weaviate.classes.config import Configure, VectorDistances

client.collections.create(
    "Article",
    vector_config=Configure.Vectors.text2vec_openai(
        vector_index_config=Configure.VectorIndex.hnsw(
            distance_metric=VectorDistances.COSINE
        ),
    )
)

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

Additional information

For details on the configuration parameters, see the following:

- [Distances](https://docs.weaviate.io/weaviate/config-refs/distances)
- [Vector indexes](https://docs.weaviate.io/weaviate/config-refs/indexing/vector-index)

## Further resources [​](https://docs.weaviate.io/weaviate/manage-collections/vector-config\#further-resources "Direct link to Further resources")

- [API References: REST: Schema](https://docs.weaviate.io/weaviate/api/rest#tag/schema/post/schema)
- [References: Configuration: Schema](https://docs.weaviate.io/weaviate/config-refs/collections)
- [Concepts: Data structure](https://docs.weaviate.io/weaviate/concepts/data)
