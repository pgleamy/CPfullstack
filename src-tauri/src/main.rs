// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod backend_commands; // Include the module
use backend_commands::send_prompt; // Import the function

use pyo3::prelude::*;
use pyo3::types::{PyList};
use std::thread;
use std::env;

extern crate keyring;
use keyring::Keyring;


fn main() -> PyResult<()> {

        let python_thread = thread::spawn(|| {

            pyo3::prepare_freethreaded_python();

            let gil = Python::acquire_gil();
            let py = gil.python();
            
            // Change the working directory
            let os = py.import("os").unwrap();
            os.call_method1("chdir", ("../src/backend",)).unwrap();
    
            // Append the directory to sys.path for Python to find your modules
            let sys_module = py.import("sys").unwrap();
            let sys_path: &PyList = sys_module.getattr("path").unwrap().downcast().unwrap();
            sys_path.append("F:\\WindowsDesktop\\Users\\Leamy\\Desktop\\ChatPerfect\\src\\backend").unwrap();
    
            let asyncio = py.import("asyncio").unwrap();
            let main_module = py.import("main").unwrap();
            
            let main_coroutine = main_module.getattr("main").unwrap().call0().unwrap();
            let event_loop = asyncio.getattr("get_event_loop").unwrap().call0().unwrap();
            event_loop.getattr("run_until_complete").unwrap().call1((main_coroutine,)).unwrap();
        });
    
        match env::current_dir() {
            Ok(dir) => {
                println!("\nThe working directory for Rust is {}\n\n", dir.display());
            }
            Err(e) => {
                println!("Error getting current directory: {}", e);
            }
        }

        // Run the Tauri application in the main thread
        tauri::Builder::default()
            .invoke_handler(tauri::generate_handler![store_openai_key, get_openai_key, send_prompt])
            .run(tauri::generate_context!())
            .expect("error while running tauri application");
    
        // Wait for Python thread to complete (optional)
        python_thread.join().unwrap();
    
        Ok(())
    }

  
    #[tauri::command]
    fn store_openai_key(key: String) -> Result<(), String> {
        let service = "ChatPerfect";
        let username = "openai_key";
        let keyring = Keyring::new(service, username);
        keyring.set_password(&key).map_err(|e| e.to_string()) // Map KeyringError to String
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



    
    