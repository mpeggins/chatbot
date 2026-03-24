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

# Create specific configuration for the chat

model_config = types.GenerateContentConfig(
    temperature=0.5,          # Controls creativity
    max_output_tokens=300,    # Hard stop limit
    top_p=0.95,               # Optional: controls diversity
    top_k=40                  # Optional: controls filtering
)

# Establish a chat session
chat = client.chats.create(model='gemini-2.5-flash-lite',
                           config=model_config,
                           history=[])

# Chat loop
while True:
    prompt = input('User: ')
    if prompt.strip().lower() == 'quit':      # Allows the user to quit the chat by typing "quit"
        break
    else:
        response = chat.send_message(prompt)
        print(response.text)