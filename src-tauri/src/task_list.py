import os
from dotenv import load_dotenv
from openai import ChatCompletion
import openai
from datetime import datetime

## OpenAI API key secret from .env file
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

## Code requires 16K context model
model = "gpt-3.5-turbo-16k"

def prompt_task_list(user_input: str):

    CONTEXT = user_input

    prompt = f"""
    If any goals or tasks are contained in the CONTEXT, then immediately skip to "$$$" below and continue from there and ignore any text below that begins with "@@@".
    
    If there are no clear goals or clear tasks evidenced in the CONTEXT, then immediately skip to the last line of this prompt, which starts with "@@@" below, and ignore all the intervening instructions, and output only " - ".
    
    $$$
    Think step by step. The first paragraph below creates a task list of steps to obtain the goal. The second paragraph below creates a sub-list for each task list item. Review each paragraph and then output completed task list. For each list and sub-list item consider several potential alternatives, then select the clearest and most logical item for each item on each list to achieve the goal. Do not provide your output until after you have considered, weighed and assessed all the alternatives of every single item on the task list and each sub-list. Ensure that all the list items work well together and build on each other sequentially and logically. Ensure that all list items are tasks that your are capable of assisting directly with. Double check your work before outputting the final list. The list is focused on the goals apparent in the CONTEXT and must not go beyond those goals. All parts of your answer must contribute to achieving the goals apparent in the CONTEXT. Lastly, if you are being asked to emulate or copy something, then your primary goal should always be to study and fully understand all aspects of the thing being emulated or copied before proceeding.

    Paragraph 1. Think step by step and weigh and consider several alternatives at each step, selecting the best alternative at each step. We need a linear causal explanation in this CONTEXT: "{CONTEXT}".
            Generate an appropriately thorough number of steps further to all of the goals and sub-goals evidenced by this CONTEXT: "{CONTEXT}".
            Itemize your answer. One noun phrase per line.
            Each list item must be checked to be 100% consistent with the goals.
            No explanations needed, just the noun phrase, nothing else.
            Avoid starting your sentence with the word "Alternative".
            Your answer should not contain ":" .
            Your answer should avoid the word "Causes" and "causes" ."

    Paragraph 2. Think step by step and weigh and consider several alternatives at each step, selecting the best alternative at each step. We need a linear causal explanation in this CONTEXT: "I need more details for each of the above individual steps in the above list of tasks."
            Generate an appropriately thorough number of sub-steps under each of the above tasks further to all of the goals and sub-goals evidenced by each of the items on the "above list".
            Itemize your answer. One noun phrase per line.
            Each list item must be checked to be 100% consistent with the goals.
            No explanations needed, just the noun phrase, nothing else.
            Avoid starting your sentence with the word "Alternative".
            Your answer should not contain ":" .
            Your answer should avoid the word "Causes" and "causes" ."
            
    Your primary task is to identify the user's goals apparent in the CONTEXT and consider the sequential steps you can follow to achieve those goals for the user. If the tasks involve code or technical steps, be as specific and factual as possible. In all cases be very concise and clear. If the resolution of any tasks or goals are self-evident or simple, there is no need to write them out and doing so will be pointless and wastful of resources. There should be no duplication or wasteful repetition in your response. Creating a task list when no goals or tasks are contained in the CONTEXT, or where those tasks or goals are very simple and obvious, is wasteful of resources and must be avoided. 
    
    @@@ If the CONTEXT does not indicate any clear tasks or a clear goals, then output only " - ". In that instance " - " should be your only response.
    """

    # Submit the prompt to the OpenAI API
    response = openai.ChatCompletion.create(
        model=model,
        temperature=0.5, 
        ## avoid repetition in the response
        #top_p=1.0,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that understands software development and python code, as well as all suitable graphics and other python libraries. You are also a good listener and can help me with my goals. You focus on things that you can directly assist with, including planning, code generation, algorithm design and assessing efficiency. If the user's prompt does not set any clear tasks or goals then there is no need to respond with a task list. Doing so in those circumstances would be wasteful of resources and confusing or frustrating to the user. Use task lists where appropriate and avoid them where they are not necessary."},
            {"role": "user", "content": prompt}
        ]
    )
      
    return response['choices'][0]['message']['content']

