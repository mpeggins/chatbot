from google import genai

# Setup Environment
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

# Initialize the client (i.e. Gemini)
client = genai.Client(api_key=api_key)
