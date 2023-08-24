import openai
import os
from dotenv import load_dotenv
from openai import ChatCompletion

## OpenAI API key secret from .env file
load_dotenv()
openai.api_key = "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"  #os.getenv('OPENAI_API_KEY')

## Code requires 16K context model
model = "gpt-3.5-turbo-16k"

def form_bright_memory(user_prompt, prompt_context_history):
    
    bright_prompt = f"""
    Let's think step by step. Which parts of the below "PROMPT_CONTEXT_HISTORY" enclosed in &&& are relevant and helpful to respond to the below "PROMPT" enclosed in @@@.  Your answer will contain all parts of the PROMPT_CONTEXT_HISTORY that are relevant and helpful to answering the PROMPT. You may use summarization in your answer if this does not remove any relevant and helpful information from your answer. Apart from this, your answer will contain nothing else. Never add facts or information to your answer that are not contained in the PROMPT_CONTEXT_HISTORY. Never make up facts. Your task is only to distill from the PROMPT_CONTEXT_HISTORY the relevant and helpful information to respond to the PROMPT. Your task is NOT to answer the PROMPT. Your task is only to anaylse it as against the PROMPT_CONTEXT_HISTORY.

    PROMPT_CONTEXT_HISTORY: &&& {prompt_context_history} &&&

    Never enclose your answer in quotes. Never explain your answer. If your answer includes any code snippets, those code snippets must always be enclosed in '''. Never answer the question posed by the PROMPT itself as that is not your task.
    
    PROMPT: @@@ {user_prompt} @@@
    
    RELEVANT MEMORIES: <your answer>

    Before providing your answer, verify that all of the RELEVANT MEMORIES are relevant and helpful to responding to the PROMPT. Do not include in the RELEVANT MEMORIES any information that is not directly relevant to and helpful to responding to the PROMPT in whole or in part. Never include notes, additional comments or explanations in the RELEVANT MEMORIES or in your answer.
    
    Once you are satisfied with the RELEVANT MEMORIES you have distilled, never mention any irrelevant information while providing your answer which will consist ONLY of the RELEVANT MEMORIES you have distilled.
    """

    # Submit the prompt to the OpenAI API
    response = openai.ChatCompletion.create(
        model=model,
        temperature=0.0,
        messages=[
            {"role": "system", "content": "You task is the comply with the user prompt precisely and to the best of your abilities."},
            {"role": "user", "content": bright_prompt}
        ],
        max_tokens=4000,
    )

    # return the assistant's reply
    return response['choices'][0]['message']['content']

## TESTING ONLY
user_prompt = """List the nations that contain rainforests from the nations with the most rainforest to nations with the least rainforest."""
prompt_context_history = """
#The Amazon rainforest (Portuguese: Floresta Amazônica or Amazônia; Spanish: Selva Amazónica, Amazonía or usually Amazonia; French: Forêt amazonienne; Dutch: Amazoneregenwoud), also known in English as Amazonia or the Amazon Jungle, is a moist broadleaf forest that covers most of the Amazon basin of South America. This basin encompasses 7,000,000 square kilometres (2,700,000 sq mi), of which 5,500,000 square kilometres (2,100,000 sq mi) are covered by the rainforest. This region includes territory belonging to nine nations. The majority of the forest is contained within Brazil, with 60% of the rainforest, followed by Peru with 13%, Colombia with 10%, and with minor amounts in Venezuela, Ecuador, Bolivia, Guyana, Suriname and French Guiana. States or departments in four nations contain "Amazonas" in their names. The Amazon represents over half of the planet's remaining rainforests, and comprises the largest and most biodiverse tract of tropical rainforest in the world, with an estimated 390 billion individual trees divided into 16,000 species.
#"""
result = user_prompt + "\n" + form_bright_memory(user_prompt, prompt_context_history)
print(result)