// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod backend_commands; // Include the module
use backend_commands::send_prompt; // Import the function

use pyo3::prelude::*;
use pyo3::types::{PyList};
use std::thread;

fn main() -> PyResult<()> {

        pyo3::prepare_freethreaded_python();

        let gil = Python::acquire_gil();
        let py = gil.python();
        let os = py.import("os")?;
        os.call_method1("chdir", ("../src/backend",))?;

        // Append the directory to sys.path for Python to find your modules
        let sys_module = py.import("sys")?;
        let sys_path: &PyList = sys_module.getattr("path")?.downcast()?;
        sys_path.append("F:\\WindowsDesktop\\Users\\Leamy\\Desktop\\ChatPerfect\\src\\backend")?;

        let asyncio = py.import("asyncio")?;
        let main_module = py.import("main")?;
        
        // Use getattr to get the Python function
        //let main_coroutine = main_module.getattr("main")?.downcast::<PyFunction>()?;
        let main_coroutine = main_module.getattr("main")?.call0()?;
        
        let event_loop = asyncio.getattr("get_event_loop")?.call0()?;
        
        event_loop.getattr("run_until_complete")?.call1((main_coroutine,))?;

    // Run the Tauri application
    tauri::Builder::default()
        
        .invoke_handler(tauri::generate_handler![send_prompt])

        .run(tauri::generate_context!())
        .expect("error while running tauri application");

    Ok(())
}