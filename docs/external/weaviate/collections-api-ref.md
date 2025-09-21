A **collection definition** specifies how to store and index a set of data objects in Weaviate. This page discusses the available parameters for configuring a collection.

## Collection definition parameters [​](https://docs.weaviate.io/weaviate/config-refs/collections\#collection-definition-parameters "Direct link to Collection definition parameters")

These are the top-level parameters you can set when creating a collection.

| Parameter | Type | Description | Default | Mutable |
| --- | --- | --- | --- | --- |
| [`class`](https://docs.weaviate.io/weaviate/config-refs/collections#class) | String | The name of the collection. | (Required) | No |
| [`description`](https://docs.weaviate.io/weaviate/config-refs/collections#description) | String | A description of the collection. | `""` | Yes |
| [`properties`](https://docs.weaviate.io/weaviate/config-refs/collections#properties) | Array | An array of property objects defining the data schema. | `[]` | Partially\* |
| [`invertedIndexConfig`](https://docs.weaviate.io/weaviate/config-refs/collections#inverted-index) | Object | Configuration for the inverted index, affecting filtering and keyword search. | See [Inverted Index reference](https://docs.weaviate.io/weaviate/config-refs/indexing/inverted-index#inverted-index-parameters) | Yes |
| [`vectorConfig`](https://docs.weaviate.io/weaviate/config-refs/collections#vector-configuration) | Object | Configure multiple named vectors each with their own `vectorizer`, `vectorIndexType`, and `vectorIndexConfig` fields. | `null` | Partially\*\* |
| [`vectorizer`](https://docs.weaviate.io/weaviate/config-refs/collections#vector-configuration) | String | The vectorizer module to use. | Default vectorizer defined by [environment variable](https://docs.weaviate.io/deploy/configuration/env-vars#DEFAULT_VECTORIZER_MODULE). See [Model provider](https://docs.weaviate.io/weaviate/model-providers) for module-specific config defaults | No |
| [`vectorIndexType`](https://docs.weaviate.io/weaviate/config-refs/collections#vector-configuration) | String | The type of vector index to use ( `hnsw`, `flat`, `dynamic`). | `hnsw` | No |
| [`moduleConfig`](https://docs.weaviate.io/weaviate/config-refs/collections#module-configuration) | Object | Module-specific configuration settings. | See [Module configuration](https://docs.weaviate.io/weaviate/config-refs/collections#module-configuration) | Partially |
| [`vectorIndexConfig`](https://docs.weaviate.io/weaviate/config-refs/collections#vector-configuration) | Object | Configuration settings specific to the chosen `vectorIndexType`. | See [Vector index reference](https://docs.weaviate.io/weaviate/config-refs/indexing/vector-index) | Partially |
| [`shardingConfig`](https://docs.weaviate.io/weaviate/config-refs/collections#sharding) | Object | Controls sharding behavior in a multi-node cluster. | See [Sharding section](https://docs.weaviate.io/weaviate/config-refs/collections#sharding) | No |
| [`replicationConfig`](https://docs.weaviate.io/weaviate/config-refs/collections#replication) | Object | Controls data replication settings for fault tolerance. | See [Replication section](https://docs.weaviate.io/weaviate/config-refs/collections#replication) | Partially |
| [`multiTenancyConfig`](https://docs.weaviate.io/weaviate/config-refs/collections#multi-tenancy) | Object | Configuration to enable multi-tenancy for the collection. | See [Multi-tenancy section](https://docs.weaviate.io/weaviate/config-refs/collections#multi-tenancy) | Partially |

\\* [New properties can be added](https://docs.weaviate.io/weaviate/manage-collections/collection-operations#add-a-property); existing properties cannot be modified

\\*\\* [New named vectors can be added](https://docs.weaviate.io/weaviate/manage-collections/vector-config#add-new-named-vectors); some vector index settings are mutable

Example collection configuration - JSON object

An example of a complete collection object including properties:

```codeBlockLines_e6Vv
{
  "class": "Article",                       // The name of the collection in string format
  "description": "An article",              // A description for your reference
  "vectorIndexType": "hnsw",                // Defaults to hnsw
  "vectorIndexConfig": {
    ...                                     // Vector index type specific settings, including distance metric
  },
  "vectorizer": "text2vec-contextionary",   // Vectorizer to use for data objects added to this collection
  "moduleConfig": {
    "text2vec-contextionary": {
      "vectorizeClassName": true            // Include the collection name in vector calculation (default true)
    }
  },
  "properties": [                           // An array of the properties you are adding, same as a Property Object\
    {\
      "name": "title",                     // The name of the property\
      "description": "title of the article",              // A description for your reference\
      "dataType": [                         // The data type of the object as described above. When\
                                            //    creating cross-references, a property can have\
                                            //    multiple data types, hence the array syntax.\
        "text"\
      ],\
      "moduleConfig": {                     // Module-specific settings\
        "text2vec-contextionary": {\
          "skip": true,                     // If true, the whole property will NOT be included in\
                                            //    vectorization. Default is false, meaning that the\
                                            //    object will be NOT be skipped.\
          "vectorizePropertyName": true,    // Whether the name of the property is used in the\
                                            //    calculation for the vector position of data\
                                            //    objects. Default false.\
        }\
      },\
      "indexFilterable": true,              // Optional, default is true. By default each property\
                                            //    is indexed with a roaring bitmap index where\
                                            //     available for efficient filtering.\
      "indexSearchable": true               // Optional, default is true. By default each property\
                                            //    is indexed with a searchable index for\
                                            //    BM25-suitable Map index for BM25 or hybrid\
                                            //    searching.\
    }\
  ],
  "invertedIndexConfig": {                  // Optional, index configuration
    "stopwords": {
      ...                                   // Optional, controls which words should be ignored in the inverted index, see section below
    },
    "indexTimestamps": false,               // Optional, maintains inverted indexes for each object by its internal timestamps
    "indexNullState": false,                // Optional, maintains inverted indexes for each property regarding its null state
    "indexPropertyLength": false            // Optional, maintains inverted indexes for each property by its length
  },
  "shardingConfig": {
    ...                                     // Optional, controls behavior of the collection in a
                                            //    multi-node setting, see section below
  },
  "multiTenancyConfig": {"enabled": true}   // Optional, for enabling multi-tenancy for this
                                            //    collection (default: false)
}

```

#### Code example - How to create a collection [​](https://docs.weaviate.io/weaviate/config-refs/collections\#code-example---how-to-create-a-collection "Direct link to Code example - How to create a collection")

This code example shows how to configure the collection parameters through a client library:

- Python Client v4

```codeBlockLines_e6Vv
from weaviate.classes.config import (
    Configure,
    DataType,
    Property,
    ReplicationDeletionStrategy,
    VectorDistances,
    VectorFilterStrategy,
)

client.collections.create(
    "Article",
    description="A collection of articles",
    properties=[\
        Property(name="title", data_type=DataType.TEXT),\
        Property(name="body", data_type=DataType.TEXT),\
    ],
    vector_config=Configure.Vectors.text2vec_openai(
        name="default",
        source_properties=["title", "body"],
        vector_index_config=Configure.VectorIndex.hnsw(
            ef_construction=300,
            distance_metric=VectorDistances.COSINE,
            filter_strategy=VectorFilterStrategy.SWEEPING,
        ),
    ),
    multi_tenancy_config=Configure.multi_tenancy(False),
    sharding_config=Configure.sharding(
        virtual_per_physical=128,
        desired_count=1,
        desired_virtual_count=128,
    ),
    replication_config=Configure.replication(
        factor=1,
        async_enabled=False,
        deletion_strategy=ReplicationDeletionStrategy.TIME_BASED_RESOLUTION,
    ),
)

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

Further resources

For more code examples and configuration guides visit the [How-to: Manage collections](https://docs.weaviate.io/weaviate/manage-collections) section.

#### `class` [​](https://docs.weaviate.io/weaviate/config-refs/collections\#class "Direct link to class")

The `class` is the name of the collection.

The collection name starts with an upper case letter. The upper case letter distinguishes collection names from primitive data types when the name is used as a property value.

Consider these examples that use the `dataType` property:

- `dataType: ["text"]` is a `text` data type.
- `dataType: ["Text"]` is a cross-reference type to a collection named `Text`.

After the first letter, collection names may use any GraphQL-compatible characters.

The collection name validation regex is `/^[A-Z][_0-9A-Za-z]*$/`.

Capitalization

Weaviate follows GraphQL naming conventions.

- Start collection names with an upper case letter.
- Start property names with a lower case letter.

If you use an initial upper case letter to define a property name, Weaviate changes it to a lower case letter internally.

#### `description` [​](https://docs.weaviate.io/weaviate/config-refs/collections\#description "Direct link to description")

A description of the collection. This is for your reference and can also provide additional information to [Weaviate Agents](https://docs.weaviate.io/agents).

* * *

### Properties [​](https://docs.weaviate.io/weaviate/config-refs/collections\#properties "Direct link to Properties")

| Parameter | Type | Description | Default | Mutable |
| --- | --- | --- | --- | --- |
| [`name`](https://docs.weaviate.io/weaviate/config-refs/collections#name) | String | The name of the property. | (Required) | No |
| [`dataType`](https://docs.weaviate.io/weaviate/config-refs/datatypes) | Array | An array containing one or more data types. For cross-references, use the capitalized collection name (e.g., `["Article"]`). | (Required) | No |
| `description` | String | A description of the property for your reference. | `null` | Yes |
| [`tokenization`](https://docs.weaviate.io/weaviate/config-refs/collections#tokenization) | String | For `text` properties, specifies how the text is split into tokens for inverted indexing. | `word` | No |
| [`indexInverted`](https://docs.weaviate.io/weaviate/config-refs/collections#inverted-index) | Boolean | If `true`, inverted index is enabled for this property. | `true` | No |
| [`indexFilterable`](https://docs.weaviate.io/weaviate/config-refs/collections#inverted-index) | Boolean | If `true`, builds a roaring bitmap index for this property to allow for efficient filtering. | `true` | No |
| [`indexSearchable`](https://docs.weaviate.io/weaviate/config-refs/collections#inverted-index) | Boolean | If `true`, builds a searchable map index for this property, suitable for BM25 or hybrid search. | `true` | No |
| [`indexRangeFilters`](https://docs.weaviate.io/weaviate/config-refs/collections#inverted-index) | Boolean | If `true`, builds a roaring bitmap index for numerical range-based filtering. | `false` | No |
| [`invertedIndexConfig`](https://docs.weaviate.io/weaviate/config-refs/collections#inverted-index) | Object | Property-level overrides for inverted index settings, such as `bm25` parameters. | `{}` | No |
| `moduleConfig` | Object | Module-specific settings, such as skipping vectorization for this property. | `{}` | No |

Example property configuration - JSON object

An example of a complete property object:

```codeBlockLines_e6Vv
{
  "name": "title", // The name of the property
  "description": "title of the article", // A description for your reference
  "dataType": [\
    // The data type of the object as described above. When creating cross-references, a property can have multiple dataTypes.\
    "text"\
  ],
  "tokenization": "word", // Split field contents into word-tokens when indexing into the inverted index. See "Property Tokenization" below for more detail.
  "moduleConfig": {
    // Module-specific settings
    "text2vec-contextionary": {
      "skip": true, // If true, the whole property is NOT included in vectorization. Default is false, meaning that the object will be NOT be skipped.
      "vectorizePropertyName": true // Whether the name of the property is used in the calculation for the vector position of data objects. Default false.
    }
  },
  "indexFilterable": true, // Optional, default is true. By default each property is indexed with a roaring bitmap index where available for efficient filtering.
  "indexSearchable": true // Optional, default is true. By default each property is indexed with a searchable index for BM25-suitable Map index for BM25 or hybrid searching.
}

```

#### Code example - How to configure collection properties [​](https://docs.weaviate.io/weaviate/config-refs/collections\#code-example---how-to-configure-collection-properties "Direct link to Code example - How to configure collection properties")

This code example shows how to configure the property parameters through a client library:

- Python Client v4

```codeBlockLines_e6Vv
from weaviate.classes.config import Property, DataType

# Note that you can use `client.collections.create_from_dict()` to create a collection from a v3-client-style JSON object
client.collections.create(
    "Article",
    vector_config=Configure.Vectors.text2vec_openai(),
    properties=[  # properties configuration is optional\
        Property(name="title", data_type=DataType.TEXT),\
        Property(name="description", data_type=DataType.TEXT, skip_vectorization=True),\
        Property(name="rating", data_type=DataType.NUMBER),\
    ],
)

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

Further resources

For more code example and configuration guides visit the [How-to: Manage collections](https://docs.weaviate.io/weaviate/manage-collections) section.

#### `name` [​](https://docs.weaviate.io/weaviate/config-refs/collections\#name "Direct link to name")

Property names can contain the following characters: `/[_A-Za-z][_0-9A-Za-z]*/`.

##### Reserved words [​](https://docs.weaviate.io/weaviate/config-refs/collections\#reserved-words "Direct link to Reserved words")

The following words are reserved and cannot be used as property names:

- `_additional`
- `id`
- `_id`

Additionally, we strongly recommend that you do not use the following words as property names, due to potential conflicts with future reserved words:

- `vector`
- `_vector`

#### `tokenization` [​](https://docs.weaviate.io/weaviate/config-refs/collections\#tokenization "Direct link to tokenization")

You can customize how `text` data is tokenized and indexed in the inverted index. Tokenization influences the results returned by the [`bm25`](https://docs.weaviate.io/weaviate/api/graphql/search-operators#bm25) and [`hybrid`](https://docs.weaviate.io/weaviate/api/graphql/search-operators#hybrid) operators, and [`where` filters](https://docs.weaviate.io/weaviate/api/graphql/filters).

Tokenization is a property-level configuration for `text` properties. [See how to set the tokenization option using a client library](https://docs.weaviate.io/weaviate/manage-collections/vector-config#property-level-settings)

Example property configuration - JSON object

```codeBlockLines_e6Vv
{
  "classes": [\
    {\
      "class": "Question",\
      "properties": [\
        {\
          "dataType": ["text"],\
          "name": "question",\
          "tokenization": "word"\
        },\
      ],\
      ...\
      "vectorizer": "text2vec-openai"\
    }\
  ]
}

```

Each token will be indexed separately in the inverted index. For example, if you have a `text` property with the value `Hello, (beautiful) world`, the following table shows how the tokens would be indexed for each tokenization method:

| Tokenization Method | Explanation | Indexed Tokens |
| --- | --- | --- |
| `word` (default) | Keep only alpha-numeric characters, lowercase them, and split by whitespace. | `hello`, `beautiful`, `world` |
| `lowercase` | Lowercase the entire text and split on whitespace. | `hello,`, `(beautiful)`, `world` |
| `whitespace` | Split the text on whitespace. Searches/filters become case-sensitive. | `Hello,`, `(beautiful)`, `world` |
| `field` | Index the whole field after trimming whitespace characters. | `Hello, (beautiful) world` |
| `trigram` | Split the property as rolling trigrams. | `Hel`, `ell`, `llo`, `lo,`, ... |
| `gse` | Use the `gse` tokenizer to split the property. | [See `gse` docs](https://pkg.go.dev/github.com/go-ego/gse#section-readme) |
| `kagome_ja` | Use the `Kagome` tokenizer with a Japanese (IPA) dictionary to split the property. | [See `kagome` docs](https://github.com/ikawaha/kagome) and the [dictionary](https://github.com/ikawaha/kagome-dict/). |
| `kagome_kr` | Use the `Kagome` tokenizer with a Korean dictionary to split the property. | [See `kagome` docs](https://github.com/ikawaha/kagome) and the [Korean dictionary](https://github.com/ikawaha/kagome-dict-ko). |

##### Tokenization and search / filtering [​](https://docs.weaviate.io/weaviate/config-refs/collections\#tokenization-and-search--filtering "Direct link to Tokenization and search / filtering")

Tokenization impacts how filters or keywords searches behave. The filter or keyword search query is also tokenized before being matched against the inverted index.

The following table shows an example scenario showing whether a filter or keyword search would identify a `text` property with value `Hello, (beautiful) world` as a hit.

- **Row**: Various tokenization methods.
- **Column**: Various search strings.

|  | `Beautiful` | `(Beautiful)` | `(beautiful)` | `Hello, (beautiful) world` |
| --- | --- | --- | --- | --- |
| `word` (default) | ✅ | ✅ | ✅ | ✅ |
| `lowercase` | ❌ | ✅ | ✅ | ✅ |
| `whitespace` | ❌ | ❌ | ✅ | ✅ |
| `field` | ❌ | ❌ | ❌ | ✅ |

`gse` and `trigram` tokenization methods

Added in `1.24`

For Japanese and Chinese text, we recommend use of `gse` or `trigram` tokenization methods. These methods work better with these languages than the other methods as these languages are not easily able to be tokenized using whitespaces.

The `gse` tokenizer is not loaded by default to save resources. To use it, set the environment variable `ENABLE_TOKENIZER_GSE` to `true` on the Weaviate instance.

`gse` tokenization examples:

- `"素早い茶色の狐が怠けた犬を飛び越えた"`: `["素早", "素早い", "早い", "茶色", "の", "狐", "が", "怠け", "けた", "犬", "を", "飛び", "飛び越え", "越え", "た", "素早い茶色の狐が怠けた犬を飛び越えた"]`
- `"すばやいちゃいろのきつねがなまけたいぬをとびこえた"`: `["すばや", "すばやい", "やい", "いち", "ちゃ", "ちゃい", "ちゃいろ", "いろ", "のき", "きつ", "きつね", "つね", "ねが", "がな", "なま", "なまけ", "まけ", "けた", "けたい", "たい", "いぬ", "を", "とび", "とびこえ", "こえ", "た", "すばやいちゃいろのきつねがなまけたいぬをとびこえた"]`

`trigram` for fuzzy matching

While originally designed for Asian languages, `trigram` tokenization is also highly effective for fuzzy matching and typo tolerance in other languages.

`kagome_ja` tokenization method

Experimental feature

Available starting in `v1.28.0`. This is an experimental feature. Use with caution.

For Japanese text, `kagome_ja` tokenization method is also available. This uses the [`Kagome` tokenizer](https://github.com/ikawaha/kagome?tab=readme-ov-file) with a Japanese [MeCab IPA](https://github.com/ikawaha/kagome-dict/) dictionary to split the property text.

The `kagome_ja` tokenizer is not loaded by default to save resources. To use it, set the environment variable `ENABLE_TOKENIZER_KAGOME_JA` to `true` on the Weaviate instance.

`kagome_ja` tokenization examples:

- `"春の夜の夢はうつつよりもかなしき 夏の夜の夢はうつつに似たり 秋の夜の夢はうつつを超え 冬の夜の夢は心に響く 山のあなたに小さな村が見える 川の音が静かに耳に届く 風が木々を通り抜ける音 星空の下、すべてが平和である"`:
  - \[ `"春", "の", "夜", "の", "夢", "は", "うつつ", "より", "も", "かなしき", "\n\t", "夏", "の", "夜", "の", "夢", "は", "うつつ", "に", "似", "たり", "\n\t", "秋", "の", "夜", "の", "夢", "は", "うつつ", "を", "超え", "\n\t", "冬", "の", "夜", "の", "夢", "は", "心", "に", "響く", "\n\n\t", "山", "の", "あなた", "に", "小さな", "村", "が", "見える", "\n\t", "川", "の", "音", "が", "静か", "に", "耳", "に", "届く", "\n\t", "風", "が", "木々", "を", "通り抜ける", "音", "\n\t", "星空", "の", "下", "、", "すべて", "が", "平和", "で", "ある"`\]
- `"素早い茶色の狐が怠けた犬を飛び越えた"`:
  - `["素早い", "茶色", "の", "狐", "が", "怠け", "た", "犬", "を", "飛び越え", "た"]`
- `"すばやいちゃいろのきつねがなまけたいぬをとびこえた"`:
  - `["すばやい", "ちゃ", "いろ", "の", "きつね", "が", "なまけ", "た", "いぬ", "を", "とびこえ", "た"]`

`kagome_kr` tokenization method

Experimental feature

Available starting in `v1.25.7`. This is an experimental feature. Use with caution.

For Korean text, we recommend use of the `kagome_kr` tokenization method. This uses the [`Kagome` tokenizer](https://github.com/ikawaha/kagome?tab=readme-ov-file) with a Korean MeCab ( [mecab-ko-dic](https://bitbucket.org/eunjeon/mecab-ko-dic/src/master/)) dictionary to split the property text.

The `kagome_kr` tokenizer is not loaded by default to save resources. To use it, set the environment variable `ENABLE_TOKENIZER_KAGOME_KR` to `true` on the Weaviate instance.

`kagome_kr` tokenization examples:

- `"아버지가방에들어가신다"`:
  - `["아버지", "가", "방", "에", "들어가", "신다"]`
- `"아버지가 방에 들어가신다"`:
  - `["아버지", "가", "방", "에", "들어가", "신다"]`
- `"결정하겠다"`:
  - `["결정", "하", "겠", "다"]`

Limit the number of `gse` and `Kagome` tokenizers

The `gse` and `Kagome` tokenizers can be resource intensive and affect Weaviate's performance.
You can limit the combined number of `gse` and `Kagome` tokenizers running at the same time using the [`TOKENIZER_CONCURRENCY_COUNT` environment variable](https://docs.weaviate.io/deploy/configuration/env-vars).

Fuzzy matching with `trigram` tokenization

The `trigram` tokenization method provides fuzzy matching capabilities by breaking text into overlapping 3-character sequences. This enables BM25 searches to find matches even with spelling errors or variations.

**Use cases for trigram fuzzy matching:**

- **Typo tolerance**: Find matches despite spelling errors (e.g., "Reliace" matches "Reliance")
- **Name reconciliation**: Match entity names with variations across datasets
- **Search-as-you-type**: Build autocomplete functionality
- **Partial matching**: Find objects with partial string matches

**How it works:**

When text is tokenized with `trigram`, it's broken into all possible 3-character sequences:

- `"hello"` → `["hel", "ell", "llo"]`
- `"world"` → `["wor", "orl", "rld"]`

Similar strings share many trigrams, enabling fuzzy matching:

- `"Morgan Stanley"` and `"Stanley Morgn"` share trigrams like `"sta", "tan", "anl", "nle", "ley"`

**Performance considerations:**

- Filtering behavior will change significantly, as text filtering will be done based on trigram-tokenized text, instead of whole words
- Creates larger inverted indexes due to more tokens
- May impact query performance for large datasets

tip

Use trigram tokenization selectively on fields where fuzzy matching is preferred. Keep exact-match fields with `word` or `field` tokenization for precision.

* * *

### Inverted index [​](https://docs.weaviate.io/weaviate/config-refs/collections\#inverted-index "Direct link to Inverted index")

Weaviate uses **inverted indexes** to enable fast and efficient filtering and searching. The inverted index maps values (like words or numbers) to the objects that contain them in order to speed-up all attribute-based filtering ( `where` filters) and keyword searching ( `bm25`, `hybrid`).
Disabling indexing for properties you will never query can speed up data imports and reduce disk usage.

More details about the `indexFilterable`, `indexSearchable`, `indexRangeFilters` and `invertedIndexConfig` parameters can be found in [Reference: Inverted index](https://docs.weaviate.io/weaviate/config-refs/indexing/inverted-index).

* * *

### Vector configuration [​](https://docs.weaviate.io/weaviate/config-refs/collections\#vector-configuration "Direct link to Vector configuration")

Weaviate supports two approaches for vector configuration:

- **Single vector collections**: One vector space per object using top-level parameters ( `vectorizer`, `vectorIndexType`, `vectorIndexConfig`)
- **Multiple named vectors**: Multiple vector spaces per object using the `vectorConfig` parameter ( **recommended**)

You cannot combine both approaches in the same collection.

We recommend using `vectorConfig`

Using the `vectorConfig` parameter allows you to start with one vector per collection and adding [new named vectors](https://docs.weaviate.io/weaviate/manage-collections/vector-config#add-new-named-vectors) afterward.

#### Vector configuration parameters [​](https://docs.weaviate.io/weaviate/config-refs/collections\#vector-configuration-parameters "Direct link to Vector configuration parameters")

| Parameter | Type | Description | Default | Mutable |
| --- | --- | --- | --- | --- |
| `vectorizer` | String | The vectorizer module to use (e.g., `text2vec-cohere`). Set to `none` to disable auto-vectorization. [Available model providers](https://docs.weaviate.io/weaviate/model-providers) | Module-specific default | No |
| [`vectorIndexType`](https://docs.weaviate.io/weaviate/config-refs/indexing/vector-index) | String | Vector index type: `hnsw` (default), `flat`, or `dynamic` | `hnsw` | No |
| [`vectorIndexConfig`](https://docs.weaviate.io/weaviate/config-refs/indexing/vector-index) | Object | Configuration settings for your chosen `vectorIndexType` | Index-specific defaults | Partially\* |
| `vectorConfig` | Object | **Alternative to above**: Define multiple named vector spaces | `null` | Partially\*\* |
| ↪ `vectorConfig.<name>.vectorizer` | Object | Vectorizer config for this named vector (e.g., `{"text2vec-openai": {"properties": ["title"]}}`) | (Required) | No |
| [↪ `vectorConfig.<name>.vectorIndexType`](https://docs.weaviate.io/weaviate/config-refs/indexing/vector-index) | String | Index type for this named vector | `hnsw` | No |
| [↪ `vectorConfig.<name>.vectorIndexConfig`](https://docs.weaviate.io/weaviate/config-refs/indexing/vector-index) | Object | Index configuration for this named vector | Index-specific defaults | Partially\* |

\\* See [vector index mutable parameters](https://docs.weaviate.io/weaviate/config-refs/indexing/vector-index)

\\*\\* [New named vectors can be added](https://docs.weaviate.io/weaviate/manage-collections/vector-config#add-new-named-vectors) after collection creation

#### Single vector collections [​](https://docs.weaviate.io/weaviate/config-refs/collections\#single-vector-collections "Direct link to Single vector collections")

If you don't explicitly define a [named vector](https://docs.weaviate.io/weaviate/config-refs/collections#named-vectors) in your collection definition, Weaviate automatically creates what's known as a _single vector_ collection. These vectors are stored internally under the named vector `default` (which is a reserved vector name).

To learn which properties of your data are vectorized, refer to the [Configure semantic indexing](https://docs.weaviate.io/weaviate/config-refs/indexing/vector-index#configure-semantic-indexing) section.

##### Code example - How to create single vector collection [​](https://docs.weaviate.io/weaviate/config-refs/collections\#code-example---how-to-create-single-vector-collection "Direct link to Code example - How to create single vector collection")

This code example shows how to configure the vectorizer parameters for a single vector collection through a client library:

- Python Client v4
- JS/TS Client v3
- Java
- Go

```codeBlockLines_e6Vv
from weaviate.classes.config import (
    Configure,
    DataType,
    Property,
    VectorDistances,
    VectorFilterStrategy,
)

client.collections.create(
    "Article",
    vector_config=Configure.Vectors.text2vec_openai(
        name="default",  # (Optional) Set the name of the vector, default name is "default"
        source_properties=["title", "body"],  # (Optional) Set the source property(ies)
        vector_index_config=Configure.VectorIndex.hnsw(
            ef_construction=300,
            distance_metric=VectorDistances.COSINE,
            filter_strategy=VectorFilterStrategy.SWEEPING,
        ),  # (Optional) Set vector index options
        vectorize_collection_name=True,  # (Optional) Set to True to vectorize the collection name
    ),
    properties=[  # properties configuration is optional\
        Property(name="title", data_type=DataType.TEXT, vectorize_property_name=True),\
        Property(name="body", data_type=DataType.TEXT),\
    ],
)

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

Further resources

For more code example and configuration guides visit the [How-to: Vectorizer and vector index config](https://docs.weaviate.io/weaviate/manage-collections/vector-config) guide.

#### Multiple vector embeddings (named vectors) [​](https://docs.weaviate.io/weaviate/config-refs/collections\#named-vectors "Direct link to Multiple vector embeddings (named vectors)")

Added in v1.24.0

Weaviate collections support multiple named vectors.

Collections can have multiple [named vectors](https://docs.weaviate.io/weaviate/config-refs/collections#named-vectors).

The vectors in a collection can have their own configurations. Each vector space can set its own index, its own compression algorithm, and its own vectorizer. This means you can use different vectorization models, and apply different distance metrics, to the same object.

To work with named vectors, adjust your queries to specify a target vector for [vector search](https://docs.weaviate.io/weaviate/search/similarity#named-vectors) or [hybrid search](https://docs.weaviate.io/weaviate/search/hybrid#named-vectors) queries.

##### Code example - How to create multiple named vectors [​](https://docs.weaviate.io/weaviate/config-refs/collections\#code-example---how-to-create-multiple-named-vectors "Direct link to Code example - How to create multiple named vectors")

This code example shows how to configure multiple named vectors through a client library:

- Python Client v4
- JS/TS Client v3
- Java
- Go

```codeBlockLines_e6Vv
from weaviate.classes.config import (
    Configure,
    DataType,
    Property,
    VectorDistances,
    VectorFilterStrategy,
)

client.collections.create(
    "Article",
    vector_config=[\
        Configure.Vectors.text2vec_openai(\
            name="default",  # (Optional) Set the name of the vector, default name is "default"\
            source_properties=[\
                "title",\
                "body",\
            ],  # (Optional) Set the source property(ies)\
            vector_index_config=Configure.VectorIndex.hnsw(\
                ef_construction=300,\
                distance_metric=VectorDistances.COSINE,\
                filter_strategy=VectorFilterStrategy.SWEEPING,\
            ),  # (Optional) Set vector index options\
            vectorize_collection_name=True,  # (Optional) Set to True to vectorize the collection name\
        ),\
        Configure.Vectors.text2vec_openai(\
            name="body_vectors",\
            source_properties=["body"],\
            vector_index_config=Configure.VectorIndex.flat(),\
        ),\
    ],
    properties=[  # properties configuration is optional\
        Property(name="title", data_type=DataType.TEXT, vectorize_property_name=True),\
        Property(name="body", data_type=DataType.TEXT),\
    ],
)

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

Further resources

For more code example and configuration guides visit the [How-to: Vectorizer and vector index config](https://docs.weaviate.io/weaviate/manage-collections/vector-config) guide.

* * *

### Module configuration [​](https://docs.weaviate.io/weaviate/config-refs/collections\#module-configuration "Direct link to Module configuration")

The `moduleConfig` parameter allows you to specify if the vectorizers will include or exclude the collection name in vector calculations (default `true`).
It is also used to specify reranker and generative [model providers](https://docs.weaviate.io/weaviate/model-providers) at a collection level.

Example module configuration - JSON object

An example of a complete `moduleConfig` object:

```codeBlockLines_e6Vv
  "moduleConfig": {
    "text2vec-contextionary": {
      "vectorizeClassName": true  // Include the collection name in vector calculation (default true)
    }
  },

```

* * *

### Vector index [​](https://docs.weaviate.io/weaviate/config-refs/collections\#vector-index "Direct link to Vector index")

Vector indexing organizes vector data to make similarity searches fast and efficient. Instead of comparing a query to every vector, an index builds a structure that rapidly narrows the search to the most relevant candidates.

More details about the `vectorIndexType` and `vectorIndexConfig` parameters can be found in [Reference: Vector index](https://docs.weaviate.io/weaviate/config-refs/indexing/vector-index).

* * *

### Replication [​](https://docs.weaviate.io/weaviate/config-refs/collections\#replication "Direct link to Replication")

Replication factor change

The replication factor of a collection cannot be updated by updating the collection's definition.

From `v1.32` by using [replica movement](https://docs.weaviate.io/deploy/configuration/replica-movement), the [replication factor](https://docs.weaviate.io/weaviate/config-refs/collections#replication) of a shard can be changed.

[Replication](https://docs.weaviate.io/deploy/configuration/replication) configurations can be set using the definition, through the `replicationConfig` parameter.

| Parameter | Type | Description | Default | Mutable |
| --- | --- | --- | --- | --- |
| `factor` | Integer | The number of copies (replicas) to maintain for each shard. A factor of `3` means one primary and two replicas. | `1` | No in `v1.25+`, Yes in earlier versions |
| `asyncEnabled` | Boolean | Enable asynchronous replication. Added in `v1.26` | `false` | Yes |
| `deletionStrategy` | String | Strategy for handling deletions in replication. Can be `NoAutomatedResolution`, `DeleteOnConflict` or `TimeBasedResolution`. Added in `v1.27` | `"NoAutomatedResolution"` | Yes |

Example replication configuration - JSON object

An example of a complete `replicationConfig` object:

```codeBlockLines_e6Vv
{
  "class": "Article",
  "vectorizer": "text2vec-openai",
  "replicationConfig": {
    "factor": 3,
    "asyncEnabled": false,
    "deletionStrategy": "NoAutomatedResolution"
  }
}

```

#### Code example - How to configure replication [​](https://docs.weaviate.io/weaviate/config-refs/collections\#code-example---how-to-configure-replication "Direct link to Code example - How to configure replication")

This code example shows how to configure the replication parameters through a client library:

- Python Client v4

```codeBlockLines_e6Vv
from weaviate.classes.config import Configure, ReplicationDeletionStrategy

client.collections.create(
    "Article",
    replication_config=Configure.replication(
        factor=3,
        async_enabled=True,
        deletion_strategy=ReplicationDeletionStrategy.TIME_BASED_RESOLUTION,
    ),
)

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

Further resources

For more code example and configuration guides visit the [How-to: Manage collections](https://docs.weaviate.io/weaviate/manage-collections) section.

* * *

### Sharding [​](https://docs.weaviate.io/weaviate/config-refs/collections\#sharding "Direct link to Sharding")

Sharding is configured via the `shardingConfig` object in the collection definition. These parameters are immutable and cannot be changed after the collection is created.

| Parameter | Type | Description | Default | Mutable |
| --- | --- | --- | --- | --- |
| `desiredCount` | Integer | The desired number of physical shards for the collection. If this value is larger than the number of cluster nodes, some nodes will host multiple shards. | Number of nodes | No |
| `virtualPerPhysical` | Integer | The number of virtual shards per physical shard. Virtual shards aid in reducing data movement during rebalancing. | `128` | No |
| `strategy` | String | The strategy for determining which shard an object belongs to. Only `"hash"` is currently supported. The hash is based on the `key` property. | `"hash"` | No |
| `key` | String | The property used for hashing to determine the target shard. Currently, only the object's internal UUID ( `_id`) can be used. | `"_id"` | No |
| `function` | String | The hashing function used on the `key`. Only `"murmur3"` is supported, which creates a 64-bit hash, making collisions highly unlikely. | `"murmur3"` | No |
| `actualCount` | Integer | **(Read-only)** The actual number of physical shards created. This typically matches `desiredCount` unless an issue occurred during creation. | `1` | No |
| `desiredVirtualCount` | Integer | **(Read-only)** A calculated value representing `desiredCount * virtualPerPhysical`. | `128` | No |
| `actualVirtualCount` | Integer | **(Read-only)** The actual number of virtual shards that were created. | `128` | No |

Example sharding configuration - JSON object

An example of a complete `shardingConfig` object:

```codeBlockLines_e6Vv
  "shardingConfig": {
    "virtualPerPhysical": 128,
    "desiredCount": 1,           // defaults to the amount of Weaviate nodes in the cluster
    "actualCount": 1,
    "desiredVirtualCount": 128,
    "actualVirtualCount": 128,
    "key": "_id",
    "strategy": "hash",
    "function": "murmur3"
  }

```

#### Code example - How to configure sharding [​](https://docs.weaviate.io/weaviate/config-refs/collections\#code-example---how-to-configure-sharding "Direct link to Code example - How to configure sharding")

This code example shows how to configure the sharding parameters through a client library:

- Python Client v4

```codeBlockLines_e6Vv
from weaviate.classes.config import Configure

client.collections.create(
    "Article",
    sharding_config=Configure.sharding(
        virtual_per_physical=128,
        desired_count=1,
        desired_virtual_count=128,
    ),
)

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

Further resources

For more code example and configuration guides visit the [How-to: Manage collections](https://docs.weaviate.io/weaviate/manage-collections) section.

* * *

### Multi-tenancy [​](https://docs.weaviate.io/weaviate/config-refs/collections\#multi-tenancy "Direct link to Multi-tenancy")

Multi-tenancy allows you to isolate data within a single collection, where objects are associated with specific tenants. This is a useful feature for building SaaS applications or any system requiring strict data partitioning.

Why use multi-tenancy?

It provides data isolation at a lower overhead than creating a separate collection for each tenant, making it more scalable when you have a large number of tenants.

To enable multi-tenancy, set the `enabled` key to `true` in the `multiTenancyConfig` object. This parameter is immutable and must be set at creation time.

| Parameter | Type | Description | Default | Mutable |
| --- | --- | --- | --- | --- |
| `enabled` | Boolean | If `true`, enables multi-tenancy for the collection. | `false` | No |
| `autoTenantCreation` | Boolean | If `true`, a new tenant is created if you try to insert an object into a non-existent tenant. Added in `v1.25` | `false` | Yes |
| `autoTenantActivation` | Boolean | If `true`, automatically activate `INACTIVE` or `OFFLOADED` tenants if a search, read, update, or delete operation is performed on them. Added in `v1.25.2` | `false` | Yes |

#### Code example - How to configure multi-tenancy [​](https://docs.weaviate.io/weaviate/config-refs/collections\#code-example---how-to-configure-multi-tenancy "Direct link to Code example - How to configure multi-tenancy")

This code example shows how to configure the multi-tenancy parameters through a client library:

- Python Client v4

```codeBlockLines_e6Vv
from weaviate.classes.config import Configure

multi_collection = client.collections.create(
    name="MultiTenancyCollection",
    # Enable multi-tenancy on the new collection
    multi_tenancy_config=Configure.multi_tenancy(enabled=True)
)

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

Further resources

For more code example and configuration guides visit the [How-to: Manage collections](https://docs.weaviate.io/weaviate/manage-collections) section.

## Mutability [​](https://docs.weaviate.io/weaviate/config-refs/collections\#mutability "Direct link to Mutability")

Some, but not all, parameters are mutable after you create your collection. To modify immutable parameters, export your data, create a new collection, and import your data into it. Use [collection aliases](https://docs.weaviate.io/weaviate/starter-guides/managing-collections#migration-workflow-with-collection-aliases) to perform such a migration with zero downtime.

Mutable parameters

Replication factor change

The replication factor of a collection cannot be updated by updating the collection's definition.

From `v1.32` by using [replica movement](https://docs.weaviate.io/deploy/configuration/replica-movement), the [replication factor](https://docs.weaviate.io/weaviate/config-refs/collections#replication) of a shard can be changed.

- `description`
- `properties description`
- `invertedIndexConfig`
  - `bm25`
    - `b`
    - `k1`
  - `cleanupIntervalSeconds`
  - `stopwords`
    - `additions`
    - `preset`
    - `removals`
- `moduleConfig` (generative & reranker modules only, from `1.26.8` and `v1.27.1`)
- `multiTenancyConfig`
  - `autoTenantCreation` (introduced in `v1.25.0`)
  - `autoTenantActivation` (introduced in `v1.25.2`)
- `replicationConfig`
  - `asyncEnabled` (introduced in `v1.26.0`)
  - `factor` (not mutable in `v1.25` or higher)
  - `deletionStrategy` (introduced in `v1.27.0`)
- `vectorIndexConfig`
  - `dynamicEfFactor`
  - `dynamicEfMin`
  - `dynamicEfMax`
  - `filterStrategy` (introduced in `v1.27.0`, applicable for HNSW)
  - `flatSearchCutoff`
  - `bq`
    - `enabled`
    - `rescoreLimit`
  - `pq`
    - `centroids`
    - `enabled`
    - `segments`
    - `trainingLimit`
    - `encoder`
      - `type`
      - `distribution`
  - `sq`
    - `enabled`
    - `rescoreLimit`
    - `trainingLimit`
  - `skip`
  - `vectorCacheMaxObjects`

After you create a collection, you can [add new properties](https://docs.weaviate.io/weaviate/manage-collections/collection-operations#add-a-property). You cannot modify existing properties after you create the collection. You can also [add new named vectors](https://docs.weaviate.io/weaviate/concepts/data#adding-a-named-vector-after-collection-creation).

## Auto-schema [​](https://docs.weaviate.io/weaviate/config-refs/collections\#auto-schema "Direct link to Auto-schema")

The "Auto-schema" feature generates a collection definition automatically by inferring parameters from data being added. It is enabled by default, and can be disabled (e.g. in `docker-compose.yml`) by setting the environment variable [`AUTOSCHEMA_ENABLED`](https://docs.weaviate.io/deploy/configuration/env-vars#AUTOSCHEMA_ENABLED) to `'false'`.

It will:

- Create a collection if an object is added to a non-existent collection.
- Add any missing property from an object being added.
- Infer array data types, such as `int[]`, `text[]`, `number[]`, `boolean[]`, `date[]` and `object[]`.
- Infer nested properties for `object` and `object[]` data types.
- Throw an error if an object being added contains a property that conflicts with an existing schema type. (e.g. trying to import text into a field that exists in the schema as `int`).

Define the collection manually for production use

Generally speaking, we recommend that you disable auto-schema for production use.

- A manual collection definition will provide more precise control.
- There is a performance penalty associated with inferring the data structure at import time. This may be a costly operation in some cases, such as complex nested properties.

#### Auto-schema data types [​](https://docs.weaviate.io/weaviate/config-refs/collections\#auto-schema-data-types "Direct link to Auto-schema data types")

Additional configurations are available to help the auto-schema infer properties to suit your needs.

- `AUTOSCHEMA_DEFAULT_NUMBER=number` \- create `number` columns for any numerical values (as opposed to `int`, etc).
- `AUTOSCHEMA_DEFAULT_DATE=date` \- create `date` columns for any date-like values.

The following are not allowed:

- Any map type is forbidden, unless it clearly matches one of the two supported types `phoneNumber` or `geoCoordinates`.
- Any array type is forbidden, unless it is clearly a reference-type. In this case, Weaviate needs to resolve the beacon and see what collection the resolved beacon is from, since it needs the collection name to be able to alter the schema.

## Collections count limit [​](https://docs.weaviate.io/weaviate/config-refs/collections\#collections-count-limit "Direct link to Collections count limit")

Added in `v1.30`

To ensure optimal performance, Weaviate **limits the number of collections per node**. Each collection adds overhead in terms of indexing, definition management, and storage. This limit aims to ensure Weaviate remains performant.

- **Default limit**: `1000` collections.
- **Modify the limit**: Use the [`MAXIMUM_ALLOWED_COLLECTIONS_COUNT`](https://docs.weaviate.io/deploy/configuration/env-vars#MAXIMUM_ALLOWED_COLLECTIONS_COUNT) environment variable to adjust the collection count limit.

note

If your instance already exceeds the limit, Weaviate will not allow the creation of any new collections. Existing collections will not be deleted.

tip

**Instead of raising the collections count limit, consider rethinking your architecture**.
For more details, see [Starter Guides: Scaling limits with collections](https://docs.weaviate.io/weaviate/starter-guides/managing-collections/collections-scaling-limits).

## Collection aliases [​](https://docs.weaviate.io/weaviate/config-refs/collections\#collection-aliases "Direct link to Collection aliases")

Technical preview

Collection aliases were added in **`v1.32`** as a **technical preview**.

This means that the feature is still under development and may change in future releases, including potential breaking changes.
**We do not recommend using this feature in production environments at this time.**

Collection aliases are alternative names for Weaviate collections that allow you to reference a collection by an alternative name.

Weaviate automatically routes alias requests to the target collection. This allows you to use aliases wherever collection names are required. This includes [collection management](https://docs.weaviate.io/weaviate/manage-collections), [queries](https://docs.weaviate.io/weaviate/search), and all other operations requiring a specific collection name with the **exception** of deleting collections. To delete a collection you need to use its name. Deleting a collection does not automatically delete aliases pointing to it.

Alias names must be unique (can't match existing collections or other aliases) and multiple aliases can point to the same collection. You can set up collection aliases [programmatically through client libraries](https://docs.weaviate.io/weaviate/manage-collections/collection-aliases) or by using the [REST endpoints](https://docs.weaviate.io/weaviate/api/rest#tag/aliases).

In order to manage collection aliases, you need to posses the right [`Collection aliases`](https://docs.weaviate.io/weaviate/configuration/rbac#available-permissions) permissions. To manage the underlying collection the alias references, you also need the [`Collections`](https://docs.weaviate.io/weaviate/configuration/rbac#available-permissions) permissions for that specific collection.

## Further resources [​](https://docs.weaviate.io/weaviate/config-refs/collections\#further-resources "Direct link to Further resources")

- [Starter guides: Collection definition](https://docs.weaviate.io/weaviate/starter-guides/managing-collections)
- [How to: Manage collections](https://docs.weaviate.io/weaviate/manage-collections)
- [Concepts: Data structure](https://docs.weaviate.io/weaviate/concepts/data)
- [REST API: Collection definition (schema)](https://docs.weaviate.io/weaviate/api/rest#tag/schema)
