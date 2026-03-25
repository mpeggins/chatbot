# imports for Gemini
from google import genai
from google.genai import types      # Allows model configuration

# imports for API
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
#api_key = "...your API key here..."

# Initialize the client (i.e. Gemini)
client = genai.Client(api_key=api_key)

# Define System Instructions for LLM
# This is important to modify this to your need.
system_instruction = """
You are a helpful assistant. Your name is Todd.
"""

# Create specific configuration for the chat
model_config = types.GenerateContentConfig(
    temperature=0.5,          # Controls creativity
    max_output_tokens=300,    # Hard stop limit
    top_p=0.95,               # Optional: controls diversity
    top_k=40,                 # Optional: controls filtering
    system_instruction = system_instruction     # Added System Instruction
)

# Establish an empty chat history
chat_history = []

while True:
    user_query = input("User: ")
    if user_query.strip().lower() == 'quit':      # Allows the user to quit the chat by typing "quit"
        break

    # Append user_query to chat_history
    chat_history.append({"role": "user", "parts": [{"text": user_query}]})

    bot_response = client.models.generate_content(
        model = "gemini-2.5-flash-lite",
        config = model_config,
        contents = chat_history
    )

    print(chat_history)
    print(f"Assistant: {bot_response.text}")

    # Append bot_response to chat_history
    chat_history.append({"role": "model", "parts": [{"text": bot_response.text}]})