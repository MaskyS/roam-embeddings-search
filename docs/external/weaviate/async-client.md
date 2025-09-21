
Added in `weaviate-client` `v4.7.0`

The async Python client is available in `weaviate-client` versions `4.7.0` and higher.

The Python client library provides a [synchronous API](https://docs.weaviate.io/weaviate/client-libraries/python) by default, but an asynchronous API is also available for concurrent applications.

For asynchronous operations, use the `WeaviateAsyncClient` async client, available in `weaviate-client` `v4.7.0` and up.

The `WeaviateAsyncClient` async client largely supports the same functions and methods as the `WeaviateClient` [synchronous client](https://docs.weaviate.io/weaviate/client-libraries/python), with the key difference that the async client is designed to be used in an `async` function running in an [`asyncio` event loop](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio-event-loop).

## Installation [​](https://docs.weaviate.io/weaviate/client-libraries/python/async\#installation "Direct link to Installation")

The async client is already included in the `weaviate-client` package. Follow the installation instructions in the [Python client library documentation](https://docs.weaviate.io/weaviate/client-libraries/python#installation).

## Instantiation [​](https://docs.weaviate.io/weaviate/client-libraries/python/async\#instantiation "Direct link to Instantiation")

An async client `WeaviateAsyncClient` object can be instantiated [using a helper function](https://docs.weaviate.io/weaviate/client-libraries/python/async#instantiation-helper-functions), or by [explicitly creating an instance of the class](https://docs.weaviate.io/weaviate/client-libraries/python/async#explicit-instantiation).

### Instantiation helper functions [​](https://docs.weaviate.io/weaviate/client-libraries/python/async\#instantiation-helper-functions "Direct link to Instantiation helper functions")

These instantiation helper functions are similar to the synchronous client helper functions, and return an equivalent async client object.

- `use_async_with_local`
- `use_async_with_weaviate_cloud`
- `use_async_with_custom`

However, the async helper functions do not connect to the server as their synchronous counterparts do.

When using the async helper functions, you must call the async `.connect()` method to connect to the server, and call `.close()` before exiting to clean up. (Except when using a [context manager](https://docs.weaviate.io/weaviate/client-libraries/python/async#context-manager).)

The async helper functions take the same parameters for external API keys, connection timeout values and authentication details.

- WCD
- Local
- Custom

```codeBlockLines_e6Vv
import weaviate
from weaviate.classes.init import Auth
import os

# Best practice: store your credentials in environment variables
weaviate_url = os.environ["WEAVIATE_URL"]
weaviate_api_key = os.environ["WEAVIATE_API_KEY"]

async_client = weaviate.use_async_with_weaviate_cloud(
    cluster_url=weaviate_url,  # Replace with your Weaviate Cloud URL
    auth_credentials=Auth.api_key(weaviate_api_key),  # Replace with your Weaviate Cloud key
)

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

### Explicit instantiation [​](https://docs.weaviate.io/weaviate/client-libraries/python/async\#explicit-instantiation "Direct link to Explicit instantiation")

If you need to pass custom parameters, use the `weaviate.WeaviateAsyncClient` class to instantiate a client. This is the most flexible way to instantiate the client object.

```codeBlockLines_e6Vv
import weaviate
from weaviate.connect import ConnectionParams
from weaviate.classes.init import AdditionalConfig, Timeout, Auth
import os

async_client = weaviate.WeaviateAsyncClient(
    connection_params=ConnectionParams.from_params(
        http_host="localhost",
        http_port=8099,
        http_secure=False,
        grpc_host="localhost",
        grpc_port=50052,
        grpc_secure=False,
    ),
    auth_client_secret=Auth.api_key("secr3tk3y"),
    additional_headers={
        "X-OpenAI-Api-Key": os.getenv("OPENAI_APIKEY")
    },
    additional_config=AdditionalConfig(
        timeout=Timeout(init=30, query=60, insert=120),  # Values in seconds
    ),
    skip_init_checks=False
)

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

When you instantiate a connection directly, you have to call the (now async) `.connect()` method to connect to the server.

```codeBlockLines_e6Vv
import weaviate
from weaviate.connect import ConnectionParams
from weaviate import WeaviateAsyncClient
import os

async def instantiate_and_connect() -> WeaviateAsyncClient:
    client = weaviate.WeaviateAsyncClient(
        connection_params=ConnectionParams.from_params(
            http_host="localhost",
            http_port=8099,
            http_secure=False,
            grpc_host="localhost",
            grpc_port=50052,
            grpc_secure=False,
        ),
        # Additional settings not shown
    )
    await client.connect()
    return client

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

## Sync and async methods [​](https://docs.weaviate.io/weaviate/client-libraries/python/async\#sync-and-async-methods "Direct link to Sync and async methods")

The async client object is designed to be used in an `async` function running in an [`asyncio` event loop](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio-event-loop).

Accordingly, a majority of the client methods are `async` functions that return [`Coroutines` objects](https://docs.python.org/3/library/asyncio-task.html#coroutine). However, some methods are synchronous and can be used in a synchronous context.

As a rule of thumb, a method that involves a request to Weaviate will be an async function, while a method that executes in a local context will be synchronous.

### How to identify async methods [​](https://docs.weaviate.io/weaviate/client-libraries/python/async\#how-to-identify-async-methods "Direct link to How to identify async methods")

Async methods are identified by their method signatures. Async methods are defined with the `async` keyword, and they return `Coroutine` objects.

To see a method signature, you can use the `help()` function in Python, or use an IDE that supports code completion such as [Visual Studio Code](https://code.visualstudio.com/docs) or [PyCharm](https://www.jetbrains.com/help/pycharm/viewing-reference-information.html).

### Example async methods [​](https://docs.weaviate.io/weaviate/client-libraries/python/async\#example-async-methods "Direct link to Example async methods")

Methods that involve sending requests to Weaviate will be async functions. For example, each of the following operations is an async function:

- `async_client.connect()`: Connect to a Weaviate server
- `async_client.collections.create()`: Create a new collection
- `<collection_object>.data.insert_many()`: Insert a list of objects into a collection

### Example sync methods [​](https://docs.weaviate.io/weaviate/client-libraries/python/async\#example-sync-methods "Direct link to Example sync methods")

Methods that execute in a local context are likely to be synchronous. For example, each of the following operations is a sync function:

- `async_client.collections.use("<COLLECTION_NAME>")`: Create a Python object to interact with an existing collection (this does not create a collection)
- `async_client.is_connected()`: Check the last known connection status to the Weaviate server

## Context manager [​](https://docs.weaviate.io/weaviate/client-libraries/python/async\#context-manager "Direct link to Context manager")

The async client can be used in an asynchronous context manager, in a pattern similar to:

```codeBlockLines_e6Vv
async def context_manager_example() -> bool:
    import weaviate

    async with weaviate.use_async_with_local() as async_client:
        # The async context manager automatically connects and disconnects
        # Use the async client - for example, check if it's ready
        readiness = await async_client.is_ready()
    return readiness

loop = asyncio.new_event_loop()
try:
    readiness = loop.run_until_complete(context_manager_example())
finally:
    loop.close()

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

When using the async client in a context manager, you do not need to call `.connect()` or `.close()` explicitly. The client handles the connection and disconnection automatically.

## Async usage examples [​](https://docs.weaviate.io/weaviate/client-libraries/python/async\#async-usage-examples "Direct link to Async usage examples")

The async client object largely provides the same functionality as the [synchronous Python client](https://docs.weaviate.io/weaviate/client-libraries/python), with some key differences. First, the async client is designed to be used in an `async` function running in an [`asyncio` event loop](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio-event-loop). Accordingly, many of the client methods are `async` functions that return [`Coroutine` objects](https://docs.python.org/3/library/asyncio-task.html#coroutine).

To execute an async client method, you must `await` it in another `async` function. To execute an `async` function in a Python script, you can use `asyncio.run(my_async_function)` or the event loop directly:

```codeBlockLines_e6Vv
loop = asyncio.new_event_loop()
loop.run_until_complete(my_async_function())

```

### Data insertion [​](https://docs.weaviate.io/weaviate/client-libraries/python/async\#data-insertion "Direct link to Data insertion")

In this example, we create a new collection and insert a list of objects into the collection using the async client.

Note the use of a context manager in the async function. The context manager is used to ensure that the client is connected to the server during the data insertion operation.

```codeBlockLines_e6Vv
import weaviate
from weaviate.collections.classes.batch import BatchObjectReturn
import asyncio
import os

cohere_api_key = os.getenv("COHERE_API_KEY")  # Best practice: store your API keys in environment variables

async_client = weaviate.use_async_with_local(
    headers={
        "X-Cohere-Api-Key": cohere_api_key  # Replace with your Cohere API key
    }
)

async def async_insert(async_client) -> BatchObjectReturn:
    from weaviate.classes.config import Configure, Property, DataType

    # This example uses an async context manager
    # The client will automatically connect and disconnect as it enters and exits the context manager
    async with async_client:
        collection = await async_client.collections.create(
            name="Movie",
            vector_config=[\
                Configure.Vectors.text2vec_cohere(\
                    name="overview_vector",\
                    source_properties=["overview"]\
                )\
            ],
            generative_config=Configure.Generative.cohere(),
            properties=[\
                Property(name="title", data_type=DataType.TEXT),\
                Property(name="overview", data_type=DataType.TEXT),\
            ],
        )

        # Build objects to insert

        response = await collection.data.insert_many(objects)
    return response

loop = asyncio.new_event_loop()
try:
    response = loop.run_until_complete(async_insert(async_client))
finally:
    loop.close()

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

### Search & RAG [​](https://docs.weaviate.io/weaviate/client-libraries/python/async\#search--rag "Direct link to Search & RAG")

In this example, we perform retrieval augmented generation (RAG) with hybrid search results using the async client.

Note the use of a context manager in the async function. The context manager is used to ensure that the client is connected to the server during the data insertion operation.

```codeBlockLines_e6Vv
import weaviate
from weaviate.collections.classes.internal import GenerativeSearchReturnType
import asyncio
import os

cohere_api_key = os.getenv("COHERE_API_KEY")  # Best practice: store your API keys in environment variables

async_client = weaviate.use_async_with_local(
    headers={
        "X-Cohere-Api-Key": cohere_api_key  # Replace with your Cohere API key
    }
)

async def async_query(async_client: WeaviateAsyncClient) -> GenerativeSearchReturnType:
    async with async_client:
        # Note `collections.use()` is not an async method
        movies = async_client.collections.use(name="Movie")

        response = await movies.generate.hybrid(
            "romantic comedy set in Europe",
            target_vector="overview_vector",
            grouped_task="Write an ad, selling a bundle of these movies together",
            limit=3,
        )
    return response

loop = asyncio.new_event_loop()
try:
    response = loop.run_until_complete(async_query(async_client))
finally:
    loop.close()

print(response.generative.text)
for o in response.objects:
    print(o.properties["title"])

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

### Bulk data insertion [​](https://docs.weaviate.io/weaviate/client-libraries/python/async\#bulk-data-insertion "Direct link to Bulk data insertion")

For server-side batch operations, we recommend using the synchronous client and its [`batch` operations](https://docs.weaviate.io/weaviate/manage-objects/import). The batch operations are designed to handle large amounts of data efficiently through concurrent requests already.

The async client still offers `insert` and `insert_many` methods for data insertion, which can be used in an async context.

### Application-level example [​](https://docs.weaviate.io/weaviate/client-libraries/python/async\#application-level-example "Direct link to Application-level example")

A common use case for the async client is in web applications, where multiple requests are handled concurrently. Here is an indicative, minimal example integrating the async client with [FastAPI](https://fastapi.tiangolo.com/), a popular web framework for creating modular web API microservices:

```codeBlockLines_e6Vv
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
import os
import weaviate
from weaviate.collections.classes.internal import GenerativeSearchReturnType

cohere_api_key = os.getenv("COHERE_API_KEY")  # Best practice: store your API keys in environment variables

# Initialize the Weaviate client
async_client = weaviate.use_async_with_local(
    headers={
        "X-Cohere-Api-Key": cohere_api_key  # Replace with your Cohere API key
    }
)

@asynccontextmanager
async def lifespan(app: FastAPI):  # See https://fastapi.tiangolo.com/advanced/events/#lifespan-function
    # Connect the client to Weaviate
    await async_client.connect()
    yield
    # Close the connection to Weaviate
    await async_client.close()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def read_root():
    collection = async_client.collections.use("Movie")
    obj_count = await collection.aggregate.over_all(total_count=True)
    return {"object_count": obj_count.total_count}

@app.get("/search")
async def search(query: str) -> dict:
    if not await async_client.is_ready():
        raise HTTPException(status_code=503, detail="Weaviate is not ready")

    collection = async_client.collections.use("Movie")
    print(query)
    response: GenerativeSearchReturnType = await collection.generate.hybrid(
        query=query,
        target_vector="overview_vector",
        single_prompt=f"""
        The user searched for query: {query}.
        Based on the following overview, simply recommend or not whether the
        user might want to watch the movie. Do not offer any follow-ups or additional info.
        MOVIE TITLE: {{title}}. OVERVIEW: {{overview}}
        """,
        limit=3,
    )

    return {
        "responses": [\
            {\
                "title": object.properties["title"],\
                "overview": object.properties["overview"],\
                "recommendation": object.generated,\
            }\
            for object in response.objects\
        ]
    }

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

```

[![py docs](https://docs.weaviate.io/img/site/logo-py.svg)  API docs](https://weaviate-python-client.readthedocs.io/en/stable "View API documentation")

If you run this example, you will see the FastAPI server running on `http://localhost:8000`. You can interact with the server using the `/` and `/search` endpoints.

Data insertion not shown

Note that this example is minimal and does not include collection creation or object insertion. It assumes that the collection `Movie` already exists.
