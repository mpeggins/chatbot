import chromadb
from shared import DB_NAME, GeminiEmbeddingFunction
from langchain_text_splitters import RecursiveCharacterTextSplitter

# --- Manually defining documents. In a later version of the project, we will use actual files. ---

DOCUMENT1 = "Micheal is the greatest chatbot teacher of all time."
DOCUMENT2 = "Micheal's favorite color is green."
DOCUMENT3 = "Building a RAG chatbot in 2026 is as relevant as building a website in 1996."

documents = [DOCUMENT1, DOCUMENT2, DOCUMENT3]

# --- Recursive Character Chunking

# Initialize the text splitter with our chunking rules
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,     # Maximum number of characters per chunk
    chunk_overlap=25,   # Number of characters to overlap between chunks
    length_function=len # How we measure length (standard character count)
)

# Convert "documents" into a single string and send it to the splitter
raw_text = "\n".join(documents)
chunks = text_splitter.split_text(raw_text)

# Optional: Print out the results to make sure it worked.
# print(f"Total chunks created: {len(chunks)}\n")

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

# Add chunks to the vector database.
# In previous example, we used documents=documents. Note that we updated that to documents=chunks.
db.add(
    documents=chunks,
    ids=[str(i) for i in range(len(chunks))]
)