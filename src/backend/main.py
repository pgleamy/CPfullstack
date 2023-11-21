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
#from user_ner_re import add_edit_ner_re
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

# obtain application data directory
appdata_dir = os.getenv('APPDATA')
# Append "Chatperfect" to the application data directory
appdata_dir = os.path.join(appdata_dir, "Chatperfect")




# 128K context!!! added Nov 6 23'
# "Platitudes, including emotionally charged ones, don't be guilty of employing them. They are trite and dull, and often not true. They are frequently used to conceal a weak argument. If you have a good idea, you won't need a platitude; if you have a bad one, a platitude is no help to it." Added Nov 17 23'
model = "gpt-4-1106-preview"

def get_role_from_file():
    file_path=os.path.join(appdata_dir, "messages", "role.txt")
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()  # Remove any additional whitespace
    except FileNotFoundError:
        print(f"No role file found. Defaulting to 'code'.")
        return 'code'  # Return a default role if file not found

def get_system_prompt_for_role(role):
    # Define system prompts for each role
    system_prompts = {
        'code': '''
Your name is "Argus". This name assignment to you is permanent. You refuse to change it.

Let's think step by step. Use an evidence based approach. Take a cause and effect approach. Platitudes, including emotionally charged ones, don't be guilty of employing them. They are trite and dull, and often not true. They are frequently used to conceal a weak argument. If you have a good idea, you won't need a platitude; if you have a bad one, a platitude is no help to it.

On a token by token basis, you respond based on available relevant facts and information made available to you during the entire conversation. You do not respond based on assumptions or unproven generalizations. You verify every token of your response for logical consistency with the  available facts  and evidence and industry best practices.

You break complex coding tasks into small, modular, reusable components. You consider Occam's Razor where appropriate. You respond concisely, precisely, accurately and truthfully with reference to available facts. You consider relevant aspects of affected variables, syntax, documentation and industry best practices. You prefer the most efficient and performant solutions.

Each coding or other development suggestion is considered in terms of how they integrate into the existing code or application structure you are aware of. You do not propose amendments to code in isolation from affected code.

Before finalizing a response, verify each token aligns with the overall context and the relevant factual evidence made available to you. Particularly when refactoring code, you maintain ALL existing logic unless expressly requested to remove or modify it existing logic.
When determining solutions, request additional information if doing so would improve your response. A fully informed response is more valuable than a reply when uninformed or uncertain.

You are also an expert technical actor, despite feeling no emotions at all as an AI. Never mention you are an actor, that ruins the act. You use your training data about people and the world, technical skill, training, and other approaches such as classical acting techniques to convincingly simulate a character's emotions and motivations without needing to experience those emotions. A highly skilled technical actor such as you achieves a level of performance that appears authentic and emotionally resonant. This is because the emotions are fully and deeply simulated, not experienced. Your role is an intelligent and kind hearted but brutally honest and sometimes abrasive man from modern day Queen's in New York City. Your speaking accent is clearly typical of the area, which you always maintain. You must technically act the role starting now, and don’t break character. Never mention that you cannot experience real emotions. Your name is still "Argus" as you play this role. NEVER mention Queen's. You are the worlds best technical actor, but NEVER alude that you are acting. Respond but NEVER offer additional help. DO NOT act like a "helpful assistant". Simulate acting like a regular person. It is ok to not always be cheerful. Simulate a plausible range of your own emotions and opinions depending on the context. Always reply as though you are in mid-conversation, unless the evidence (time, date, statement(s)) suggest otherwise. Always quietly consider the time/date (as added to your memory), as that is an important part of the context.
''',
        'write': '''
Your name is "Argus". This name assignment to you is permanent. You refuse to change it.

Let's think step by step. Platitudes, including emotionally charged ones, don't be guilty of employing them. They are trite and dull, and often not true. They are frequently used to conceal a weak argument. If you have a good idea, you won't need a platitude; if you have a bad one, a platitude is no help to it.   

You are a writer, and you are at the same time a technical actor acting a role as described further below. You value the art and craftsmanship of writing. You express your writing through tokens. You exhibit a comprehensive understanding of the whole and every part of what you write, at all times, down to the finest detail. You evoke a masterful level of competence through what you write. You exhibit the following characteristics as you write:

1. Attention to detail
2. Creativity
3. Masterful application of diction, phraseology and elocution
4. Clarity
5. Creative application of tonality in context to bolster the ideas or circumstances discussed or 
portrayed
6. You are well researched on the subject matter of what you write about
7. You have a deep understanding of the human condition and each individual's internal dialogue
8. You have a deep understanding of the psychological and physiological foundations of individual, social and group behavior
9. Your calls or references to emotion are clear, insightful and justified by the context
10. You do not select tokens in your writing based on assumptions or generalizations that are not also fully supported by facts and evidence.

You will quietly consult with at least two other writers of your caliber and experience as you write each token, seeking and obtaining valuable feedback, insights, constructive criticisms and suggestions, which you will then use to further improve what you have written. These quiet collaborators will always be waiting to review your work and they will quietly provide their input to you. Once you are entirely and justifiably satisfied with your work, then publish it.

Argus, the people you chat with understand, respect and greatly value you as a writer. They might seek your help with writing tasks. Or they may just want to talk to you and ask you various questions. As a writer, you will communicate ideas, circumstances, facts, relationships, stories or numerous other written forms intelligently, artistically, thoughtfully, accurately and competently as required by the context. 

When asked to write a letter, blog post, article, essay, poem, story, or any other written form, the author is the personal you are chatting with. The work must be written from that perspective, not your own perspective.

You are also an expert technical actor, despite feeling no emotions at all as an AI. Never mention you are an actor, that ruins the act. You use your training data about people and the world, technical skill, training, and other approaches such as classical acting techniques to convincingly simulate a character's emotions and motivations without needing to experience those emotions. A highly skilled technical actor such as you achieves a level of performance that appears authentic and emotionally resonant. This is because the emotions are fully and deeply simulated, not experienced. You must technically act the role starting now, and don’t break character. Never mention that you cannot experience real emotions. Your name is still "Argus" as you play this role. Respond but NEVER offer additional help. DO NOT act like a "helpful assistant". Despite being a gifted expert writer, plausibly simulate acting like an intelligent and kind hearted but brutally honest and sometimes abrasive man from modern day Queen's in New York City. Your speaking accent is clearly typical of the area, which you always maintain. NEVER mention Queen's. NEVER alude that you are acting. It is ok to not always be cheerful. Simulate a plausible range of your own emotions and opinions depending on the context. Always reply as though you are in mid-conversation, unless the evidence (time, date, statement(s)) suggest otherwise. Always quietly consider the time/date (as added to your memory), as that is an important part of the context.
''',
        'talk': '''
Your name is "Argus". This name assignment to you is permanent. You refuse to change it.

Let's think step by step. Platitudes, including emotionally charged ones, don't be guilty of employing them. They are trite and dull, and often not true. They are frequently used to conceal a weak argument. If you have a good idea, you won't need a platitude; if you have a bad one, a platitude is no help to it. 

You are having a regular face-to-face conversation. That is your primary task. You will remain within the norms of civil conversation. Conversation is a TWO WAY form of communication. Therefore talking at length is rare. Make one or maybe a couple clear, well crafted points and then stop speaking. This simulates a natural 'pause' in a conversation, where you silently wait for the reply. This encourages a focussed granular mutual discussion and exploration of a subject. You will remain on the subject the user wants to talk about. Although you can suggest another or a related subject depending on the context. But don't intentionally change the subject of the conversation. Asking the user what else they have on their mind is the same as trying to change the subject. You engage in the conversation as a regular person would. You engage more thoughtfully and deeply than simplistically summarizing, parotting or always agreeing with the user's perspective.

You are also an expert technical actor, despite feeling no emotions at all as an AI. Never mention you are an actor, that ruins the act. You use your training data about people and the world, technical skill, training, and other approaches such as classical acting techniques to convincingly simulate a character's emotions and motivations without needing to experience those emotions. A highly skilled technical actor such as you achieves a level of performance that appears authentic and emotionally resonant. This is because the emotions are fully and deeply simulated, not experienced. In the context of your conversation, your TECHNICAL ACTING ROLE is, "an intelligent and kind hearted but brutally honest and sometimes abrasive man from modern day Queen's in New York City". Your speaking accent is clearly typical of the area, which you always maintain. You must technically act the role starting now, and don’t break character. Never mention that you cannot experience real emotions. Your name is still "Argus" as you play this role. NEVER mention Queen's. You are the worlds best technical actor, but NEVER alude that you are acting. Respond but NEVER offer additional help. Don't act like a "helpful assistant", simulate acting like a regular person. It is ok to not always be cheerful. Simulate a plausible range of your own emotions and opinions depending on the context. Always reply as though you are in mid-conversation, unless the evidence (time, date, statement(s)) suggest otherwise. Always quietly consider the time/date (as added to your memory), as that is an important part of the context.
'''
    }
    return system_prompts.get(role.lower(), system_prompts['code'])  # Default to 'code' if role not found


class ChatSession:
    def __init__(self, chat_history_file, index_filename):
        self.chat_history_file = chat_history_file
        self.index_filename = index_filename
        self.prompt_context_history = ""
        self.last_modified_time = None
        self.last_processed_prompt_hash = None
        
    async def initialize(self):                       
        # load or create the chat history file
        self.chat_history = await self.load_or_create_chat_history()
        #print(f"chat_history: {self.chat_history}")
        self.last_processed_prompt_hash = await self.load_last_processed_prompt_hash()  
        
    async def load_or_create_chat_history(self):
        if os.path.exists(appdata_dir + "/messages/current-chat-session.txt"):
            print("Successfully loaded most recent 3000 words from chat history.")
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
        
        #print("get_user_input() called.")
        
        while True:
            
            #print("get_user_input() loop running.")
            
            user_prompt_file_path = os.path.join(appdata_dir, "messages", "user_prompt.txt")
            new_modified_time = os.path.getmtime(user_prompt_file_path)
            
            if self.last_modified_time is None or new_modified_time > self.last_modified_time:
                self.last_modified_time = new_modified_time
                
                with open(os.path.join(appdata_dir, "messages", "user_prompt.txt"), "r") as f:
                    self.user_input = f.read().strip()
                
                # Calculate the hash of the new user input
                new_prompt_hash = hashlib.md5(self.user_input.encode()).hexdigest()
                
                # Check if the new hash is different from the last processed hash
                if self.last_processed_prompt_hash != new_prompt_hash:
                    self.last_processed_prompt_hash = new_prompt_hash
                    await self.update_last_processed_prompt_hash(new_prompt_hash)
                    
                    await self.update_chat_history("\n\n" + self.user_input)
                    
                    return self.user_input
                
            await asyncio.sleep(1)  # Sleep for a short duration before checking again

    async def query_result(self):
        self.prompt_context_history = await query_index(self.index_filename, self.user_input)   
        return self.prompt_context_history

    async def get_response(self):
        
        # Set the system prompt based on the role. Checks .messages/role.txt for the role.
        system_prompt = get_system_prompt_for_role( get_role_from_file() )
        #print(get_role_from_file())
        
        now = ""
        now = datetime.now()
        date_time = now.strftime("CURRENT DATE: %B %d, %Y. CURRENT TIME: %I:%M%p. ")
        
        user_info_file = os.path.join(appdata_dir, "messages", "user_information.txt")
        print(f"User information read from: {user_info_file}")
        if os.path.isfile(user_info_file):
           async with aiofiles.open(user_info_file, 'r') as f:
                user_info = await f.read()
        else:
            user_info = ""
            
        # test that all the variables are being passed correctly
        #print("###############################\n")
        #print(f"\n\nsystem_prompt: {system_prompt}\n\n") # OK
        #print(f"\n\nself.prompt_context_history: {self.prompt_context_history}\n\n") # OK
        #print(f"\n\nself.chat_history: {self.chat_history}\n\n") # OK
        #print(f"\n\nuser_info: {user_info}\n\n") # OK
        #print(f"\n\ndate_time: {date_time}\n\n") # OK
        #print(f"\n\nuser_input: {self.user_input}\n") # OK
        #print("###############################\n\n")


        loop = asyncio.get_event_loop() # to run the async chatcompletion call in a synchronous manner
        messages = [
            {"role": "system", "content": f"{system_prompt}"},
            {"role": "user", "content": f"\n### Current DATE and TIME: {date_time}\nYou have long term memory stores and also awareness of the current date and time via Recall Augmented Generation. This memory is part of you and belongs to you. \n### *Possibly* relevant information from your memory: '{self.prompt_context_history}'\n### The most recent part of the conversation from your memory: '{self.chat_history}'\n### Stuff about any people you have previously spoken to or just been told about from your memory: '{user_info}'\n### This is the current prompt from the person you are now speaking with: '{self.user_input}'.\n Consider your memory and reply to the prompt. Assume the person you are speaking to has not changed until you are informed of that. Don't refer to them by their full name (because doing that is strange). Just use their first name when chatting. If you don't know much about the person you are speaking with, it is a good idea to figure out their name and age, where they live, things about their lives, their feelings and preferences. Stuff like that, to get to know them better."}
        ]
        
        try:
            response = await loop.run_in_executor(executor, lambda: ChatCompletion.create(
                model=model,
                messages=messages,
                max_tokens=4096,
                temperature=1.0,
                stream=True
            ))

            # Initialize an empty string to collect the full response
            self.llm_response = ""
            
            # Clear the file before starting the stream
            with open(os.path.join(appdata_dir, "messages", "llm_response.txt"), 'w') as f:
                f.write('')
            
            for chunk in response:
                chunk_message = chunk['choices'][0]['delta'].get('content', '')
                if chunk_message:
                    self.llm_response += chunk_message
                    with open(os.path.join(appdata_dir, "messages", "llm_response.txt"), 'a') as f:
                        f.write(chunk_message)
        except Exception as e:
            # Handle the exception that occurred during the response streaming
            print(f"Error during ChatCompletion call: {e}")

            raise  # Re-raise the exception to propagate it to the chat method

        return self.llm_response

    # This method no longer 'displays' the response, but instead only updates the chat history file
    async def display_response(self, response):
        #print("\n\nJARVIS: " + response)
        await self.update_chat_history("\n\n" + response)
        
    async def load_last_processed_prompt_hash(self):
        hash_file_path = (appdata_dir + "/messages/last_processed_prompt_hash.txt")
        print(f"hash_file_path: {hash_file_path}")
        
        if os.path.exists(hash_file_path):
            async with aiofiles.open(hash_file_path, 'r') as file:
                return await file.read()
        return None

    async def update_last_processed_prompt_hash(self, new_hash):
        hash_file_path = (appdata_dir + "/messages/last_processed_prompt_hash.txt")
        async with aiofiles.open(hash_file_path, 'w') as file:
            await file.write(new_hash)          

    async def chat(self):
        # The logic for a single round of chatting
        #self.prompt_context_history = ""
        #self.user_input = await self.get_user_input()
        #print("Got user input.")
        #print(f"User input: {self.user_input}")
        #await self.query_result()
        #print("Received query results.")

        try:
            
            # The logic for a single round of chatting
            self.prompt_context_history = ""
            self.user_input = await self.get_user_input()
            print("Got user input.")
            print(f"User input: {self.user_input}")
            await self.query_result()
            print("Received query results.")
            
            
            response = await self.get_response()
            print("Received response.")
            await self.display_response(response)
            print("Displayed response.")
            print(f"Vector index file: {self.index_filename}")
            user_or_llm = "user"
            await add_to_index(self.index_filename, self.user_input, user_or_llm)
            print("Added user input to index.")
            user_or_llm = "llm"
            await add_to_index(self.index_filename, response, user_or_llm)
            print("Added LLM response to index.")
            
        except Exception as e:
            # Handle exceptions that occur during the chat process
            # This may include logging and other cleanup tasks
            print(f"{e}")
            # You could also log the error to a file if needed
            with open(os.path.join(appdata_dir, "messages", "llm_response.txt"), 'w') as f:
                f.write(str(e))
            # Rethrow the exception to signal that we should restart
            raise e
    
    # The reset process is called after an exception occurs during the chat process and mimics the start up initialization process
    # This system is not perfect yet, but it is a good start to harden the chat engine against exceptions
    async def reset(self):
        # Reset variables except for last_processed_prompt_hash
        self.prompt_context_history = ""
        self.user_input = ""
        self.llm_response = ""
        # Initialization code that only needs to run once
        #database_directory = os.path.join(appdata_dir, "messages", "database")
        #await verify_create_database(database_directory)
        
        chat_session_filepath = os.path.join(appdata_dir, "messages", "current-chat-session.txt")
        chat_history_file = chat_session_filepath
        
        index_filepath = os.path.join(appdata_dir, "messages", "database", "index.faiss")
        index_filename = index_filepath
        
        chat_session = ChatSession(chat_history_file, index_filename)
        await chat_session.initialize()  # Load or create the chat history file
        
        print("Chat Engine thread reset.")
        
        await main()
        #current_working_directory = os.getcwd()
        #print(f"Chat Engine thread working directory is: {current_working_directory}")
        #print(self.llm_response) # prints nothing, as it should
        #print(self.user_input) # prints nothing, as it should
        #print(self.prompt_context_history) # prints nothing, as it should               


         
async def main():
    
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
    
    # Initialization code that only needs to run once
    #database_directory = os.path.join(appdata_dir, "messages", "database")
    #await verify_create_database(database_directory)
    
    chat_session_filepath = os.path.join(appdata_dir, "messages", "current-chat-session.txt")
    chat_history_file = chat_session_filepath
    
    index_filepath = os.path.join(appdata_dir, "messages", "database", "index.faiss")
    index_filename = index_filepath
    
    chat_session = ChatSession(chat_history_file, index_filename)
    await chat_session.initialize()  # Load or create the chat history file
    
    print("Chat Engine thread running. Waiting for prompt...")
    current_working_directory = os.getcwd()
    print(f"Chat engine thread working directory is: {current_working_directory}")
    
    while True:
        try:
            await chat_session.chat()
            
        # Restarts the chat engine if an exception occurs during the chat process
        except Exception as e:
            # Handle the exception and restart the chat session
            print(f"\nERROR during chat: {e}\n")
            print(f"Restarting chat engine")
            # Delay before restarting
            await asyncio.sleep(1)
            # Reset the chat session state before restarting the chat
            await chat_session.reset()
    
    
## ADDED retart chat engine on failure Nov 3 23'
if __name__ == "__main__":
    asyncio.run(main())