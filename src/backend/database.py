import os
import aiosqlite

async def verify_create_database(database_path: str):
    db_dir = database_path
    db_name = "full_text_store.db"
    db_full_path = os.path.join(db_dir, db_name)

    # Check the existence and some attributes of the path
    print(f"Checking existence of {db_full_path}: {os.path.exists(db_full_path)}")
    print(f"Is file: {os.path.isfile(db_full_path)}")
    print(f"Is directory: {os.path.isdir(db_full_path)}")
    print(f"Can access: {os.access(db_full_path, os.R_OK)}")


    conn = await aiosqlite.connect(db_full_path)
    c = await conn.cursor()
    
    # Check if the database file already exists before attempting to connect
    if not os.path.exists(db_full_path):
        
        print("Creating database...")

        print("Creating table...")
        await c.execute('''
            CREATE TABLE text_blocks (
                block_id TEXT PRIMARY KEY,
                text TEXT NOT NULL,l;.
                timestamp TEXT NOT NULL,
                status TEXT NOT NULL, 
                source TEXT NOT NULL,
                llm_name TEXT NOT NULL,
                llm_role TEXT NOT NULL, 
                username TEXT NOT NULL,
                message_num INTEGER NOT NULL
            );
        ''')

        await conn.commit()
        print("Database created.")
    else:
        print("Database file seems to exist already.")
        # Add more checks here if needed

    return conn
