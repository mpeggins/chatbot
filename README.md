This project demonstrates how to build a simple chatbot using a Gemini API.

Before starting this project, you must generate an API key from Google's Gemini.

## I. API Integration

Before running your chatbot, you must integrate your API key. 

There are two ways to do this:

### 1. Locally (easier, less secure)

If running locally on your server, you can simply have the following line in your main.py file:

    api_key = "...your api key goes here..."

### 2. Securely in a .env folder

If you would like to run this on a server, be sure to guard your API key and use a .env file.

Here are the steps:

#### a. Create a .env file and place the following code:

    GEMINI_API_KEY = "...your api key goes here..."

#### b. In your main.py file, use the following code:

    import os
    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

#### c. Run the following command in your Terminal:

    pip install python-dotenv

## II. Choosing a Model

For this project, I am using the gemini-2.0-flash-lite model. It is lightweight and cost-efficient. However, it is an older model. If you would like to explore other models, use the following code after you initialize the API key to explore other models:

    for model in client.models.list():
    print(model.name)

## III. Updating the Prompt

Using this method of a chatbot requires you to send a manual prompt. This is currently the most important tool at your disposal. To update it, simply change what's in the quotes after *prompt =*
