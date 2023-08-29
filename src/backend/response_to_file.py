import os
import asyncio
import aiofiles

async def write_to_file(content, file_path = os.path.join('messages', 'llm-response.txt')):
    """
    Writes the entire content to the specified file at once.

    :param content: The content to write to the file.
    :param file_path: The path to the file where the content will be written.
    """
    async with aiofiles.open(file_path, 'w') as file:
        await file.write(content)

# Asyncronously streamed file writing. The "content_generator" must be an asyncronous generator.
async def stream_to_file(content_generator, file_path = os.path.join('messages', 'llm-response.txt')):
    """
    Writes content to the specified file in real-time as it's generated.

    :param content_generator: A generator that yields content to be written to the file.
    :param file_path: The path to the file where the content will be written.
    """
    async with aiofiles.open(file_path, 'w') as file:
        loop = asyncio.get_event_loop()
        async for chunk in content_generator:
            await file.write(chunk)
            await file.flush() # Flush the content to the file as it's generated
            await loop.run_in_executor(None, os.fsync, file.fileno()) # Ensure the content is written to disk
