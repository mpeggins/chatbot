This project demonstrates how to build a simple chatbot using a Gemini API.

## Updates:

This is version 3 of the project.

In the previous version, we used Gemini's native chat feature in order to have an iterative back and forth conversation with the model.

This approach is strong if you want to use Gemini's existing knowledge base. Unfortunately, it does not work for RAG (i.e. using your own data).

In this version of the project, we update the code to establish a chat_history list that appends the user's queries, the bot's responses, and the complete chat history.

