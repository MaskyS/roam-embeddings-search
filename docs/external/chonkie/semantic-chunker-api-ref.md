# Semantic Chunker

> Splits text into chunks based on semantic similarity, ensuring that related content stays together in the same chunk.

## OpenAPI

````yaml chonkie-cloud/openapi.json post /v1/chunk/semantic
paths:
  path: /v1/chunk/semantic
  method: post
  servers:
    - url: https://api.chonkie.ai
      description: Chonkie Cloud API
  request:
    security:
      - title: BearerAuth
        parameters:
          query: {}
          header:
            Authorization:
              type: http
              scheme: bearer
              description: >-
                Your API Key from the [Chonkie Cloud
                dashboard](https://cloud.chonkie.ai/keys)
          cookie: {}
    parameters:
      path: {}
      query: {}
      header: {}
      cookie: {}
    body:
      multipart/form-data:
        schemaArray:
          - type: object
            properties:
              file:
                allOf:
                  - type: string
                    format: binary
                    description: The file to chunk.
              embedding_model:
                allOf:
                  - type: string
                    title: Embedding Model
                    default: minishlab/potion-base-32M
                    description: >-
                      Model identifier or embedding model instance to use for
                      semantic analysis.
              threshold:
                allOf:
                  - anyOf:
                      - type: string
                        const: auto
                      - type: number
                      - type: integer
                    title: Threshold
                    default: auto
                    description: >-
                      Similarity threshold for grouping sentences. Can be a
                      float [0,1] for direct threshold, int (1,100] for
                      percentile, or 'auto' for automatic calculation.
              chunk_size:
                allOf:
                  - type: integer
                    title: Chunk Size
                    default: 2048
                    description: Maximum tokens per chunk.
              similarity_window:
                allOf:
                  - type: integer
                    title: Similarity Window
                    default: 1
                    description: >-
                      Number of preceding sentences to consider for similarity
                      comparison.
              min_sentences:
                allOf:
                  - type: integer
                    title: Min Sentences
                    default: 1
                    description: Minimum number of sentences per chunk.
              min_chunk_size:
                allOf:
                  - type: integer
                    title: Min Chunk Size
                    default: null
                    description: Minimum tokens per chunk (optional).
              min_characters_per_sentence:
                allOf:
                  - type: integer
                    title: Min Characters Per Sentence
                    default: 12
                    description: Minimum number of characters per sentence.
              threshold_step:
                allOf:
                  - type: number
                    title: Threshold Step
                    default: 0.01
                    description: >-
                      Step size used when automatically calculating the
                      similarity threshold.
              delim:
                allOf:
                  - anyOf:
                      - type: string
                      - items:
                          type: string
                        type: array
                    title: Delim
                    default:
                      - .
                      - '!'
                      - '?'
                      - |+

                    description: Delimiters to split sentences on.
              include_delim:
                allOf:
                  - anyOf:
                      - type: string
                        enum:
                          - prev
                          - next
                      - type: 'null'
                    title: Include Delim
                    default: prev
                    description: >-
                      Include delimiters in the chunk text. If so, specify
                      whether to include the previous or next delimiter.
              return_type:
                allOf:
                  - type: string
                    title: Return Type
                    default: chunks
                    enum:
                      - texts
                      - chunks
                    description: >-
                      Return type for chunking. If 'chunks', returns a list of
                      `SemanticChunk` objects. If 'texts', returns a list of
                      strings.
            required: true
        examples:
          example:
            value:
              embedding_model: minishlab/potion-base-32M
              threshold: <string>
              chunk_size: 2048
              similarity_window: 1
              min_sentences: 1
              min_chunk_size: null
              min_characters_per_sentence: 12
              threshold_step: 0.01
              delim: <string>
              include_delim: prev
              return_type: chunks
    codeSamples:
      - label: Python
        lang: python
        source: |-
          from chonkie.cloud import SemanticChunker

          chunker = SemanticChunker(api_key="{api_key}")

          chunks = chunker(text="YOUR_TEXT")
      - label: JavaScript
        lang: JavaScript
        source: |-
          import { SemanticChunker } from 'chonkie/cloud';

          const chunker = new SemanticChunker(apiKey);

          const chunks = await chunker({ text: 'YOUR_TEXT' });
  response:
    '200':
      application/json:
        schemaArray:
          - type: array
            items:
              allOf:
                - $ref: '#/components/schemas/SemanticChunkSchema'
            title: SemanticChunkResponse
            description: >-
              A list containing `SemanticChunk` objects, detailing segments and
              sentences with optional embeddings.
        examples:
          example:
            value:
              - text: <string>
                start_index: 123
                end_index: 123
                token_count: 123
                sentences:
                  - text: <string>
                    start_index: 123
                    end_index: 123
                    token_count: 123
                    embedding:
                      - 123
        description: 'Successful Response: A list of `SemanticChunk` objects.'
  deprecated: false
  type: path
components:
  schemas:
    SemanticSentenceSchema:
      title: SemanticSentence
      description: >-
        Represents a single sentence within a semantic chunk, including an
        optional embedding vector.
      type: object
      properties:
        text:
          type: string
          title: Text
          description: The actual text content of the sentence.
        start_index:
          type: integer
          title: Start Index
          description: >-
            The starting character index of the sentence within the original
            input text.
        end_index:
          type: integer
          title: End Index
          description: >-
            The ending character index (exclusive) of the sentence within the
            original input text.
        token_count:
          type: integer
          title: Token Count
          description: >-
            The number of tokens in this specific sentence, according to the
            tokenizer used.
        embedding:
          type: array
          items:
            type: number
            format: float
          title: Embedding
          description: Embedding vector (list of floats) for the sentence.
    SemanticChunkSchema:
      title: SemanticChunk
      description: >-
        Represents a chunk generated by semantic chunking methods (Semantic,
        SDPM), containing `SemanticSentence` objects potentially with
        embeddings.
      type: object
      properties:
        text:
          type: string
          title: Text
          description: The actual text content of the chunk.
        start_index:
          type: integer
          title: Start Index
          description: >-
            The starting character index of the chunk within the original input
            text.
        end_index:
          type: integer
          title: End Index
          description: >-
            The ending character index (exclusive) of the chunk within the
            original input text.
        token_count:
          type: integer
          title: Token Count
          description: >-
            The number of tokens in this specific chunk, according to the
            tokenizer used.
        sentences:
          type: array
          items:
            $ref: '#/components/schemas/SemanticSentenceSchema'
          title: Sentences
          description: List of `SemanticSentence` objects contained within this chunk.

````
