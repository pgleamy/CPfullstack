use std::fs::write;
use std::path::Path;
use tauri::command;
use tauri::InvokeError;

// Custom error type
pub struct CustomError(std::io::Error);

impl From<std::io::Error> for CustomError {
    fn from(error: std::io::Error) -> Self {
        CustomError(error)
    }
}

impl From<CustomError> for InvokeError {
    fn from(error: CustomError) -> Self {
        InvokeError::from(error.0.to_string())
    }
}

// Saves the user's prompt to a file to be picked up by the Python backend code
#[command]
pub fn send_prompt(message_text: String) -> Result<(), CustomError> {
    let path = Path::new("..\\src\\backend\\messages\\user_prompt.txt");
    println!("\nWriting to ..\\src\\backend\\messages\\user_prompt.txt. LLM responses are passed by file at the same location. \n\n{}", message_text); 
    write(path, message_text).map_err(CustomError::from)
}
