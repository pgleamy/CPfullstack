use std::fs::write;
use tauri::InvokeError;
use tauri::api::path::data_dir; 

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

impl From<serde_json::Error> for CustomError {
    fn from(error: serde_json::Error) -> Self {
        CustomError(std::io::Error::new(std::io::ErrorKind::Other, error.to_string()))
    }
}

// Saves the user's prompt to a file to be picked up by the Python backend code
#[tauri::command]
pub fn send_prompt(message_text: String) -> Result<(), CustomError> {
    // Get the application directory of the Tauri application
    let app_dir = data_dir().expect("failed to get app data dir");
    //println!("app_dir: {:?}", app_dir);
    // Append "Chatperfect" to the app directory path
    let chatperfect_dir = app_dir.join("Chatperfect").join("messages").join("user_prompt.txt");
    // Write the message text to the user_prompt.txt file
    write(&chatperfect_dir, message_text)?;

    Ok(())
}