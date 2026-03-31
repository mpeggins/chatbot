The project is a progressively complex display of how to build a RAG chatbot using a Gemini API.

## v4 Updates:

This is version 4 of the project. This is our first implementation of RAG.

In this version, we build a chatbot that can chat with us about custom information, more than just making an API call.

There are several large changes. 

### Chunk Sizes
How to determine chunk sizes

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,     # Maximum number of characters per chunk
        chunk_overlap=25,   # Number of characters to overlap between chunks
        length_function=len # How we measure length (standard character count)
    )

 ## How to Run
 
 1. **Install Dependencies**  
    Make sure you have all the required Python packages installed. Run the following command in your terminal:
    ```sh
    pip install -r requirements.txt
    ```
 
 2. **Set up your API Key**  
    Create a new file named `.env` in the root directory of the project. Add your Gemini API key to this file like so:
    ```env
    GEMINI_API_KEY="your_actual_api_key_here"
    ```
 
 3. **Start the Chatbot**  
    Run the main script to start chatting. (Note: Because we are using an in-memory database for this version, running this script will automatically ingest the documents into RAM for you).
    ```sh
    python main.py