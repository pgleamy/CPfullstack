use std::env;

extern crate tauri;
//use pyo3::types::IntoPyDict;
use pyo3::types::PyList;

mod backend_commands; // Include the module
use backend_commands::send_prompt; // Import the function

use pyo3::prelude::*;
use std::thread;

fn main() -> tauri::Result<()> {

    println!("running main.rs 1");

    let gil = Python::acquire_gil();
    let py = gil.python();
    let sys = py.import("sys").unwrap();
    let executable = sys.getattr("executable").unwrap();
    println!("Python executable: {:?}", executable);
    


    pyo3::prepare_freethreaded_python();

    println!("running main.rs 2");

    let path = "F:\\WindowsDesktop\\Users\\Leamy\\Desktop\\ChatPerfect\\src\\backend";
    // Spawn a new thread for running Python code
    thread::spawn(move|| {

        println!("running main.rs 3");

        let gil = Python::acquire_gil();
        let py = gil.python();
        let sys = py.import("sys").unwrap();

        // Add your script's directory to the Python path
        // Get sys.path
        let sys_path = sys.getattr("path").expect("Failed to get sys.path");
        println!("sys.path: {:?}", sys_path);

        // Cast to PyList
        let py_list = sys_path.cast_as::<PyList>().expect("Failed to cast sys.path to PyList");
        println!("PyList: {:?}", py_list);

        // Append new path
        py_list.append(path).expect("Failed to append path to sys.path");
        println!("Path appended: {}", path);

        // Import and run your Python code
let code = r#"
import main_async
main_async.main()
"#;
        py.run(code, None, None).unwrap();
    });

    // Run the Tauri UI in the main thread
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![send_prompt])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");

    Ok(())
}
