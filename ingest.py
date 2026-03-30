import chromadb
from google import genai
from shared import DB_NAME, GeminiEmbeddingFunction

# --- Manually defining documents. In a later version of the project, we will use actual files. ---

DOCUMENT1 = "Micheal is the greatest chatbot teacher of all time."
DOCUMENT2 = "Micheal's favorite color is green."
DOCUMENT3 = "Building a RAG chatbot in 2026 is as relevant as building a website in 1996."

documents = [DOCUMENT1, DOCUMENT2, DOCUMENT3]

# --- Define the Vector Database where document embeddings will live. ---

embed_fn = GeminiEmbeddingFunction()
embed_fn.document_mode = True

# Define the main path for the vector database.
chroma_client = chromadb.Client()
# chroma_client = chromadb.PersistentClient(path="./chroma_db")
db = chroma_client.get_or_create_collection(
    name=DB_NAME,
    embedding_function=embed_fn
)

# Add documents to the vector database.
db.add(
    documents=documents,
    ids=[str(i) for i in range(len(documents))]
)