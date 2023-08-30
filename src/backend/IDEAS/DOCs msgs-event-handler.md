Handler Class

Purpose: Inherits from FileSystemEventHandler to handle file modification events.
Methods:
    on_modified(event): Triggered when a file is modified.

def on_modified(self, event):
    asyncio.run_coroutine_threadsafe(self.callback(event.src_path), self.loop)

'monitor_files' Method

Purpose: Sets up file monitoring.
Flow:
Retrieves the current asyncio event loop.
Initializes the Handler class.
Creates an Observer object and schedules it.
Starts the observer.

async def monitor_files(self):
    loop = asyncio.get_event_loop()
    event_handler = self.Handler(loop, self.file_changed_callback)
    observer = Observer()
    observer.schedule(event_handler, path='./messages/', recursive=False)
    observer.start()

'file_changed_callback' Method

Purpose: Called when a file is modified.
Flow:
Checks if the modified file is user_prompt.txt.
Reads the file, updates self.user_input, and sets the new_prompt_event.
Checks if the modified file is llm_response.txt.
Reads the file and updates self.llm_response.

async def file_changed_callback(self, filename):
    if "user_prompt.txt" in filename:
        with open("./messages/user_prompt.txt", "r") as f:
            self.user_input = f.read().strip()
            self.new_prompt_event.set()

'new_prompt_event'
Purpose: An asyncio Event object.
Usage:
Set in file_changed_callback.
Waited on in get_user_input.
Cleared in get_user_input.

self.new_prompt_event = asyncio.Event()

'get_user_input' Method
Purpose: To get the user's input.
Flow:
Waits for new_prompt_event to be set.
Clears new_prompt_event.
Reads self.user_input.
Updates the chat history.

async def get_user_input(self):
    await self.new_prompt_event.wait()
    self.new_prompt_event.clear()
    await asyncio.gather (
        self.update_chat_history("\n--> HUMAN: " + self.user_input + " <--"),
    )
    return self.user_input

How It Works Together

'monitor_files' sets up file monitoring.
When user_prompt.txt is modified, 'file_changed_callback' is triggered.
'file_changed_callback' sets 'new_prompt_event'.
'get_user_input' waits for 'new_prompt_event' to be set, then proceeds to process the new prompt.
This ensures that 'get_user_input' will wait until a new prompt is submitted.