// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod backend_commands; // Include the module
use backend_commands::send_prompt; // Import the function

use pyo3::prelude::*;
use pyo3::types::IntoPyDict;
use std::env;
use std::thread;

fn main() -> PyResult<()> {
    // Spawn a new thread to run the Python code
    thread::spawn(|| -> PyResult<()> {
        
        pyo3::prepare_freethreaded_python(); // Initialize the Python interpreter

        let py_main = include_str!(concat!(
            env!("CARGO_MANIFEST_DIR"),
            "/../src/backend/__main__.py"
        ));

        Python::with_gil(|py| -> PyResult<()> {
            let locals = [("asyncio", py.import("asyncio")?)].into_py_dict(py);
            let path = format!("{}/../src/backend", env!("CARGO_MANIFEST_DIR").replace("\\", "/"));
            py.run(&format!("import sys; sys.path.append('{}')", path), None, None)?;

            // Load the Python code
            py.run(py_main, Some(locals), None)?;

            // Run the main_async.main() function within an asyncio event loop
            py.run(
                "loop = asyncio.get_event_loop()\n\
                 result = loop.run_forever(__main__.main())",

                Some(locals),
                None,
            )?;

            Ok(())
        })
    });

    // Run the Tauri application
    tauri::Builder::default()
        
        .invoke_handler(tauri::generate_handler![send_prompt])

        .run(tauri::generate_context!())
        .expect("error while running tauri application");

    Ok(())
}