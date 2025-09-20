# Metadata Filtering

The where argument in get and query is used to filter records by their metadata. For example, in this query operation, Chroma will only query records that have the page metadata field with the value 10:

PythonTypescript

```

collection.query(
    query_texts=["first query", "second query"],
    where={"page": 10}
)

```

In order to filter on metadata, you must supply a where filter dictionary to the query. The dictionary must have the following structure:

PythonTypescript

```

{
    "metadata_field": {
        <Operator>: <Value>
    }
}

```

Using the $eq operator is equivalent to using the metadata field directly in your where filter.

PythonTypescript

```

{
    "metadata_field": "search_string"
}

# is equivalent to

{
    "metadata_field": {
        "$eq": "search_string"
    }
}

```

For example, here we query all records whose page metadata field is greater than 10:

PythonTypescript

```

collection.query(
    query_texts=["first query", "second query"],
    where={"page": { "$gt": 10 }}
)

```

## Using Logical Operators [\#](https://docs.trychroma.com/docs/querying-collections/metadata-filtering\#using-logical-operators)

You can also use the logical operators $and and $or to combine multiple filters.

An $and operator will return results that match all the filters in the list.

PythonTypescript

```

{
    "$and": [\
        {\
            "metadata_field": {\
                <Operator>: <Value>\
            }\
        },\
        {\
            "metadata_field": {\
                <Operator>: <Value>\
            }\
        }\
    ]
}

```

For example, here we query all records whose page metadata field is between 5 and 10:

PythonTypescript

```

collection.query(
    query_texts=["first query", "second query"],
    where={
        "$and": [\
            {"page": {"$gte": 5 }},\
            {"page": {"$lte": 10 }},\
        ]
    }
)

```

An $or operator will return results that match any of the filters in the list.

PythonTypescript

```

{
    "or": [\
        {\
            "metadata_field": {\
                <Operator>: <Value>\
            }\
        },\
        {\
            "metadata_field": {\
                <Operator>: <Value>\
            }\
        }\
    ]
}

```

For example, here we get all records whose color metadata field is red or blue:

PythonTypescript

```

collection.get(
    where={
        "or": [\
            {"color": "red"},\
            {"color": "blue"},\
        ]
    }
)

```

## Using Inclusion Operators [\#](https://docs.trychroma.com/docs/querying-collections/metadata-filtering\#using-inclusion-operators)

The following inclusion operators are supported:

- $in \- a value is in predefined list (string, int, float, bool)
- $nin \- a value is not in predefined list (string, int, float, bool)

An $in operator will return results where the metadata attribute is part of a provided list:

PythonTypescript

```

{
  "metadata_field": {
    "$in": ["value1", "value2", "value3"]
  }
}

```

An $nin operator will return results where the metadata attribute is not part of a provided list (or the attribute's key is not present):

PythonTypescript

```

{
  "metadata_field": {
    "$nin": ["value1", "value2", "value3"]
  }
}

```

For example, here we get all records whose author metadata field is in a list of possible values:

PythonTypescript

```

collection.get(
    where={
       "author": {"$in": ["Rowling", "Fitzgerald", "Herbert"]}
    }
)

```

## Combining with Document Search [\#](https://docs.trychroma.com/docs/querying-collections/metadata-filtering\#combining-with-document-search)

.get and .query can handle metadata filtering combined with [document search](https://docs.trychroma.com/docs/querying-collections/full-text-search):

PythonTypescript

```

collection.query(
    query_texts=["doc10", "thus spake zarathustra", ...],
    n_results=10,
    where={"metadata_field": "is_equal_to_this"},
    where_document={"$contains":"search_string"}
)

```
