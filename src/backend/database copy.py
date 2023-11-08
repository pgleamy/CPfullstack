import os
import aiosqlite

async def verify_create_database(database_path: str):
    db_dir = database_path
    db_name = 'full_text_store.db'
    db_path = os.path.join(db_dir, db_name)

    if not os.path.exists(db_path):  # Check if the database file already exists
        os.makedirs(db_dir, exist_ok=True)  # Make sure the directory exists

        conn = await aiosqlite.connect(db_path)  # This line creates a new database file
        c = await conn.cursor()

        # This line creates a new table called text_blocks with the columns block_id, text, timestamp, status, source, llm_name, llm_role, and username
        # extended the columns on Nov 6 23' to include source, llm_name, llm_role, username, and message_num. Also status now defaults to 'SEEN' 
        # SEEN vs IGNORED will be implemented later, to not query within IGNORED message block_ids or return any IGNORED messages
        await c.execute('''
            CREATE TABLE text_blocks
            (block_id TEXT PRIMARY KEY,
             text TEXT NOT NULL,
             timestamp TEXT NOT NULL,
             status TEXT NOT NULL DEFAULT 'SEEN',
             source TEXT NOT NULL,
             llm_name TEXT NOT NULL,
             llm_role TEXT NOT NULL,
             username TEXT NOT NULL,
             message_num INTEGER NOT NULL);
        ''')

        await conn.commit()  # This line saves the changes to the database

        return conn  # Return the connection instead of closing it