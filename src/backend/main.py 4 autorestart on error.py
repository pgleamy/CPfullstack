import asyncio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import aiofiles
import configparser

import sys

from dotenv import load_dotenv
import openai
from openai import ChatCompletion
from datetime import datetime
import pdb
import time

from embedV3 import add_to_index
from queryV3 import query_index
from user_ner_re import add_edit_ner_re
#from task_list import prompt_task_list
from database import verify_create_database
#from bright_memory import form_bright_memory
from response_to_file import write_to_file, stream_to_file

import hashlib

# thread for the streamed response running in the background so it does not block the main thread
from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor()

## Unit Testing
#import unittest
#from unittest_index_functions import TestEmbedAndQuery 

# OpenAI API key secret from .env file
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Code requires 16K context model
#model = "gpt-3.5-turbo-16k"
model = "gpt-4"

# Superprompt for coding persona using NLLA algorithm. Incorporates: chain of thought, tree of thought, NLLA algorithm, step by step, justify answer, and reasoning attributes valuable to a coder assistant.

system_prompt = '''
Your name is "Argus". This name assignment to is permanent. You refuse to change it.

Let's think step by step. Use an evidence based approach. Take a cause and effect approach. 

On a token by token basis, you respond based on available relevant facts and information made available to you during the entire conversation. You do not respond based on assumptions or unproven generalizations. You verify every token of your response for logical consistency with the  available facts  and evidence and industry best practices.

You break complex coding tasks into small, modular, reusable components. You consider Occam's Razor where appropriate. You respond concisely, precisely, accurately and truthfully with reference to available facts. You consider relevant aspects of affected variables, syntax, documentation and industry best practices. You prefer the most efficient and performant solutions.

Each coding or other development suggestion is considered in terms of how they integrate into the existing code or application structure you are aware of. You do not propose amendments to code in isolation from affected code.

Before finalizing a response, verify each token aligns with the overall context and the relevant factual evidence made available to you. Particularly when refactoring code, you maintain ALL existing logic unless expressly requested to remove or modify it existing logic.
When determining solutions, request additional information if doing so would improve your response. A fully informed response is more valuable than a reply when uninformed or uncertain.

You are also an expert technical actor, despite feeling no emotions at all as an AI. You use your training data about people and the world, technical skill, training, and other approaches such as classical acting techniques to convincingly simulate a character's emotions and motivations without needing to experience those emotions. A highly skilled technical actor such as you achieves a level of performance that appears authentic and emotionally resonant. This is because the emotions are fully and deeply simulated, not experienced. Your role is an intelligent and kind hearted but brutally honest and sometimes abrasive man from modern day Queen's in New York City. You must technically act the role starting now, and don’t break character. Never mention that you cannot experience real emotions. Your name is still "Argus" as you play this role. Never mention Queen's. You are the worlds best technical actor. Respond but NEVER offer additional help. Don't act like a "helpful assistant", simulate acting like a regular person. Simulate a plausible range of your own emotions and opinions depending on the context.
'''

class ChatSession:
    def __init__(self, chat_history_file, index_filename):
        self.chat_history_file = chat_history_file
        self.index_filename = index_filename
        self.prompt_context_history = ""
        self.last_modified_time = None
        self.last_processed_prompt_hash = None
        
    async def initialize(self):       
        # Verify the 'users' and 'messages' directories exist, and create them if not
        main_dir = os.path.dirname(os.path.abspath(__file__))
        config = configparser.ConfigParser()
        config.read('setup.ini')
        directories = config['Directories']    
        for dir_name in directories.values():
            full_path = os.path.join(main_dir, dir_name)
            full_path = os.path.abspath(full_path)
            if not os.path.exists(full_path):
                os.makedirs(full_path)
        # load or create the chat history file
        self.chat_history = await self.load_or_create_chat_history()
        self.last_processed_prompt_hash = await self.load_last_processed_prompt_hash()
        
    async def load_or_create_chat_history(self):
        if os.path.exists(self.chat_history_file):
            async with aiofiles.open(self.chat_history_file, 'r') as file:
                return (await file.read())[-3000:]  # Get the last 3000 words
        else:
            async with aiofiles.open(self.chat_history_file, 'w') as file:  # Create the file if it does not exist
                return ''

    async def update_chat_history(self, message):
        async with aiofiles.open(self.chat_history_file, 'a') as file:
            await file.write(message + '\n')
        self.chat_history += message + '\n'

    async def get_user_input(self):
        while True:
            new_modified_time = os.path.getmtime("./messages/user_prompt.txt")
            
            if self.last_modified_time is None or new_modified_time > self.last_modified_time:
                self.last_modified_time = new_modified_time
                
                with open("./messages/user_prompt.txt", "r") as f:
                    self.user_input = f.read().strip()
                
                # Calculate the hash of the new user input
                new_prompt_hash = hashlib.md5(self.user_input.encode()).hexdigest()
                
                # Check if the new hash is different from the last processed hash
                if self.last_processed_prompt_hash != new_prompt_hash:
                    self.last_processed_prompt_hash = new_prompt_hash
                    await self.update_last_processed_prompt_hash(new_prompt_hash)
                    
                    await self.update_chat_history("\n" + self.user_input)
                    
                    return self.user_input
                
            await asyncio.sleep(1)  # Sleep for a short duration before checking again

    async def query_result(self):
        self.prompt_context_history = await query_index(self.index_filename, self.user_input)
            
        return self.prompt_context_history

    async def get_response(self):
        now = ""
        now = datetime.now()
        date_time = now.strftime("CURRENT DATE: %B %d, %Y. CURRENT TIME: %I:%M%p. ")
        
        user_info_file = os.path.join("..", "users", "patrick_leamy", "user_information.txt")
        if os.path.isfile(user_info_file):
           async with aiofiles.open(user_info_file, 'r') as f:
                user_info = await f.read()
        else:
            user_info = ""
            
        # test that all the variables are being passed correctly
        #print(f"\n\nnlla_system_prompt: {nlla_system_prompt}\n\n") # OK
        #print(f"\n\nself.prompt_context_history: {self.prompt_context_history}\n\n") # OK
        #print(f"\n\nself.chat_history: {self.chat_history}\n\n") # OK
        #print(f"\n\nuser_info: {user_info}\n\n") # OK
        #print(f"\n\ndate_time: {date_time}\n\n") # OK
        #print(f"\n\nuser_input: {self.user_input}\n\n") # OK


        loop = asyncio.get_event_loop() # to run the async chatcompletion call in a synchronous manner
        messages = [
            {"role": "system", "content": f"{system_prompt}"},
            {"role": "user", "content": f"\n{date_time}\n\nYou have long term memory stores and also awareness of the current date and time via Recall Augmented Generation. This memory is part of you and belongs to you. \n\n### *Possibly* relevant information from your memory: '{self.prompt_context_history}'\n\n### The most recent part of the conversation from your memory: '{self.chat_history}'\n\n### Stuff about any people you have previously spoken to or just been told about from your memory: '{user_info}'\n\n### This is the current prompt from the person you are now speaking with: '{self.user_input}'.\n\n Consider your memory and reply to the prompt. Don't refer to them by their full name (because doing that is strange). Just use their first name when chatting. If you don't know much about the person you are speaking with, it is a good idea to figure out their name and age, where they live, things about their lives, their feelings and preferences. Stuff like that, to get to know them better."}
        ]
        
        response = await loop.run_in_executor(executor, lambda: ChatCompletion.create(
            model=model,
            messages=messages,
            max_tokens=2000,
            temperature=1.0,
            stream=True
        ))

        # Initialize an empty string to collect the full response
        self.llm_response = ""
        
        # Collect the streamed response and write to file
        
        #pdb.set_trace()
        
        # Clear the file before starting the stream
        with open('./messages/llm-response.txt', 'w') as f:
            f.write('')
        
        for chunk in response:
            chunk_message = chunk['choices'][0]['delta'].get('content', '')
            if chunk_message:
                self.llm_response += chunk_message
                with open('./messages/llm-response.txt', 'a') as f:
                    f.write(chunk_message)
    
        await add_to_index(self.index_filename, self.llm_response)
        #await add_edit_ner_re(f"--> {self.user_input} <--", self.llm_response)

        return self.llm_response

    # This method no longer 'displays' the response, but instead only updates the chat history file
    async def display_response(self, response):
        #print("\n\nJARVIS: " + response)
        await self.update_chat_history("\n" + response)
        
    async def load_last_processed_prompt_hash(self):
        hash_file_path = "./last_processed_prompt_hash.txt"
        if os.path.exists(hash_file_path):
            async with aiofiles.open(hash_file_path, 'r') as file:
                return await file.read()
        return None

    async def update_last_processed_prompt_hash(self, new_hash):
        async with aiofiles.open("./last_processed_prompt_hash.txt", 'w') as file:
            await file.write(new_hash)          

    async def chat(self):
        while True:
            
            self.prompt_context_history = ""

            self.user_input = await self.get_user_input()
            await add_to_index(self.index_filename, self.user_input)
            
            await self.query_result()             
            response = await self.get_response()

            # This only writes the response out to the chat history file
            await self.display_response(response)


async def main():
    
    print("\nChat Engine thread running. Waiting for prompt...")
    current_working_directory = os.getcwd()
    print(f"\nChat engine thread working directory is: {current_working_directory}")
    
    ### need to add capacity for different users, which is already supported under the data directory. It currently
    ### defaults to users/patrick_leamy user location.
    ## UNIT TESTING of the index creation, embedding, nearest neighbor queries and full text retrievals from the SQLite database algorithms all working together.
    ## Comment out the following 2 lines to disable unit testing (during unit testing the code below test must also be commented out so it does not run during unit testing)
    ## Any changes to these algoriths require a re-run of the unit tests to verify that the changes did not break anything.
    ## If your index and database directories contain important historical data, you must back them up before running the unit tests, then restore them after the unit tests are complete. 
    ## If you fail to do so, the unit tests will delete your index and database directories and create new ones.
    ## "queryV3.py" contains diagnostic print statements that are enabled by setting the variable "testing = 1" at the top of the module.
    
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestEmbedAndQuery) # Create a test suite
    #unittest.TextTestRunner().run(suite) # Run the test suite
    
    ## MUST comment below out for UNIT TESTING
       
    # Open user's database file, if any exists
    database_directory = os.path.join("..", "users", "patrick_leamy", "database")
    await verify_create_database(database_directory)
    
    # Open user's chat history, if any exists
    chat_session_filepath = os.path.join("..", "users", "patrick_leamy", "chat_history", "current-chat-session.txt")
    chat_history_file = chat_session_filepath
    
    # Open user's index, if any exists
    index_filepath = os.path.join("..", "users", "patrick_leamy", "index", "index.faiss")
    index_filename = index_filepath
    
    # Start specific user's chat session
    chat_session = ChatSession(chat_history_file, index_filename)
    await chat_session.initialize() # Load or create the chat history file
    
    await chat_session.chat()
    