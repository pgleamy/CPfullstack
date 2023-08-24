import os

async def write_to_file(content, file_path='..\\src\\backend\\messages\\llm-response.txt'):
    """
    Writes the entire content to the specified file at once.

    :param content: The content to write to the file.
    :param file_path: The path to the file where the content will be written.
    """
    with open(file_path, 'w') as file:
        file.write(content)

async def stream_to_file(content_generator, file_path='..\\src\\backend\\messages\\llm-response.txt'):
    """
    Writes content to the specified file in real-time as it's generated.

    :param content_generator: A generator that yields content to be written to the file.
    :param file_path: The path to the file where the content will be written.
    """
    with open(file_path, 'w') as file:
        for chunk in content_generator:
            file.write(chunk)
            file.flush() # Flush the content to the file as it's generated
            os.fsync(file.fileno()) # Ensure the content is written to disk
