import os
import pickle
import pandas as pd
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    CSVLoader,
    Docx2txtLoader,
    WebBaseLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.retrievers import ParentDocumentRetriever
from langchain_classic.storage import LocalFileStore, EncoderBackedStore
from langchain_community.vectorstores import Chroma
from langchain_core.embeddings import Embeddings
from shared import DB_NAME, GeminiEmbeddingFunction



# --- 1. CONFIGURATION ---
base_dir = os.path.dirname(__file__)
# This is the FOLDER where the database files live
CHROMA_FOLDER = os.path.join(base_dir, "chroma_db")
# This is the FOLDER where the large Parent chunks live
PARENT_DATA_FOLDER = os.path.join(base_dir, "parent_chunks")

# Create folders if they don't exist
for folder in [CHROMA_FOLDER, PARENT_DATA_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# --- 2a. EMBEDDING ADAPTER ---
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

# --- 2b. SETTING UP THE "LIBRARY" (Storage) ---

# We use the LangChain 'Chroma' wrapper because it knows how to talk to the 'Retriever'
embed_fn = LangChainEmbeddingAdapter(GeminiEmbeddingFunction())

vectorstore = Chroma(
    collection_name=DB_NAME,  # Consistent with shared.py!
    embedding_function=embed_fn,
    persist_directory=CHROMA_FOLDER
)

# This saves the full "Parent" text to your hard drive
fs = LocalFileStore(PARENT_DATA_FOLDER)
# This uses pickle to translate the complex documents into bytes for the hard drive
store = EncoderBackedStore(
    store=fs,
    key_encoder=lambda x: x,
    value_serializer=pickle.dumps,
    value_deserializer=pickle.loads,
)

# --- 3. THE "LIBRARIAN" (Retriever) ---

# Define our two levels of splitting
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
child_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)

retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
)


# --- 4. THE LOADING LOGIC ---

def get_raw_docs(path):
    """Loads a file but DOES NOT chunk it yet."""
    ext = os.path.splitext(path)[1].lower()

    if path.startswith(('http://', 'https://')):
        return WebBaseLoader(path).load()

    if ext == '.txt':
        loader = TextLoader(path, encoding='utf-8')
    elif ext == '.pdf':
        loader = PyPDFLoader(path)
    elif ext == '.docx':
        loader = Docx2txtLoader(path)
    elif ext == '.csv':
        loader = CSVLoader(path)
    elif ext == '.xlsx':
        df = pd.read_excel(path)
        df = df.dropna(how='all')  # Clean up empty rows
        documents = []
        for index, row in df.iterrows():
            # Stitch the row headers and values together
            row_text = " | ".join([f"{col}: {val}" for col, val in row.items() if pd.notna(val)])
            # Create the LangChain Document object manually
            doc = Document(page_content=row_text, metadata={"source": path, "row": index})
            documents.append(doc)
        return documents
    else:
        raise ValueError(f"Unknown format: {ext}")

    return loader.load()


# --- 5. RUNNING THE INGESTION ---

# List of items to ingest (Add your files and links here!)
sources_to_ingest = [
    os.path.join(base_dir, "data", "MP FAQs.txt"),
    # You can add more like this:
    # os.path.join(base_dir, "data", "menu.pdf"),
    # "https://www.example.com/about-us"
]

for source in sources_to_ingest:
    print(f"Feeding the Librarian: {source}...")

    try:
        # 1. Route the file/link to the correct loader
        raw_data = get_raw_docs(source)

        # 2. The Librarian creates the big parents, tiny children, and saves them
        retriever.add_documents(raw_data)

        print(f"✅ Successfully added: {source}\n")

    except Exception as e:
        print(f"❌ Uh oh, skipped {source}. Error: {e}\n")

print("All done! Your hierarchical database is ready.")