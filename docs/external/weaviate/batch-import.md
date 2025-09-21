
[Batch imports](https://docs.weaviate.io/weaviate/tutorials/import#to-batch-or-not-to-batch) are an efficient way to add multiple data objects and cross-references.

Additional information

To create a bulk import job, follow these steps:

1. Initialize a batch object.
2. Add items to the batch object.
3. Ensure that the last batch is sent (flushed).

## Basic import [​](https://docs.weaviate.io/weaviate/manage-objects/import\#basic-import "Direct link to Basic import")

The following example adds objects to the `MyCollection` collection.

- Python Client v4
- Python Client v3
- JS/TS Client v3
- JS/TS Client v2
- Java
- Go

```codeBlockLines_e6Vv
data_rows = [\
    {"title": f"Object {i+1}"} for i in range(5)\
]

collection = client.collections.use("MyCollection")

with collection.batch.fixed_size(batch_size=200) as batch:
    for data_row in data_rows:
        batch.add_object(
            properties=data_row,
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

### Error handling [​](https://docs.weaviate.io/weaviate/manage-objects/import\#error-handling "Direct link to Error handling")

During a batch import, any failed objects or references will be stored and can be obtained through `batch.failed_objects` and `batch.failed_references`.
Additionally, a running count of failed objects and references is maintained and can be accessed through `batch.number_errors` within the context manager.
This counter can be used to stop the import process in order to investigate the failed objects or references.

Find out more about error handling on the Python client [reference page](https://docs.weaviate.io/weaviate/client-libraries/python).

## Use the gRPC API [​](https://docs.weaviate.io/weaviate/manage-objects/import\#use-the-grpc-api "Direct link to Use the gRPC API")

Added in `v1.23`.

The [gRPC API](https://docs.weaviate.io/weaviate/api) is faster than the REST API. Use the gRPC API to improve import speeds.

- Python Client v4
- JS/TS Client v3
- Java
- Go
- Spark

The Python client uses gRPC by default.

The legacy Python client does not support gRPC.

## Specify an ID value [​](https://docs.weaviate.io/weaviate/manage-objects/import\#specify-an-id-value "Direct link to Specify an ID value")

Weaviate generates an UUID for each object. Object IDs must be unique. If you set object IDs, use one of these deterministic UUID methods to prevent duplicate IDs:

- `generate_uuid5` (Python)
- `generateUuid5` (TypeScript)

- Python Client v4
- Python Client v3
- JS/TS Client v3
- JS/TS Client v2
- Java
- Go

```codeBlockLines_e6Vv
from weaviate.util import generate_uuid5  # Generate a deterministic ID

data_rows = [{"title": f"Object {i+1}"} for i in range(5)]

collection = client.collections.use("MyCollection")

with collection.batch.fixed_size(batch_size=200) as batch:
    for data_row in data_rows:
        obj_uuid = generate_uuid5(data_row)
        batch.add_object(
            properties=data_row,
            uuid=obj_uuid
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

## Specify a vector [​](https://docs.weaviate.io/weaviate/manage-objects/import\#specify-a-vector "Direct link to Specify a vector")

Use the `vector` property to specify a vector for each object.

- Python Client v4
- Python Client v3
- JS/TS Client v3
- JS/TS Client v2
- Java
- Go

```codeBlockLines_e6Vv
data_rows = [{"title": f"Object {i+1}"} for i in range(5)]
vectors = [[0.1] * 1536 for i in range(5)]

collection = client.collections.use("MyCollection")

with collection.batch.fixed_size(batch_size=200) as batch:
    for i, data_row in enumerate(data_rows):
        batch.add_object(
            properties=data_row,
            vector=vectors[i]
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

## Specify named vectors [​](https://docs.weaviate.io/weaviate/manage-objects/import\#specify-named-vectors "Direct link to Specify named vectors")

Added in `v1.24`

When you create an object, you can specify named vectors (if [configured in your collection](https://docs.weaviate.io/weaviate/manage-collections/vector-config#define-named-vectors)).

- Python Client v4
- Python Client v3
- JS/TS Client v3
- JS/TS Client v2

```codeBlockLines_e6Vv
data_rows = [{\
    "title": f"Object {i+1}",\
    "body": f"Body {i+1}"\
} for i in range(5)]

title_vectors = [[0.12] * 1536 for _ in range(5)]
body_vectors = [[0.34] * 1536 for _ in range(5)]

collection = client.collections.use("MyCollection")

with collection.batch.fixed_size(batch_size=200) as batch:
    for i, data_row in enumerate(data_rows):
        batch.add_object(
            properties=data_row,
            vector={
                "title": title_vectors[i],
                "body": body_vectors[i],
            }
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

## Import with references [​](https://docs.weaviate.io/weaviate/manage-objects/import\#import-with-references "Direct link to Import with references")

You can batch create links from an object to another other object through cross-references.

- Python Client v4
- Python Client v3
- JS/TS Client v2

```codeBlockLines_e6Vv
collection = client.collections.use("Author")

with collection.batch.fixed_size(batch_size=100) as batch:
    batch.add_reference(
        from_property="writesFor",
        from_uuid=from_uuid,
        to=target_uuid,
    )

failed_references = collection.batch.failed_references
if failed_references:
    print(f"Number of failed imports: {len(failed_references)}")
    print(f"First failed reference: {failed_references[0]}")

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

## Python-specific considerations [​](https://docs.weaviate.io/weaviate/manage-objects/import\#python-specific-considerations "Direct link to Python-specific considerations")

The Python clients have built-in batching methods to help you optimize import speed. For details, see the client documentation:

- [Python client `v4`](https://docs.weaviate.io/weaviate/client-libraries/python)

### Async Python client and batching [​](https://docs.weaviate.io/weaviate/manage-objects/import\#async-python-client-and-batching "Direct link to Async Python client and batching")

Currently, the [async Python client does not support batching](https://docs.weaviate.io/weaviate/client-libraries/python/async#bulk-data-insertion). To use batching, use the sync Python client.

## Stream data from large files [​](https://docs.weaviate.io/weaviate/manage-objects/import\#stream-data-from-large-files "Direct link to Stream data from large files")

If your dataset is large, consider streaming the import to avoid out-of-memory issues.

To try the example code, download the sample data and create the sample input files.

Get the sample data

- Python
- TypeScript

```codeBlockLines_e6Vv
import requests

# Download the json file
response = requests.get(
    "https://raw.githubusercontent.com/weaviate-tutorials/intro-workshop/main/data/jeopardy_1k.json"
)

# Write the json file to disk
data = response.json()
with open('jeopardy_1k.json', 'w') as f:
    json.dump(data, f)

# # Uncomment this section to create a csv file
# import pandas as pd

# df = pd.read_json("jeopardy_1k.json")
# df.to_csv("jeopardy_1k.csv", index=False)

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

Stream JSON files example code

- Python Client v4
- Python Client v3
- TypeScript

```codeBlockLines_e6Vv
import ijson

# Settings for displaying the import progress
counter = 0
interval = 200  # print progress every this many records; should be bigger than the batch_size

print("JSON streaming, to avoid running out of memory on large files...")
with client.batch.fixed_size(batch_size=100) as batch:
    with open("jeopardy_1k.json", "rb") as f:
        objects = ijson.items(f, "item")
        for obj in objects:
            properties = {
                "question": obj["Question"],
                "answer": obj["Answer"],
            }
            batch.add_object(
                collection="JeopardyQuestion",
                properties=properties,
                # If you Bring Your Own Vectors, add the `vector` parameter here
                # vector=obj.vector["default"]
            )

            # Calculate and display progress
            counter += 1
            if counter % interval == 0:
                print(f"Imported {counter} articles...")

print(f"Finished importing {counter} articles.")

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

Stream CSV files example code

- Python Client v4
- Python Client v3
- TypeScript

```codeBlockLines_e6Vv
import pandas as pd

# Settings for displaying the import progress
counter = 0
interval = 200  # print progress every this many records; should be bigger than the batch_size

def add_object(obj) -> None:
    global counter
    properties = {
        "question": obj["Question"],
        "answer": obj["Answer"],
    }

    with client.batch.fixed_size(batch_size=100) as batch:
        batch.add_object(
            collection="JeopardyQuestion",
            properties=properties,
            # If you Bring Your Own Vectors, add the `vector` parameter here
            # vector=obj.vector["default"]
        )

        # Calculate and display progress
        counter += 1
        if counter % interval == 0:
            print(f"Imported {counter} articles...")

print("pandas dataframe iterator with lazy-loading, to not load all records in RAM at once...")
with client.batch.fixed_size(batch_size=200) as batch:
    with pd.read_csv(
        "jeopardy_1k.csv",
        usecols=["Question", "Answer", "Category"],
        chunksize=100,  # number of rows per chunk
    ) as csv_iterator:
        # Iterate through the dataframe chunks and add each CSV record to the batch
        for chunk in csv_iterator:
            for index, row in chunk.iterrows():
                properties = {
                    "question": row["Question"],
                    "answer": row["Answer"],
                }
                batch.add_object(
                    collection="JeopardyQuestion",
                    properties=properties,
                    # If you Bring Your Own Vectors, add the `vector` parameter here
                    # vector=obj.vector["default"]
                )

        # Calculate and display progress
        counter += 1
        if counter % interval == 0:
            print(f"Imported {counter} articles...")

print(f"Finished importing {counter} articles.")

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

## Batch vectorization [​](https://docs.weaviate.io/weaviate/manage-objects/import\#batch-vectorization "Direct link to Batch vectorization")

Added in `v1.25`.

Some [model providers](https://docs.weaviate.io/weaviate/model-providers) provide batch vectorization APIs, where each request can include multiple objects.

From Weaviate `v1.25.0`, a batch import automatically makes use of the model providers' batch vectorization APIs where available. This reduces the number of requests to the model provider, improving throughput.

## Model provider configurations [​](https://docs.weaviate.io/weaviate/manage-objects/import\#model-provider-configurations "Direct link to Model provider configurations")

You can configure the batch vectorization settings for each model provider, such as the requests per minute or tokens per minute. The following examples sets rate limits for Cohere and OpenAI integrations, and provides API keys for both.

Note that each provider exposes different configuration options.

- Python Client v4

```codeBlockLines_e6Vv
from weaviate.classes.config import Integrations

integrations = [\
    # Each model provider may expose different parameters\
    Integrations.cohere(\
        api_key=cohere_key,\
        requests_per_minute_embeddings=rpm_embeddings,\
    ),\
    Integrations.openai(\
        api_key=openai_key,\
        requests_per_minute_embeddings=rpm_embeddings,\
        tokens_per_minute_embeddings=tpm_embeddings,   # e.g. OpenAI also exposes tokens per minute for embeddings\
    ),\
]
client.integrations.configure(integrations)

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

## Additional considerations [​](https://docs.weaviate.io/weaviate/manage-objects/import\#additional-considerations "Direct link to Additional considerations")

Data imports can be resource intensive. Consider the following when you import large amounts of data.

### Asynchronous imports [​](https://docs.weaviate.io/weaviate/manage-objects/import\#asynchronous-imports "Direct link to Asynchronous imports")

Experimental

Available starting in `v1.22`. This is an experimental feature. Use with caution.

To maximize import speed, enable [asynchronous indexing](https://docs.weaviate.io/weaviate/config-refs/indexing/vector-index#asynchronous-indexing).

To enable asynchronous indexing, set the `ASYNC_INDEXING` environment variable to `true` in your Weaviate configuration file.

```codeBlockLines_e6Vv
weaviate:
  image: cr.weaviate.io/semitechnologies/weaviate:1.33.0
  ...
  environment:
    ASYNC_INDEXING: 'true'
  ...

```

### Automatically add new tenants [​](https://docs.weaviate.io/weaviate/manage-objects/import\#automatically-add-new-tenants "Direct link to Automatically add new tenants")

By default, Weaviate returns an error if you try to insert an object into a non-existent tenant. To change this behavior so Weaviate creates a new tenant, set `autoTenantCreation` to `true` in the collection definition.

The auto-tenant feature is available from `v1.25.0` for batch imports, and from `v1.25.2` for single object insertions as well.

Set `autoTenantCreation` when you create the collection, or reconfigure the collection to update the setting as needed.

Automatic tenant creation is useful when you import a large number of objects. Be cautious if your data is likely to have small inconsistencies or typos. For example, the names `TenantOne`, `tenantOne`, and `TenntOne` will create three different tenants.

For details, see [auto-tenant](https://docs.weaviate.io/weaviate/manage-collections/multi-tenancy#automatically-add-new-tenants).
