#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod backend_commands;
use backend_commands::send_prompt;

mod loadconversationhistory;
use loadconversationhistory::{fetch_chat_history};

use pyo3::prelude::*;
use pyo3::types::PyList;
use std::thread;
use std::env;
use std::collections::HashMap;
use std::time::SystemTime;
use std::fs::{metadata, remove_file};

extern crate keyring;
use keyring::Keyring;

// global mutable variable 'CONVERSATION_HISTORY' to hold all chat messages in the database
#[macro_use]
extern crate lazy_static;
use std::sync::Mutex;
lazy_static! {
    static ref CONVERSATION_HISTORY: Mutex<Vec<HashMap<String, String>>> = Mutex::new(Vec::new());
}
lazy_static! {
    static ref NUM_MESSAGES: Mutex<usize> = Mutex::new(0);
}

/*old version that returns a string
lazy_static! {
    static ref CONVERSATION_HISTORY: Mutex<String> = Mutex::new(String::new());
}
*/


fn main() -> PyResult<()> {

    clear_screen(); // clears the terminal screen for a clean loading screen
    
    // Load the full conversation history from the database into a json string variable
    {
        let mut data = CONVERSATION_HISTORY.lock().unwrap();
        match fetch_chat_history() {
            Ok(fetched_data) => {
                *data = fetched_data;
                println!("Messages in conversation at startup: {}", data.len());  // Added line
            },
            Err(e) => println!("An error occurred while fetching chat history: {}", e),
        }
    }
    
    // Print the first part of the conversation history to the terminal for testing
    /*
    {
        let data = CONVERSATION_HISTORY.lock().unwrap();
        let output: String = data.chars().take(5000).collect();
        println!("First 5000 characters: {}", output);
    }
   */
    
    
    let current_dir = env::current_dir().unwrap();
    println!("\nTauri/Svelte thread working directory is: {:?}", current_dir);

    // Start the Python backend thread
    let python_thread = thread::spawn(|| {
        pyo3::prepare_freethreaded_python();
        let gil = Python::acquire_gil();
        let py = gil.python();
        let os = py.import("os").unwrap();
        os.call_method1("chdir", ("../src/backend",)).unwrap();
        let sys_module = py.import("sys").unwrap();
        let sys_path: &PyList = sys_module.getattr("path").unwrap().downcast().unwrap();
        sys_path.append("F:\\WindowsDesktop\\Users\\Leamy\\Desktop\\ChatPerfect\\src\\backend").unwrap();
        let asyncio = py.import("asyncio").unwrap();
        let main_module = py.import("main").unwrap();
        let main_coroutine = main_module.getattr("main").unwrap().call0().unwrap();
        let event_loop = asyncio.getattr("get_event_loop").unwrap().call0().unwrap();
        event_loop.getattr("run_until_complete").unwrap().call1((main_coroutine,)).unwrap();
    });

    //
    // Realtime file monitoring of the backend files to update the frontend
    //

    // Alerts the frontend that the llm response file has been updated with new information streamed into it
    let mut file_timestamps: HashMap<String, SystemTime> = HashMap::new();
    file_timestamps.insert(
        "F:\\WindowsDesktop\\Users\\Leamy\\Desktop\\ChatPerfect\\src\\backend\\messages\\llm-response.txt".to_string(),
        SystemTime::now(),
    );

    // DB_CHANGED is the file that the backend creates when the database has been updated with a new entry.
    // This will trigger the backend to append the new entry to the chat_history json structure kept in memory
    let flag_files: Vec<String> = vec![
        "F:\\WindowsDesktop\\Users\\Leamy\\Desktop\\ChatPerfect\\src\\users\\patrick_leamy\\database\\DB_CHANGED".to_string(),
    ];

    // The files monitored are the DB_CHANGE flag file and the llm-response.txt file
    let monitor_thread = thread::spawn(move || {
        println!("\nLLM message file monitoring thread started...");
        loop {

            // DB_CHANGED file monitoring changed flag
            for file_path in &flag_files {
                if metadata(file_path).is_ok() {
                    println!("Database has been updated.");
                    // Logic for DB_CHANGED here:

                    // add a pause of 2 seconds for testing
                    //thread::sleep(std::time::Duration::from_secs_f32(2.0));

                    // Delete the flag file to lower the flag
                    if let Err(e) = remove_file(file_path) {
                        println!("Failed to remove flag file {}: {}", file_path, e);
                    }
                }
            }
            // llm-response.txt file monitoring
            for (file_path, last_checked) in &mut file_timestamps {
                match metadata(file_path) {
                    Ok(metadata) => {
                        if let Ok(modified) = metadata.modified() {
                            if modified.duration_since(*last_checked).is_ok() {
                                println!("LLM response file updated.");
                                *last_checked = SystemTime::now();
                                // Your existing logic for handling llm-response.txt
                            }
                        } else {
                            println!("Failed to get modified time for {}", file_path);
                        }
                    }
                    Err(e) => println!("Failed to get metadata for {}: {}", file_path, e),
                }
            }

            thread::sleep(std::time::Duration::from_secs_f32(0.5));
        }

    });

    tauri::Builder::default()

        .invoke_handler(tauri::generate_handler![store_openai_key, get_openai_key, send_prompt, fetch_conversation_history, get_num_messages])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");

    python_thread.join().unwrap();
    monitor_thread.join().unwrap();

    Ok(())
}


use rusqlite::{Connection, Result};
#[tauri::command]
fn get_num_messages() -> Result<usize, String> {
    let conn = Connection::open("F:\\WindowsDesktop\\Users\\Leamy\\Desktop\\ChatPerfect\\src\\users\\patrick_leamy\\database\\big.db").map_err(|e| e.to_string())?;
    
    let mut stmt = conn.prepare("SELECT COUNT(*) FROM text_blocks").map_err(|e| e.to_string())?;
    let num_messages: usize = stmt.query_row([], |row| row.get(0)).map_err(|e| e.to_string())?;

    let mut num = NUM_MESSAGES.lock().unwrap();
    *num = num_messages;

    Ok(num_messages)  // Return the number of messages
}




#[tauri::command]
fn store_openai_key(key: String) -> Result<(), String> {
    let service = "ChatPerfect";
    let username = "openai_key";
    let keyring = Keyring::new(service, username);
    keyring.set_password(&key).map_err(|e| e.to_string())
}

#[tauri::command]
fn get_openai_key() -> Result<String, String> {
    let service = "ChatPerfect";
    let username = "openai_key";
    let keyring = Keyring::new(service, username);
    match keyring.get_password() {
        Ok(key) => Ok(key),
        Err(e) => Err(e.to_string()),
    }
}

// Tauri Command to fetch a slice of CONVERSATION_HISTORY to the frontend
use serde::{Deserialize, Serialize};
use serde_json::Value;

#[derive(Deserialize)]
struct FetchParams {
  start: usize,
  end: usize,
}

#[derive(Serialize)]
struct Reply {
  message: Vec<HashMap<String, String>>,
}

#[tauri::command]
fn fetch_conversation_history(params: FetchParams) -> tauri::Result<Reply> {
  let data = CONVERSATION_HISTORY.lock().unwrap();
  
  // No need for parsing, directly use the data
  let slice = &data[params.start..params.end];

  Ok(Reply {
    message: slice.to_vec(),
  })
}



/* old version that returns a string
use serde::{Deserialize, Serialize};
use serde_json::Value;
#[derive(Deserialize)]
struct FetchParams {
  start: usize,
  end: usize,
}
#[derive(Serialize)]
struct Reply {
  message: Vec<Value>,
}
#[tauri::command]
fn fetch_conversation_history(params: FetchParams) -> tauri::Result<Reply> {
  let data = CONVERSATION_HISTORY.lock().unwrap();
  let parsed_data: Vec<Value> = serde_json::from_str(&data).unwrap();
  
  let slice = &parsed_data[params.start..params.end];

  Ok(Reply {
    message: slice.to_vec(),
  })
}
*/

// Just clears the terminal screen :)
use std::io::{self, Write};
use std::process::Command;
fn clear_screen() {
    if cfg!(target_os = "windows") {
        let _ = Command::new("cmd")
            .args(&["/C", "cls"])
            .status();
    } else {
        print!("\x1b[2J\x1b[1;1H");
        let _ = io::stdout().flush();
    }
}

