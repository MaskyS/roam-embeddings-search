VoyageAI
Chroma also provides a convenient wrapper around VoyageAI's embedding API. This embedding function runs remotely on VoyageAI’s servers, and requires an API key. You can get an API key by signing up for an account at VoyageAI.

This embedding function relies on the voyageai python package, which you can install with pip install voyageai.


import chromadb.utils.embedding_functions as embedding_functions
voyageai_ef  = embedding_functions.VoyageAIEmbeddingFunction(api_key="YOUR_API_KEY",  model_name="voyage-3-large")
voyageai_ef(input=["document1","document2"])
