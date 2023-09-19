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

// global mutable variable 'chat_history' to hold all chat messages in the database
#[macro_use]
extern crate lazy_static;
use std::sync::Mutex;
//use tauri::State;
lazy_static! {
    static ref conversation_history: Mutex<String> = Mutex::new(String::new());
}


fn main() -> PyResult<()> {

    clear_screen(); // clears the terminal screen
    
    // Load the full conversation history from the database into a json string variable
    {
        let mut data = conversation_history.lock().unwrap();
        match fetch_chat_history() {
            Ok(fetched_data) => *data = fetched_data,
            Err(e) => println!("An error occurred while fetching chat history: {}", e),
        }
    }
    
    
    let current_dir = env::current_dir().unwrap();
    println!("\nTauri/Svelte thread working directory is: {:?}", current_dir);

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

        .invoke_handler(tauri::generate_handler![store_openai_key, get_openai_key, send_prompt])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");

    python_thread.join().unwrap();
    monitor_thread.join().unwrap();

    Ok(())
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

/* #[tauri::command]
fn get_chat_history() -> String {
  
  conversation_history.clone()
} */


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

