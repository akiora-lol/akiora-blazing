use std::error::Error;

use crate::setup::setup;
use axum::{
    Router,
    routing::{delete, get, patch, post, put},
};
use redis::{AsyncTypedCommands, aio::ConnectionManager};
mod setup;
#[derive(Clone)]
struct AppState {
    redis_manager: ConnectionManager,
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let redis_manager = setup().await?;
    let _ = redis_manager.clone().set("key", 123).await?;
    let app_state = AppState { redis_manager };
    let app = Router::new()
        .route("/health", get(|| async { "healthy".to_string() }))
        .with_state(app_state);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:8000").await.unwrap();

    println!("Сервер запущен на http://127.0.0.1:8000");

    axum::serve(listener, app).await.unwrap();
    Ok(())
}
