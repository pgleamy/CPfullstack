// Import necessary modules
extern crate rusqlite;
extern crate serde_json;

use rusqlite::{params, Connection, Result};
use std::collections::HashMap;
use std::error::Error;

pub fn fetch_chat_history() -> Result<Vec<HashMap<String, String>>, Box<dyn Error>> {
    // Open the database file
    let conn = Connection::open("F:\\WindowsDesktop\\Users\\Leamy\\Desktop\\ChatPerfect\\src\\users\\patrick_leamy\\database\\big.db")?;

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

        let mut record = HashMap::new();
        record.insert("block_id".to_string(), block_id);
        record.insert("text".to_string(), text);
        record.insert("timestamp".to_string(), timestamp);
        record.insert("status".to_string(), status);
        record.insert("source".to_string(), source);
        record.insert("llm_name".to_string(), llm_name);
        record.insert("llm_role".to_string(), llm_role);
        record.insert("user_name".to_string(), user_name);

        Ok(record)
    })?;

    // Collect the rows into results vector
    for row in rows {
        results.push(row?);
    }

    // Return results
    Ok(results)
}







/* old version that returns a string
pub fn fetch_chat_history() -> Result<String, Box<dyn std::error::Error>> {
    // Open the database file
    let conn = Connection::open("F:\\WindowsDesktop\\Users\\Leamy\\Desktop\\ChatPerfect\\src\\users\\patrick_leamy\\database\\big.db")?;

    // Prepare to query all entries from the table
    let mut stmt = conn.prepare("SELECT * FROM text_blocks ORDER BY timestamp")?;
    let mut results = Vec::new();

    let rows = stmt.query_map(params![], |row| {
        let block_id: String = row.get(0)?;
        let text: String = row.get(1)?;
        let timestamp: String = row.get(2)?;
        let status: String = row.get(3)?;
        let source: String = row.get(4)?;
        let llm_name: String = row.get(5)?;
        let llm_role: String = row.get(6)?;
        let user_name: String = row.get(7)?;

        let mut record = HashMap::new();
        record.insert("block_id", block_id);
        record.insert("text", text);
        record.insert("timestamp", timestamp);
        record.insert("status", status);
        record.insert("source", source);
        record.insert("llm_name", llm_name);
        record.insert("llm_role", llm_role);
        record.insert("user_name", user_name);

        Ok(record)
    })?;

    for row in rows {
        results.push(row?);
    }

    // Serialize the results into pretty-formatted JSON
    let db_history = serde_json::to_string_pretty(&results)?;

    println!("Conversation history loaded to memory...");

    // Return the pretty-formatted JSON string as the Result
    Ok(db_history)
}
*/


/*
use tauri::State;
// Function to add a new message and update the state
pub fn add_new_message(new_message: HashMap<String, String>, chat_history_state: &State<Vec<HashMap<String, String>>>) {
    // Update the database with the new message here...
    
    // Then, update the Tauri state
    let mut chat_history = chat_history_state.lock().unwrap();
    chat_history.push(new_message);
}
*/

