# database.py
## function: verify_create_database()
- Takes no value.
- Teturns no value.
- Checks if the database directory and file exist and creates if not.
- Requires endpoint.

# bright_memory.py
## function: form_bright_memory()
- Takes user_prompt: str, prompt_context_history: str.
- Returns a string containing only the distilled portions of prompt_context_history that are directly relevant and helpful to the user_prompt.
- Return value used for new embedding of a 'bright memory' allowing the system to refined prompt/memory pairs and learn from experience over time.
- Requires endpoint.

# embedV3.py
## function: add_to_index(index_filename: str, text: str, status: str = "NONE") -> None
- Parameters:
    index_filename: str. The name of the Faiss index file.
    text: str, The text block to be added to the index.
    status: str (optional) An optional status flag that can be set to "ACCEPTED" or "DELETED". 
                            By default, it's set to "NONE".
- Responsible to chunk, vectorize, embed, collate with SQL db full text store of full text block.
- Uses local pretrained model intfloat/e5-large-v2.
- Uses local SQL3 db to store full text.
- Requires endpoint.
## function: timestamp()
- takes no value.
- returns str.
- returns a string containing a system timestamp accurate to 1/1000 second.
- Timestamp may be used to order text blocks returned from queries chronologically.
- Does not require endpoint.
## function: load_text(filename: str)
- Takes str of filename.
- Returns utf-8 encoded str of file contents.
- Used to read files for embedding by add_to_index(). Not currently used, but will be implemented as a drag-and-drop feature of the user interface to add documents to the index for rapid memory creation.
- Usage would be: add_to_index("index", load_text("file.txt"), "ACCEPTED")
- The ACCEPTED attribute tells the system the contents consist of vital memories.
- Requires endpoint. Return value will indicate successful embedding (after function is refactored)

# queryV3.py
## function: query_index(index_filename: str, query_text: str, top_k=2)
- Takes index_filename: str, query_text: str, top_k=2: int.
- Returns str containing chronologically sorted full text query results from SQL db after near neighbour search of index.
- Number of nearest neighbours to return is set by top_k (default is 2).
- Requires endpoint.

# retrieve_text.py
## get_full_text(db_path, block_id)
- Takes db_path: str, block_id: str.
- Returns full text located at block_id in SQL db.
- Called by queryV3.py
- Does not require endpoint.

# task_list.py
## function: prompt_task_list(user_input: str)
- Takes user_input str, which is the user's current prompt.
- Returns str, which contains a task and sub-task list.
- This module is currently not in use. It requires refactoring to only be run when the user presses the "Create Task List" button in the user interface. Also, rather than only the user prompt being used as a foundation for the Task List, the prompt plus the prior 1000 word chat_history should be used together to formulate the Task List.
- Requires endpoint.

# user_ner_re.py
The only function to call programmatically is add_edit_ner_re()
## function: add_edit_ner_re(user_prompt)
- Takes str, containing current user prompt
- Returns str, containing an edited version of user_information.txt adding an new or modified entity and/or relationship information about or related to the user contained in the user's prompt. If no such information exists there the function returns a number (as a string) representing where it exited the algorithm without finding anything.
- Requires endpoint.
## function: get_ner_re(user_prompt)
- Takes str, containing current user prompt
- Returns str, containing the consolidated string resulting from the entity / relationship information from the prompt and the existing user_information.txt file, outputing the new string back to the user_information.txt file.
- This function is never called directly. Rather, it is only called by add_edit_ner_re().
- Does not require endpoint.

# test_index_function.py AND unittest_index_functions.py
## These files conduct unit testing on the embedding, database and retrieval operations.
- Usage of unit testing is described in main.py. This use of these modules will need to be removed from main.py and placed elsewhere.
- Unit testing is currently DESTRUCTIVE of any existing index, database files! This must be refactored to use a generic dataset for testing that is non-destructive of existing data which could be rather valuable at the time of testing.
- Does not require endpoint.

# main.py
## class ChatSession
- Defines the main chat session class, which creates a chat session loop with the function main(). Unit testing code is commented out in main() with instructions on how to implement.
- User interface on start executes verify_create_database() and executes this loop automatically.
- Requires endpoint?






