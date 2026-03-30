The project is a progressively complex display of how to build a RAG chatbot using a Gemini API.

## v4 Updates:

This is version 4 of the project. This is our first implementation of RAG.

In this version, we build a chatbot that can chat with us about custom information, more than just making an API call.

There are several large changes. 

#### Two new Files

For this project, we create two new python files: **ingest.py** and **shared.py**. The **ingest.py** file is designed to take your documents and transform them into *vector embeddings*, numerical representations of your data that the machine can understand (more on that below).

The **shared.py** file contains variables and functions that both **ingest.py** and **main.py** use.

## RAG Overview

Before reviewing the code, it is important to understand what actually happens during RAG.

First, RAG stands for _Retrieval Augmented Generation_. It is the process of mathematically defining your data and comparing it to a query. Let's take a look at the steps:

### Document Embeddings

Machines cannot read text. So, we must convert our files into something the machines can understand: numbers! Specifically, a long string of numbers called vector embeddings. These are mathematical representations of your data. 

When developing a RAG chatbot, we must first transform our documents into embeddings. 

The Document Embedding function is defined in ingest.py. It is called when running main.py. We will change this specific architecture in a later version. 

All that is important to understand at this stage is that this changes your text to numbers.

#### Documents

Before we continue, just a quick note on Documents. For this version of the chatbot, we are manually defining the documents as strings of text. In a later version, we will learn about "chunking" where we can upload an actual file and transform it into chunks of information for the model to embed.

### Vector Database

Once the system embeds the data, it must store those embeddings. For this project, we use chromadb as our *vector database*.

### Query Embedding

At this point, the model has embedded our documents and stored those embeddings in a vector database.

Now, the model must take our query, embed the query, and compare it to the document embeddings in the database. It will find the most mathematically related information related to your query.

#### Query Rewriting

A user's query might not always be phrased appropriately in order to make a mathematically accurate comparison search. The query might be too vague or even too wordy. It might use terms that aren't even in the source documents.

As a solution, before comparing the query embedding to the vector database, we first send the user's query to an LLM for a rewrite that will maximize the best retrieval possibilities.


### How to Run

python main.py