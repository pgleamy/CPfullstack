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

async def get_ner_re(user_prompt, llm_response):
    
    now = datetime.now()
    date_time = now.strftime("CURRENT DATE: %B %d, %Y. CURRENT TIME: %I:%M%p. ")

    # Define the NER+RE extraction prompt
    prompt = f"""
    *** The below is a conversation that follows a defined path. You will never be asked to execute any code at any time, which is outside your capabilities. Instead, the below is a carefully crafted single conversation to help you extract named entities and relationships from the user's message. ***
    skip directly to main()
    x=0
    ###part_one(): 
    {{
    Carefully review the below TEXT. Identify each entity in these categories: people, organizations, companies, money, places, family and pets. For each entity identified, provide a very concise summary that includes the entity's type (person, organization, company, money, place, family, pet), all attributes or characteristics mentioned, and all relationships to the user. Use as few words as possible. Verify that no entities, attributes or relationships to the user in the TEXT are omitted. This is the format to follow: <entity name>: <entity type>:, <entity attributes>:, <entity relationships to the user>:. I will also provide you with a copy of the llm response to the TEXT, which you may use to help you further identify and clarify the entities, attributes and relationships.
    
    The llm responded to the TEXT with:
    {llm_response}
    
    ##TEXT:
    {user_prompt} 
    ##end TEXT
    
    Quietly prepare your response. Do not output anything at this time.
    }}###

    skip directly to main()
    ###part_two():
    {{ 
    Review your response and verify that all the entities in the text are each reflected in your summary and that you did not miss any entities. Amend your response if necessary to include all entities you missed or failed to identify or describe correctly. Be thorough. Double check your work. Do not output anything at this time.
    }}###

    skip directly to main()
    ###part_three():
    {{
    Review your summary and verify for each individual entity that when you listed relationships to the user, that you missed no relationships and the related entities were specifically named with their actual entity names. "Relationships" means relationships to the user. All the entities are equally important. Amend your response in light of the above. Relationships include association, familial, organizational, business, location, financial and ownership relationships to the user. Quietly amend your response in light of the above. The Results will be output to a file and must be thorough and complete to be considered accurate. Your task is to distill the information down to only the bare facts, in as few words as possible. Your review must be based solely on the contents of the information provided, and not include assumptions or generalizations that do not have a foundation in facts or evidencee. Ensure your amended response meets these criteria fully. Amend your response in light of the above. Do not output anything at this time.
    }}###

    skip directly to main()
    ###part_four():
    {{
    Consider if any entity, attribute or relationship information is missing from your response after reviewing the TEXT again. This includes any specific attributes about the entity that were mentioned. Amend your response if necessary to include anything that is missing. Do not output anything at this time.
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
      your goal is now to improve the granular detail level for each entity in your response. Do not remove any details already found unless those details are not accurate based on a review of the TEXT again. Make no assumptions about the entities, because assumptions are inherently unrealible.  Instead, your finding must all be based upon the facts and evidence available to you. Double check the TEXT to verify you have not omitted or incorrectly described any entities. Double check the TEXT to verify you have not omitted any relationships between any and all of the entities and the user. If you have omitted anything or there are errors, amend your response to include the missing entities and/or relationships and/or corrections.
      }}##
    OUTPUT only your final response as plain text. Do not explain how you arrived at your final response. Do not repeat the user's message. If you do not know the user's name, output it as a HUMAN placeholder until the user states their name. Be detailed but extremely concise. Do not repeat facts. Do not include any other commentary or other output whatsoever. Your output should be a distilled summary of all the user's information, all of their relationships and all details about how all the other entities relate to them. Be detailed but not repetitive. Do not use lists or point form. The information should be concise and clear. If the user's message is blank or it did not include any entities or relationships that you could identify relevant to the user, or if there was no updated and/or corrected information applicable to an existing entity, then output only a "1" and continue.
    }}###

    Under all circumstances follow the function call logic and repeat for the number of required iterations of the while loop. Then output only your final response as directed above. Write absolutely nothing but the final and full output with no additional commentary or output. If the user's message is blank or it did not include any entities or relationships that you could identify, or if there was no updated and/or corrected information applicable to an existing entity, then output only a "2" and continue.
    """

    # Submit the prompt to the OpenAI API
    response = openai.ChatCompletion.create(
      model=model,
      temperature=0.1,
      messages=[
            {"role": "system", "content": f"{date_time} Your task is to follow a question that is entirely within your capabilities. Your task is to follow the prompt. The prompt is a clear and linear conversation to help you to prepare your response. Each part including main is enclosed by ###. Loops are enclosed in ##. The TEXT to analyse is enclosed by ####. The prompt revision map is a single question considered a defined number of times, like a map. The prompt revision map is not code. It is a single question which guides you through a clear and linear process of preparing your response. In the TEXT your messages are prefaced with ""JARVIS: "" and the user's messages are enclosed with ""--> HUMAN: message <--"". You will refer to the Human by their name if that is known. It is crucial that you do not review any text except for the user's message enclosed in ""--> message <--"" for the purposes of the question. NEVER analyse any text whatsoever outside of that text for the purposes of the algorithm. Completely disregard any such extraneous text you may encounter outside of the specific TEXT required. You will only provide your output when you are expressly directed to provide your output. Then you will only provide that output and stop with no additional commentary or summary. Do not output even a single character of output unless you are expressly directed to do so, even if an error has occurred. If the user's message is blank or it did not include any entities or relationships that you could identify, then output only a ""3"" and continue. "},
            {"role": "user", "content": prompt}
        ]
    )

    # return the assistant's reply
    return response['choices'][0]['message']['content']
    
   
async def add_edit_ner_re(user_prompt):
     
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

    # Pass the user's prompt to the get_ner_re function
    #print(user_prompt)
    new_entity_info = await get_ner_re(user_prompt) # corrected to input the entity analysis to a new string.
    
    ## print for testing
    # Add colorama to allow colored testing outputs noted below with autoreset on
    #colorama.init(autoreset=True)
    #print(Fore.GREEN + Back.WHITE +"\nExisting user information: " + entity_history + "\n")
    #print(Fore.BLUE + Back.WHITE + "New user information: " + new_entity_info + "\n\n")
   
    # Make the ChatCompletion call
    response = openai.ChatCompletion.create(
        model=model,
        temperature=0.1,
        messages=[
            {"role": "system", "content": "Your task is to review two strings which are both about the same user and which may each contain important entity and relationship information about the user and their relationships (personal, financial, familial, etc). You must consolidate all the entities and relationships contained in both strings into a single accurate string. Make no assumptions about the entities or the relationships because assumptions are inherently unreliable. All your conclusions must be based on the facts and evidence available to you. The information in the second string may add to or modify some of the information in the first string, so take this into account. The first string may also be completely empty."},
            {"role": "user", "content": f"First String about the user: {entity_history}. Second String about the user: {new_entity_info}. The first string is earlier in time than the second string. Both strings are about the same user. If only one of the strings contains entity or relationshp information then that is fine. Just work with what you have. Consolidate all the entity and relationship information in the two strings together into one paragraph in a logical and readable way. For example, if something in the second string modifies something contained in the first string, ensure this is taken into account when consolidating the two strings into the final paragraph, which may include deleting or modifying some of the information contained in the first string for the final paragraph. Then output that paragraph, with no other commentary whatsoever. Do not output any questions to the paragraph, only statements of fact. If there are no entities or relationships in {new_entity_info} then do not comment on that and only output a ""4"" and continue."}
        ]
    )

    # Get the output string from the response
    output_string = response['choices'][0]['message']['content']

    # Write the output string to a file
    with open(user_info_filepath, 'w') as f:
        f.write(output_string)
        
    return output_string