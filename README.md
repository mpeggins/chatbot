# Gemini RAG Chatbot - Version 6

The project is a progressively complex display of how to build a Retrieval-Augmented Generation (RAG) chatbot using the Google Gemini API.

## v6 Updates:

This is version 6 of the project, focusing on improving data ingestion and document processing, and further improving chunking capabilities.

We have expanded the capabilities of our ingestion pipeline to automatically handle various file formats and dynamically process entire directories of documents.

### Key Concepts Highlighted

*   **Multi-Document Ingestion:** Developed a robust ingestion function capable of handling lists of multiple files and URLs. This significantly streamlines the process of adding large amounts of data to the vector database.
*   **Dynamic File Type Handling:** The ingestion pipeline now intelligently identifies file extensions (e.g., `.txt`, `.pdf`, `.csv`, `.docx`) and automatically selects the appropriate LangChain document loader for each specific type.
*   **Parent-Child Chunking:** We moved away from manual recursive character chunking and implemented an advanced retrieval strategy called Parent-Child Chunking. This involves splitting documents into smaller "child" chunks for highly accurate vector search, but retrieving the larger "parent" chunks to provide the LLM with broader, more useful context.
*   **LangChain Integration:** We integrated `langchain` libraries to build our "librarian" (the Retriever) located in `shared.py`. This powerful abstraction simplifies the complex process of document storage, retrieval, and managing the relationships between parent and child chunks.
*   **Centralized Retriever:** The retriever logic is now modularized in `shared.py` and actively called in both `ingest.py` (to save documents) and `main.py` (to search documents), keeping the code clean and DRY (Don't Repeat Yourself).
*   **Configuration Management:** Added an `app_config.py` file to centralize our models, database names, and file paths. This provides consistency across the project and makes future updates much easier.

---

## How to Run

Follow these steps to set up and run your custom RAG chatbot.

### 1. Install Dependencies
Make sure you have all the required Python packages installed. Run the following command in your terminal:
```bash
pip install -r requirements.txt
```

### 2. Set Up Your API Key
Create a new file named `.env` in the root directory of the project. Add your Gemini API key to this file like so:
```env
GEMINI_API_KEY="your_actual_api_key_here"
```

### 3. Customize Your Bot's Persona
Navigate to the `data/` folder and open the `system_prompt.txt` file. Update the instructions inside to define how you want your chatbot to behave and respond.

### 4. Provide Your Data
You need to provide the information the chatbot will use as its knowledge base.
*   **Local Files:** Place your documents into the `data/` folder. Supported formats include: `.txt`, `.pdf`, `.docx`, `.csv`, `.xlsx`.
*   **Update Ingestion Script:** Open `ingest.py`. Locate the `sources_to_ingest` list and add the paths to your local files or paste any relevant URLs directly into the list.

### 5. Configure Chunking Preferences (Optional)
If you want to fine-tune how your documents are split before saving them to the database, open `shared.py` and locate the `get_retriever()` function. Here, you can adjust the `chunk_size` and `chunk_overlap` parameters for both the `parent_splitter` and `child_splitter` to better suit the structure of your specific data.

### 6. Ingest (Chunk and Embed) Your Documents
Run the ingestion script. This will read your documents, split them into chunks, create embeddings using the Gemini API, and save them to your local `chroma_db` database.
```bash
python ingest.py
```
*(Note: You only need to run this when you add or update documents in your `data` folder.)*

### 7. Start the Chatbot
Run the main script to start the interactive chat interface in your terminal.
```bash
python main.py
```
Type your questions to chat with your documents. To exit the program, simply type `quit`.