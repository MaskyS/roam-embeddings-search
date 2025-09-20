from chromadb.utils.embedding_functions.ollama_embedding_function import (
    OllamaEmbeddingFunction,
)

ollama_ef = OllamaEmbeddingFunction(
    url="http://localhost:11434",
    model_name="llama2",
)

embeddings = ollama_ef(["This is my first text to embed",
                        "This is my second document"])
