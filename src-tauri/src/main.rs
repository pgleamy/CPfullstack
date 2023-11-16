#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

// Supports single instance plugin PLUS local directory structure builder
use tauri::Manager;

#[derive(Clone, serde::Serialize)]
struct Payload {
  args: Vec<String>,
  cwd: String,
} // end single instance plugin support

mod backend_commands;
use backend_commands::send_prompt;

mod load_conversation_history;
use load_conversation_history::fetch_chat_history;

use pyo3::prelude::*;
use pyo3::types::PyList;
use std::thread;
use std::env;
use std::collections::HashMap;
use std::time::SystemTime;
use std::fs::{metadata, remove_file};


use tauri::api::path::app_data_dir;
//use serde_json;
use std::fs;
use std::path::PathBuf;

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

/// Creates a custom directory structure within the app's directory and saves the paths to a JSON file.
// Define a structure to hold the paths
#[derive(Serialize, Deserialize)]
struct DirectoryPaths {
    messages_path: PathBuf,
    database_path: PathBuf,
    docs_drop_path: PathBuf,
}

fn create_directory_structure<A: tauri::Assets>(ctx: &tauri::Context<A>) -> Result<DirectoryPaths, std::io::Error> {
    let data_directory = app_data_dir(ctx.config()).expect("failed to get app data dir");
    let custom_directories = vec![
        data_directory.join("messages"),
        data_directory.join("messages/database"),
        data_directory.join("messages/docs_drop"),
    ];

    let mut directory_paths = Vec::new();

    for dir in custom_directories.iter() {
        if !dir.exists() {
            fs::create_dir_all(dir)?;
        }
        //println!("User data directory confirmed: {}", dir.to_string_lossy());
        directory_paths.push(dir.to_str().unwrap_or_default().to_string());
    }


    let messages_path = data_directory.join("messages");
    let database_path = messages_path.join("database");
    let docs_drop_path = messages_path.join("docs_drop");


    let file_path = data_directory.join("directory_paths.json");

    // Convert the Vec<String> into JSON
    let json = serde_json::to_string(&directory_paths).map_err(|e| std::io::Error::new(std::io::ErrorKind::Other, e))?;

    // Write the JSON to the file in the current directory
    fs::write(file_path, json)?;

    // Populate the DirectoryPaths struct
    let path = DirectoryPaths {
        messages_path,
        database_path,
        docs_drop_path,
    };
    //println!("Messages Path: {:?}", path.messages_path);
    //println!("Database Path: {:?}", path.database_path);
    //println!("Docs Drop Path: {:?}", path.docs_drop_path);

    Ok(path)
}


// If the DB file does not exist then create it and populate it with the correct schema
use rusqlite::params;
pub fn ensure_db_schema(database_path: &PathBuf) -> Result<(), rusqlite::Error> {
    // Append the database file name to the path
    let db_full_path = database_path.join("full_text_store.db");
    // Convert PathBuf to a string representation
    let db_full_path_str = db_full_path
        .to_str()
        .ok_or_else(|| rusqlite::Error::InvalidPath(database_path.clone()))?;   

    let conn = Connection::open(db_full_path_str)?;

    // This SQL statement will only create the table if it doesn't already exist
    conn.execute(
        "CREATE TABLE IF NOT EXISTS text_blocks (
            block_id TEXT PRIMARY KEY,
            text TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            status TEXT NOT NULL, 
            source TEXT NOT NULL,
            llm_name TEXT NOT NULL,
            llm_role TEXT NOT NULL, 
            username TEXT NOT NULL,
            message_num INTEGER NOT NULL
        );",
        params![],
    )?;

    Ok(())
}


fn main() -> PyResult<()> {

    //clear_screen(); // clears the terminal screen for a clean loading screen


    // Use the current directory as the base path or specify another path
    let ctx = tauri::generate_context!();

    let mut messages_path = PathBuf::new();
    let mut database_path = PathBuf::new();
    let mut docs_drop_path = PathBuf::new();

    let directory_structure_result = create_directory_structure(&ctx);

    // Populate the variables with the paths
    match directory_structure_result {
        Ok(path) => {
            // Now you can use dir_paths_struct in your main function
            println!("Directory structure created/confirmed successfully.");

            // Store the paths in the variables.
            messages_path = path.messages_path;
            database_path = path.database_path;
            docs_drop_path = path.docs_drop_path;
            
            println!("Docs drop path initialized but not yet used: {:?}", docs_drop_path);
        },
        Err(e) => {
            eprintln!("Failed to create or confirm existing user data directory structure: {}", e);
        }
    }
   
    let current_dir = env::current_dir().unwrap();
    println!("Tauri/Svelte thread working directory is: {:?}", current_dir);

    ensure_db_schema(&database_path).unwrap();


    // Load the full conversation history from the database into a json string variable
    {
        let mut data = CONVERSATION_HISTORY.lock().unwrap();
        // print current database path
        println!("Database path: {:?}", &database_path);
        //let db_file_path = database_path.join("full_text_store.db");
        //println!("Database file path: {:?}", &database_path);
    
        match fetch_chat_history(&database_path) {
            Ok(fetched_data) => {
                *data = fetched_data;
                println!("Messages in conversation at startup: {}", data.len());
            },
            Err(e) => println!("An error occurred while fetching chat history: {}", e),
        }
    }

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
    let mut file_timestamps: HashMap<PathBuf, SystemTime> = HashMap::new();
    let llm_response_file = messages_path.join("llm_response.txt"); // Use the messages_path from DirectoryPaths
    file_timestamps.insert(llm_response_file, SystemTime::now());

    // DB_CHANGED is the file that the backend creates when the database has been updated with a new entry.
    // This will trigger the backend to append the new entry to the chat_history json structure kept in memory
    let flag_files: Vec<PathBuf> = vec![database_path.join("DB_CHANGED")];


    println!("Flag files: {:?}", flag_files); // debug


    // The files monitored are the DB_CHANGE flag file and the llm-response.txt file
    let monitor_thread = thread::spawn(move || {
        println!("LLM message file monitoring thread started.");
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
                        println!("Failed to remove flag file {}: {}", file_path.display(), e);
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
                            println!("Failed to get modified time for {}", file_path.display());
                        }
                    }
                    Err(e) => println!("Failed to get metadata for {}: {}", file_path.display(), e),
                }
            }

            thread::sleep(std::time::Duration::from_secs_f32(0.5));
        }

    });

    tauri::Builder::default()



        .plugin(tauri_plugin_single_instance::init(|app, argv, cwd| { // limits ChatPerfect to a single running instance See: https://github.com/tauri-apps/plugins-workspace/tree/v1/plugins/single-instance
            println!("{}, {argv:?}, {cwd}", app.package_info().name);

            app.emit_all("single-instance", Payload { args: argv, cwd }).unwrap();
        }))
        .invoke_handler(tauri::generate_handler![store_openai_key, get_openai_key, send_prompt, fetch_conversation_history, get_num_messages, get_total_llm_user_messages, write_role_to_file, write_message_meta_file])
        .plugin(tauri_plugin_window_state::Builder::default().build()) // persist Window state plugin See: https://github.com/tauri-apps/plugins-workspace/tree/v1/plugins/window-state
        .plugin(tauri_plugin_printer::init()) // printer access plugin See: https://crates.io/crates/tauri-plugin-printer/versions version 0.5.2
        .plugin(tauri_plugin_fs_watch::init()) // file system watch plugin See: https://github.com/tauri-apps/plugins-workspace/tree/v1/plugins/fs-watch
        .plugin(tauri_plugin_sql::Builder::default().build()) // sqlite access plugin See: https://github.com/tauri-apps/plugins-workspace/tree/v1/plugins/sql
        .run(tauri::generate_context!())
        .expect("error while running tauri application");

    python_thread.join().unwrap();
    monitor_thread.join().unwrap();

    Ok(())
}

// Counts ALL messages, including from user, llm and bright_memory
use rusqlite::{Connection, Result};
#[tauri::command]
fn get_num_messages(database_path: PathBuf) -> Result<usize, String> {

    let db_file = database_path.join("full_text_store.db");

    let conn = Connection::open(db_file).map_err(|e| e.to_string())?;
    
    //let mut stmt = conn.prepare("SELECT COUNT(*) FROM text_blocks").map_err(|e| e.to_string())?;
    let mut stmt = conn.prepare("SELECT COUNT(*) FROM text_blocks").map_err(|e| e.to_string())?;
    let num_messages: usize = stmt.query_row([], |row| row.get(0)).map_err(|e| e.to_string())?;

    let mut num = NUM_MESSAGES.lock().unwrap();
    *num = num_messages;

    Ok(num_messages)  // Return the number of llm, user and bright_memory messages
}

// Counts ONLY messages from user and llm
#[tauri::command]
fn get_total_llm_user_messages(database_path: PathBuf) -> Result<usize, String> {

    let db_file = database_path.join("full_text_store.db");
    let conn = Connection::open(db_file).map_err(|e| e.to_string())?;

    // Table name is 'text_blocks' and the relevant column is 'source'
    let mut stmt = conn.prepare("SELECT COUNT(*) FROM text_blocks WHERE source IN ('user', 'llm')").map_err(|e| e.to_string())?;
    
    let count: usize = stmt.query_row([], |row| row.get(0)).map_err(|e| e.to_string())?;
    
    Ok(count) // return the number of llm and user messages
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
//use serde_json::Value;

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



#[tauri::command]
fn write_role_to_file(role: &str, messages_path: PathBuf) -> Result<(), String> {
    use std::fs::File;
    use std::io::Write;
    let role_file_path = messages_path.join("role.txt");
    print!("Role file path: {:?}", role_file_path);
    let mut file = File::create(role_file_path).map_err(|e| e.to_string())?;
    file.write_all(role.as_bytes()).map_err(|e| e.to_string())?;
    Ok(())
}

#[tauri::command]
fn write_message_meta_file(message_meta_json: &str, path: PathBuf) -> Result<(), String> {
    use std::fs::File;
    use std::io::Write;
    let mut file = File::create(path).map_err(|e| e.to_string())?;
    file.write_all(message_meta_json.as_bytes()).map_err(|e| e.to_string())?;
    Ok(())
}

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