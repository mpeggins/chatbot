import os
import pickle

from dotenv import load_dotenv

from google import genai
from google.api_core import retry
from google.genai import types

from chromadb import Documents, EmbeddingFunction

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.retrievers import ParentDocumentRetriever
from langchain_classic.storage import LocalFileStore, EncoderBackedStore
from langchain_community.vectorstores import Chroma
from langchain_core.embeddings import Embeddings

from app_config import DB_NAME, CHROMA_FOLDER, PARENT_DATA_FOLDER, EMBEDDING_MODEL

# Setup Environment
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

# Initialize the client (i.e. Gemini)
client = genai.Client(api_key=api_key)



# --- Gemini Embedding Function used for Document AND Query Embeddings --- #



# Define a helper to retry when per-minute quota is reached.
is_retriable = lambda e: (isinstance(e, genai.errors.APIError) and e.code in {429, 503})

class GeminiEmbeddingFunction(EmbeddingFunction):
    # Specify whether to generate embeddings for documents, or queries:
    # True for Document Embeddings, False for Query Embeddings.
    def __init__(self, document_mode: bool = True):
        self.document_mode = document_mode

    @retry.Retry(predicate=is_retriable)
    def __call__(self, input: Documents) -> Embeddings:
        # Define the embedding model.
        MODEL_ID = EMBEDDING_MODEL

        # Determine the embedding task type based on the current mode.
        if self.document_mode:
            embedding_task = "retrieval_document"
        else:
            embedding_task = "retrieval_query"

        # Call the Gemini API to generate embeddings for the input documents or queries.
        response = client.models.embed_content(
            model=MODEL_ID,
            contents=input,
            config=types.EmbedContentConfig(
                task_type=embedding_task,
            ),
        )
        # Return the list of embedding values from the response.
        return [e.values for e in response.embeddings]



# --- LangChain Embedding Adapter specifically used for Chunking --- #



class LangChainEmbeddingAdapter(Embeddings):
    """Adapts our Chroma-style embedding function to work with LangChain."""
    def __init__(self, chroma_ef):
        self.chroma_ef = chroma_ef

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        self.chroma_ef.document_mode = True
        return self.chroma_ef(texts)

    def embed_query(self, text: str) -> list[float]:
        self.chroma_ef.document_mode = False
        # Chroma returns a list of results; we just need the first one for a single query
        return self.chroma_ef([text])[0]



# --- Setting Up the Library --- #



def get_retriever():
    """
    Builds and returns the ParentDocumentRetriever.
    This acts as the single source of truth for database connections.
    """
    # 1. Define Splitters
    parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    child_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)

    # 2. Setup Embeddings
    # Wraps your custom Gemini function in the LangChain adapter
    lc_embed_fn = LangChainEmbeddingAdapter(GeminiEmbeddingFunction())

    # 3. Setup VectorStore (Stores the small CHILD chunks for fast searching)
    vectorstore = Chroma(
        collection_name=DB_NAME,
        embedding_function=lc_embed_fn,
        persist_directory=CHROMA_FOLDER
    )

    # 4. Setup Document Store (Stores the large PARENT chunks for context)
    # This uses pickle to translate the complex documents into bytes for the hard drive
    fs = LocalFileStore(PARENT_DATA_FOLDER)
    store = EncoderBackedStore(
        store=fs,
        key_encoder=lambda x: x,
        value_serializer=pickle.dumps,
        value_deserializer=pickle.loads
    )

    # 5. Combine them into the Retriever
    retriever = ParentDocumentRetriever(
        vectorstore=vectorstore,
        docstore=store,
        child_splitter=child_splitter,
        parent_splitter=parent_splitter,
    )

    """
    By default, LangChain will return the top 4 relevant chunks.
    For more control, you could put this line at the end of retriever:
    search_kwargs={"k": 5}
    The number specified will be the amount of returned chunks.
    """

    return retriever