# Model Choices [Skip link to Model Choices](https://docs.voyageai.com/docs/contextualized-chunk-embeddings\#model-choices)



Voyage currently provides the following contextualized chunk embedding models:



| Model | Context Length (tokens) | Embedding Dimension | Description |

| --- | --- | --- | --- |

| `voyage-context-3` | 32,000 | 1024 (default), 256, 512, 2048 | Contextualized chunk embeddings optimized for general-purpose and multilingual retrieval quality. See [blog post](https://blog.voyageai.com/2025/07/23/voyage-context-3/) for details. |



* * *



# Python API [Skip link to Python API](https://docs.voyageai.com/docs/contextualized-chunk-embeddings\#python-api)



Voyage contextualized chunk embeddings are accessible in Python through the `voyageai` [package](https://docs.voyageai.com/docs/api-key-and-installation#install-voyage-python-package). Please install the `voyageai` package, [set up](https://docs.voyageai.com/docs/api-key-and-installation) the API key, and use the `voyageai.Client.contextualized_embed()` function to vectorize your inputs.



> `voyageai.Client.contextualized_embed(inputs : List[List[str]], model : str, input_type : Optional[str] = None, output_dimension: Optional[int] = None, output_dtype: Optional[str] = "float", chunk_fn: Optional[Callable[[str], List[str]]] = None)`



**Parameters**



- **inputs** (List\[List\[str\]\]) - A list of lists, where each inner list contains a query, a document, or document chunks to be vectorized.



- Each inner list in `inputs` represents a set of text elements that will be embedded together. Each element in the list is encoded not just independently, but also encodes context from the other elements in the same list.



`inputs = [["text_1_1", "text_1_2", ..., "text_1_n"], ["text_2_1", "text_2_2", ..., "text_2_m"]]`

- **Document Chunks**. Most commonly, each inner list contains chunks from a single document, ordered by their position in the document. In this case:



`inputs = [["doc_1_chunk_1", "doc_1_chunk_2", ..., "doc_1_chunk_n"], ["doc_2_chunk_1", "doc_2_chunk_2", ..., "doc_2_chunk_m"]]`





Each chunk is encoded in context with the others from the same document, resulting in more context-aware embeddings. **We recommend that supplied chunks _not_ have any overlap**.

- **Context-Agnostic Behavior for Queries and Documents**. If there is one element per inner list, each text is embedded independently—similar to standard (context-agnostic) embeddings:



`inputs = [["query_1"], ["query_2"], ..., ["query_k"]]`



`inputs = [["doc_1"], ["doc_2"], ..., ["doc_k"]]`





Therefore, if the inputs are queries, each inner list should contain a single query (i.e., a length of one), as shown above, and the `input_type` should be set to `query`.

- The following constraints apply to the `inputs` list:



- The list must not contain more than 1,000 inputs.

- The total number of tokens across all inputs must not exceed 120K.

- The total number of chunks across all inputs must not exceed 16K.

- **model** (str) - Name of the model. Recommended options: `voyage-context-3`.

- **input\_type** (str, optional, defaults to `None`) \- Type of the input text. Options: `None`, `query`, `document`.



- When `input_type` is `None` , the embedding model directly converts the inputs into numerical vectors. For retrieval/search purposes, where a "query" is used to search for relevant information among a collection of data, referred to as "documents", we recommend specifying whether your inputs are intended as queries or documents by setting `input_type` to `query` or `document` , respectively. In these cases, Voyage automatically prepends a prompt to your inputs before vectorizing them, creating vectors more tailored for retrieval/search tasks. Embeddings generated with and without the `input_type` argument are compatible.

- For transparency, the following prompts are prepended to your input.

- For query, the prompt is "\_Represent the query for retrieving supporting documents: \_".

- For document, the prompt is "\_Represent the document for retrieval: \_".

- **output\_dimension** (int, optional, defaults to `None`) \- The number of dimensions for resulting output embeddings. `voyage-context-3` supports the following `output_dimension` values: 2048, 1024 (default), 512, and 256.

- **output\_dtype** (str, optional, defaults to `float`) \- The data type for the embeddings to be returned. Options: `float`, `int8`, `uint8`, `binary`, `ubinary`. Please see our [guide](https://docs.voyageai.com/docs/flexible-dimensions-and-quantization#quantization) for more details about output data types.



- `float`: Each returned embedding is a list of 32-bit (4-byte) [single-precision floating-point](https://en.wikipedia.org/wiki/Single-precision_floating-point_format) numbers. This is the default and provides the highest precision / retrieval accuracy.

- `int8` and `uint8`: Each returned embedding is a list of 8-bit (1-byte) integers ranging from -128 to 127 and 0 to 255, respectively.

- `binary` and `ubinary`: Each returned embedding is a list of 8-bit integers that represent bit-packed, quantized single-bit embedding values: `int8` for `binary` and `uint8` for `ubinary`. The length of the returned list of integers is 1/8 of `output_dimension` (which is the actual dimension of the embedding). The `binary` type uses the offset binary method. Please refer to our guide for details on [offset binary](https://docs.voyageai.com/docs/flexible-dimensions-and-quantization#offset-binary) and [binary embeddings](https://docs.voyageai.com/docs/flexible-dimensions-and-quantization#quantization).

- **chunk\_fn** (Callable\[\[str\], List\[str\]\], optional, defaults to `None`) \- A custom chunking function that takes a single string (e.g., document) and returns a list of strings (e.g., chunk of documents). If provided, this function is applied to each string in `inputs`. For convenience, `voyageai.default_chunk_fn` is available, which currently use [LangChain's `RecursiveCharacterTextSplitter.split_text`](https://python.langchain.com/api_reference/text_splitters/character/langchain_text_splitters.character.RecursiveCharacterTextSplitter.html) method. We recommend avoiding chunk overlap, so do not use functions that produce overlapping chunks.



**Returns**



- A `ContextualizedEmbeddingsObject`, containing the following attributes:



- **results** (List\[ `ContextualizedEmbeddingsResult`\]) \- A list of `ContextualizedEmbeddingsResult` objects, each representing the result from a query or document and contains the following attributes:



- **embeddings** (List\[List\[float\]\] or List\[List\[int\]\]) - A list of embeddings corresponding to a list of input texts, which may be either a query, document, or chunks from the same document. For document chunks, the embeddings are ordered to match the chunk order, which reflects their position within the document. Each embedding is a vector represented as a list of [floats](https://docs.python.org/3/library/functions.html#float) when `output_dtype` is set to `float` and as a list of [integers](https://docs.python.org/3/library/functions.html#int) for all other values of `output_dtype` ( `int8`, `uint8`, `binary`, `ubinary`).

- **chunk\_texts** (List\[str\]) - The text of the document chunks, included only when a chunking function ( `chunk_fn`) is provided. If no chunking function is supplied, it is assumed that the chunks were provided by the user, and `chunk_texts` is not returned.

- **index** (int) - The index of the query or document in the input list.

- **total\_tokens** (int) - The total number of tokens in the input texts.



**Example**: See our [quickstart](https://docs.voyageai.com/docs/contextualized-chunk-embeddings#quickstart) below.



* * *



# REST API [Skip link to REST API](https://docs.voyageai.com/docs/contextualized-chunk-embeddings\#rest-api)



Voyage contextualized chunk embeddings can be accessed by calling the endpoint `POST https://api.voyageai.com/v1/contextualizedembeddings`. Please refer to the [Contextualized Chunk Embeddings API Reference](https://docs.voyageai.com/reference/contextualized-embeddings-api) for the specification.



**Example**



Shell



```rdmd-code lang-shell theme-light



curl -X POST https://api.voyageai.com/v1/contextualizedembeddings \

-H "Authorization: Bearer $VOYAGE_API_KEY" \

-H "content-type: application/json" \

-d '

{

"inputs": [\

["doc_1_chunk_1", "doc_1_chunk_2"],\

["doc_2_chunk_1", "doc_2_chunk_2"]\

]

"input_type": "document",

"model": "voyage-context-3"

}'

```



* * *



# TypeScript Library [Skip link to TypeScript Library](https://docs.voyageai.com/docs/contextualized-chunk-embeddings\#typescript-library)



Voyage text embeddings are accessible in TypeScript through the [Voyage TypeScript Library](https://www.npmjs.com/package/voyageai), which exposes all the functionality of our text embeddings endpoint (see [Contextualized Chunk Embeddings API Reference](https://docs.voyageai.com/reference/contextualized-embeddings-api)).



* * *



# Quickstart [Skip link to Quickstart](https://docs.voyageai.com/docs/contextualized-chunk-embeddings\#quickstart)



This quickstart will show you how easy it is to use contextualized chunk embeddings and highlight their advantages over standard, context-agnostic embedding models. As you will see, contextualized chunk embeddings can serve as a seamless drop-in replacement for the standard embeddings used in existing RAG pipelines.



If you haven't already, follow the [installation](https://docs.voyageai.com/docs/api-key-and-installation) guide to install the Voyage Python package and obtain your API key. Additionally, to avoid interrupting your workflow during the walkthrough, install the third-party packages required by the quickstart using pip.



Shell



```rdmd-code lang-shell theme-light



pip install -qU langchain-text-splitters numpy

```



## Set up [Skip link to Set up](https://docs.voyageai.com/docs/contextualized-chunk-embeddings\#set-up)



**Prepare data**. You can replace the documents below with your own corpus. We've provided a simplified sample set that, when chunked, suffer from context loss—an issue that contextualized chunk embeddings are designed to address.



Python



```rdmd-code lang-python theme-light



documents = [\

"This is the SEC filing on Greenery Corp.'s Q2 2024 performance.\n"\

"The company's revenue increased by 7% compared to the previous quarter.",\

\

"This is the SEC filing on Greenery Corp.'s Q1 2024 performance.\n"\

"The company's revenue increased by 7% compared to the previous quarter.",\

\

"This is the SEC filing on Leafy Inc.'s Q2 2024 performance.\n"\

"The company's revenue increased by 15% compared to the previous quarter.",\

\

"This is the SEC filing on Leafy Inc.'s Q1 2024 performance.\n"\

"The company's revenue increased by 10% compared to the previous quarter.",\

\

"This is the SEC filing on Elephant Ltd.'s Q2 2024 performance.\n"\

"The company's revenue decreased by 2% compared to the previous quarter."\

]

```



**Chunk documents**. We'll start by chunking the documents with a basic [recursive text splitter from LangChain](https://python.langchain.com/docs/how_to/recursive_text_splitter/).



PythonOutput



```rdmd-code lang-python theme-light



from langchain_text_splitters import RecursiveCharacterTextSplitter

import json



text_splitter = RecursiveCharacterTextSplitter(separators=["\n"], chunk_size=100, chunk_overlap=0)

texts = [text_splitter.split_text(d) for d in documents]



print(f"Texts:\n{json.dumps(texts, indent=2)}")

```



```rdmd-code lang-python theme-light



Texts:

[\

[\

"This is the SEC filing on Greenery Corp.'s Q2 2024 performance.",\

"The company's revenue increased by 7% compared to the previous quarter."\

],\

[\

"This is the SEC filing on Greenery Corp.'s Q1 2024 performance.",\

"The company's revenue increased by 7% compared to the previous quarter."\

],\

[\

"This is the SEC filing on Leafy Inc.'s Q2 2024 performance.",\

"The company's revenue increased by 15% compared to the previous quarter."\

],\

[\

"This is the SEC filing on Leafy Inc.'s Q1 2024 performance.",\

"The company's revenue increased by 10% compared to the previous quarter."\

],\

[\

"This is the SEC filing on Elephant Ltd.'s Q2 2024 performance.",\

"The company's revenue decreased by 2% compared to the previous quarter."\

]\

]

```



We want to maintain document provenance for each chunk so that we can perform document-level (parent-document) retrieval and return the entire document that contains a chunks retrieved by semantic search.



PythonOutput



```rdmd-code lang-python theme-light



# Flatten list while maintaining document provenance

all_chunks = []

for doc_id, doc in enumerate(texts):

doc_chunks = [{"chunk": chunk, "doc_id": doc_id} for chunk in doc]

all_chunks.extend(doc_chunks)



print(f"All chunks:\n{json.dumps(all_chunks, indent=2)}")

```



```rdmd-code lang-python theme-light



All chunks:

[\

{\

"chunk": "This is the SEC filing on Greenery Corp.'s Q2 2024 performance.",\

"doc_id": 0\

},\

{\

"chunk": "The company's revenue increased by 7% compared to the previous quarter.",\

"doc_id": 0\

},\

{\

"chunk": "This is the SEC filing on Greenery Corp.'s Q1 2024 performance.",\

"doc_id": 1\

},\

{\

"chunk": "The company's revenue increased by 7% compared to the previous quarter.",\

"doc_id": 1\

},\

{\

"chunk": "This is the SEC filing on Leafy Inc.'s Q2 2024 performance.",\

"doc_id": 2\

},\

{\

"chunk": "The company's revenue increased by 15% compared to the previous quarter.",\

"doc_id": 2\

},\

{\

"chunk": "This is the SEC filing on Leafy Inc.'s Q1 2024 performance.",\

"doc_id": 3\

},\

{\

"chunk": "The company's revenue increased by 10% compared to the previous quarter.",\

"doc_id": 3\

},\

{\

"chunk": "This is the SEC filing on Elephant Ltd.'s Q2 2024 performance.",\

"doc_id": 4\

},\

{\

"chunk": "The company's revenue decreased by 2% compared to the previous quarter.",\

"doc_id": 4\

}\

]

```



**Query**. We want to identify the most relevant chunk for the following query: “What was the revenue growth for Leafy Inc. in Q2 2024?”



Python



```rdmd-code lang-python theme-light



query = "What was the revenue growth for Leafy Inc. in Q2 2024?"

```



## Approach 1: Standard, context-agnostic embeddings [Skip link to Approach 1: Standard, context-agnostic embeddings](https://docs.voyageai.com/docs/contextualized-chunk-embeddings\#approach-1-standard-context-agnostic-embeddings)



**Vectorize/embed the chunks**



Python



```rdmd-code lang-python theme-light



import voyageai



vo = voyageai.Client()

# This will automatically use the environment variable VOYAGE_API_KEY.

# Alternatively, you can use vo = voyageai.Client(api_key="<your secret key>")



# Embed the chunks

chunk_embds = vo.embed(

texts=[record["chunk"] for record in all_chunks],

model="voyage-3-large",

input_type="document"

).embeddings

```



**Perform basic semantic similarity search**. To find out the chunk that is most similar to the query among the existing data, we can first embed/vectorize the query:



Python



```rdmd-code lang-python theme-light



query_embd = vo.embed([query], model="voyage-3-large", input_type="query").embeddings[0]

```



We can compute the cosine similarity between the query and each chunk embedding, then retrieve the chunk with the highest similarity score.



PythonOutput



```rdmd-code lang-python theme-light



import numpy as np



# Compute the similarity

# Voyage embeddings are normalized to length 1, therefore dot-product and cosine

# similarity are the same.

similarities = np.dot(chunk_embds, query_embd)



# Rank similiarities

ranks = np.argsort(np.argsort(-similarities)) + 1



# Combine chunks with their ranks and similarities

ranked_chunks = []

for i, (chunk_data, similarity, rank) in enumerate(zip(all_chunks, similarities, ranks)):

ranked_chunks.append({

"chunk": chunk_data["chunk"],

"doc_id": chunk_data["doc_id"],

"similarity": float(similarity),

"rank": int(rank)

})



print(f"Chunk similarities:\n{json.dumps(ranked_chunks, indent=2)}")

```



```rdmd-code lang-python theme-light



Chunk similarities:

[\

{\

"chunk": "This is the SEC filing on Greenery Corp.'s Q2 2024 performance.",\

"doc_id": 0,\

"similarity": 0.4513495880308087,\

"rank": 3\

},\

{\

"chunk": "The company's revenue increased by 7% compared to the previous quarter.",\

"doc_id": 0,\

"similarity": 0.35663545808598424,\

"rank": 7\

},\

{\

"chunk": "This is the SEC filing on Greenery Corp.'s Q1 2024 performance.",\

"doc_id": 1,\

"similarity": 0.4166124680496381,\

"rank": 4\

},\

{\

"chunk": "The company's revenue increased by 7% compared to the previous quarter.",\

"doc_id": 1,\

"similarity": 0.35663545808598424,\

"rank": 6\

},\

{\

"chunk": "This is the SEC filing on Leafy Inc.'s Q2 2024 performance.",\

"doc_id": 2,\

"similarity": 0.6311910174756162,\

"rank": 1\

},\

{\

"chunk": "The company's revenue increased by 15% compared to the previous quarter.",\

"doc_id": 2,\

"similarity": 0.3472309722297028,\

"rank": 8\

},\

{\

"chunk": "This is the SEC filing on Leafy Inc.'s Q1 2024 performance.",\

"doc_id": 3,\

"similarity": 0.5992214666926985,\

"rank": 2\

},\

{\

"chunk": "The company's revenue increased by 10% compared to the previous quarter.",\

"doc_id": 3,\

"similarity": 0.34059832265203566,\

"rank": 9\

},\

{\

"chunk": "This is the SEC filing on Elephant Ltd.'s Q2 2024 performance.",\

"doc_id": 4,\

"similarity": 0.3860622636731734,\

"rank": 5\

},\

{\

"chunk": "The company's revenue decreased by 2% compared to the previous quarter.",\

"doc_id": 4,\

"similarity": 0.31796281117887043,\

"rank": 10\

}\

]

```



We see that the most relevant chunk is the fifth one, which simply states that it is the SEC filing for Leafy Inc.'s Q2 2024 performance—an appropriate result. This is followed by the seventh chunk, which references the SEC filing for Leafy Inc.'s Q1 2024 performance, also a sensible match given its relevance to Leafy Inc. and 2024 performance. After that, however, the next highest-ranked chunks reference SEC filings for other companies.



The chunk that actually contains the answer to the query is the sixth one, which states that the company’s revenue increased by 15% compared to the previous quarter. However, because this chunk was separated from the broader document, it lost the context linking it to Leafy Inc.’s Q2 2024 SEC filing. As a result, this "golden chunk" was ranked only eighth out of the ten chunks.



Next, we'll create contextualized chunk embeddings to see how they handle this kind of context loss.



## Approach 2: Contextualized chunk embeddings [Skip link to Approach 2: Contextualized chunk embeddings](https://docs.voyageai.com/docs/contextualized-chunk-embeddings\#approach-2-contextualized-chunk-embeddings)



We can directly pass the output of our text splitter (chunker), which is already structured as the required list of lists—each inner list containing the chunks of a single document.



Python



```rdmd-code lang-python theme-light



# Contextualized embedding model

query_embd_context = vo.contextualized_embed(inputs=[[query]], model="voyage-context-3", input_type="query").results[0].embeddings[0]



embds_obj = vo.contextualized_embed(

inputs=texts,

model="voyage-context-3",

input_type="document"

)



contextualized_chunk_embds = [emb for r in embds_obj.results for emb in r.embeddings]

```



**Perform semantic similarity search with contextualized chunk embeddings**. We can now perform the same semantic similarity search, but using our contextualized chunk embeddings.



PythonOutput



```rdmd-code lang-python theme-light



# Compute the similarity

# Voyage embeddings are normalized to length 1, therefore dot-product and cosine

# similarity are the same.

similarities_context = np.dot(contextualized_chunk_embds, query_embd_context)



# Rank similiarities

ranks_context = np.argsort(np.argsort(-similarities_context)) + 1



# Combine chunks with their ranks and similarities

ranked_contextualized_chunks = []

for i, (chunk_data, similarity, rank) in enumerate(zip(all_chunks, similarities_context, ranks_context)):

ranked_contextualized_chunks.append({

"chunk": chunk_data["chunk"],

"doc_id": chunk_data["doc_id"],

"similarity": float(similarity),

"rank": int(rank)

})



print(f"Contextualized chunk similarities:\n{json.dumps(ranked_contextualized_chunks, indent=2)}")

```



```rdmd-code lang-python theme-light



Contextualized chunk similarities:

[\

{\

"chunk": "This is the SEC filing on Greenery Corp.'s Q2 2024 performance.",\

"doc_id": 0,\

"similarity": 0.4890238923220861,\

"rank": 7\

},\

{\

"chunk": "The company's revenue increased by 7% compared to the previous quarter.",\

"doc_id": 0,\

"similarity": 0.5549016527374564,\

"rank": 5\

},\

{\

"chunk": "This is the SEC filing on Greenery Corp.'s Q1 2024 performance.",\

"doc_id": 1,\

"similarity": 0.4372318483382978,\

"rank": 9\

},\

{\

"chunk": "The company's revenue increased by 7% compared to the previous quarter.",\

"doc_id": 1,\

"similarity": 0.5096683171316662,\

"rank": 6\

},\

{\

"chunk": "This is the SEC filing on Leafy Inc.'s Q2 2024 performance.",\

"doc_id": 2,\

"similarity": 0.6630080274283974,\

"rank": 3\

},\

{\

"chunk": "The company's revenue increased by 15% compared to the previous quarter.",\

"doc_id": 2,\

"similarity": 0.7112170390868932,\

"rank": 1\

},\

{\

"chunk": "This is the SEC filing on Leafy Inc.'s Q1 2024 performance.",\

"doc_id": 3,\

"similarity": 0.6141823847063445,\

"rank": 4\

},\

{\

"chunk": "The company's revenue increased by 10% compared to the previous quarter.",\

"doc_id": 3,\

"similarity": 0.6637902760998357,\

"rank": 2\

},\

{\

"chunk": "This is the SEC filing on Elephant Ltd.'s Q2 2024 performance.",\

"doc_id": 4,\

"similarity": 0.3961326436687487,\

"rank": 10\

},\

{\

"chunk": "The company's revenue decreased by 2% compared to the previous quarter.",\

"doc_id": 4,\

"similarity": 0.44325838626567066,\

"rank": 8\

}\

]

```



The table below summarizes the retrieval rankings from `voyage-3-large` (context-agnostic) and `voyage-context-3` (contextualized chunk embeddings). We can see that contextualized chunk embeddings can significantly improve the retrieval accuracy where there is severe context loss. Instead of prioritizing chunks that reference SEC filings, `voyage-context-3` correctly ranks information about Leafy Inc.’s revenue increase as most relevant, placing the “golden chunk” at the top.



| Chunk | voyage-3-large Rank | voyage-context-3 Rank |

| --- | --- | --- |

| This is the SEC filing on Greenery Corp.'s Q2 2024 performance. | 3 | 7 |

| The company's revenue increased by 7% compared to the previous quarter. | 7 | 5 |

| This is the SEC filing on Greenery Corp.'s Q1 2024 performance. | 4 | 9 |

| The company's revenue increased by 7% compared to the previous quarter. | 6 | 6 |

| This is the SEC filing on Leafy Inc.'s Q2 2024 performance. | 1 | 3 |

| **The company's revenue increased by 15% compared to the previous quarter**. | 8 | **1** |

| This is the SEC filing on Leafy Inc.'s Q1 2024 performance. | 2 | 4 |

| The company's revenue increased by 10% compared to the previous quarter. | 9 | 2 |

| This is the SEC filing on Elephant Ltd.'s Q2 2024 performance. | 5 | 10 |

| The company's revenue decreased by 2% compared to the previous quarter. | 10 | 8 |
