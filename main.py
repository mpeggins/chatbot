import os

from google.genai import types

from shared import client, get_retriever
from app_config import CHAT_MODEL


# SYSTEM PROMPT
def load_system_prompt():
    base_dir = os.path.dirname(__file__)
    prompt_path = os.path.join("data", "system_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

system_instruction = load_system_prompt()

# RAG / LLM CONFIG
rag_config = types.GenerateContentConfig(
    temperature=0.6,          # Controls creativity
    max_output_tokens=1000,    # Hard stop limit
    system_instruction = system_instruction     # Added System Instruction
)


# --- Initialize the Librarian --- #
retriever = get_retriever()


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
            model=CHAT_MODEL,
            contents=rewrite_prompt
        )
        search_query = rewrite_response.text.strip()

    # --- 2: Search the Database ---
    # We ask the Librarian to find the documents. It handles the child-to-parent swap automatically.
    retrieved_docs = retriever.invoke(search_query)

    # Extract the actual text content from the LangChain Document objects
    all_passages = [doc.page_content for doc in retrieved_docs]

    # Join them together with a clear separation
    context_text = "\n\n---\n\n".join(all_passages)

    # --- 3: Final Answer Generation ---
    # We send the ORIGINAL query to the bot so it feels natural,
    # but we give it the context found using the rewritten query.
    final_prompt = f"""Answer the user's question. 
        Use the REFERENCE TEXT below to inform your answer. If the REFERENCE TEXT does not contain the answer, just respond normally using your system persona.
        
        REFERENCE TEXT: {context_text}
        USER QUESTION: {user_query}"""

    # We include chat_history so it remembers the "vibe" and previous facts
    response = client.models.generate_content(
        model=CHAT_MODEL,
        config=rag_config,
        contents=chat_history + [{"role": "user", "parts": [{"text": final_prompt}]}]
    )

    # --- 4: Update History ---
    # IMPORTANT: We save the ORIGINAL question and the answer.
    # We do NOT save the chunks or the rewritten search query in the history.
    print(f"Assistant: {response.text}")
    chat_history.append({"role": "user", "parts": [{"text": user_query}]})
    chat_history.append({"role": "model", "parts": [{"text": response.text}]})