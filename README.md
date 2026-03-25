The project is a progressively complex display of how to build a RAG chatbot using a Gemini API.

## v3 Updates:

This is version 3 of the project.

In the previous version, we used Gemini's native chat feature in order to have an iterative back and forth conversation with the model.

This approach is strong if you want to use Gemini's existing knowledge base. Unfortunately, it does not work for RAG (i.e. using your own data).

In this version of the project, we update the code to establish a chat_history list that appends the user's queries, the bot's responses, and the complete chat history.

### chat_history

This is the biggest modification to the code. 

In the previous version we used this:

    chat = client.chats.create(...)

This uses Gemini's SDK to instantiate a multi-turn conversation (i.e. chat). This will eventually cause a problem when we update to RAG. So the new change is adding a chat_history variable that begins as an empty list. 

It is also important to note that we updated the client code to:

    bot_response = client.models.generate_content(...)

After the user's query is received, we append the user_query to chat_history. Once a response is received from the model, we also append bot_response to chat_history.

With each query, we send the entire chat_history. The reason for this method is that using the *generate_content* function sends a one-off query to the LLM and this is how the model retains a working memory of the entire conversation.

### system_instruction

In this version of the code, I also implemented a system instruction for the model configuration. This guides the model on how you want it to respond. You can provide simple or extremely detailed information here.
