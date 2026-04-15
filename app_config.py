# --- Models ---

CHAT_MODEL = "gemini-2.5-flash"
EMBEDDING_MODEL = "models/gemini-embedding-001"

# --- Database Paths ---

import os
base_dir = os.path.dirname(__file__)
# Database Name for stored vector embeddings.
DB_NAME = "chatbot_class_faqs"
# This is the folder where the database files live
CHROMA_FOLDER = os.path.join(base_dir, "chroma_db")
# This is the folder where the large Parent chunks live
PARENT_DATA_FOLDER = os.path.join(base_dir, "parent_chunks")