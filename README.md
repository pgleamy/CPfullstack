ChatPerfect (pre-alpha)
Patrick Leamy, pgleamy@gmail.com (January 30, 2024)

This is an unfinished Windows chatbot I wrote over the last 8-9 months. I have not worked on it for a while. I am not a programmer! More of an enthusiast tinkerer/hacker. My son tells me my code gives him nightmares. He would know and I do believe him. I wanted to get some experience with AI, programming and full stack application development through self teaching and experimentation. Initially I wrote the chat engine in Python as a command line program. Then I moved to creating a Widows interface for it. So this is somewhat of a Frankenstein. The frontend uses Svelte, running on a Tauri (Rust) backend. The Python chat engine runs in a Rust thread under Tauri and communicates with the frontend through various monitored files. There are likely a million ways to do this correctly/better, and I believe I may have avoided all or most of them. But I did learn a lot in the process! I was learning literally everything as I went along. I don't want to work on it any longer. So if the code and/or ideas here are useful to someone else, then it was worth it on top of everything I learned. If you find any of this mess useful drop me a star or a quick email.

The "main" branch is 117 commits behind the "UI-Reconfiguration-/-Beautification branch"! The most recent code is on the UI-Reconfiguration-/-Beautification branch. Ignore the main branch. I won't be merging them or adding more commits to either branch. There are several extraneous directories throughout with some "IDEAS" or backups etc. Those can be ignored unless you are curious.

Features of the Chat Engine (src/backend & src/backend/messages. IGNORE the src/users director because the application now uses the correct Windows user directory for all data):

* asyncronous Python.
* embeds all chat interactions to a vector store (FAISS/HNSW), with cross referenced full text saved to a mySQL database.
* uses a very simple RAG (retrieval augmented generation) implementation to retrieve relevant contents from past interactions and insert them into the prompt context.
* the vector store and database run 100% locally, including the vector embedding model. So all of that is private.
* uses OpenAI API for inference, but does not use OpenAI for embeddings. OpenAI does not train on API calls, so that is effectively 'private' also, although not local.
* has a cursory named entity recognition module that is not enabled but can be. It is very token inneficient. It will silently extract named entities from user prompts and save them to a file that is then injected into and informs the prompt context. Or, you could just edit the contents of that data file yourself. Either way, the chat engine learns about you over time and learns from your chat history over time. This information informs its responses.
* the chat engine has 3 shaped 'personalities'. It also supports male or female, but only male is actually implemented. The female personality is UNFINISHED. It can be a writer, coder or just a conversation bot that likes to learn about you and chat with you. These personalities are set through the Windows interface. The male personality is shaped to be less OpenAI generic sounding. The female personality does not yet exist.
* the general idea is a very private local chat bot that 'remembers' your conversations permanently and has selectable personalities.
* LLM outputs are streamed to a temporary file for use by the frontend. The user's prompts are stored to a temporary file for use by the frontend. (src/messages)

Features of the Tauri backend (src-tauri/src & src-tauri/icons):

* runs the Python chat engine as a Rust thread. If that thread crashes for any reason it is re-started.
* supports the communications between the chat engine and the Svelte frontend.
* handles the Windows user files for the application in the correct Windows user directory.
* handles saving the user's OpenAI API key securely using Windows Credentials Manager.
* loads the chat conversation history into memory from the database.
* monitors DB file changes for the frontend.
* fetches slices or parts of the full conversation history for use by the frontend infinite scrolling functions.
* does not yet implement grabbing new user and LLM messages from the DB and passing them to the frontend adding them to the current conversation array manipulated by Svelte. This is one of the main parts of the application that is UNFINISHED.
* the docs drop directory feature is not implemented (embedding documents via drag/drop from the frontend). UNFINISHED. Not even started.

Features of the Svelte frontend (scr/routes & src/routes/roles src/routes/lib):

* The idea of the interface is this: There is only ONE conversation thread. Yes, only 1. As the user changes the chatbot personalities or roles, all of this is part of a single infinite conversation, much like would happen in real life with a real person.
* all messages are consecutively numbered and timestamped, noting the LLM role and whether male/female for each message.
* because the conversation is infinite it must be searchable. This functionality is not added to the frontend yet. This feature is UNFINISHED.
* because the conversation is infinite the user interface is fully custom to support quick and fine scrolling insanely long conversations. It has been tested up to 200,000 messages and would likely support a million messages. I then broke that functionality to implement the integration with an updated database format. So the infinite scrolling is mainly implemented but is UNFINISHED.
* scrubbing grip interface element moves quickly through the entire conversation from top to bottom as dragged. Drag it to the top and you will end up at the first message, to the middle for the middle messages, and to the botton for the last. There is a bottom arrow element to get to the bottom quickly.
* elastic grip fine scroll element scrolls through the visible conversation depending on how far the user drags the mouse up or down. Can move fast or very slowly.
* user prompt area supports markdown and code snippet highlighting.
* diplay of past prompts and LLM messages does not yet implement the same markdown support as the prompt area. They are currently just plain text. This is UNFINISHED.
* The interface is designed to 'get out of the way' most of the time. So the header menu auto hides when not needed. The user prompt area is large and fixed, but uses opacity changes to mostly disappear if the user wants it out of the way. Makes for a mostly clean interface for scrolling and reviewing the conversation. The only elements that stay on the screen are the scrolling user elements. The "Search" feature is UNFINISHED (not started) and is supposed to occupy the right side of the autohidden header, which is why the right side of the header is empty. Search results are supposed to occupy a vertical line to the right of the scrolling elements. This is why there is extra space there. Search hits are supposed to appear as bright red dots on that thin vertical line. The interface then would allow for quick jumping between those hits up or down.

<img width="1115" alt="Screenshot 2024-01-30 161316" src="https://github.com/pgleamy/CPfullstack/assets/28472888/80e636d5-b568-4320-b8ce-08d8c33dcae9">
<img width="1116" alt="Screenshot 2024-01-30 161330" src="https://github.com/pgleamy/CPfullstack/assets/28472888/bc07abb4-038b-45d4-be6f-eb837beb0c26">


