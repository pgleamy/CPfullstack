import os
import aiofiles, aiosqlite
import pickle
import torch
from transformers import AutoModel, AutoTokenizer
import faiss
faiss.omp_set_num_threads(4) # set number of threads for Faiss to use for embeddings
from transformers import logging
import numpy as np
import spacy
from datetime import datetime
import json

# obtain application data directory
appdata_dir = os.getenv('APPDATA')
# Append "Chatperfect" to the application data directory
appdata_dir = os.path.join(appdata_dir, "Chatperfect")

## Database path
db_path = os.path.join(os.getcwd(), appdata_dir, 'messages', 'database', 'full_text_store.db')
print("db_path is: ", db_path)

## message_meta.json path
message_meta = os.path.join(os.getcwd(), appdata_dir, 'messages', 'message_meta.json')
#print("message_meta data path: ", message_meta)

logging.set_verbosity_error()  # to only display error messages
nlp = spacy.load("en_core_web_sm")

# Returns a formatted human readable stamp
## Use: timestamp = timestamp()
def timestamp():
    # Get the current date and time
    now = datetime.now()

    # Pre-compute month names
    MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    # Extract various components of the datetime object
    year = now.year
    month = MONTH_NAMES[now.month - 1]
    day = now.day
    hour = now.hour
    minute = now.minute
    second = now.second

    # Determine AM or PM
    ampm = "am" if hour < 12 else "pm"
    
    # Convert hour to 12-hour format
    hour_12 = hour % 12
    if hour_12 == 0:
        hour_12 = 12

    # Assemble the timestamp string
    timestamp = f"{month} {day}, {year}, {hour_12}:{str(minute).zfill(2)} {str(second).zfill(2)}s {ampm}"
    return timestamp


# All messages have the status of SEEN initially, until they are later marked as IGNORED
async def add_to_index(index_filename: str, text: str, user_or_llm: str, status: str = "SEEN", ) -> None:
    if os.path.exists(index_filename):
        index = faiss.read_index(index_filename)
        async with aiofiles.open(f"{index_filename}_metadata_mapping.pkl", "rb") as f:
            metadata_mapping = pickle.loads(await f.read())
    else:
        dimension = 1024
        index = faiss.IndexHNSWFlat(dimension, 64) # determines the number of bidirectional links each element will have with other elements in the index. 64 is high for accuracy
        index.hnsw.efConstruction = 60  # affects the size of the dynamic candidate list when inserting new elements, which influences quality. 60 is high for accuracy
        metadata_mapping = {}

    # Old embedding model
    #model = AutoModel.from_pretrained("intfloat/e5-large-v2")
    #tokenizer = AutoTokenizer.from_pretrained("intfloat/e5-large-v2")
    # Upgraded to BAAI embedding model Nov 1 2023
    # model stored within project folder
    model = AutoModel.from_pretrained("../backend/models/bge-large-en-v1.5")
    tokenizer = AutoTokenizer.from_pretrained("../backend/models/bge-large-en-v1.5")
    model.eval()

    # Define the window size and stride
    # increasing the overlap may allow for more accurate query results, but each vector will be 50% watered down, so perhaps not
    window_size = 1  # embed 1 sentence at a time for better semantic accuracy and retrieval accuracy (best in chatbot context)
    stride = 1  # move forward 1 sentence and repeat. This is a 0% overlap. Stores maximal context for each sentence.

    # nlp uses spaCy to cut the text into individual sentences
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]

    # Process each window separately
    start_idx = index.ntotal
    for i in range(0, len(sentences) - window_size + 1, stride):
        window_sentences = sentences[i:i+window_size]
        window_text = " ".join(window_sentences)
        input_ids = tokenizer(window_text, return_tensors="pt", truncation=True, padding=True, max_length=window_size)["input_ids"]

        for ids in input_ids:
            with torch.no_grad():
                outputs = model(ids.unsqueeze(0))
            embeddings = outputs.last_hidden_state

            # Calculate the average of the token embeddings
            vector = embeddings.mean(dim=1).numpy().squeeze()

            # Ensure the vector is 1-D and has the correct dimension
            vector = vector.reshape(-1)
            if vector.shape[0] != index.d:
                vector = vector[:index.d]

            # Add the vector to the index
            index.add(vector.reshape(1, -1))
    end_idx = index.ntotal - 1
    
    # Determine the next message_num from the database
    async with aiosqlite.connect(db_path) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT MAX(message_num) FROM text_blocks")
            result = await cursor.fetchone()
            current_max_message_num = result[0] if result[0] is not None else 1
            message_num = current_max_message_num + 1
    
    # Get message metadata from message_meta.json
    async with aiofiles.open(message_meta, "r") as f:
        message_meta_json = json.loads(await f.read())
        source = user_or_llm
        llm_name = message_meta_json["llm_name"]
        llm_role = message_meta_json["llm_role"]
        username = message_meta_json["username"]
        print("Current message_meta_json: ", message_meta_json)
    
    # Create metadata for the full text block of the message
    block_id = f"block_id_{index.ntotal - 1}"  # Unique block_id for this message
    metadata = {
        "block_id": block_id,  # Unique block_id representing this text in the vector index. Each message will encompass a range of block_ids
        "timestamp": timestamp(),  # The current timestamp
        "status": "SEEN",  # The status of the message, defaulted to SEEN via hardcoded value
        "source": source,  # passed into the function from main.py
        "llm_name": llm_name,  # from message_meta.json
        "llm_role": llm_role,  # from message_meta.json
        "username": username,  # from message_meta.json
        "message_num": message_num,  # sequential message numbers starting from 1
    }

    # Store the full text in DB
    async with aiosqlite.connect(db_path) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(
                """
                INSERT INTO text_blocks 
                (block_id, text, timestamp, status, source, llm_name, llm_role, username, message_num) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, 
                (
                    metadata["block_id"], 
                    text, 
                    metadata["timestamp"], 
                    metadata["status"], 
                    metadata["source"], 
                    metadata["llm_name"], 
                    metadata["llm_role"], 
                    metadata["username"], 
                    metadata["message_num"]
                )
            )            
        await conn.commit()
            
    # Set a file flag to 1 (dirty) to indicate that the database has been updated
    # This is used by the frontend to trigger a refresh of messages displayed in the UI
    async with aiofiles.open(os.path.join(appdata_dir, "messages", "database", "DB_CHANGED.txt"), 'w') as f: await f.write(str(1))

    # Update the metadata_mapping
    metadata_mapping[block_id] = (start_idx, end_idx, message_num)

    # Save the index and metadata_mapping
    faiss.write_index(index, index_filename)
    async with aiofiles.open(f"{index_filename}_metadata_mapping.pkl", "wb") as f:
        await f.write(pickle.dumps(metadata_mapping))
 

