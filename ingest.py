from chromadb import Documents, EmbeddingFunction, Embeddings
from google.api_core import retry
from google.genai import types

from shared import client

# View which embedding models are available
for m in client.models.list():
    if "embedContent" in m.supported_actions:
        print(m.name)

DOCUMENT1 = "Micheal is the greatest chatbot teacher of all time."
DOCUMENT2 = "Micheal's favorite color is green."
DOCUMENT3 = "Building a RAG chatbot in 2026 is as relevant as building a website in 1996."

documents = [DOCUMENT1, DOCUMENT2, DOCUMENT3]

# Define a helper to retry when per-minute quota is reached.
is_retriable = lambda e: (isinstance(e, genai.errors.APIError) and e.code in {429, 503})

# Creating the embedding database with ChromaDB
class GeminiEmbeddingFunction(EmbeddingFunction):
    # Specify whether to generate embeddings for documents, or queries
    document_mode = True

    @retry.Retry(predicate=is_retriable)
    def __call__(self, input: Documents) -> Embeddings:
        MODEL_ID = "models/gemini-embedding-001"

        if self.document_mode:
            embedding_task = "retrieval_document"
        else:
            embedding_task = "retrieval_query"

        response = client.models.embed_content(
            model=MODEL_ID,
            contents=input,
            config=types.EmbedContentConfig(
                task_type=embedding_task,
            ),
        )
        return [e.values for e in response.embeddings]


# This is the name of the FAQ database
DB_NAME = "chatbot_class_faqs"