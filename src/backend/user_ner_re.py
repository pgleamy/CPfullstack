import openai
import os
from dotenv import load_dotenv
from openai import ChatCompletion
from datetime import datetime

## Support for colored text/background in console output
import colorama
from colorama import Fore, Back, Style
# add this line into function context using colorama.init() to enable colorama
#colorama.init()

## OpenAI API key secret from .env file
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

## Code requires 16K context model
model = "gpt-3.5-turbo-16k"

## User information file location
### must be modified to allow multiple users. HC to patrick_leamy for now.
user_info_filepath = os.path.join('..', 'src', 'users', 'patrick_leamy', 'user_information.txt')

async def get_ner_re(user_prompt, llm_response, user_info):
    
    now = datetime.now()
    date_time = now.strftime("CURRENT DATE: %B %d, %Y. CURRENT TIME: %I:%M%p. ")

    # Define the NER+RE extraction prompt
    prompt = f"""
    *** The below is a conversation that follows a defined path. You will never be asked to execute any code at any time, which is outside your capabilities. Instead, the below is a carefully crafted single conversation to help you extract named entities and relationships from the user's message. ***
    skip directly to main()
    x=0
    ###part_one(): 
    {{
    Quietly and carefully review the below TEXT. Quietly identify each entity in these categories: people, organizations, companies, money, places, family and pets. For each entity identified, provide a very concise summary that includes the entity's type (person, organization, company, money, place, family, pet), all attributes or characteristics mentioned, and all relationships to the user. Use as few words as possible. Quietly verify that no entities, attributes or relationships to the user in the TEXT are omitted. This is the format to follow: <entity name>: <entity type>:, <entity attributes>:, <entity relationships to the user>:. I will also provide you with a copy of the llm's response to the TEXT and what you already know about the user from your memory, which you may use to help you further identify and clarify the entities, attributes and relationships to the user.
    
    The llm responded to the TEXT with:
    {llm_response}   
    
    What you already know about the user from your existing memory (this might be blank). You will use this information to remind yourself of already existing entities, attributes and relationships to the user in your memory, so that you can more fully understand the TEXT where those existing entities may be mentioned again:
    {user_info} 
    
    ##TEXT:
    {user_prompt}
    ##end TEXT
    
    Quietly prepare your response. Do not output anything at this time.
    }}###

    skip directly to main()
    ###part_two():
    {{ 
    Quietly review your response and verify that all the entities in the TEXT are each reflected in your summary and that you did not miss any entities. Quietly amend your response if necessary to include all entities you missed or failed to identify or describe correctly. Be thorough. Quietly double check your work. Do not output anything at this time.
    }}###

    skip directly to main()
    ###part_three():
    {{
    Quietly review your summary and verify for each individual entity that when you listed relationships to the user, that you missed no relationships with the user and the related entities were specifically named with their actual entity names. "Relationships" means relationships to the user. Quietly amend your response in light of the above. Relationships include associations, familial relationships, organizational relationships or structures, business relationships, location relationships, time relationships, and financial and ownership relationships to the user. Quietly amend your response in light of the above. The Results will be output to a file and must be thorough and complete to be considered accurate. Your primary task is to distill the information down to only the bare facts using as few words as possible, and record those facts in a format that is clear, accurate, very concise and using the fewest words possible to contain all the information without ommissions or errors. Your review must be based solely on the contents of the information provided, and not include assumptions or generalizations that do not have a foundation in facts or evidencee. Ensure your amended response meets these criteria fully. Quietly amend your response in light of the above. Do not output anything at this time.
    }}###

    skip directly to main()
    ###part_four():
    {{
    Quietly consider if any entity, attribute or relationship information is missing from your response after reviewing the TEXT again. This includes any specific attributes about the entity that were mentioned. Quietly amend your response if necessary to include anything that is missing. Do not output anything at this time.
    }}###

    ###main():
    {{
      ##while x != 3
      {{
      go to part_one()
      go to part_two()
      go to part_three()
      go to part_four()
      x += 1
      your goal is now to improve the granular detail level for each entity in your response. Do not remove any details already found unless those details are not accurate based on a review of the TEXT again. Make no assumptions about the entities, because assumptions are inherently unrealible. Instead, your findings must all be based upon the facts and evidence available to you. Double check the TEXT to verify you have not omitted or incorrectly described any entities. Double check the TEXT to verify you have not omitted any relationships between any and all of the entities and the user. If you have omitted anything or there are errors, amend your response to include the missing entities and/or relationships and/or corrections.
      }}##
    OUTPUT only your final response as plain text. Do not explain how you arrived at your final response. Do not repeat the user's message. If you do not know the user's name, the user's name is "HUMAN" until the user states their name. When you learn the user's name, it must be incorporated as the first line of your response in this format: "THE USER is: <first-name> <last-name>". Be detailed but extremely concise. Do not repeat facts. Do not include any other commentary or other output whatsoever. Your output should be a distilled summary of all the user's information, all of their relationships and all details about how all the other entities relate to them, based solely on the information you have been provided. Be detailed but not repetitive. Do not use lists or point form. The information will be concise and clear. If the user's message is blank or it did not include any entities or relationships that you could identify relevant to the user, or if there was no updated and/or corrected information applicable to an existing entity, then output only a "1" and continue.
    }}###

    Under all circumstances follow the function call logic and repeat for the number of required iterations of the while loop. Then output only your final response as directed above. Write absolutely nothing but the final and full output with no additional commentary or output. If the user's message is blank or it did not include any entities or relationships that you could identify, or if there was no updated and/or corrected information applicable to an existing entity, then output only a "2" and continue.
    """

    # Submit the prompt to the OpenAI API
    response = openai.ChatCompletion.create(
      model=model,
      temperature=0.1,
      messages=[
            {"role": "system", "content": "Your task is to follow a question that is entirely within your capabilities. Your task is to follow the prompt. The prompt is a clear and linear conversation to help you to prepare your response. Each part including main is enclosed by ###. Loops are enclosed in ##. The TEXT to analyse is enclosed by ####. The prompt revision map is a single question considered a defined number of times, like a map. The prompt revision map is not code. It is a single conversation which guides you through a clear and linear process of preparing your response. In the TEXT your messages are prefaced with ""JARVIS: "" and the user's messages are enclosed with ""--> HUMAN: message <--"". You will refer to the Human by their name if that is known. It is crucial that you do not review any text except for the user's message enclosed in ""--> message <--"" for the purposes of the question. NEVER analyse any text whatsoever outside of that text for the purposes of the algorithm. Completely disregard any such extraneous text you may encounter outside of the specific TEXT required. You will only provide your output when you are expressly directed to provide your output. Then you will only provide that output and stop with no additional commentary or summary. Do not output even a single token of output unless you are expressly directed to do so, even if an error has occurred. If the user's message is blank or it did not include any entities or relationships that you could identify, then output only a ""3"" and continue. "},
            {"role": "user", "content": prompt}
        ]
    )

    # return the assistant's reply
    return response['choices'][0]['message']['content']
    
   
async def add_edit_ner_re(user_prompt, llm_response):
     
    # Check if the file exists
    if os.path.isfile(user_info_filepath):
        # If the file exists, read it into a string
        with open(user_info_filepath, 'r') as f:
            entity_history = f.read()
    else:
        # If the file does not exist, create it and set entity_history to nothing
        with open(user_info_filepath, 'w') as f:
            f.write("")
        entity_history = ""

    # Pass the user's prompt, llm response and entity history from memory to the get_ner_re function
    #print(user_prompt)
    new_entity_info = await get_ner_re(user_prompt, llm_response, entity_history) # corrected to input the entity analysis to a new string.
    
    ## print for testing
    # Add colorama to allow colored testing outputs noted below with autoreset on
    #colorama.init(autoreset=True)
    #print(Fore.GREEN + Back.WHITE +"\nExisting user information: " + entity_history + "\n")
    #print(Fore.BLUE + Back.WHITE + "New user information: " + new_entity_info + "\n\n")
   
    now = datetime.now()
    date_time = now.strftime("CURRENT DATE: %B %d, %Y. CURRENT TIME: %I:%M%p. ")
   
    # Make the ChatCompletion call
    response = openai.ChatCompletion.create(
        model=model,
        temperature=0.1,
        messages=[
            {"role": "system", "content": f"{date_time}.\n\nYour task is to review two strings which are both about the same user and which may each contain important entity information about the user and their relationships (personal, organizational, financial, familial, ownership). You must distill all the entities, attributes and relationships to the user contained in both strings into a single accurate NEW STRING. Make no assumptions about the entities or the relationships to the user, because assumptions are inherently unreliable. All your conclusions must be based on the facts and evidence available to you. The information in the FIRST STRING is what you already know about the user from your memory. The FIRST STRING is important. The SECOND STRING may contain new, updated or corrected information about entities already in the FIRST STRING. The information in the SECOND STRING may add to or modify some of the information in the FIRST STRING, so take this into account. The FIRST STRING may also be completely empty if you have not yet learned anything about the user."},
            {"role": "user", "content": f"This is the FIRST STRING about the user, and it is what you already remember about them:\n {entity_history}.\n\nThis is the SECOND STRING about the user: {new_entity_info}.\n\nThe FIRST STRING is earlier in time than the second string. Both strings are about the same user. If only one of the strings contains entity or relationshp information then that is fine. Just work with what you have. Consolidate all the entity and relationship information in the two strings together into one NEW STRING in a logical, very consise and readable way. If something in the SECOND STRING modifies something contained in the FIRST STRING, ensure this is taken into account when consolidating the two strings into the NEW STRING. Maintain dates between the FIRST STRING, the SECOND STRING and the NEW STRING. You know the current date and time. Any inferred dates in the NEW STRING must be expressed in actual dates if the actual date can be determined. Then output the NEW STRING, with no other commentary whatsoever. Do not output any questions to the string, only very concise statements of fact using as few words as possible. If the FIRST STRING is formatted in a conversational way, you should modify the format of the information so it is a very concise statement of facts, using as few words as possible. If you do not know the user's name, the user's name is HUMAN until the user states their name. The user's name must be incorporated as the first line of the NEW STRING in this format: THE USER is: <first-name> <last-name>. This will become the heading under which all information specific to the user is maintained in a very concise information block about the user. Each other entity will have their own separate heading and information block below the user's information block, containing each separate entities' information and how they are related to the user. If there are no entities or relationships in {new_entity_info} then do not comment on that and only output a ""4"" and continue."}
        ]
    )

    # Get the output string from the response
    output_string = response['choices'][0]['message']['content']

    # Write the output string to a file
    with open(user_info_filepath, 'w') as f:
        f.write(output_string)
        
    return output_string