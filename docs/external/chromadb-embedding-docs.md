Embedding Functions
Embeddings are the way to represent any kind of data, making them the perfect fit for working with all kinds of AI-powered tools and algorithms. They can represent text, images, and soon audio and video. Chroma collections index embeddings to enable efficient similarity search on the data they represent. There are many options for creating embeddings, whether locally using an installed library, or by calling an API.

Chroma provides lightweight wrappers around popular embedding providers, making it easy to use them in your apps. You can set an embedding function when you create a Chroma collection, to be automatically used when adding and querying data, or you can call them directly yourself.

Python	Typescript
OpenAI	✓	✓
Google Generative AI	✓	✓
Cohere	✓	✓
Hugging Face	✓	-
Instructor	✓	-
Hugging Face Embedding Server	✓	✓
Jina AI	✓	✓
Cloudflare Workers AI	✓	✓
Together AI	✓	✓
Mistral	✓	✓
Morph	✓	✓
We welcome pull requests to add new Embedding Functions to the community.

Default: all-MiniLM-L6-v2#
Chroma's default embedding function uses the Sentence Transformers all-MiniLM-L6-v2 model to create embeddings. This embedding model can create sentence and document embeddings that can be used for a wide variety of tasks. This embedding function runs locally on your machine, and may require you download the model files (this will happen automatically).

If you don't specify an embedding function when creating a collection, Chroma will set it to be the DefaultEmbeddingFunction:


collection = client.create_collection(name="my_collection")
Using Embedding Functions#
Embedding functions can be linked to a collection and used whenever you call add, update, upsert or query.


# Set your OPENAI_API_KEY environment variable
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

collection = client.create_collection(
    name="my_collection",
    embedding_function=OpenAIEmbeddingFunction(
        model_name="text-embedding-3-small"
    )
)

# Chroma will use OpenAIEmbeddingFunction to embed your documents
collection.add(
    ids=["id1", "id2"],
    documents=["doc1", "doc2"]
)
You can also use embedding functions directly which can be handy for debugging.


from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

default_ef = DefaultEmbeddingFunction()
embeddings = default_ef(["foo"])
print(embeddings) # [[0.05035809800028801, 0.0626462921500206, -0.061827320605516434...]]

collection.query(query_embeddings=embeddings)
Custom Embedding Functions#
You can create your own embedding function to use with Chroma; it just needs to implement EmbeddingFunction.


from chromadb import Documents, EmbeddingFunction, Embeddings

class MyEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        # embed the documents somehow
        return embeddings
We welcome contributions! If you create an embedding function that you think would be useful to others, please consider submitting a pull request.
