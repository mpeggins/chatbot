from google.genai import types
# import chromadb
from shared import client, DB_NAME, GeminiEmbeddingFunction
from ingest import chroma_client # Use only for temporary local runs

# Define System Instructions for LLM
# This is important to modify this to your need.
system_instruction = """
You are a helpful assistant. Your name is Todd.
"""

# Create specific configuration for the chat
rag_config = types.GenerateContentConfig(
    temperature=1.0,          # Controls creativity
    max_output_tokens=1000,    # Hard stop limit
    system_instruction = system_instruction     # Added System Instruction
)

# Switch to query mode when generating query embeddings.
embed_fn = GeminiEmbeddingFunction()
embed_fn.document_mode = False

# Connect to the SAME folder in ingest.py
# chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Access the collection
# Note: We use .get_collection here instead of .get_or_create
# This ensures we are talking to the data we just uploaded!
db = chroma_client.get_collection(
    name=DB_NAME,
    embedding_function=embed_fn
)

# Establish an empty chat history
chat_history = []

while True:
    user_query = input("User: ")
    if user_query.strip().lower() == 'quit':      # Allows the user to quit the chat by typing "quit"
        break
    search_query = user_query

    # --- 1: Query Rewriting ---
    # Query rewriting helps transform the user's query to a more appropriate vector search.
    if len(chat_history) > 0:
        rewrite_prompt = f"""
            Given the following chat history and a new user question, 
            rewrite the question to be a standalone search query that includes all necessary context.
            If the question is already standalone, just return the original text.

            CHAT HISTORY: {chat_history}
            NEW QUESTION: {user_query}
            Standalone Search Query:"""

        # We use a fast call here just to get the search terms
        rewrite_response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=rewrite_prompt
        )
        search_query = rewrite_response.text.strip()

    # --- 2: Search the Database ---
    # Use the rewritten query to find relevant data, not the original user text
    result = db.query(query_texts=[search_query], n_results=1)
    all_passages = result["documents"][0] # Extract just the text
    context_text = "\n".join(all_passages)

    # --- 3: Final Answer Generation ---
    # We send the ORIGINAL query to the bot so it feels natural,
    # but we give it the context found using the rewritten query.
    final_prompt = f"""Answer the user's question. 
        Use the REFERENCE TEXT below to inform your answer. If the REFERENCE TEXT does not contain the answer, just respond normally using your system persona.
        
        REFERENCE TEXT: {context_text}
        USER QUESTION: {user_query}"""

    # We include chat_history so it remembers the "vibe" and previous facts
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        config=rag_config,
        contents=chat_history + [{"role": "user", "parts": [{"text": final_prompt}]}]
    )

    # --- 4: Update History ---
    # IMPORTANT: We save the ORIGINAL question and the answer.
    # We do NOT save the chunks or the rewritten search query in the history.
    print(f"Assistant: {response.text}")
    chat_history.append({"role": "user", "parts": [{"text": user_query}]})
    chat_history.append({"role": "model", "parts": [{"text": response.text}]})