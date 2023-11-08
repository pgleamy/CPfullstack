import os
import pickle
import torch
from transformers import AutoModel, AutoTokenizer
import faiss
from transformers import logging
import numpy as np
import spacy
from retrieve_text import get_full_text
import pdb
import aiofiles

## DIAGNOSTICS. Set to 1 to run the testing print statements and 0 to not run them 
testing = 0

# obtain application data directory
appdata_dir = os.getenv('APPDATA')
# Append "Chatperfect" to the application data directory
appdata_dir = os.path.join(appdata_dir, "Chatperfect")

## SQLite database path
db_path = os.path.join(os.getcwd(), appdata_dir, 'messages', 'database', 'full_text_store.db')

logging.set_verbosity_error()  # to only display error messages
nlp = spacy.load("en_core_web_sm")


"""
This function queries an index for text similar to the input query_text and returns a list of full texts corresponding to each block_id, sorted by similarity score from highest to lowest.

Parameters:
index_filename (str): The name of the index file.
query_text (str): The text to query the index with.
top_k (int): The number of most similar results to store for each sentence in the query.

The function works as follows:
1. It checks if the index file exists. If not, it prints an error message and returns.
2. It reads the index and the associated metadata from the index file.
3. It loads a pretrained BERT model and tokenizer.
4. It breaks the query_text into sentences.
5. For each sentence, it tokenizes the sentence, feeds it into the BERT model to get an embedding, and queries the index with the embedding.
6. It stores the metadata of the top_k most similar results from the index in the relevant_vectors list.
7. It extracts the unique block_ids from the relevant_vectors and sorts them in descending order.
8. It uses the get_full_text function to find the full text for each block_id in the sorted list.
9. It returns a list of full texts corresponding to each block_id, sorted by similarity score from highest to lowest.

Returns:
list: A list of full texts corresponding to each block_id, sorted by similarity score from highest to lowest.
"""
async def query_index(index_filename: str, query_text: str, top_k=5): # the number of nearest neighbors to return is = top_k
    if not os.path.exists(index_filename):
        return

    index = faiss.read_index(index_filename)
    async with aiofiles.open(f"{index_filename}_metadata_mapping.pkl", "rb") as f:
        metadata_mapping = pickle.loads(await f.read())
        if testing == 1:
            print("metadata_mapping: ", metadata_mapping)

    #model = AutoModel.from_pretrained("intfloat/e5-large-v2")
    #tokenizer = AutoTokenizer.from_pretrained("intfloat/e5-large-v2")
    
    model = AutoModel.from_pretrained("../backend/models/bge-large-en-v1.5")
    tokenizer = AutoTokenizer.from_pretrained("../backend/models/bge-large-en-v1.5")
    model.eval()
    
    # breaks query_text into sentences and stores in results
    doc = nlp(query_text)
    sentences = [sent.text for sent in doc.sents]
    relevant_vectors = []

    for sentence in sentences:
        input_ids = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True, max_length=128)["input_ids"]

        with torch.no_grad():
            outputs = model(input_ids)
        embeddings = outputs.last_hidden_state
        vector = embeddings.mean(dim=1).numpy().squeeze()
        vector = vector.reshape(-1)
        if vector.shape[0] != index.d:
            vector = vector[:index.d]

        D, I = index.search(vector.reshape(1, -1), top_k)
        for i in range(I.shape[1]):
            idx = I[0, i]
            metadata = next((block_id for block_id, (start, end) in metadata_mapping.items() if start <= idx <= end), None)
            if metadata is not None:
                if testing == 1:
                    print(f"idx: {idx}, metadata: {metadata}")
                relevant_vectors.append(metadata)
            
    # Extract unique block_ids
    block_ids = list(set(relevant_vectors))
    if testing == 1:
        print("block_ids: ", block_ids)
    block_ids.sort(reverse=True)

    # Use get_full_text to find the full text for each block_id
    full_texts = [await get_full_text(db_path, block_id) for block_id in block_ids]

    if testing == 1:
        print("full_texts: ", full_texts)
    
    return full_texts