from google import genai
from chromadb import Documents, EmbeddingFunction, Embeddings
from google.api_core import retry
from google.genai import types

# Setup Environment
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

# Define Database Name for stored vector embeddings.
DB_NAME = "chatbot_class_faqs"

# Initialize the client (i.e. Gemini)
client = genai.Client(api_key=api_key)

# View which embedding models are available
# for m in client.models.list():
#     if "embedContent" in m.supported_actions:
#         print(m.name)

# --- Embedding Function used for Document and Query Embeddings --- #

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
        MODEL_ID = "models/gemini-embedding-001"

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