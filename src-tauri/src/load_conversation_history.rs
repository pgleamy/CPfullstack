// Import necessary modules
extern crate rusqlite;
extern crate serde_json;

use rusqlite::{params, Connection, Result};
use std::collections::HashMap;
use std::error::Error;
use std::path::PathBuf;


pub fn fetch_chat_history(database_path: &PathBuf) -> Result<Vec<HashMap<String, String>>, Box<dyn Error>> {

    // Append the database file name to the directory path
    let db_file = database_path.join("full_text_store.db");
    // Open the database file
    let conn = Connection::open(db_file)?;

    // Prepare the SQL statement
    //let mut stmt = conn.prepare("SELECT * FROM text_blocks ORDER BY timestamp")?;
    // Prepare the SQL statement
    let mut stmt = conn.prepare("SELECT * FROM text_blocks ORDER BY timestamp")?;

    let mut results: Vec<HashMap<String, String>> = Vec::new();

    // Query the database
    let rows = stmt.query_map(params![], |row| {
        let block_id: String = row.get(0)?;
        let text: String = row.get(1)?;
        let timestamp: String = row.get(2)?;
        let status: String = row.get(3)?;
        let source: String = row.get(4)?;
        let llm_name: String = row.get(5)?;
        let llm_role: String = row.get(6)?;
        let user_name: String = row.get(7)?;
        let message_num: u32 = row.get(8)?;

        let mut record = HashMap::new();
        record.insert("block_id".to_string(), block_id);
        record.insert("text".to_string(), text);
        record.insert("timestamp".to_string(), timestamp);
        record.insert("status".to_string(), status);
        record.insert("source".to_string(), source);
        record.insert("llm_name".to_string(), llm_name);
        record.insert("llm_role".to_string(), llm_role);
        record.insert("user_name".to_string(), user_name);
        record.insert("message_num".to_string(), message_num.to_string());

        Ok(record)
    })?;

    // Collect the rows into results vector
    for row in rows {
        results.push(row?);
    }

    println!("Fetched chat history from database.");

    // Return results
    Ok(results)
}



