mod domain;
mod infra;

use anyhow::{self, Result};
use redis::streams::StreamReadOptions;
use redis::{AsyncCommands, Value};
mod app;

use crate::app::consumer::Consumer;

use shared::get_redis_manager;
use tokio;
use uuid::Uuid;
#[tokio::main]
async fn main() -> Result<()> {
    let mut con = get_redis_manager("redis://localhost:6379").await?;
    let _: Option<Value> = con
        .xgroup_create_mkstream("draft", "draft-workers", "$")
        .await
        .ok();

    println!("connected");
    let cons_id = Uuid::new_v4();
    let opts = StreamReadOptions::default()
        .group("draft-workers", format!("draft-worker-{}", cons_id.clone()))
        .count(10)
        .block(1000);
    let mut consumer = Consumer::new(con.clone(), opts);
    let handle = tokio::spawn(async move {
        println!("Consumer {} started", cons_id.clone());
        if let Err(e) = consumer.consume().await {
            eprintln!("Consumer {} error: {}", cons_id.clone(), e);
        }
    });

    handle.await?;

    Ok(())
}
