# Execution Map
## Map of execution identifying functions running async with one another

### main.py
- verify_create_database() is called once to verify that the database exists
- file names are assigned for the chat history file, and the faiss index file
- chat_session = ChatSession(chat_history_file) # inputs the chat history, if any, from the current-chat-session.txt file by calling load_or_create_chat_history(self) from __init__(self, chat_history_file)
- chat_session = ChatSession(chat_history_file) # creates ChatSession class instance
- chat_session.chat() is called to start the chat session and the below operations happen within chat_session.chat() in a "while TRUE" loop.
- self.get_user_input() handles obtaining and processing the user's prompt
- On return from input() in self.get_user_input() class method, runs these functions ASYNC: self.update_chat_history(), add_edit_ner_re(), add_to_index(), all of which do not depend on the return values from the other functions so are run ASYNC for efficiency. All these calls are in the get_user_input(self) class method which returns a string containing the user's prompt (user_input). All these async functions must be fully completed before proceeding
- self.query_result(self, user_input), queries the index after chunking and vectorizing each sentence of the user's prompt, returns the top 2 nearest neighbours (if any) for each sentence and retrieves the full text blocks from the SQL db for the top 2 nearest neigbours found for each separate sentence (if any). The block_ids of each find are listed chronologically while removing any duplicates. These text blocks are returned from the query_result(self, user_input) class method as a list of the retrieved text blocks in chronological order (strings) as self.prompt_context_history.
- self.get_response(f"{self.load_or_create_chat_history()}") class method takes the user's input and consolidates it into a single string which includes system content and user content in an OpenAI ChatCompletion API call. The user content consists of an fstring consisting of self.chat_history, user_info (from add_edit_ner_re(), date and time, and the user's prompt, formatted as a large super-prompt). This prompt assists the model to the fullest extent possible from the chat history and the index/db while simultaneously serving the prompt itself to the model
- self.display_response(response) formats and displays the model's response
- "While TRUE" loop repeats.




