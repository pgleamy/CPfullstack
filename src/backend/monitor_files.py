import os
import asyncio

async def monitor_files():
    user_prompt_path = "/messages/user_prompt.txt"
    llm_response_path = "/messages/llm_response.txt"

    user_prompt_mtime = 0
    llm_response_mtime = 0

    user_prompt_last_pos = 0
    llm_response_last_pos = 0

    while True:
        # Check if user_prompt.txt has been modified
        new_user_prompt_mtime = os.path.getmtime(user_prompt_path)
        if new_user_prompt_mtime != user_prompt_mtime:
            user_prompt_mtime = new_user_prompt_mtime
            with open(user_prompt_path, 'r') as f:
                file_size = os.path.getsize(user_prompt_path)
                if file_size < user_prompt_last_pos:
                    # File has been truncated, reset position
                    user_prompt_last_pos = 0
                f.seek(user_prompt_last_pos)
                new_data = f.read()
                user_prompt_last_pos = f.tell()
            # Do something with new_data

        # Check if llm_response.txt has been modified
        new_llm_response_mtime = os.path.getmtime(llm_response_path)
        if new_llm_response_mtime != llm_response_mtime:
            llm_response_mtime = new_llm_response_mtime
            with open(llm_response_path, 'r') as f:
                file_size = os.path.getsize(llm_response_path)
                if file_size < llm_response_last_pos:
                    # File has been truncated, reset position
                    llm_response_last_pos = 0
                f.seek(llm_response_last_pos)
                new_data = f.read()
                llm_response_last_pos = f.tell()
            # Do something with new_data

        await asyncio.sleep(0.5)



