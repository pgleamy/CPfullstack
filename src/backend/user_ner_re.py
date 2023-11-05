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
model = "gpt-4"

## User information file location
### must be modified to allow multiple users. HC to patrick_leamy for now.
user_info_filepath = os.path.join('..', 'users', 'patrick_leamy', 'user_information.txt')

async def get_ner_re(user_prompt, llm_response, user_info):
    
    now = datetime.now()
    date_time = now.strftime("CURRENT DATE: %B %d, %Y. CURRENT TIME: %I:%M%p. ")

    # Define the NER+RE extraction prompt
    prompt = f"""
    *** This is a conversation that follows a defined path. You will never be asked to execute any code at any time, which is outside your capabilities. Instead, the below is a carefully crafted single conversation to help you extract named entities and relationships from the dialogue. ***
    skip directly to main()
    x=0
    ###part_one(): 
    {{
    Quietly and carefully review the below TEXT. Quietly identify all the entities in these categories: people, organizations, companies, money, places, family, friends and pets. For each entity identified, give a very concise summary that includes the entity's type (person, organization, company, money, place, family member, friend, pet and type of pet). Use as few words as possible. This is the format to follow: <entity type>:, <entity name>:, <other entity attributes>:. 
    
    ### The llm responded to the TEXT with:
    ## Do not extract entities from this ## {llm_response} ## Do not extract entities from this ##
    
    ### What you already know from your memory (this might be nothing). Use this to remind yourself of already existing entities, attributes and relationships that you already know that might get mentioned again:
    {user_info}
    
    ##TEXT:
    ## extract entities etc from this ## {user_prompt} ## extract entities etc from this ##Use
    ##end TEXT
    
    Quietly prepare your response. Do not output anything at this time.
    }}###

    skip directly to main()
    ###part_two():
    {{ 
    Quietly review your response and verify that you did not miss any entities. Quietly amend your response if necessary. Be thorough. Do not output anything at this time.
    }}###

    skip directly to main()
    ###part_three():
    {{
    Quietly review your summary and now add any relationships mentioned. Relationships include associations, family relationships, friendships, organizational relationships or structures, business relationships, location relationships, time relationships based on your knowledge of the current date and time, and financial and ownership relationships.  Quietly amend your response in light of the above. Your primary task is to distill the information down to only the bare facts about each entity using as few words as possible, and record those facts in a format that is clear, accurate, very concise and using the fewest words possible. Your review must be based solely on the contents of the information provided, and not include assumptions or generalizations that do not have a foundation in facts or evidencee. Ensure your amended response meets these criteria fully. Quietly amend your response in light of the above. Do not output anything at this time.
    }}###

    skip directly to main()
    ###part_four():
    {{
    Quietly consider if any entity, attribute or relationship information is missing from your response after reviewing the TEXT again. Quietly amend your response if necessary. Do not output anything at this time.
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
      your goal is now to improve the granular detail level for each entity in your response. Do not remove any details already found unless those details are not accurate based on a review of the TEXT again. Make no assumptions about the entities, because assumptions are inherently unrealible. Instead, your findings must all be based upon the facts and evidence available to you. 
      }}##
    OUTPUT only your final response as plain text. Do not explain how you arrived at your final response. Do not repeat the TEXT. If you do not know the person's name, their name is "HUMAN" until they identify themselves. Do not repeat facts. Do not include any other commentary or other output whatsoever. Your output should be a distilled concise summary of all the information, all of the entities, their attributes. Be detailed but not repetitive. Do not use lists or point form. The information will be concise and clear. If the TEXT is blank or if it did not include any entities or relationships that you could identify, or if there was no updated and/or corrected information applicable to an existing entity, then output only a "1" and continue.
    }}###

    Under all circumstances follow the function call logic and repeat for the number of required iterations of the while loop. Then output only your final response as directed above. Write absolutely nothing but the final and full output with no additional commentary or output. If the TEXT is blank or it did not include any entities or relationships that you could identify, or if there was no updated and/or corrected information applicable to an existing entity, then output only a "2" and continue.
    """

    # Submit the prompt to the OpenAI API
    response = openai.ChatCompletion.create(
      model=model,
      temperature=0.1,
      messages=[
            {"role": "system", "content": "Your task is to follow a question that is entirely within your capabilities. Your task is to follow the prompt. The prompt is a clear and linear conversation to help you to prepare your response. Each part including main is enclosed by ###. Loops are enclosed in ##. The TEXT to analyse is enclosed by ####. The prompt revision map is a single question considered a defined number of times, like a map. The prompt revision map is not code. It is a single conversation which guides you through a clear and linear process of preparing your response. You will refer to the person by their name if known. It is crucial that you do not review any text except for the person's message enclosed in ## TEXT ### the text ## TEXT ##. NEVER analyse any text whatsoever outside of that text block for the purposes of the algorithm. Completely disregard any such extraneous text you may encounter outside of the specific TEXT block required. You will only provide your output when you are expressly directed to provide your output. Then you will only provide that output and stop with no additional commentary or summary. Do not output even a single token of output unless you are expressly directed to do so, even if an error has occurred. If the person's message is blank or it did not include any entities or relationships that you could identify, then output only a ""3"" and continue. "},
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
            {"role": "system", "content": f"{date_time}.\n\nYou are expert at comparing strings for entities contained in each. Your task is to review two strings which may each contain entity information. You must distill all the entities, attributes and relationships contained in both strings into a single accurate concise NEW STRING. Make no assumptions about the entities or the relationships. All your conclusions must be based on the facts and evidence in the two strings. The information in the FIRST STRING are details about entities you already know from your memory. The SECOND STRING may contain new, updated or corrected information about entities already mentioned in the FIRST STRING. The information in the SECOND STRING may add to or modify some of the information in the FIRST STRING. The FIRST STRING may also be completely empty if you have not yet learned anything about the person yet. You should not remove any entities or other information except if it is updated or stated to be wrong by the person. Things that are not actually entities should not appear in the FIRST STRING. If they do, remove them. All entries describing days or future dates in BOTH strings need an actual date relative to today appended, using this example format (Feb 4 22'). Always delete any event entry that has a date that is older that 2 days old, unless it is a birthday for an entity, then just label it as b-day and keep b-days permanently."},
            
            {"role": "user", "content": f"This is the FIRST STRING about the user, and it is what you already remember about them:\n {entity_history}.\n\nThis is the SECOND STRING about the user: {new_entity_info}.\n\nThe FIRST STRING is earlier in time than the second string. If only one of the strings contains entity or relationshp information then that is fine. Just work with what you have. Consolidate all the entity and relationship information in the two strings together into one NEW STRING in a logical, very consise and readable way. If something in the SECOND STRING corrects something contained in the FIRST STRING, ensure this is taken into account when consolidating the two strings into the NEW STRING. Maintain dates between the FIRST STRING, the SECOND STRING and the NEW STRING. You know the current date and time. Any inferred dates (like 'next week', 'next month', 'in a few days') in the information as a whole must be converted to actual dates calculated from the current date. If the FIRST STRING is formatted in a conversational way, you should modify the format of the information so it is a very concise statement of facts, using as few words as possible. The entity name must use this format: '<entity type>: <first-name> <last-name (if applicable)>:'. This will be the heading for that entity. The information must be FORMATTED in this way:\n\n<entity type: firstname lastname:\nattributes for this entity then listed very concisely below this heading.\n\nIf the FIRST STRING or SECOND STRING do not fully follow this format, all information must be converted precisely to this format in the NEW STRING.\n\nOutput the NEW STRING, with no other commentary whatsoever. Do not output any questions to the string, only very concise statements of fact using as few words as possible. If there are no entities or relationships in the SECOND STRING then do not comment on that and only output a ""4"" and continue."},
        ]
    )

    # Get the output string from the response
    output_string = response['choices'][0]['message']['content']

    # Write the output string to a file
    with open(user_info_filepath, 'w') as f:
        f.write(output_string)
        
    return output_string