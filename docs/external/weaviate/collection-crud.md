
Every object in Weaviate belongs to exactly one collection. Use the examples on this page to manage your collections.

Terminology

Newer Weaviate documentation discuses "collections." Older Weaviate documentation refers to "classes" instead. Expect to see both terms throughout the documentation.

Python and JS/TS client - Vectorizer Configuration API Changes

Starting with Weaviate Python client `v4.16.0`, the [vectorizer configuration API has been updated](https://docs.weaviate.io/weaviate/client-libraries/python#vectorizer-api-changes-v4160).

Starting with Weaviate JS/TS client `v3.8.0`, the [vectorizer configuration API has been updated](https://docs.weaviate.io/weaviate/client-libraries/typescript#vectorizer-api-changes-v380).

Action required: **Update to the latest client version** and migrate your code to use the [new vectorizer configuration API](https://docs.weaviate.io/weaviate/manage-collections/vector-config#specify-a-vectorizer).

## Create a collection [​](https://docs.weaviate.io/weaviate/manage-collections/collection-operations\#create-a-collection "Direct link to Create a collection")

To create a collection, specify at least the collection name. If you don't specify any properties, [`auto-schema`](https://docs.weaviate.io/weaviate/config-refs/collections#auto-schema) creates them.

Capitalization

Weaviate follows GraphQL naming conventions.

- Start collection names with an upper case letter.
- Start property names with a lower case letter.

If you use an initial upper case letter to define a property name, Weaviate changes it to a lower case letter internally.

- Python Client v4
- Python Client v3
- JS/TS Client v3
- JS/TS Client v2
- Java
- Go

```codeBlockLines_e6Vv
client.collections.create("Article")

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

Production ready collections

- **Manually define you data schema**:
Avoid using the [`auto-schema`](https://docs.weaviate.io/weaviate/config-refs/collections#auto-schema) feature, instead, manually [define the properties for your collection](https://docs.weaviate.io/weaviate/manage-collections/collection-operations#create-a-collection-and-define-properties).
- **Avoid creating too many collections**:
Using too many collections can lead to scalability issues like high memory usage and degraded query performance. Instead, consider [using multi-tenancy](https://docs.weaviate.io/weaviate/manage-collections/multi-tenancy), where a single collection is subdivided into multiple tenants. For more details, see [Starter Guides: Scaling limits with collections](https://docs.weaviate.io/weaviate/starter-guides/managing-collections/collections-scaling-limits).

## Create a collection and define properties [​](https://docs.weaviate.io/weaviate/manage-collections/collection-operations\#create-a-collection-and-define-properties "Direct link to Create a collection and define properties")

Properties are the data fields in your collection. Each property has a name and a data type.

Additional information

Use properties to configure additional parameters such as data type, index characteristics, or tokenization.

For details, see:

- [References: Configuration: Schema](https://docs.weaviate.io/weaviate/config-refs/collections)
- [API References: REST: Schema](https://docs.weaviate.io/weaviate/api/rest#tag/schema)
- [Available data types](https://docs.weaviate.io/weaviate/config-refs/datatypes)

- Python Client v4
- Python Client v3
- JS/TS Client v3
- JS/TS Client v2
- Java
- Go

```codeBlockLines_e6Vv
from weaviate.classes.config import Property, DataType

# Note that you can use `client.collections.create_from_dict()` to create a collection from a v3-client-style JSON object
client.collections.create(
    "Article",
    properties=[\
        Property(name="title", data_type=DataType.TEXT),\
        Property(name="body", data_type=DataType.TEXT),\
    ],
)

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

## Create a collection with a vectorizer [​](https://docs.weaviate.io/weaviate/manage-collections/collection-operations\#create-a-collection-with-a-vectorizer "Direct link to Create a collection with a vectorizer")

Specify a `vectorizer` for a collection that will generate vector embeddings when creating objects and executing vector search queries.

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

Vectorizer configuration

Find out more about the vectorizer and vector index configuration in [Manage collections: Vectorizer and vector index](https://docs.weaviate.io/weaviate/manage-collections/vector-config).

## Disable auto-schema [​](https://docs.weaviate.io/weaviate/manage-collections/collection-operations\#disable-auto-schema "Direct link to Disable auto-schema")

By default, Weaviate creates missing collections and missing properties. When you configure collections manually, you have more precise control of the collection settings.

To disable [`auto-schema`](https://docs.weaviate.io/weaviate/config-refs/collections#auto-schema) set `AUTOSCHEMA_ENABLED: 'false'` in your system configuration file.

## Check if a collection exists [​](https://docs.weaviate.io/weaviate/manage-collections/collection-operations\#check-if-a-collection-exists "Direct link to Check if a collection exists")

Get a boolean indicating whether a given collection exists.

- Python Client v4
- JS/TS Client v3

```codeBlockLines_e6Vv
exists = client.collections.exists("Article")  # Returns a boolean

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

## Read a single collection definition [​](https://docs.weaviate.io/weaviate/manage-collections/collection-operations\#read-a-single-collection-definition "Direct link to Read a single collection definition")

Retrieve a collection definition from the schema.

- Python Client v4
- Python Client v3
- JS/TS Client v3
- JS/TS Client v2
- Java
- Go

```codeBlockLines_e6Vv
articles = client.collections.use("Article")
articles_config = articles.config.get()

print(articles_config)

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

Sample configuration: Text objects

This configuration for text objects defines the following:

- The collection name ( `Article`)
- The vectorizer module ( `text2vec-cohere`) and model ( `embed-multilingual-v2.0`)
- A set of properties ( `title`, `body`) with `text` data types.

```codeBlockLines_e6Vv
{
  "class": "Article",
  "vectorizer": "text2vec-cohere",
  "moduleConfig": {
    "text2vec-cohere": {
      "model": "embed-multilingual-v2.0"
    }
  },
  "properties": [\
    {\
      "name": "title",\
      "dataType": ["text"]\
    },\
    {\
      "name": "body",\
      "dataType": ["text"]\
    }\
  ]
}

```

Sample configuration: Nested objects

Added in `v1.22`

This configuration for nested objects defines the following:

- The collection name ( `Person`)

- The vectorizer module ( `text2vec-huggingface`)

- A set of properties ( `last_name`, `address`)
  - `last_name` has `text` data type
  - `address` has `object` data type
- The `address` property has two nested properties ( `street` and `city`)


```codeBlockLines_e6Vv
{
  "class": "Person",
  "vectorizer": "text2vec-huggingface",
  "properties": [\
    {\
      "dataType": ["text"],\
      "name": "last_name"\
    },\
    {\
      "dataType": ["object"],\
      "name": "address",\
      "nestedProperties": [\
        { "dataType": ["text"], "name": "street" },\
        { "dataType": ["text"], "name": "city" }\
      ]\
    }\
  ]
}

```

Sample configuration: Generative search

This configuration for [retrieval augmented generation](https://docs.weaviate.io/weaviate/search/generative) defines the following:

- The collection name ( `Article`)
- The default vectorizer module ( `text2vec-openai`)
- The generative module ( `generative-openai`)
- A set of properties ( `title`, `chunk`, `chunk_no` and `url`)
- The tokenization option for the `url` property
- The vectorization option ( `skip` vectorization) for the `url` property

```codeBlockLines_e6Vv
{
  "class": "Article",
  "vectorizer": "text2vec-openai",
  "vectorIndexConfig": {
    "distance": "cosine"
  },
  "moduleConfig": {
    "generative-openai": {}
  },
  "properties": [\
    {\
      "name": "title",\
      "dataType": ["text"]\
    },\
    {\
      "name": "chunk",\
      "dataType": ["text"]\
    },\
    {\
      "name": "chunk_no",\
      "dataType": ["int"]\
    },\
    {\
      "name": "url",\
      "dataType": ["text"],\
      "tokenization": "field",\
      "moduleConfig": {\
        "text2vec-openai": {\
          "skip": true\
        }\
      }\
    }\
  ]
}

```

Sample configuration: Images

This configuration for image search defines the following:

- The collection name ( `Image`)

- The vectorizer module ( `img2vec-neural`)
  - The `image` property configures collection to store image data.
- The vector index distance metric ( `cosine`)

- A set of properties ( `image`), with the `image` property set as `blob`.


For image searches, see [Image search](https://docs.weaviate.io/weaviate/search/image).

```codeBlockLines_e6Vv
{
  "class": "Image",
  "vectorizer": "img2vec-neural",
  "vectorIndexConfig": {
    "distance": "cosine"
  },
  "moduleConfig": {
    "img2vec-neural": {
      "imageFields": ["image"]
    }
  },
  "properties": [\
    {\
      "name": "image",\
      "dataType": ["blob"]\
    }\
  ]
}

```

## Read all collection definitions [​](https://docs.weaviate.io/weaviate/manage-collections/collection-operations\#read-all-collection-definitions "Direct link to Read all collection definitions")

Fetch the database schema to retrieve all of the collection definitions.

- Python Client v4
- Python Client v3
- JS/TS Client v3
- JS/TS Client v2
- Java
- Go

```codeBlockLines_e6Vv
response = client.collections.list_all(simple=False)

print(response)

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

## Update a collection definition [​](https://docs.weaviate.io/weaviate/manage-collections/collection-operations\#update-a-collection-definition "Direct link to Update a collection definition")

Replication factor change

The replication factor of a collection cannot be updated by updating the collection's definition.

From `v1.32` by using [replica movement](https://docs.weaviate.io/deploy/configuration/replica-movement), the [replication factor](https://docs.weaviate.io/weaviate/config-refs/collections#replication) of a shard can be changed.

You can update a collection definition to change the [mutable collection settings](https://docs.weaviate.io/weaviate/config-refs/collections#mutability).

- Python Client v4
- Python Client v3
- JS/TS Client v3
- JS/TS Client v2
- Java
- Go

```codeBlockLines_e6Vv
from weaviate.classes.config import (
    Reconfigure,
    VectorFilterStrategy,
    ReplicationDeletionStrategy,
)

articles = client.collections.use("Article")

# Update the collection definition
articles.config.update(
    description="An updated collection description.",
    property_descriptions={
        "title": "The updated title description for article",
    },  # Available from Weaviate v1.31.0
    inverted_index_config=Reconfigure.inverted_index(bm25_k1=1.5),
    vector_config=Reconfigure.Vectors.update(
        name="default",
        vector_index_config=Reconfigure.VectorIndex.hnsw(
            filter_strategy=VectorFilterStrategy.ACORN  # Available from Weaviate v1.27.0
        ),
    ),
    replication_config=Reconfigure.replication(
        deletion_strategy=ReplicationDeletionStrategy.TIME_BASED_RESOLUTION  # Available from Weaviate v1.28.0
    ),
)
articles = client.collections.use("Article")

article_shards = articles.config.update_shards(
    status="READY",
    shard_names=shard_names,  # The names (List[str]) of the shard to update (or a shard name)
)

print(article_shards)

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

## Delete a collection [​](https://docs.weaviate.io/weaviate/manage-collections/collection-operations\#delete-a-collection "Direct link to Delete a collection")

You can delete any unwanted collection(s), along with the data that they contain.

Deleting a collection also deletes its objects

When you **delete a collection, you delete all associated objects**!

Be very careful with deletes on a production database and anywhere else that you have important data.

This code deletes a collection and its objects.

- Python Client v4
- Python Client v3
- JS/TS Client v3
- JS/TS Client v2
- Go
- Java
- Curl

```codeBlockLines_e6Vv
# collection_name can be a string ("Article") or a list of strings (["Article", "Category"])
client.collections.delete(
    collection_name
)  # THIS WILL DELETE THE SPECIFIED COLLECTION(S) AND THEIR OBJECTS

# Note: you can also delete all collections in the Weaviate instance with:
# client.collections.delete_all()

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

## Add a property [​](https://docs.weaviate.io/weaviate/manage-collections/collection-operations\#add-a-property "Direct link to Add a property")

Indexing limitations after data import

There are no index limitations when you add collection properties before you import data.

If you add a new property after you import data, there is an impact on indexing.

Property indexes are built at import time. If you add a new property after importing some data, pre-existing objects index aren't automatically updated to add the new property. This means pre-existing objects aren't added to the new property index. Queries may return unexpected results because the index only includes new objects.

To create an index that includes all of the objects in a collection, do one of the following:

- New collections: Add all of the collection's properties before importing objects.
- Existing collections: Export the existing data from the collection. Re-create it with the new property. Import the data into the updated collection.

We are working on a re-indexing API to allow you to re-index the data after adding a property. This will be available in a future release.

- Python Client v4
- Python Client v3
- JS/TS Client v3
- JS/TS Client v2
- Go
- Java

```codeBlockLines_e6Vv
from weaviate.classes.config import Property, DataType

articles = client.collections.use("Article")

articles.config.add_property(Property(name="onHomepage", data_type=DataType.BOOL))

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

## Set inverted index parameters [​](https://docs.weaviate.io/weaviate/manage-collections/collection-operations\#set-inverted-index-parameters "Direct link to Set inverted index parameters")

Various [inverted index parameters](https://docs.weaviate.io/weaviate/config-refs/indexing/inverted-index#inverted-index-parameters) are configurable for each collection. Some parameters are set at the collection level, while others are set at the property level.

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
    # Additional settings not shown
    properties=[  # properties configuration is optional\
        Property(\
            name="title",\
            data_type=DataType.TEXT,\
            index_filterable=True,\
            index_searchable=True,\
        ),\
        Property(\
            name="chunk",\
            data_type=DataType.TEXT,\
            index_filterable=True,\
            index_searchable=True,\
        ),\
        Property(\
            name="chunk_number",\
            data_type=DataType.INT,\
            index_range_filters=True,\
        ),\
    ],
    inverted_index_config=Configure.inverted_index(  # Optional
        bm25_b=0.7,
        bm25_k1=1.25,
        index_null_state=True,
        index_property_length=True,
        index_timestamps=True,
    ),
)

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

## Further resources [​](https://docs.weaviate.io/weaviate/manage-collections/collection-operations\#further-resources "Direct link to Further resources")

- [Manage collections: Vectorizer and vector index](https://docs.weaviate.io/weaviate/manage-collections/vector-config)
- [References: Collection definition](https://docs.weaviate.io/weaviate/config-refs/collections)
- [Concepts: Data structure](https://docs.weaviate.io/weaviate/concepts/data)
- [API References: REST: Schema](https://docs.weaviate.io/weaviate/api/rest#tag/schema/post/schema)
