# Google Gemini

Chroma provides a convenient wrapper around Google's Generative AI embedding API. This embedding function runs remotely on Google's servers, and requires an API key.

You can get an API key by signing up for an account at [Google MakerSuite](https://makersuite.google.com/).

### python

This embedding function relies on the `google-generativeai` python package, which you can install with `pip install google-generativeai`.

```python
# import
import chromadb.utils.embedding_functions as embedding_functions

# use directly
google_ef  = embedding_functions.GoogleGenerativeAiEmbeddingFunction(api_key="YOUR_API_KEY")
google_ef(["document1","document2"])

# pass documents to query for .add and .query
collection = client.create_collection(name="name", embedding_function=google_ef)
collection = client.get_collection(name="name", embedding_function=google_ef)
```

You can view a more [complete example](https://github.com/chroma-core/chroma/tree/main/examples/gemini) chatting over documents with Gemini embedding and langauge models.

For more info - please visit the [official Google python docs](https://ai.google.dev/tutorials/python_quickstart).
