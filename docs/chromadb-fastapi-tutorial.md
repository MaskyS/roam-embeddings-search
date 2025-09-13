First steps with Chroma: building the database
As with any database, the first thing to do is build the database so that later we can add collections, insert new texts, etc.

In this sense, currently (June 2023) Chroma offers two different ways of storing information:

DuckDB : persists the information by saving the data in parquet files.
Clickhouse: saves the information in another Clickhouse database.
The main difference between the two is that DuckDB allows you to create a standalone Chroma service, but it will be much less scalable. On the contrary, if we store the data in Clickhouse, we will be able to scale better, although it will not be a standalone service.

Personally, if you’re going to do tests or require a vector database that isn’t very large, I recommend you use DuckDB, while if you want to scale more, I recommend implementing Chroma with Clickhouse.

Now, how can we mount the database in each case? Let’s see.

How to create a Chroma database with DuckDB as backend
To create a Chroma database with DuckDB as a backend, you will need to do two steps:

Create the Chroma database and make it accessible using an API such as FastAPI.
Create the Docker image and deploy it. Additionally, if you want data persistence, you can always create a Docker Compose with a volume.
To create the Chroma database and make it accessible via an API, Chroma provides the Settings class, which allows us to define how we want it to be implemented. In our case, there are two parameters that we must define:

chroma_db_impl: indicates which backend will use Chroma. In our case, we must indicate duckdb+parquet.
persist_directory allows us to indicate in which folder the parquet files will be saved to achieve persistent storage.
If we want the persist_directory folder to persist within the container, remember to create a volume for that folder.

Finally, we’ll pass the results of those settings to FastAPI to create the API to interact with Chroma.

So, the code will be the following:

python
# server.py
import chromadb
import chromadb.config
from chromadb.server.fastapi import FastAPI

settings = chromadb.config.Settings(
    chroma_db_impl="duckdb+parquet", 
    persist_directory='chroma_data'
)
server = FastAPI(settings)
app = server.app
Copy
Finally, we need to create a Dockerfile that will install the necessary libraries and run the API on a webserver.

I personally had problems with the latest version of FastAPI, so I recommend using FastAPI version 0.85.1.

That process is done in the following Dockerfile:

dockerfile
FROM python:3.8
RUN pip install uvicorn
RUN pip install chromadb 
RUN pip install --force-reinstall fastapi==0.85.1
COPY server.py .
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
Copy
With this, we have our Chroma ready to be deployed in a container using DuckDB as backend. Now, let’s see how to use Chroma with Clickhouse as a backend.

How to create a Chroma database with Clickhouse as backend
To use Chroma with Clickhouse yes or yes we are going to need to use Docker Compose, since we will need to run Chroma in one microservice and Clickhouse in another.

If you don’t know what Docker Compose is or how it works, you can learn more about it here.

Once this is done, we are going to modify the script that creates the server. Specifically, in the configuration we must indicate:

chroma_db_impl – How Chroma is implemented. In this case it will receive the value clickhouse.
clickhouse_host – The host where Clickhouse is running. As we will execute it inside a Compose, we will indicate the name of the service.
clickhouse_port: HTTP port on which Clickhouse is listening, which we can configure in the compose, although by default it is 8123.
Note: Both the host and the port can be defined as an environment variable, which is better, since you don’t expose any data. The Chroma implementation type can be defined with the CHROMA_DB_IMPL variable, the clickhouse host can be defined in the CLICKHOUSE_HOST variable, and the port in the CLICKHOUSE_PORT.

python
import chromadb
import chromadb.config
from chromadb.server.fastapi import FastAPI

settings = chromadb.config.Settings(
    chroma_db_impl = 'clickhouse',
    clickhouse_host ='clickhouse',
    clickhouse_port = 8123 
)

server = FastAPI(settings)
app = server.app()
Copy
Once this is done, we are going to use the same Dockerfile as for the implementation of Chroma with DuckDB, which is the following:

dockerfile
FROM python:3.8
RUN pip install uvicorn
RUN pip install chromadb 
RUN pip install --force-reinstall fastapi==0.85.1
COPY server.py .
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
Copy
Finally, let’s define a Compose that will kick up both Chroma and Clickhouse. Also, we have to define the network so that both containers are connected.

In addition, it is recommended to also define volumes for both Chroma and Clickhouse. Here is an example inspired by the test that Chroma itself uses:

yaml
services:
  chroma:
    image: chroma
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - 8000:8000
    depends_on:
      - clickhouse
    networks:
      - net

  clickhouse:
    image: clickhouse/clickhouse-server:22.9-alpine
    environment:
      - ALLOW_EMPTY_PASSWORD=yes
      - CLICKHOUSE_TCP_PORT=9000
      - CLICKHOUSE_HTTP_PORT=8123
    ports:
      - '8123:8123'
      - '9000:9000'
    volumes:
      - clickhouse_data:/var/lib/clickhouse
      - clickhouse_logs:/var/log/clickhouse-server
    networks:
      - net

volumes:
  clickhouse_data:
    driver: local
  clickhouse_logs:
    driver: local

networks:
  net:
    driver: bridge
Copy
Running compose we would already have our Chroma database up and running on port 8000.

Okay, now that we know how to set up Chroma, a vector database, let’s see how we can work with it from Python.

How to work with Chroma in Python
When we work with Chroma we have to know several different things:

How to connect the client to our Chroma database.
How to create and manage collections.
How to insert new documents and/or vectors into collections.
How to query our database to obtain the most similar vectors.
So, we are going to go step by step looking at each of these points. Let’s go with it!

1. How to connect the client to our Chroma database
To connect and interact with a Chroma database what we need is a client. We can achieve this in Python by installing the following library:

undefined
pip install chromadb
Copy
Okay, now that we have Chroma installed, let’s connect to our Chroma database. To do this we must indicate:

The way we will work with Chroma, which in this case is 'rest', that is, through API.
The host Chroma is running on. If you’re running Chroma on Docker locally, you’ll need to specify 'localhost' and otherwise the host or IP it’s running on.
The port on which Chroma is running, which must match the port that we have indicated in the Dockerfile and in Compose (if applicable). In our case, port 8000.
Once this is done, let’s execute the get_version() method to check that it can connect correctly:

python
import chromadb
from chromadb.config import Settings

setting = Settings(
    chroma_api_impl="rest",
    chroma_server_host= 'localhost',
    chroma_server_http_port = 8000
)

client = chromadb.Client(setting)

client.get_version()
Copy
python
'0.3.25'
Copy
Perfect, we already have our client connected to our vector database. Now, let’s see how we can create and manage collections.

2. How to create and manage collections
Although it may not seem like it, the creation and management of vector database collections is not a minor thing. When creating the collection is when we will define the model that the database will use to create the embeddings in case we insert a document and not a vector.

There are different ways to create a collection, but the easiest is using the create_collection method:

python
from chromadb.utils import embedding_functions

collection = client.create_collection(
    name="test",
    embedding_function= embedding_functions.DefaultEmbeddingFunction()
)
Copy
As you can see, when we create a collection I have defined an embedding function that it should apply. Let’s see what options Chroma offers us in this regard.

Chroma Embedding Functions
As seen in the above function, Chroma offers different functions to get the embeddings from the documents. More specifically, as of June 2023 it offers the following functions:

Any model from the SentenceTransformers library link. In fact, by default, it uses the all-MiniLM-L6-v2 model.
These functions can be loaded as follows:

python
# Change mode_name by desired model
embed = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="model-name")
Copy
Models from the Instructor library: these are models that you can run locally on the GPU. To do this, you must first install the library using the following command pip install InstructorEmbedding. Then, you can define the embedder as I show below:
python
# Change mode_name by desired model
embedder = embedding_functions.InstructorEmbeddingFunction(
     model_name="model_name",
     device="cuda" # Accepts cuda or CPU
)
Copy
The OpenAI API. This requires you to have an OpenAI API Key, which is paid. You can learn how to get it here. If you already have it, the way to use the API is as follows:
undefined
pip isntall openai
Copy
Definition of the embedder using the OpenAIEmbeddingFunction class:

bash
# Change mode_name by desired model
embed = embedding_functions.OpenAIEmbeddingFunction(
     api_key="API_KEY",
     model_name="model-name
)
Copy
The Cohere API: The procedure is the same as for the OpenAI API, you must first register, which you can learn here. Then, you must install its library by running pip install cohere and finally, you must define the embedder as follows:
python
# Change mode_name by desired model
embeddedger = embedding_functions.CohereEmbeddingFunction(
     api_key="YOUR_API_KEY",
     model_name="model-name"
)
Copy
The Google Palm API: the procedure is the same as with the other APIs, first you must register and then you must install its library by running pip install google-generativeai and finally, you must define the embedder as follows:
python
# Change mode_name by desired model
embedder = embedding_functions.GooglePalmEmbeddingFunction(
     api_key=api_key,
     model=model_name
)
Copy
Custom embedding function: You can create your own class of embeddings by inheriting the EmbeddingFunciton class, as shown below:
python
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings

class MyEmbeddingFunction(EmbeddingFunction):
     def __call__(self, texts: Documents) -> Embeddings:
         # embed the documents somehow
         return embeddings
Copy
As you can see there are many different embedding models that we can use. So, given this, let’s see how we can delete and manage the collections.

How to manage collections
An interesting thing is that if you try to create a collection that already exists, you will get an error, as shown below:

python
client.create_collection(
     name="test",
     embedding_function= embedding_functions.DefaultEmbeddingFunction()
)
Copy
python
----------------------------------- ----------------------------------------
ValueError: Collection with name test already exists
Copy
A simple way to avoid it, without having to check whether the collection name exists or not, is by passing the get_or_create parameter as True. This way, if the collection already exists, it will update its metadata and not return an error. If it does not exist, it will create it. Let’s see an example of creating the same collection, but with another model:

python
embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
     model_name= 'all-mpnet-base-v2'
)

client. create_collection(
     name="test",
     embedding_function=embedder,
     get_or_create = True
)
Copy
As you can see, the function has executed successfully and has actually downloaded the model since it was not previously downloaded. Finally, you can delete a collection with the delete_collection function, indicating the name of the collection:

python
client.delete_collection(name = 'test')
Copy
Now that we know how to create and manage collections, let’s see how we can insert documents and/or vectors into those collections:

How to insert new documents and/or vectors in the collections
To work with a collection, the first thing we need to do is get the collection as an object in Python. We can do this using the get_collection function of the client. In this case we must also indicate the embedding function that should be applied.

python
collection = client.get_collection(name = 'test', embedding_function= embedder)
Copy
Now that we have the collection, we can insert data into it. To do this, we use the add method of the object we just created. In any case, there are two different ways to push content to Chroma:

Insert a document or a list of documents, in such a way that Chroma itself transforms those documents into embeddings. To do this, we must pass a list of texts to the parameter documents..
Insert a vector manually. Either because we have previously calculated the embeddings or because we are going to store vectors of another type. After all, a vector database is designed to host vectors, they don’t necessarily have to be emebeddings. To do this, we must pass a list of embeddings (lists) to the embeddings parameter.
Also, when inserting the information we can indicate the following issues:

id: This is the identifier of the vector, which is mandatory and must be unique.
metadata: this is additional information that we can use later in order to filter the information. For example, suppose we have the year of the document, it could be filtered to obtain similar vectors for a specific year or period. In this case, it is optional.
Given this, we are going to extract a series of documents (texts) to be able to save them in our vector database. The approach is as follows:

Download the list of 500 companies that make up the S&P500, which we will do from this page (link).
For each company, extract the company’s main description from Wikipedia. We will do this with the summary function from the wikipedia library.
Note: the goal of this part is not to get clean and perfect information 100% of the time, but to make a quick and simple extraction that serves as an example. Therefore, the cases in which the extraction does not work will be discarded.

So first I install the libraries:

undefined
pip install lxml wikipedia
Copy
And now I download the data I need (it will take a few minutes).

python
import pandas as pd
import wikipedia


def get_wikipedia_summary(name):
     try:
         summary = wikipedia.summary(name + 'company')
     except:
         summary = None
     finally:
         return summary

url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

df = pd.read_html(url, attrs = {"id": "constituents"})[0]
df['company_summary'] = df['Security'].apply(lambda x: get_wikipedia_summary(x))

df.head()
Copy
Symbol	Security	GICS Sector	GICS Sub-Industry	Headquarters Location	Date added	CIK	Founded	company_summary
0	MMM	3M	Industrials	Industrial Conglomerates	Saint Paul, Minnesota	1957-03-04	66740	1902	3M (originally the Minnesota Mining and Manufa…
1	AOS	A. O. Smith	Industrials	Building Products	Milwaukee, Wisconsin	2017-07-26	91142	1916	A. O. Smith Corporation is an American manufac…
2	ABT	Abbott	Health Care	Health Care Equipment	North Chicago, Illinois	1957-03-04	1800	1888	Abbott Laboratories is an American multination…
3	ABBV	AbbVie	Health Care	Pharmaceuticals	North Chicago, Illinois	2012-12-31	1551152	2013 (1888)	AbbVie Inc. is a pharmaceutical company headqu…
4	ACN	Accenture	Information Technology	IT Consulting & Other Services	Dublin, Ireland	2011-07-06	1467373	1989	Accenture plc is an Irish-American profession…
Finally, let’s clear the data with nulls and get:

A list with the documents (the summaries of the texts).
A list with the ids that we will create.
A list of dictionaries with the metadata we want to upload per document. This metadata will include filtering information that may be of interest to us, such as the Sector, the sub-sector, the date the company was founded or the date it was added to the S&P500.
python
cleaned_df = (
    df
    .query("~company_summary.isnull()")
    .assign(
        date_founded = lambda x: x['Founded'].str.replace('\(.*\)|/.*', '', regex = True).astype(int),
        date_added = lambda x: pd.to_datetime(x['Date added'], errors='ignore') 
    )
    [['Security', 'GICS Sector', 'GICS Sub-Industry', 'date_founded', 'date_added', 'company_summary']]
    .dropna()
    .reset_index(drop=True)
)

documents = cleaned_df['company_summary'].tolist()
ids = cleaned_df.index.astype(str).tolist()
metadata = cleaned_df.drop('company_summary', axis = 1).to_dict(orient = 'records')
Copy
Now that we have this information, let’s add it to our vector database. Important, for each document you have to create an embedding, so it can take a while:

undefined
collection.add(
     ids = ids,
     documents=documents,
     metadatas=metadata
)
Copy
We already have the documents created. If instead of documents we wanted to add vectors the approach would be the same, but passing a list of vectors to the embeddings parameter, instead of the documents parameter.

Okay, now that we know how we can insert documents into our Chroma vector database, let’s see how we can query the database.

How to query our Chroma database to get the closest matching vectors
Now that we have our data uploaded, we can search for the n documents that most resemble text or embedding. To do this, we’ll use the query method of our collection. This method allows receiving the following parameters:

query_texts: input in text format on which we want to find similar vectors.
query_embeddings: input in vector format over which we want to find similar vectors.
n_results: Number of results to be returned by the search.
where: Filter vectors based on metadata.
where_document: Filter vectors based on which documents contain specific content.
include: what the search should return. By default it returns all available information: (“metadatas”, “documents”, “distances”).
So, let’s extract the documents that most closely resemble the prompt phone manufacturer:

python
results = collection.query(
    query_texts="phone manufacturers", 
    n_results=5
)

results
Copy
python
{'ids': [['375', '62', '124', '48', '314']],
 'distances': [[1.03172767162323,
   1.1286187171936035,
   1.164528250694275,
   1.1696319580078125,
   1.1702216863632202]],
 'embeddings': None,
 'metadatas': [[{'Security': 'Qualcomm',
    'GICS Sector': 'Information Technology',
    'GICS Sub-Industry': 'Semiconductors',
    'date_founded': 1985,
    'date_added': '1999-07-22'},
   {'Security': 'Best Buy',
    'GICS Sector': 'Consumer Discretionary',
    'GICS Sub-Industry': 'Computer & Electronics Retail',
    'date_founded': 1966,
    'date_added': '1999-06-29'},
   {'Security': 'Corning Inc.',
    'GICS Sector': 'Information Technology',
    'GICS Sub-Industry': 'Electronic Components',
    'date_founded': 1851,
    'date_added': '1995-02-27'},
   {'Security': 'AT&T',
    'GICS Sector': 'Communication Services',
    'GICS Sub-Industry': 'Integrated Telecommunication Services',
    'date_founded': 1983,
    'date_added': '1983-11-30'},
   {'Security': 'Motorola Solutions',
    'GICS Sector': 'Information Technology',
    'GICS Sub-Industry': 'Communications Equipment',
    'date_founded': 1928,
    'date_added': '1957-03-04'}]],
 }
Copy
As we can see, before this search, the database has returned the companies Qualcomm, AT&T, Motorola Solutions, Best Buy and T-Mobile US. Although it is true that in reality they are not companies that manufacture their own phones in all cases, they are companies that are closely related to it.

The quality of the responses we obtain will depend to a large extent both on the prompt we introduce and on the operation of the model used to create the embeddings.

So we could filter the results to only include companies whose GICS Sector is Information Technology. Let’s see:

bash
collection.query(
    query_texts="phone manufacturers", 
    n_results=5, 
    where = {'GICS Sector': 'Information Technology'}
)
Copy
python
{'ids': [['375', '124', '314', '373', '333']],
 'distances': [[1.03172767162323,
   1.164528250694275,
   1.1702216863632202,
   1.1854088306427002,
   1.2617770433425903]],
 'embeddings': None,
 'metadatas': [[{'Security': 'Qualcomm',
    'GICS Sector': 'Information Technology',
    'GICS Sub-Industry': 'Semiconductors',
    'date_founded': 1985,
    'date_added': '1999-07-22'},
   {'Security': 'Corning Inc.',
    'GICS Sector': 'Information Technology',
    'GICS Sub-Industry': 'Electronic Components',
    'date_founded': 1851,
    'date_added': '1995-02-27'},
   {'Security': 'Motorola Solutions',
    'GICS Sector': 'Information Technology',
    'GICS Sub-Industry': 'Communications Equipment',
    'date_founded': 1928,
    'date_added': '1957-03-04'},
   {'Security': 'Qorvo',
    'GICS Sector': 'Information Technology',
    'GICS Sub-Industry': 'Semiconductors',
    'date_founded': 2015,
    'date_added': '2015-06-11'},
   {'Security': 'Nvidia',
    'GICS Sector': 'Information Technology',
    'GICS Sub-Industry': 'Semiconductors',
    'date_founded': 1993,
    'date_added': '2001-11-30'}]],
 }
Copy
As you can see, in this case, it has only returned information from companies in that sector. This would be the equivalent of an exact match search. However, this is not the only type of filtering that can be done. Specifically, there are the following operators:

$eq: equal to (previously used).
$ne: not equal to.
$gt: greater than.
$gte: greater than or equal to.
$lt: less than.
$lte: less than or equal to.
It is important not to forget the $ symbol, otherwise the query will not work.

Also, if we want several conditions to be applied (either one of the two or both at the same time), we must include the filter in a dictionary with the operator $or or the operator $and.

So, let’s apply the same query to companies in the Information Technology sector but, in addition, their creation date is greater than 1990.

bash
where_clause = {
    "$and" : [
        {"GICS Sector" : {"$eq": "Information Technology"}}, 
        {"date_founded": {"$gte": 1990}}
    ]
}

results = collection.query(
    query_texts="phone manufacturers", 
    n_results=5, 
    where = where_clause
)

[(el['Security'], el['GICS Sector'], el['date_founded']) for el in results['metadatas'][0]]
Copy
python
[('Qorvo', 'Information Technology', 2015),
 ('Nvidia', 'Information Technology', 1993),
 ('ON Semiconductor', 'Information Technology', 1999),
 ('Palo Alto Networks', 'Information Technology', 2005),
 ('Arista Networks', 'Information Technology', 2004)]
Copy
Likewise, we could also add filters, such as that the document contains a specific word, such as Apple. Let’s try:

bash
results = collection.query(
    query_texts="Phone", 
    n_results=5, 
    where = {"GICS Sector" : {"$eq": "Information Technology"}},
    where_document= {"$contains": "Apple"}
)

queried_companies = [el['Security'] for el in results['metadatas'][0]]
queried_companies
Copy
python
['Corning Inc.', 'Microsoft', 'Apple Inc.', 'ON Semiconductor', 'Adobe Inc.']
Copy
Finally we are going to check if, indeed, these companies have the word Apple in their description:

python
(
    cleaned_df
    .query('Security in @queried_companies')
    .assign(
        contains_apple = lambda x: x['company_summary'].str.contains('Apple')
    )
    [['Security', 'contains_apple']]
)
Copy
Security	contains_apple
7	Adobe Inc.	True
42	Apple Inc.	True
124	Corning Inc.	True
303	Microsoft	True
339	ON Semiconductor	True
As you can see, indeed, all the companies that it returns actually have the word “Apple” in their description.