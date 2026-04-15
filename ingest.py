import os
import pandas as pd

from langchain_core.documents import Document
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    CSVLoader,
    Docx2txtLoader,
    WebBaseLoader
)

from app_config import base_dir, CHROMA_FOLDER, PARENT_DATA_FOLDER
from shared import get_retriever


# --- Create folders if they don't exist --- #


for folder in [CHROMA_FOLDER, PARENT_DATA_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)


# --- Load Documents Logic --- #


def get_raw_docs(path):
    """Loads a file but DOES NOT chunk it yet."""
    ext = os.path.splitext(path)[1].lower()

    if path.startswith(('http://', 'https://', 'www.')):
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


# --- Run the Ingestion --- #


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
        raw_data = get_raw_docs(source)
        retriever = get_retriever()
        retriever.add_documents(raw_data)

        print(f"✅ Successfully added: {source}\n")

    except Exception as e:
        print(f"❌ Uh oh, skipped {source}. Error: {e}\n")

print("All done! Your hierarchical database is ready.")