import unittest
import os
from embedV3 import add_to_index, load_text
from queryV3 import query_index
import sqlite3
import time

class TestEmbedAndQuery(unittest.TestCase):
    def setUp(self):
        print("Setting up test...\n")
        self.index_filename = os.path.join("index", "index.faiss")
        self.text_filename = os.path.join("DOCS", "test_text.txt")
        self.query_text = "This is a test query"
        self.db_path = os.path.join(os.getcwd(), 'database', 'full_text_store.db')

    def test_add_to_index_and_query_index(self):
        print("Testing add_to_index and query_index functions...\n")
        # Ensure the text file exists
        self.assertTrue(os.path.exists(self.text_filename), "Text file does not exist.")

        # Load text from the file
        print("Loading text from file...\n")
        text = load_text(self.text_filename)

        # Add the text to the index
        print("Adding text to index...\n")
        add_to_index(self.index_filename, text)

        # Ensure the index file was created
        print("Ensuring index file was created...\n")
        self.assertTrue(os.path.exists(self.index_filename), "Index file was not created.")

        # Query the index
        print("Querying index...\n")
        results = query_index(self.index_filename, self.query_text)

        # Ensure the query returned results
        print("Ensuring query returned results...\n")
        self.assertIsNotNone(results, "No results returned from query.")

        # Ensure the results are a list
        print("Ensuring results are a list...\n")
        self.assertIsInstance(results, list, "Results are not a list.")

        # Ensure the list is not empty
        print("Ensuring results list is not empty...\n")
        self.assertTrue(len(results) > 0, "Results list is empty.")

    def tearDown(self):
        # time.sleep(60) # Pause a short time to allow prior operation to complete
        # Delete the index file and metadata mapping file if they exist
        if os.path.exists(self.index_filename):
            os.remove(self.index_filename)
        if os.path.exists(f"{self.index_filename}_metadata_mapping.pkl"):
            os.remove(f"{self.index_filename}_metadata_mapping.pkl")

        # Delete the text blocks from the SQLite database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM text_blocks WHERE block_id LIKE 'block_id_%'")
        conn.commit()
        conn.close()

if __name__ == "__main__":
    unittest.main()

