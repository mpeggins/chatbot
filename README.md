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

 ### Retrieval (Search)
 
 Once the query is rewritten and embedded, the system searches the ChromaDB vector database. It compares the numbers and pulls out the documents that are mathematically closest to the search query. 
 
 ### Augmented Generation
 
 Finally, we take the original text from those retrieved documents and "augment" (combine) it with the user's original query. We send this combined prompt to the LLM. By forcing the LLM to look at our retrieved context, it can confidently answer questions about our custom data without hallucinating!
 
 ## How to Run
 
 1. **Install Dependencies**  
    Make sure you have all the required Python packages installed. Run the following command in your terminal:
    ```sh
    pip install -r requirements.txt
    ```
 
 2. **Set up your API Key**  
    Create a new file named `.env` in the root directory of the project. Add your Gemini API key to this file like so:
    ```env
    GEMINI_API_KEY="your_actual_api_key_here"
    ```
 
 3. **Start the Chatbot**  
    Run the main script to start chatting. (Note: Because we are using an in-memory database for this version, running this script will automatically ingest the documents into RAM for you).
    ```sh
    python main.py