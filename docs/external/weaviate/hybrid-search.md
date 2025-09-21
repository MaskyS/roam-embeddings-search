`Hybrid` search combines the results of a vector search and a keyword (BM25F) search by fusing the two result sets.

The [fusion method](https://docs.weaviate.io/weaviate/search/hybrid#change-the-fusion-method) and the [relative weights](https://docs.weaviate.io/weaviate/search/hybrid#balance-keyword-and-vector-search) are configurable.

## Basic hybrid search [​](https://docs.weaviate.io/weaviate/search/hybrid\#basic-hybrid-search "Direct link to Basic hybrid search")

Combine the results of a vector search and a keyword search. The search uses a single query string.

- Python Client v4
- Python Client v3
- JS/TS Client v3
- JS/TS Client v2
- Go
- GraphQL

```codeBlockLines_e6Vv
jeopardy = client.collections.use("JeopardyQuestion")
response = jeopardy.query.hybrid(query="food", limit=3)

for o in response.objects:
    print(o.properties)

```

[![python docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

Example response

The output is like this:

```codeBlockLines_e6Vv
{
  "data": {
    "Get": {
      "JeopardyQuestion": [\
        {\
          "answer": "a closer grocer",\
          "question": "A nearer food merchant"\
        },\
        {\
          "answer": "Famine",\
          "question": "From the Latin for \"hunger\", it's a period when food is extremely scarce"\
        },\
        {\
          "answer": "Tofu",\
          "question": "A popular health food, this soybean curd is used to make a variety of dishes & an ice cream substitute"\
        }\
      ]
    }
  }
}

```

## Named vectors [​](https://docs.weaviate.io/weaviate/search/hybrid\#named-vectors "Direct link to Named vectors")

Added in `v1.24`

A hybrid search on a collection that has [named vectors](https://docs.weaviate.io/weaviate/config-refs/collections#named-vectors) must specify a `target` vector. Weaviate uses the query vector to search the target vector space.

- Python Client v4
- Python Client v3
- JS/TS Client v3
- JS/TS Client v2
- GraphQL

```codeBlockLines_e6Vv
reviews = client.collections.use("WineReviewNV")
response = reviews.query.hybrid(
    query="A French Riesling",
    target_vector="title_country",
    limit=3
)

for o in response.objects:
    print(o.properties)

```

[![python docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

Example response

The output is like this:

```codeBlockLines_e6Vv

```

## Explain the search results [​](https://docs.weaviate.io/weaviate/search/hybrid\#explain-the-search-results "Direct link to Explain the search results")

To see the object rankings, set the `explain score` field in your query. The search rankings are part of the object metadata. Weaviate uses the score to order the search results.

- Python Client v4
- Python Client v3
- JS/TS Client v3
- JS/TS Client v2
- Go
- GraphQL

```codeBlockLines_e6Vv
from weaviate.classes.query import MetadataQuery

jeopardy = client.collections.use("JeopardyQuestion")
response = jeopardy.query.hybrid(
    query="food",
    alpha=0.5,
    return_metadata=MetadataQuery(score=True, explain_score=True),
    limit=3,
)

for o in response.objects:
    print(o.properties)
    print(o.metadata.score, o.metadata.explain_score)

```

[![python docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

Example response

The output is like this:

```codeBlockLines_e6Vv
{
  "data": {
    "Get": {
      "JeopardyQuestion": [\
        {\
          "_additional": {\
            "explainScore": "(bm25)\n(hybrid) Document df958a90-c3ad-5fde-9122-cd777c22da6c contributed 0.003968253968253968 to the score\n(hybrid) Document df958a90-c3ad-5fde-9122-cd777c22da6c contributed 0.012295081967213115 to the score",\
            "score": "0.016263336"\
          },\
          "answer": "a closer grocer",\
          "question": "A nearer food merchant"\
        },\
        {\
          "_additional": {\
            "explainScore": "(vector) [0.0223698 -0.02752683 -0.0061537363 0.0023812135 -0.00036100898 -0.0078375945 -0.018505432 -0.037500713 -0.0042215516 -0.012620432]...  \n(hybrid) Document ec776112-e651-519d-afd1-b48e6237bbcb contributed 0.012096774193548387 to the score",\
            "score": "0.012096774"\
          },\
          "answer": "Famine",\
          "question": "From the Latin for \"hunger\", it's a period when food is extremely scarce"\
        },\
        {\
          "_additional": {\
            "explainScore": "(vector) [0.0223698 -0.02752683 -0.0061537363 0.0023812135 -0.00036100898 -0.0078375945 -0.018505432 -0.037500713 -0.0042215516 -0.012620432]...  \n(hybrid) Document 98807640-cd16-507d-86a1-801902d784de contributed 0.011904761904761904 to the score",\
            "score": "0.011904762"\
          },\
          "answer": "Tofu",\
          "question": "A popular health food, this soybean curd is used to make a variety of dishes & an ice cream substitute"\
        }\
      ]
    }
  }
}

```

## Balance keyword and vector search [​](https://docs.weaviate.io/weaviate/search/hybrid\#balance-keyword-and-vector-search "Direct link to Balance keyword and vector search")

Hybrid search results can favor the keyword component or the vector component. To change the relative weights of the keyword and vector components, set the `alpha` value in your query.

- An `alpha` of `1` is a pure vector search.
- An `alpha` of `0` is a pure keyword search.

- Python Client v4
- Python Client v3
- JS/TS Client v3
- JS/TS Client v2
- Go
- GraphQL

```codeBlockLines_e6Vv
jeopardy = client.collections.use("JeopardyQuestion")
response = jeopardy.query.hybrid(
    query="food",
    alpha=0.25,
    limit=3,
)

for o in response.objects:
    print(o.properties)

```

[![python docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

Example response

The output is like this:

```codeBlockLines_e6Vv
{
  "data": {
    "Get": {
      "JeopardyQuestion": [\
        {\
          "answer": "a closer grocer",\
          "question": "A nearer food merchant"\
        },\
        {\
          "answer": "food stores (supermarkets)",\
          "question": "This type of retail store sells more shampoo & makeup than any other"\
        },\
        {\
          "answer": "cake",\
          "question": "Devil's food & angel food are types of this dessert"\
        }\
      ]
    }
  }
}

```

## Change the fusion method [​](https://docs.weaviate.io/weaviate/search/hybrid\#change-the-fusion-method "Direct link to Change the fusion method")

`Relative Score Fusion` is the default fusion method starting in `v1.24`.

- To use the keyword and vector search relative scores instead of the search rankings, use `Relative Score Fusion`.
- To use [`autocut`](https://docs.weaviate.io/weaviate/api/graphql/additional-operators#autocut) with the `hybrid` operator, use `Relative Score Fusion`.

- Python Client v4
- Python Client v3
- JS/TS Client v3
- JS/TS Client v2
- Go
- GraphQL

```codeBlockLines_e6Vv
from weaviate.classes.query import HybridFusion

jeopardy = client.collections.use("JeopardyQuestion")
response = jeopardy.query.hybrid(
    query="food",
    fusion_type=HybridFusion.RELATIVE_SCORE,
    limit=3,
)

for o in response.objects:
    print(o.properties)

```

[![python docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

Example response

The output is like this:

```codeBlockLines_e6Vv
{
  "data": {
    "Get": {
      "JeopardyQuestion": [\
        {\
          "answer": "a closer grocer",\
          "question": "A nearer food merchant"\
        },\
        {\
          "answer": "food stores (supermarkets)",\
          "question": "This type of retail store sells more shampoo & makeup than any other"\
        },\
        {\
          "answer": "cake",\
          "question": "Devil's food & angel food are types of this dessert"\
        }\
      ]
    }
  }
}

```

Additional information

For a discussion of fusion methods, see [this blog post](https://weaviate.io/blog/hybrid-search-fusion-algorithms) and [this reference page](https://docs.weaviate.io/weaviate/api/graphql/search-operators#variables-2)

## Keyword search operators [​](https://docs.weaviate.io/weaviate/search/hybrid\#keyword-search-operators "Direct link to Keyword search operators")

Added in `v1.31`

Keyword (BM25) search operators define the minimum number of query [tokens](https://docs.weaviate.io/weaviate/search/hybrid#tokenization) that must be present in the object to be returned. The options are `and`, or `or` (default).

### `or` [​](https://docs.weaviate.io/weaviate/search/hybrid\#or "Direct link to or")

With the `or` operator, the search returns objects that contain at least `minimumOrTokensMatch` of the tokens in the search string.

- Python Client v4
- GraphQL

```codeBlockLines_e6Vv
from weaviate.classes.query import BM25Operator

jeopardy = client.collections.use("JeopardyQuestion")
response = jeopardy.query.hybrid(
    query="Australian mammal cute",
    bm25_operator=BM25Operator.or_(minimum_match=2),
    limit=3,
)

for o in response.objects:
    print(o.properties)

```

[![python docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

### `and` [​](https://docs.weaviate.io/weaviate/search/hybrid\#and "Direct link to and")

With the `and` operator, the search returns objects that contain all tokens in the search string.

- Python Client v4
- GraphQL

```codeBlockLines_e6Vv
from weaviate.classes.query import BM25Operator

jeopardy = client.collections.use("JeopardyQuestion")
response = jeopardy.query.hybrid(
    query="Australian mammal cute",
    bm25_operator=BM25Operator.and_(),  # Each result must include all tokens (e.g. "australian", "mammal", "cute")
    limit=3,
)

for o in response.objects:
    print(o.properties)

```

[![python docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

## Specify keyword search properties [​](https://docs.weaviate.io/weaviate/search/hybrid\#specify-keyword-search-properties "Direct link to Specify keyword search properties")

Added in `v1.19.0`

The keyword search portion of hybrid search can be directed to only search a subset of object properties. This does not affect the vector search portion.

- Python Client v4
- Python Client v3
- JS/TS Client v3
- JS/TS Client v2
- Go
- GraphQL

```codeBlockLines_e6Vv
jeopardy = client.collections.use("JeopardyQuestion")
response = jeopardy.query.hybrid(
    query="food",
    query_properties=["question"],
    alpha=0.25,
    limit=3,
)

for o in response.objects:
    print(o.properties)

```

[![python docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

Example response

The output is like this:

```codeBlockLines_e6Vv
{
  "data": {
    "Get": {
      "JeopardyQuestion": [\
        {\
          "answer": "a closer grocer",\
          "question": "A nearer food merchant"\
        },\
        {\
          "answer": "cake",\
          "question": "Devil's food & angel food are types of this dessert"\
        },\
        {\
          "answer": "honey",\
          "question": "The primary source of this food is the Apis mellifera"\
        }\
      ]
    }
  }
}

```

## Set weights on property values [​](https://docs.weaviate.io/weaviate/search/hybrid\#set-weights-on-property-values "Direct link to Set weights on property values")

Specify the relative value of an object's `properties` in the keyword search. Higher values increase the property's contribution to the search score.

- Python Client v4
- Python Client v3
- JS/TS Client v3
- JS/TS Client v2
- Go
- GraphQL

```codeBlockLines_e6Vv
jeopardy = client.collections.use("JeopardyQuestion")
response = jeopardy.query.hybrid(
    query="food",
    query_properties=["question^2", "answer"],
    alpha=0.25,
    limit=3,
)

for o in response.objects:
    print(o.properties)

```

[![python docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

Example response

The output is like this:

```codeBlockLines_e6Vv
{
  "data": {
    "Get": {
      "JeopardyQuestion": [\
        {\
          "answer": "a closer grocer",\
          "question": "A nearer food merchant"\
        },\
        {\
          "answer": "cake",\
          "question": "Devil's food & angel food are types of this dessert"\
        },\
        {\
          "answer": "food stores (supermarkets)",\
          "question": "This type of retail store sells more shampoo & makeup than any other"\
        }\
      ]
    }
  }
}

```

## Specify a search vector [​](https://docs.weaviate.io/weaviate/search/hybrid\#specify-a-search-vector "Direct link to Specify a search vector")

The vector component of hybrid search can use a query string or a query vector. To specify a query vector instead of a query string, provide a query vector (for the vector search) and a query string (for the keyword search) in your query.

- Python Client v4
- Python Client v3
- JS/TS Client v3
- JS/TS Client v2
- Go
- GraphQL

```codeBlockLines_e6Vv
query_vector = [-0.02] * 1536  # Some vector that is compatible with object vectors

jeopardy = client.collections.use("JeopardyQuestion")
response = jeopardy.query.hybrid(
    query="food",
    vector=query_vector,
    alpha=0.25,
    limit=3,
)

for o in response.objects:
    print(o.properties)

```

[![python docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

Example response

The output is like this:

```codeBlockLines_e6Vv
{
  "data": {
    "Get": {
      "JeopardyQuestion": [\
        {\
          "answer": "Risotto",\
          "question": "From the Italian word for rice, it's a rice dish cooked with broth & often grated cheese"\
        },\
        {\
          "answer": "arrabiata",\
          "question": "Italian for \"angry\", it describes a pasta sauce spiced up with plenty of chiles"\
        },\
        {\
          "answer": "Fettucine Alfredo",\
          "question": "Ribbon-shaped noodles, sweet butter, cream, parmesan cheese & black pepper make up this pasta dish"\
        }\
      ]
    }
  }
}

```

## Vector search parameters [​](https://docs.weaviate.io/weaviate/search/hybrid\#vector-search-parameters "Direct link to Vector search parameters")

Added in `v1.25`

Note that the hybrid threshold ( `max_vector_distance`) was introduced later in `v1.26.3`.

You can specify [vector similarity search](https://docs.weaviate.io/weaviate/search/similarity) parameters similar to [near text](https://docs.weaviate.io/weaviate/search/similarity#search-with-text) or [near vector](https://docs.weaviate.io/weaviate/search/similarity#search-with-a-vector) searches, such as `group by` and `move to` / `move away`. An equivalent `distance` [threshold for vector search](https://docs.weaviate.io/weaviate/search/similarity#set-a-similarity-threshold) can be specified with the `max vector distance` parameter.

- Python Client v4
- GraphQL
- JS/TS Client v3

```codeBlockLines_e6Vv
from weaviate.classes.query import HybridVector, Move, HybridFusion

jeopardy = client.collections.use("JeopardyQuestion")
response = jeopardy.query.hybrid(
    query="California",
    max_vector_distance=0.4,  # Maximum threshold for the vector search component
    vector=HybridVector.near_text(
        query="large animal",
        move_away=Move(force=0.5, concepts=["mammal", "terrestrial"]),
    ),
    alpha=0.75,
    limit=5,
)

```

[![python docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

Example response

The output is like this:

```codeBlockLines_e6Vv
{
  "data": {
    "Get": {
      "JeopardyQuestion": [\
        {\
          "answer": "Rhinoceros",\
          "points": 400,\
          "question": "The \"black\" species of this large horned mammal can grasp twigs with its upper lip"\
        },\
        {\
          "answer": "the hippopotamus",\
          "points": 400,\
          "question": "Close relative of the pig, though its name means \"river horse\""\
        },\
        {\
          "answer": "buffalo",\
          "points": 400,\
          "question": "Animal that was the main staple of the Plains Indians economy"\
        },\
        {\
          "answer": "California",\
          "points": 200,\
          "question": "Its state animal is the grizzly bear, & the state tree is a type of redwood"\
        },\
        {\
          "answer": "California",\
          "points": 200,\
          "question": "This western state sent its first refrigerated trainload of oranges back east February 14, 1886"\
        }\
      ]
    }
  }
}

```

## Hybrid search thresholds [​](https://docs.weaviate.io/weaviate/search/hybrid\#hybrid-search-thresholds "Direct link to Hybrid search thresholds")

Added in `v1.25`

The only available search threshold is `max vector distance`, which will set the maximum allowable distance for the vector search component.

- Python Client v4
- JS/TS Client v3

```codeBlockLines_e6Vv
from weaviate.classes.query import HybridVector, Move, HybridFusion

jeopardy = client.collections.use("JeopardyQuestion")
response = jeopardy.query.hybrid(
    query="California",
    max_vector_distance=0.4,  # Maximum threshold for the vector search component
    alpha=0.75,
    limit=5,
)

```

[![python docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

## Group results [​](https://docs.weaviate.io/weaviate/search/hybrid\#group-results "Direct link to Group results")

Added in `v1.25`

Define criteria to group search results.

- Python Client v4
- JS/TS Client v3

```codeBlockLines_e6Vv
# Grouping parameters
group_by = GroupBy(
    prop="round",  # group by this property
    objects_per_group=3,  # maximum objects per group
    number_of_groups=2,  # maximum number of groups
)

# Query
jeopardy = client.collections.use("JeopardyQuestion")
response = jeopardy.query.hybrid(
    alpha=0.75,
    query="California",
    group_by=group_by
)

for grp_name, grp_content in response.groups.items():
    print(grp_name, grp_content.objects)

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

Example response

The response is like this:

```codeBlockLines_e6Vv
'Jeopardy!'
'Double Jeopardy!'

```

## `limit` & `offset` [​](https://docs.weaviate.io/weaviate/search/hybrid\#limit--offset "Direct link to limit--offset")

Use `limit` to set a fixed maximum number of objects to return.

Optionally, use `offset` to paginate the results.

- Python Client v4
- Python Client v3
- JS/TS Client v3
- JS/TS Client v2
- Go
- GraphQL

```codeBlockLines_e6Vv
jeopardy = client.collections.use("JeopardyQuestion")
response = jeopardy.query.hybrid(
    query="food",
    limit=3,
    offset=1
)

for o in response.objects:
    print(o.properties)

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

## Limit result groups [​](https://docs.weaviate.io/weaviate/search/hybrid\#limit-result-groups "Direct link to Limit result groups")

To limit results to groups with similar distances from the query, use the [`autocut`](https://docs.weaviate.io/weaviate/api/graphql/additional-operators#autocut) filter. Specify the `Relative Score Fusion` ranking method when you use autocut with hybrid search.

info

Autocut requires `Relative Score Fusion` method because it uses actual similarity scores to detect cutoff points. Autocut shouldn't be used with `Ranked Fusion` as this fusion method relies on ranking positions, not similarity scores.

To learn more about the different fusion algorithms, visit the [search operators reference page](https://docs.weaviate.io/weaviate/api/graphql/search-operators#fusion-algorithms).

- Python Client v4
- Python Client v3
- JS/TS Client v3
- JS/TS Client v2
- Go
- GraphQL

```codeBlockLines_e6Vv
from weaviate.classes.query import HybridFusion

jeopardy = client.collections.use("JeopardyQuestion")
response = jeopardy.query.hybrid(
    query="food",
    fusion_type=HybridFusion.RELATIVE_SCORE,
    auto_limit=1
)

for o in response.objects:
    print(o.properties)

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

Example response

The output is like this:

```codeBlockLines_e6Vv
{
  "data": {
    "Get": {
      "JeopardyQuestion": [\
        {\
          "answer": "Guards",\
          "question": "Life, Security, Shin",\
          "_additional": {\
            "score": "0.75"\
          },\
        },\
        # ... trimmed for brevity\
      ]
    }
  }
}

```

## Filter results [​](https://docs.weaviate.io/weaviate/search/hybrid\#filter-results "Direct link to Filter results")

To narrow your search results, use a [`filter`](https://docs.weaviate.io/weaviate/api/graphql/filters).

- Python Client v4
- Python Client v3
- JS/TS Client v3
- JS/TS Client v2
- Go
- GraphQL

```codeBlockLines_e6Vv
from weaviate.classes.query import Filter

jeopardy = client.collections.use("JeopardyQuestion")
response = jeopardy.query.hybrid(
    query="food",
    filters=Filter.by_property("round").equal("Double Jeopardy!"),
    limit=3,
)

for o in response.objects:
    print(o.properties)

```

[![python docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

Example response

The output is like this:

```codeBlockLines_e6Vv
{
  "data": {
    "Get": {
      "JeopardyQuestion": [\
        {\
          "answer": "food stores (supermarkets)",\
          "question": "This type of retail store sells more shampoo & makeup than any other",\
          "round": "Double Jeopardy!"\
        },\
        {\
          "answer": "Tofu",\
          "question": "A popular health food, this soybean curd is used to make a variety of dishes & an ice cream substitute",\
          "round": "Double Jeopardy!"\
        },\
        {\
          "answer": "gastronomy",\
          "question": "This word for the art & science of good eating goes back to Greek for \"belly\"",\
          "round": "Double Jeopardy!"\
        }\
      ]
    }
  }
}

```

### Tokenization [​](https://docs.weaviate.io/weaviate/search/hybrid\#tokenization "Direct link to Tokenization")

Weaviate converts filter terms into tokens. The default tokenization is `word`. The `word` tokenizer keeps alphanumeric characters, lowercase them and splits on whitespace. It converts a string like "Test\_domain\_weaviate" into "test", "domain", and "weaviate".

For details and additional tokenization methods, see [Tokenization](https://docs.weaviate.io/weaviate/config-refs/collections#tokenization).
