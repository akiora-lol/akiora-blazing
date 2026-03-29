use mongodb::{Client, Database};
use std::env;

use crate::constants::{
    MONGO_DB_NAME_DEFAULT, MONGO_DB_NAME_ENV, MONGO_URL_DEFAULT, MONGO_URL_ENV,
};

pub async fn connect_to_db() -> anyhow::Result<Database> {
    let mongo_url = env::var(MONGO_URL_ENV)
        .unwrap_or_else(|_| MONGO_URL_DEFAULT.to_string());
    let db_name = env::var(MONGO_DB_NAME_ENV)
        .unwrap_or_else(|_| MONGO_DB_NAME_DEFAULT.to_string());
    let client = Client::with_uri_str(&mongo_url).await?;
    Ok(client.database(&db_name))
}
