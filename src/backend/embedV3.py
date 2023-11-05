import os
import aiofiles, aiosqlite
import pickle
import torch
from transformers import AutoModel, AutoTokenizer
import faiss
from transformers import logging
import numpy as np
import spacy
from datetime import datetime
# prior syncrounous version
#import sqlite3

## SQLite3 Database path
db_path = os.path.join(os.getcwd(), '..', 'users', 'patrick_leamy', 'database', 'full_text_store.db')

logging.set_verbosity_error()  # to only display error messages
nlp = spacy.load("en_core_web_sm")

## Functions: add_to_index, timestamp, load_text

# Returns a date/time stamp accurate to a 1000th of a second.
## Use: timestamp = timestamp()

# old function
#def timestamp():
    # Get the current date and time
#    now = datetime.now()
    # Convert it to a string, including milliseconds
 #   timestamp = now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
 #   return timestamp
 
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

"""
The add_to_index function takes as input an index filename, a text block, and an optional status flag, and adds the text to the 
Faiss index file specified. 

Parameters:
    index_filename (str): The name of the Faiss index file.
    text (str): The text block to be added to the index.
    status (str, optional): An optional status flag that can be set to "ACCEPTED" or "DELETED". 
                            By default, it's set to "NONE".

Returns:
    None

The function performs the following steps:

1. It checks if the index file already exists. If it does, the function loads the existing Faiss index. 
   If it doesn't, a new Faiss index is created with a dimensionality of 1024 and an hnsw (hierarchical 
   navigable small world) construction parameter of 50.

2. It loads a pre-trained BERT-large model and tokenizer from the transformers library.

3. It sets a window size and stride for tokenizing the text. Here, window size refers to the number of 
   sentences to be tokenized together as a single unit, and stride refers to the number of sentences to move 
   forward after each window.

4. It uses spaCy to split the input text into individual sentences.

5. It then starts a loop where each window of sentences (as defined by the stride and window size) is 
   processed separately. 

6. Inside this loop, for each window, it tokenizes the sentences using the BERT tokenizer and then generates 
   an embedding for the tokens using the BERT model. The function then computes an average of the token 
   embeddings to create a single vector representation for the window of sentences. 

7. It checks if the generated vector has the correct dimensionality, and if not, trims it to the right size.

8. The vector is then added to the Faiss index.

9. A unique block ID is generated for each text block, which is simply "block_id_" followed by the total number 
   of vectors in the index minus 1 (since indexing starts from 0). 

10. It then inserts the block ID, the entire original text block, timestamp, and status flag into a SQLite database.

11. Finally, the updated Faiss index is written back to the file.
"""
async def add_to_index(index_filename: str, text: str, status: str = "NONE") -> None:
    if os.path.exists(index_filename):
        index = faiss.read_index(index_filename)
        async with aiofiles.open(f"{index_filename}_metadata_mapping.pkl", "rb") as f:
            metadata_mapping = pickle.loads(await f.read())
    else:
        dimension = 1024
        index = faiss.IndexHNSWFlat(dimension, 32)
        index.hnsw.efConstruction = 50
        metadata_mapping = {}

    #model = AutoModel.from_pretrained("intfloat/e5-large-v2")
    #tokenizer = AutoTokenizer.from_pretrained("intfloat/e5-large-v2")
    
    model = AutoModel.from_pretrained("BAAI/bge-large-en-v1.5")
    tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-large-en-v1.5")

    # Define the window size and stride
    # increasing the overlap may allow for more accurate query results, but each vector will be 50% watered down, so perhaps not
    window_size = 1  # embed 1 sentence at a time
    stride = 1  # move forward 1 sentence and repeat. This is a 0% overlap. Stores maximal context for each sentence.

    # nlp uses spaCy to cut the text into individual sentences
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]

    # Process each window separately
    start_idx = index.ntotal
    for i in range(0, len(sentences) - window_size + 1, stride):
        window_sentences = sentences[i:i+window_size]
        window_text = " ".join(window_sentences)
        input_ids = tokenizer(window_text, return_tensors="pt", truncation=True, max_length=window_size)["input_ids"]

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

    # Create metadata for this text block
    block_id = f"block_id_{index.ntotal - 1}"  # Unique block_id
    metadata = {"block_id": block_id, "timestamp": timestamp() }

    # Store the full text in SQLite3
    async with aiosqlite.connect(db_path) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("INSERT INTO text_blocks (block_id, text, timestamp, status) VALUES (?, ?, ?, ?)", (block_id, text, timestamp(), status))  #metadata["timestamp"], status))
            await conn.commit()
            
            # Set a file flag to 1 (dirty) to indicate that the database has been updated
            async with aiofiles.open('../users/patrick_leamy/database/DB_CHANGED', 'w') as f: await f.write(str(1))

    # Update the metadata_mapping
    metadata_mapping[block_id] = (start_idx, end_idx)

    # Save the index and metadata_mapping
    faiss.write_index(index, index_filename)
    async with aiofiles.open(f"{index_filename}_metadata_mapping.pkl", "wb") as f:
        await f.write(pickle.dumps(metadata_mapping))
    # prior syncronouse code
    #with open(f"{index_filename}_metadata_mapping.pkl", "wb") as f:
    #    pickle.dump(metadata_mapping, f)
        

# Function to load text from a .txt file in utf-8 encoding, returns the file contents as a string
## Use: text = load_text("filename.txt")
## Used to ensure that any file loaded for embedding is loaded in the correct format

def load_text(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

