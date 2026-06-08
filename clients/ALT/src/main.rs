mod backend;
mod schemas;
mod service;
mod ui;

use crate::backend::BackendClient;
use std::io::{self, Write};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let auth_url =
        std::env::var("AKIORA_AUTH_URL").unwrap_or_else(|_| "http://localhost:8000".to_string());
    let backend = BackendClient::new(auth_url);

    println!("Akiora ALT desktop login");
    let email = prompt("Email: ")?;
    let start = backend.start_email_login(email).await?;

    println!("Verification code was sent to your email.");
    let code = prompt("Code: ")?;
    let session = backend
        .finish_email_login(start.verification_id, code)
        .await?;

    let path = BackendClient::save_session(&session)?;
    println!("Authenticated.");
    println!("Session saved to {}", path.display());

    Ok(())
}

fn prompt(label: &str) -> io::Result<String> {
    print!("{label}");
    io::stdout().flush()?;

    let mut value = String::new();
    io::stdin().read_line(&mut value)?;
    Ok(value.trim().to_string())
}
