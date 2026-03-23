# imports for Gemini
from google import genai

# imports for API
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
#api_key = ""

client = genai.Client(api_key=api_key)

# You can explore different models here:
# for model in client.models.list():
#     print(model.name)

prompt = "Explain AI to me like I'm a kid."

response = client.models.generate_content(
    model = "gemini-2.0-flash-lite",
    contents = prompt)

print(response.text)