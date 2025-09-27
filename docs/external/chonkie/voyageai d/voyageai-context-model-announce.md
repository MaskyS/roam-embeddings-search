## Introducing voyage-context-3: focused chunk-level details with global document context



TL;DR – We’re excited to introduce `voyage-context-3`, a contextualized chunk embedding model that produces vectors for chunks that capture the full document context without any manual metadata and context augmentation, leading to higher retrieval accuracies than with or without augmentation. It’s also simpler, faster and cheaper, and is a drop-in replacement for standard embeddings without downstream workflow changes, also reducing chunking strategy sensitivity.



On chunk-level and document-level retrieval tasks, `voyage-context-3 ` outperforms OpenAI-v3-large by 14.24% and 12.56%, Cohere-v4 by 7.89% and 5.64%, Jina-v3 late chunking by 23.66% and 6.76%, and contextual retrieval by 20.54% and 2.40%, respectively.



It also supports multiple dimensions and multiple quantization options enabled by Matryoshka learning and quantization-aware training, saving vectorDB costs while maintaining retrieval accuracy. For example, `voyage-context-3` (binary, 512) outperforms OpenAI-v3-large (float, 3072) by 0.73% while reducing vector database storage costs by 99.48%—virtually the same performance at 0.5% of the cost.



We’re excited to introduce `voyage-context-3`, a novel contextualized chunk embedding model, where chunk embedding encodes not only the chunk’s own content, but also captures the contextual information from the full document. `voyage-context-3` provides a seamless drop-in replacement for standard, context-agnostic embedding models used in existing RAG pipelines, while offering improved retrieval quality through its ability to capture relevant contextual information.



Compared to both context-agnostic models with isolated chunking (e.g., OpenAI-v3-large, Cohere-v4) as well as existing methods that add context and metadata to chunks, including overlapping chunks and attaching metadata, `voyage-context-3` delivers significant gains in retrieval performance while simplifying the tech stack.



On chunk-level (retrieving the most relevant chunk) and document-level retrieval (retrieving the document containing the most relevant chunk), `voyage-context-3` outperforms on average:



- OpenAI-v3-large and Cohere-v4 by 14.24% and 12.56%, and 7.89% and 5.64%, respectively.

- Context augmentation methods Jina-v3 late chunking[1](https://blog.voyageai.com/2025/07/23/voyage-context-3/#0a80c5b1-474b-4b0a-9298-d7b960a17102) and contextual retrieval[2](https://blog.voyageai.com/2025/07/23/voyage-context-3/#743690f5-85d7-4a84-b7df-17ab03f2bb09) by 23.66% and 6.76%, and 20.54% and 2.40%, respectively.

- `voyage-3-large` by 7.96% and 2.70%, respectively.



![](https://i0.wp.com/blog.voyageai.com/wp-content/uploads/2025/07/domain-average.png?resize=1024%2C427&quality=80&ssl=1)



## Chunking Challenges in RAG



**Focused detail vs global context.** Chunking—breaking large documents into smaller segments, or chunks—is a common and often necessary step in retrieval-augmented generation (RAG) systems. Originally chunking was primarily driven by the models’ limited context window (which is significantly extended by e.g., Voyage’s models lately).  More importantly, it allows the embeddings to contain precise fine-grained information about the corresponding passages, and as a result, allows the search system to pinpoint precisely relevant passages. However, this focus can come at the expense of broader context. Finally, without chunking, users must pass complete documents to downstream LLMs, driving up costs as many tokens may be irrelevant to the query.



For instance, if a 50-page legal document is vectorized into a single embedding, detailed information—such as the sentence “All data transmissions between the Client and the Service Provider’s infrastructure shall utilize AES-256 encryption in GCM mode”—is likely to be buried or lost in the aggregate. By chunking the document into paragraphs and vectorizing each one separately, the resulting embeddings can better capture localized details like “AES-256 encryption.” However, such a paragraph may not contain global context—such as the Client’s name—which is necessary to answer queries like “What encryption methods does Client VoyageAI want to use?”



Ideally, **we want both focused detail and global context**— **without tradeoffs**. Common workarounds—such as chunk overlaps, context summaries using LLMs (e.g., Anthropic’s contextual retrieval), or metadata augmentation—can introduce extra steps into an already complex AI application pipeline. These steps often require further experimentation to tune, resulting in increased development time and serving cost overhead.



## Introducing Contextualized Chunk Embeddings



We’re excited to introduce _contextualized chunk embeddings_ that capture both focused detail and global context. Our model processes the entire document in a single pass and generates a distinct embedding for each chunk. Each vector encodes not only the specific information within its chunk but also coarse-grained, document-level context, enabling richer and more semantically aware retrieval. The key is that the neural network sees all the chunks at the same time and decides intelligently what global information from other chunks should be injected into the individual chunk embeddings.



![](https://i0.wp.com/blog.voyageai.com/wp-content/uploads/2025/07/voyage-context-3-Neural-Network-1.png?resize=2363%2C1261&quality=80&ssl=1)



1. **Full document automatic context aware.** Contextualized chunk embeddings capture the full context of the document without requiring the user to manually or explicitly provide contextual information. This leads to improved retrieval performance compared to isolated chunk embeddings, while remaining simpler, faster, cheaper than other context-augmentation methods.



2. **Seamless drop-in replacement and storage cost parity.** `voyage-context-3` is a seamless drop-in replacement for standard, context-agnostic embedding models used in existing search systems, RAG pipelines, and agentic systems. It accepts the same input chunks and produces vectors with identical output dimensions and quantization—now enriched with document-level context for better retrieval performance. In contrast to [ColBERT](https://arxiv.org/abs/2004.12832) that introduces an extensive amount of vectors and storage costs, `voyage-context-3` generates the same number of vectors and is fully compatible with any existing vector database.



3. **Less sensitive to chunking strategy.** While chunking strategy still influences RAG system behavior—and the optimal approach depends on data and downstream tasks—our contextualized chunk embeddings are empirically shown to reduce the system’s sensitivity to these strategies, because the model intelligently supplement overly short chunks with global contexts.



Contextualized chunk embeddings outperform manual or LLM-based  contextualization because neural networks are trained to capture context intelligently from large datasets, surpassing the limitations of ad hoc effort. `voyage-context-3` was trained using both document-level and chunk-level relevance labels, along with a dual objective that teaches the model to preserve chunk-level granularity while incorporating global context.



| | **Context Preservation** | **Engineering Complexity** | Retrieval Accuracy |

| --- | --- | --- | --- |

| **Standard Embeddings**<br>(e.g., OpenAI-v3-large) | None | **Low** | Moderate |

| **Metadata Augmentation & Contextual Retrieval**<br>(e.g., Jina-v3 late chunking) | Partial | High | Moderate-High |

| **Contextualized Chunk Embeddings**<br>(e.g., `voyage-context-3`) | **Full, Principled** | **Low** | **Highest** |



## Evaluation Details



**Chunk-Level and Document-Level Retrieval**. For a given query, **chunk-level retrieval** returns the most relevant chunks, while **document-level retrieval** returns the documents containing those chunks. The figure below illustrates both retrieval levels across chunks from _n_ documents. The most relevant chunk, often referred to as the “golden chunk” and is bolded and shown in green. Its corresponding parent document is shown in blue.



![](https://i0.wp.com/blog.voyageai.com/wp-content/uploads/2025/07/voyage-context-3-Chunk-Level-and-Document-Level-Retrieval.png?resize=1024%2C838&quality=80&ssl=1)



**Datasets**. We evaluate on 93 domain-specific retrieval datasets, spanning nine domains: web reviews, law, medical, long documents, technical documentation, code, finance, conversations, and multilingual, which are listed in [this spreadsheet](https://docs.google.com/spreadsheets/d/1qLBWWvN7-4W53BveJgkQiDSoK_j2RYLh5DafDdEOPnc/edit?gid=291808049#gid=291808049). Every dataset contains a set of queries and a set of documents. Each document consists of an ordered sequence of chunks, which are created by us via a reasonable chunking strategy. As usual, every query has a number of relevant documents with potential a score indicating the degree of relevance, which we call document-level relevance labels and can be used for evaluation document-level retrieval. Moreover, each query also has a list of most relevant chunks with relevance scores, which are curated through various ways including labeling by LLMs. These are referred to as chunk-level relevance labels and used for chunk-level retrieval evaluation.



We also include proprietary real-world datasets, such as technical documentation and documents containing header metadata. Finally, we assess `voyage-context-3` across different embedding dimensions and various quantization options, on standard single-embedding retrieval evaluation, using the same datasets as in our [previous retrieval-quality-versus-storage-cost analysis](https://blog.voyageai.com/2025/01/07/voyage-3-large/).



**Models**. We evaluate `voyage-context-3` alongside several alternatives, including: OpenAI-v3-large ( `text-embedding-3-large`), Cohere-v4 ( `embed-v4.0`), Jina-v3 late chunking ( `jina-embeddings-v3`), contextual retrieval, `voyage-3.5`, and `voyage-3-large`.



**Metrics**. Given a query, we retrieve the top 10 documents based on cosine similarities and report the normalized discounted cumulative gain (NDCG@10), a standard metric for retrieval quality and a variant of the recall.



## Results



All the evaluation results are available in [this spreadsheet](https://docs.google.com/spreadsheets/d/1qLBWWvN7-4W53BveJgkQiDSoK_j2RYLh5DafDdEOPnc/edit?gid=291808049#gid=291808049) and we analyze the data below.



**Domain-specific quality.** The bar charts below show the average retrieval quality of `voyage-context-3` with full-precision 2048 embeddings for each domain. In the following chunk-level retrieval chart, we can see that `voyage-context-3` outperforms all other models across all domains. As noted earlier, for chunk-level retrieval, `voyage-context-3` outperforms on average OpenAI-v3-large, Cohere-v4, Jina-v3 late chunking, and contextual retrieval by 14.24%, 7.89%, 23.66%, and 20.54%, respectively.



![](https://i0.wp.com/blog.voyageai.com/wp-content/uploads/2025/07/domain-chunk-level.png?resize=1024%2C492&quality=80&ssl=1)



`voyage-context-3` also outperforms all other models across all domains in document-level retrieval, as shown in the corresponding chart below. On average, `voyage-context-3` outperforms OpenAI-v3-large, Cohere-v4, Jina-v3 late chunking, and contextual retrieval by 12.56%, 5.64%, 6.76%, and 2.40%, respectively.



![](https://i0.wp.com/blog.voyageai.com/wp-content/uploads/2025/07/domain-document-level.png?resize=1024%2C493&quality=80&ssl=1)



**Real-world datasets.** `voyage-context-3` performs strongly on our proprietary real-world technical documentation and in-house datasets, outperforming all other models. The bar chart below shows chunk-level retrieval results. Document-level retrieval results are provided in the [evaluation spreadsheet](https://docs.google.com/spreadsheets/d/1qLBWWvN7-4W53BveJgkQiDSoK_j2RYLh5DafDdEOPnc/edit?gid=291808049#gid=291808049).



![](https://i0.wp.com/blog.voyageai.com/wp-content/uploads/2025/07/real-world-chunk-level.png?resize=1024%2C426&quality=80&ssl=1)



**Chunking sensitivity.** Compared to standard, context-agnostic embeddings, `voyage-context-3` is less sensitive to variations in chunk size and delivers stronger performance with smaller chunks. For example, on document-level retrieval, `voyage-context-3` shows only a 2.06% variance, compared to 4.34% for `voyage-3-large`, and outperforms `voyage-3-large` by 6.63% when using 64-token chunks.



![](https://i0.wp.com/blog.voyageai.com/wp-content/uploads/2025/07/sensitivity.png?resize=1024%2C731&quality=80&ssl=1)



**Context metadata.** We also evaluate performance when context metadata is prepended to chunks. Even with metadata prepended to chunks embedded by `voyage-3-large`, `voyage-context-3` outperforms it by up to 5.53%, demonstrating better retrieval performance without the extra work and resources required to prepend metadata.



![](https://i0.wp.com/blog.voyageai.com/wp-content/uploads/2025/07/metadata-context.png?resize=770%2C671&quality=80&ssl=1)



**Matryoshka embeddings and quantization.** `voyage-context-3` supports 2048, 1024, 512, and 256 dimensional embeddings enabled by [Matryoshka learning](https://arxiv.org/abs/2205.13147?_kx=TdpXFbbY158jONPIc5tqSw.VU3S4W) and multiple embedding quantization options—including 32-bit floating point, signed and unsigned 8-bit integer, and binary precision—while minimizing quality loss. To clarify in relation to the previous figures, the chart below illustrates single-embedding retrieval on documents. Compared with OpenAI-v3-large (float, 3072), `voyage-context-3` (int8, 2048) reduces vector database costs by 83% with 8.60% better retrieval quality. Further, comparing OpenAI-v3-large (float, 3072) with `voyage-context-3` (binary, 512), vector database costs are reduced by 99.48% with 0.73% better retrieval quality; that’s virtually the same retrieval performance at 0.5% of the cost.



![](https://i0.wp.com/blog.voyageai.com/wp-content/uploads/2025/07/retrieval-quality-vs-cost-1.png?resize=1024%2C929&quality=80&ssl=1)



## Try voyage-context-3!



`voyage-context-3` is available today! The first 200 million tokens are free. Get started with this [quickstart](https://docs.voyageai.com/docs/contextualized-chunk-embeddings#quickstart) tutorial.



You can swap in `voyage-context-3` into any existing RAG pipeline you have without requiring any downstream changes. Contextualized chunk embeddings are especially effective for:



1. **Long, unstructured documents** such as white papers, legal contracts, and research reports.

2. **Cross-chunk reasoning**, where queries require information that spans multiple sections.

3. **High-sensitivity retrieval tasks—** such as in finance, medical, or legal domains—where missing context can lead to costly errors.



Follow us on [X (Twitter)](https://x.com/VoyageAI) and [LinkedIn](https://www.linkedin.com/company/voyageai/) to stay up-to-date with our latest releases.



1. Jina. “ [Late Chunking in Long-Context Embedding Models](https://jina.ai/news/late-chunking-in-long-context-embedding-models/).” August 22, 2024 [↩︎](https://blog.voyageai.com/2025/07/23/voyage-context-3/#0a80c5b1-474b-4b0a-9298-d7b960a17102-link)

2. Anthropic. “ [Introducing Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval).” September 19, 2024. [↩︎](https://blog.voyageai.com/2025/07/23/voyage-context-3/#743690f5-85d7-4a84-b7df-17ab03f2bb09-link)
