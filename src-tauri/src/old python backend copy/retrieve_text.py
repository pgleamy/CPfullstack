import aiosqlite

async def get_full_text(db_path, block_id):
    """
    This function takes as input a SQLite database file and a target block_id. 
    Returns the full text associated with the block_id number from the SQLite database.

    Parameters:
    db_path (str): The path to the SQLite database file.
    block_id (str): The target block_id.

    Returns:
    str: The full text associated with the block_id. If the block_id is not found, returns None.
    """
    # Connect to the SQLite database
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.cursor()
    
        # Query the database for the full text associated with the block_id
        await cursor.execute("SELECT text FROM text_blocks WHERE block_id = ?", (block_id,))
        result = await cursor.fetchone()

        # If the block_id was found, return the full text. Otherwise, return None.
        if result is not None:
            return result[0]
        else:
            return None

