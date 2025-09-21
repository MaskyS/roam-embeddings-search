[Skip to main content](https://docs.weaviate.io/weaviate/api/graphql/filters#__docusaurus_skipToContent_fallback)

[Product update: The Weaviate Query Agent has been released!](https://docs.weaviate.io/agents/query)

**Go to documentation:**

⌘U

✕

**Weaviate Database**

Develop AI applications using Weaviate's APIs and tools

**Deploy**

Deploy, configure, and maintain Weaviate Database

**Weaviate Agents**

Build and deploy intelligent agents with Weaviate

**Weaviate Cloud**

Manage and scale Weaviate in the cloud

#### Additional resources

Academy

Integrations

Contributor guide

Events & Workshops

#### Need help?

![Weaviate Logo](https://docs.weaviate.io/img/site/weaviate-logo-w.png)Ask AI Assistant⌘K

Community Forum

On this page

Conditional filters may be added to queries such as [`Object-level`](https://docs.weaviate.io/weaviate/api/graphql/get) and [`Aggregate`](https://docs.weaviate.io/weaviate/api/graphql/aggregate) queries, as well as [batch deletion](https://docs.weaviate.io/weaviate/manage-objects/delete#delete-multiple-objects). The operator used for filtering is also called a `where` filter.

A filter may consist of one or more conditions, which are combined using the `And` or `Or` operators. Each condition consists of a property path, an operator, and a value.

## Single operand (condition) [​](https://docs.weaviate.io/weaviate/api/graphql/filters\#single-operand-condition "Direct link to Single operand (condition)")

Each set of algebraic conditions is called an "operand". For each operand, the required properties are:

- The operator type,
- The property path, and
- The value as well as the value type.

For example, this filter will only allow objects from the class `Article` with a `wordCount` that is `GreaterThan` than `1000`.

- Python Client v4
- Python Client v3
- JS/TS Client v2
- Go
- Java
- Curl
- GraphQL

```codeBlockLines_e6Vv
import weaviate
from weaviate.classes.query import Filter, GeoCoordinate, MetadataQuery, QueryReference  # Import classes as needed
import os

client = weaviate.connect_to_local()

collection = client.collections.use("Article")
response = collection.query.fetch_objects(
    filters=Filter.by_property("wordCount").greater_than(1000),
    limit=5
)

for o in response.objects:
    print(o.properties)  # Inspect returned objects
client.close()

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

Expected response

```codeBlockLines_e6Vv
{
  "data": {
    "Get": {
      "Article": [\
        {\
          "title": "Anywhere but Washington: an eye-opening journey in a deeply divided nation"\
        },\
        {\
          "title": "The world is still struggling to implement meaningful climate policy"\
        },\
        ...\
      ]
    }
  }
}

```

## Filter structure [​](https://docs.weaviate.io/weaviate/api/graphql/filters\#filter-structure "Direct link to Filter structure")

The `where` filter is an [algebraic object](https://en.wikipedia.org/wiki/Algebraic_structure), which takes the following arguments:

- `Operator` (which takes one of the following values)
  - `And`
  - `Or`
  - `Equal`
  - `NotEqual`
  - `GreaterThan`
  - `GreaterThanEqual`
  - `LessThan`
  - `LessThanEqual`
  - `Like`
  - `WithinGeoRange`
  - `IsNull`
  - `ContainsAny` (\*Only for array and text properties)
  - `ContainsAll` (\*Only for array and text properties)
- `Path`: Is a list of strings in [XPath](https://en.wikipedia.org/wiki/XPath#Abbreviated_syntax) style, indicating the property name of the collection.
  - If the property is a cross-reference, the path should be followed as a list of strings. For a `inPublication` reference property that refers to `Publication` collection, the path selector for `name` will be `["inPublication", "Publication", "name"]`.
- `valueType`
  - `valueInt`: For `int` data type.
  - `valueBoolean`: For `boolean` data type.
  - `valueString`: For `string` data type (note: `string` has been deprecated).
  - `valueText`: For `text`, `uuid`, `geoCoordinates`, `phoneNumber` data types.
  - `valueNumber`: For `number` data type.
  - `valueDate`: For `date` (ISO 8601 timestamp, formatted as [RFC3339](https://datatracker.ietf.org/doc/rfc3339/)) data type.

If the operator is `And` or `Or`, the operands are a list of `where` filters.

Example filter structure (GraphQL)

```codeBlockLines_e6Vv
{
  Get {
    <Class>(where: {
        operator: <operator>,
        operands: [{\
          path: [path],\
          operator: <operator>\
          <valueType>: <value>\
        }, {\
          path: [<matchPath>],\
          operator: <operator>,\
          <valueType>: <value>\
        }]
      }) {
      <propertyWithBeacon> {
        <property>
        ... on <ClassOfWhereBeaconGoesTo> {
          <propertyOfClass>
        }
      }
    }
  }
}

```

Example response

```codeBlockLines_e6Vv
{
  "data": {
    "Get": {
      "Article": [\
        {\
          "title": "Opinion | John Lennon Told Them ‘Girls Don't Play Guitar.' He Was So Wrong."\
        }\
      ]
    }
  },
  "errors": null
}

```

`Not` operator

Weaviate doesn't have an operator to invert a filter (e.g. `Not Like ...` ). If you would like us to add one, please [upvote the issue](https://github.com/weaviate/weaviate/issues/3683).

### Filter behaviors [​](https://docs.weaviate.io/weaviate/api/graphql/filters\#filter-behaviors "Direct link to Filter behaviors")

#### Multi-word queries in `Equal` filters [​](https://docs.weaviate.io/weaviate/api/graphql/filters\#multi-word-queries-in-equal-filters "Direct link to multi-word-queries-in-equal-filters")

The behavior for the `Equal` operator on multi-word textual properties in `where` filters depends on the `tokenization` of the property.

See the [Schema property tokenization section](https://docs.weaviate.io/weaviate/config-refs/collections#tokenization) for the difference between the available tokenization types.

#### Stopwords in `text` filters [​](https://docs.weaviate.io/weaviate/api/graphql/filters\#stopwords-in-text-filters "Direct link to stopwords-in-text-filters")

Starting with `v1.12.0` you can configure your own [stopword lists for the inverted index](https://docs.weaviate.io/weaviate/config-refs/indexing/inverted-index#stopwords).

## Multiple operands [​](https://docs.weaviate.io/weaviate/api/graphql/filters\#multiple-operands "Direct link to Multiple operands")

You can set multiple operands or [nest conditions](https://docs.weaviate.io/weaviate/search/filters#nested-filters).

tip

You can filter datetimes similarly to numbers, with the `valueDate` given as `string` in [RFC3339](https://datatracker.ietf.org/doc/rfc3339/) format.

- Python Client v4
- Python Client v3
- JS/TS Client v2
- Go
- Java
- Curl
- GraphQL

```codeBlockLines_e6Vv
import weaviate
from weaviate.classes.query import Filter, GeoCoordinate, MetadataQuery, QueryReference  # Import classes as needed
import os

client = weaviate.connect_to_local()

collection = client.collections.use("Article")
response = collection.query.fetch_objects(
    filters=(
        Filter.by_property("wordCount").greater_than(1000)
        & Filter.by_property("title").like("*economy*")
    ),
    limit=5,
)

for o in response.objects:
    print(o.properties)  # Inspect returned objects
client.close()

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

Expected response

```codeBlockLines_e6Vv
{
  "data": {
    "Get": {
      "Article": [\
        {\
          "title": "China\u2019s long-distance lorry drivers are unsung heroes of its economy"\
        },\
        {\
          "title": "\u2018It\u2019s as if there\u2019s no Covid\u2019: Nepal defies pandemic amid a broken economy"\
        },\
        {\
          "title": "A tax hike threatens the health of Japan\u2019s economy"\
        }\
      ]
    }
  }
}

```

## Filter operators [​](https://docs.weaviate.io/weaviate/api/graphql/filters\#filter-operators "Direct link to Filter operators")

### `Like` [​](https://docs.weaviate.io/weaviate/api/graphql/filters\#like "Direct link to like")

The `Like` operator filters `text` data based on partial matches. It can be used with the following wildcard characters:

- `?` -\> exactly one unknown character
  - `car?` matches `cart`, `care`, but not `car`
- `*` -\> zero, one or more unknown characters
  - `car*` matches `car`, `care`, `carpet`, etc
  - `*car*` matches `car`, `healthcare`, etc.

- Python Client v4
- Python Client v3
- JS/TS Client v2
- Go
- Java
- Curl
- GraphQL

```codeBlockLines_e6Vv
import weaviate
from weaviate.classes.query import Filter, GeoCoordinate, MetadataQuery, QueryReference  # Import classes as needed
import os

client = weaviate.connect_to_local()

collection = client.collections.use("Article")
response = collection.query.fetch_objects(
    filters=Filter.by_property("title").like("New *"),
    limit=5
)

for o in response.objects:
    print(o.properties)  # Inspect returned objects
client.close()

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

Expected response

```codeBlockLines_e6Vv
{
  "data": {
    "Get": {
      "Publication": [\
        {\
          "name": "The New York Times Company"\
        },\
        {\
          "name": "International New York Times"\
        },\
        {\
          "name": "New York Times"\
        },\
        {\
          "name": "New Yorker"\
        }\
      ]
    }
  }
}

```

#### Performance of `Like` [​](https://docs.weaviate.io/weaviate/api/graphql/filters\#performance-of-like "Direct link to performance-of-like")

Each `Like` filter iterates over the entire inverted index for that property. The search time will go up linearly with the dataset size, and may become slow for large datasets.

#### Wildcard literal matches with `Like` [​](https://docs.weaviate.io/weaviate/api/graphql/filters\#wildcard-literal-matches-with-like "Direct link to wildcard-literal-matches-with-like")

Currently, the `Like` filter is not able to match wildcard characters ( `?` and `*`) as literal characters. For example, it is currently not possible to only match the string `car*` and not `car`, `care` or `carpet`. This is a known limitation and may be addressed in future versions of Weaviate.

### `ContainsAny` / `ContainsAll` [​](https://docs.weaviate.io/weaviate/api/graphql/filters\#containsany--containsall "Direct link to containsany--containsall")

The `ContainsAny` and `ContainsAll` operators filter objects using values of an array as criteria.

Both operators expect an array of values and return objects that match based on the input values.

`ContainsAny` and `ContainsAll` notes:

- The `ContainsAny` and `ContainsAll` operators treat texts as an array. The text is split into an array of tokens based on the chosen tokenization scheme, and the search is performed on that array.
- When using `ContainsAny` or `ContainsAll` with the REST api for [batch deletion](https://docs.weaviate.io/weaviate/manage-objects/delete#delete-multiple-objects), the text array must be specified with the `valueTextArray` argument. This is different from the usage in search, where the `valueText` argument that can be used.

#### `ContainsAny` [​](https://docs.weaviate.io/weaviate/api/graphql/filters\#containsany "Direct link to containsany")

`ContainsAny` returns objects where at least one of the values from the input array is present.

Consider a dataset of `Person`, where each object represents a person with a `languages_spoken` property with a `text` datatype.

A `ContainsAny` query on a path of `["languages_spoken"]` with a value of `["Chinese", "French", "English"]` will return objects where at least one of those languages is present in the `languages_spoken` array.

#### `ContainsAll` [​](https://docs.weaviate.io/weaviate/api/graphql/filters\#containsall "Direct link to containsall")

`ContainsAll` returns objects where all the values from the input array are present.

Using the same dataset of `Person` objects as above, a `ContainsAll` query on a path of `["languages_spoken"]` with a value of `["Chinese", "French", "English"]` will return objects where all three of those languages are present in the `languages_spoken` array.

## Filter performance [​](https://docs.weaviate.io/weaviate/api/graphql/filters\#filter-performance "Direct link to Filter performance")

In some edge cases, filter performance may be slow due to a mismatch between the filter architecture and the data structure. For example, if a property has very large cardinality (i.e. a large number of unique values), its range-based filter performance may be slow.

If you are experiencing slow filter performance, you have several options:

- Further restrict your query by adding more conditions to the `where` operator
- Add a `limit` parameter to your query
- Configure `indexRangeFilters` for properties that require range-based filtering. You can [set inverted index parameters](https://docs.weaviate.io/weaviate/manage-collections/collection-operations#set-inverted-index-parameters) when creating your collection. Learn more about [configuring the inverted index](https://docs.weaviate.io/weaviate/concepts/indexing/inverted-index#configure-inverted-indexes) to optimize filter performance for your specific use case.

## Special cases [​](https://docs.weaviate.io/weaviate/api/graphql/filters\#special-cases "Direct link to Special cases")

### By id [​](https://docs.weaviate.io/weaviate/api/graphql/filters\#by-id "Direct link to By id")

You can filter object by their unique id or uuid, where you give the `id` as `valueText`.

- Python Client v4
- Python Client v3
- JS/TS Client v2
- Go
- Java
- Curl
- GraphQL

```codeBlockLines_e6Vv
import weaviate
from weaviate.classes.query import Filter, GeoCoordinate, MetadataQuery, QueryReference  # Import classes as needed
import os

client = weaviate.connect_to_local()

collection = client.collections.use("Article")
response = collection.query.fetch_objects(
    filters=Filter.by_id().equal("00037775-1432-35e5-bc59-443baaef7d80")
)

for o in response.objects:
    print(o.properties)  # Inspect returned objects
client.close()

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

Expected response

```codeBlockLines_e6Vv
{
  "data": {
    "Get": {
      "Article": [\
        {\
          "title": "Backs on the rack - Vast sums are wasted on treatments for back pain that make it worse"\
        }\
      ]
    }
  }
}

```

### By timestamps [​](https://docs.weaviate.io/weaviate/api/graphql/filters\#by-timestamps "Direct link to By timestamps")

Filtering can be performed with internal timestamps as well, such as `creationTimeUnix` and `lastUpdateTimeUnix`. These values can be represented either as Unix epoch milliseconds, or as [RFC3339](https://datatracker.ietf.org/doc/rfc3339/) formatted datetimes. Note that epoch milliseconds should be passed in as a `valueText`, and an RFC3339 datetime should be a `valueDate`.

info

Filtering by timestamp requires the target class to be configured to index timestamps. See [here](https://docs.weaviate.io/weaviate/config-refs/indexing/inverted-index#indextimestamps) for details.

- Python Client v4
- Python Client v3
- JS/TS Client v2
- Go
- Java
- Curl
- GraphQL

```codeBlockLines_e6Vv
import weaviate
from weaviate.classes.query import Filter, GeoCoordinate, MetadataQuery, QueryReference  # Import classes as needed
import os
from datetime import datetime

client = weaviate.connect_to_local()

collection = client.collections.use("Article")
year2k = datetime.strptime("2000-01-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ")

response = collection.query.fetch_objects(
    filters=Filter.by_creation_time().greater_or_equal(year2k),
    return_metadata=MetadataQuery(creation_time=True),
    limit=2
)

for o in response.objects:
    print(o.properties)  # Inspect returned objects
    print(o.metadata)  # Inspect returned creation time
client.close()

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

Expected response

```codeBlockLines_e6Vv
{
  "data": {
    "Get": {
      "Article": [\
        {\
          "title": "Army builds new body armor 14-times stronger in the face of enemy fire"\
        },\
        ...\
      ]
    }
  }
}

```

### By property length [​](https://docs.weaviate.io/weaviate/api/graphql/filters\#by-property-length "Direct link to By property length")

Filtering can be performed with the length of properties.

The length of properties is calculated differently depending on the type:

- array types: the number of entries in the array is used, where null (property not present) and empty arrays both have the length 0.
- strings and texts: the number of characters (unicode characters such as 世 count as one character).
- numbers, booleans, geo-coordinates, phone-numbers and data-blobs are not supported.

```codeBlockLines_e6Vv
{
  Get {
    <Class>(
      where: {
        operator: <Operator>,
        valueInt: <value>,
        path: ["len(<property>)"]
      }
    )
  }
}

```

Supported operators are `(not) equal` and `greater/less than (equal)` and values need to be 0 or larger.

Note that the `path` value is a string, where the property name is wrapped in `len()`. For example, to filter for objects based on the length of the `title` property, you would use `path: ["len(title)"]`.

To filter for `Article` class objects with `title` length greater than 10, you would use:

```codeBlockLines_e6Vv
{
  Get {
    Article(
      where: {
        operator: GreaterThan,
        valueInt: 10,
        path: ["len(title)"]
      }
    )
  }
}

```

note

Filtering by property length requires the target class to be [configured to index the length](https://docs.weaviate.io/weaviate/config-refs/indexing/inverted-index#indexpropertylength).

### By cross-references [​](https://docs.weaviate.io/weaviate/api/graphql/filters\#by-cross-references "Direct link to By cross-references")

You can also search for the value of the property of a cross-references, also called beacons.

For example, these filters select based on the class Article but who have `inPublication` set to New Yorker.

- Python Client v4
- Python Client v3
- JS/TS Client v2
- Go
- Java
- Curl
- GraphQL

```codeBlockLines_e6Vv
import weaviate
from weaviate.classes.query import Filter, GeoCoordinate, MetadataQuery, QueryReference  # Import classes as needed
import os

client = weaviate.connect_to_local()

collection = client.collections.use("Article")

response = collection.query.fetch_objects(
    filters=Filter.by_ref(link_on="inPublication").by_property("name").like("*New*"),
    return_references=QueryReference(link_on="inPublication", return_properties=["name"]),
    limit=2
)

for o in response.objects:
    print(o.properties)  # Inspect returned objects
    for ref_o in o.references["inPublication"].objects:
        print(ref_o.properties)
client.close()

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

Expected response

```codeBlockLines_e6Vv
{
  "data": {
    "Get": {
      "Article": [\
        {\
          "inPublication": [\
            {\
              "name": "New Yorker"\
            }\
          ],\
          "title": "The Hidden Costs of Automated Thinking"\
        },\
        {\
          "inPublication": [\
            {\
              "name": "New Yorker"\
            }\
          ],\
          "title": "The Real Deal Behind the U.S.\u2013Iran Prisoner Swap"\
        },\
        ...\
      ]
    }
  }
}

```

### By count of reference [​](https://docs.weaviate.io/weaviate/api/graphql/filters\#by-count-of-reference "Direct link to By count of reference")

Above example shows how filter by reference can solve straightforward questions like "Find all articles that are published by New Yorker". But questions like "Find all articles that are written by authors that wrote at least two articles", cannot be answered by the above query structure. It is however possible to filter by reference count. To do so, simply provide one of the existing compare operators ( `Equal`, `LessThan`, `LessThanEqual`, `GreaterThan`, `GreaterThanEqual`) and use it directly on the reference element. For example:

- Python Client v4
- Python Client v3
- JS/TS Client v2
- Java
- Go
- Curl
- GraphQL

```codeBlockLines_e6Vv
import weaviate
from weaviate.classes.query import Filter, GeoCoordinate, MetadataQuery, QueryReference  # Import classes as needed
import os

client = weaviate.connect_to_local()

response = collection.query.fetch_objects(
    filters=Filter.by_ref_count(link_on="inPublication").greater_than(2),
    return_references=QueryReference(link_on="inPublication", return_properties=["name"]),
    limit=2
)

for o in response.objects:
    print(o.properties)  # Inspect returned objects
    for ref_o in o.references["inPublication"].objects:
        print(ref_o.properties)
client.close()

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

Expected response

```codeBlockLines_e6Vv
{
  "data": {
    "Get": {
      "Author": [\
        {\
          "name": "Agam Shah",\
          "writesFor": [\
            {\
              "name": "Wall Street Journal"\
            },\
            {\
              "name": "Wall Street Journal"\
            }\
          ]\
        },\
        {\
          "name": "Costas Paris",\
          "writesFor": [\
            {\
              "name": "Wall Street Journal"\
            },\
            {\
              "name": "Wall Street Journal"\
            }\
          ]\
        },\
        ...\
      ]
    }
  }
}

```

### By geo coordinates [​](https://docs.weaviate.io/weaviate/api/graphql/filters\#by-geo-coordinates "Direct link to By geo coordinates")

A special case of the `Where` filter is with geoCoordinates. This filter is only supported by the `Get{}` function. If you've set the `geoCoordinates` property type, you can search in an area based on kilometers.

For example, this curious returns all in a radius of 2KM around a specific geo-location:

- Python Client v4
- Python Client v3
- JS/TS Client v2
- Go
- Java
- Curl
- GraphQL

```codeBlockLines_e6Vv
import weaviate
from weaviate.classes.query import Filter, GeoCoordinate, MetadataQuery, QueryReference  # Import classes as needed
import os

client = weaviate.connect_to_local()

response = publications.query.fetch_objects(
    filters=(
        Filter
        .by_property("headquartersGeoLocation")
        .within_geo_range(
            coordinate=GeoCoordinate(
                latitude=33.7579,
                longitude=84.3948
            ),
            distance=10000  # In meters
        )
    ),
)

for o in response.objects:
    print(o.properties)  # Inspect returned objects
client.close()

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

Expected response

```codeBlockLines_e6Vv
{
  "data": {
    "Get": {
      "Publication": [\
        {\
          "headquartersGeoLocation": {\
            "latitude": 51.512737,\
            "longitude": -0.0962234\
          },\
          "name": "Financial Times"\
        },\
        {\
          "headquartersGeoLocation": {\
            "latitude": 51.512737,\
            "longitude": -0.0962234\
          },\
          "name": "International New York Times"\
        }\
      ]
    }
  }
}

```

Note that `geoCoordinates` uses a vector index under the hood.

Limitations

Currently, geo-coordinate filtering is limited to the nearest 800 results from the source location, which will be further reduced by any other filter conditions and search parameters.

If you plan on a densely populated dataset, consider using another strategy such as geo-hashing into a `text` datatype, and filtering further, such as with a `ContainsAny` filter.

### By null state [​](https://docs.weaviate.io/weaviate/api/graphql/filters\#by-null-state "Direct link to By null state")

Using the `IsNull` operator allows you to do filter for objects where given properties are `null` or `not null`. Note that zero-length arrays and empty strings are equivalent to a null value.

```codeBlockLines_e6Vv
{
  Get {
    <Class>(where: {
        operator: IsNull,
        valueBoolean: <true/false>
        path: [<property>]
  }
}

```

note

Filtering by null-state requires the target class to be configured to index this. See [here](https://docs.weaviate.io/weaviate/config-refs/indexing/inverted-index#indexnullstate) for details.

## Related pages [​](https://docs.weaviate.io/weaviate/api/graphql/filters\#related-pages "Direct link to Related pages")

- [How-to search: Filters](https://docs.weaviate.io/weaviate/search/filters)

## Questions and feedback [​](https://docs.weaviate.io/weaviate/api/graphql/filters\#questions-and-feedback "Direct link to Questions and feedback")

If you have any questions or feedback, let us know in the [user forum](https://forum.weaviate.io/).

[Technical questions\\
\\
If you have questions feel free to post on ourCommunity forum.](https://forum.weaviate.io/new-topic?title=%5BQuestion%5D%20YOUR%20TOPIC&body=Details%20here&category=support&tags=technical) [Documentation feedback\\
\\
Leave feedback by opening a GitHub issue.](https://github.com/weaviate/docs/issues)

- [Single operand (condition)](https://docs.weaviate.io/weaviate/api/graphql/filters#single-operand-condition)
- [Filter structure](https://docs.weaviate.io/weaviate/api/graphql/filters#filter-structure)
  - [Filter behaviors](https://docs.weaviate.io/weaviate/api/graphql/filters#filter-behaviors)
- [Multiple operands](https://docs.weaviate.io/weaviate/api/graphql/filters#multiple-operands)
- [Filter operators](https://docs.weaviate.io/weaviate/api/graphql/filters#filter-operators)
  - [`Like`](https://docs.weaviate.io/weaviate/api/graphql/filters#like)
  - [`ContainsAny` / `ContainsAll`](https://docs.weaviate.io/weaviate/api/graphql/filters#containsany--containsall)
- [Filter performance](https://docs.weaviate.io/weaviate/api/graphql/filters#filter-performance)
- [Special cases](https://docs.weaviate.io/weaviate/api/graphql/filters#special-cases)
  - [By id](https://docs.weaviate.io/weaviate/api/graphql/filters#by-id)
  - [By timestamps](https://docs.weaviate.io/weaviate/api/graphql/filters#by-timestamps)
  - [By property length](https://docs.weaviate.io/weaviate/api/graphql/filters#by-property-length)
  - [By cross-references](https://docs.weaviate.io/weaviate/api/graphql/filters#by-cross-references)
  - [By count of reference](https://docs.weaviate.io/weaviate/api/graphql/filters#by-count-of-reference)
  - [By geo coordinates](https://docs.weaviate.io/weaviate/api/graphql/filters#by-geo-coordinates)
  - [By null state](https://docs.weaviate.io/weaviate/api/graphql/filters#by-null-state)
- [Related pages](https://docs.weaviate.io/weaviate/api/graphql/filters#related-pages)
- [Questions and feedback](https://docs.weaviate.io/weaviate/api/graphql/filters#questions-and-feedback)

## Weaviate documentation structure

✕

The Weaviate documentation is divided into the following four sections: [core database](https://docs.weaviate.io/weaviate), [deployment](https://docs.weaviate.io/deploy), [Weaviate Cloud](https://docs.weaviate.io/cloud) and [Weaviate Agents](https://docs.weaviate.io/agents) docs.

Documentation structure - Guideflow

Weaviate Documentation

![](https://storage.googleapis.com/guideflow-images/f09e05484dfbc0c5523d38d3ee5ec1873c25ca52c7d671b414c3d74f134654aa590c758a5c3ee592d6d4757eb7a303b3..png)

Open the **navigation menu**

1/4

Back

Next

reCAPTCHA

Recaptcha requires verification.

[Privacy](https://www.google.com/intl/en/policies/privacy/) \- [Terms](https://www.google.com/intl/en/policies/terms/)

protected by **reCAPTCHA**

[Privacy](https://www.google.com/intl/en/policies/privacy/) \- [Terms](https://www.google.com/intl/en/policies/terms/)
