use anyhow::{Context, Result};
use dotenvy::dotenv;
use mongodb::{
    Client, Database,
    options::ClientOptions,
};
use std::env;
#[derive(Debug)]
struct MongoConfig {
    connection_string: String,
    database_name: String,
}

impl MongoConfig {
    fn from_env() -> Result<Self> {
        dotenv().ok();

        let connection_string =
            env::var("MONGODB_URI").context("MONGODB_URI environment variable not set")?;

        let database_name = env::var("MONGODB_DATABASE").unwrap_or_else(|_| "myapp".to_string());
        println!("📡 Using MongoDB URI: {}", connection_string);
        Ok(MongoConfig {
            connection_string,
            database_name,
        })
    }
}

async fn connect_to_replicaset(config: &MongoConfig) -> Result<Client> {
    let mut client_options = ClientOptions::parse(&config.connection_string)
        .await
        .context("Failed to parse MongoDB connection string")?;

    client_options.app_name = Some("game-replicaset-app".to_string());
    client_options.max_pool_size = Some(10);
    client_options.min_pool_size = Some(2);

    client_options.direct_connection = Some(false);

    client_options.connect_timeout = Some(std::time::Duration::from_secs(10));
    client_options.server_selection_timeout = Some(std::time::Duration::from_secs(30));

    let client = Client::with_options(client_options).context("Failed to create MongoDB client")?;

    client
        .database("admin")
        .run_command(mongodb::bson::doc! {"ping": 1})
        .await
        .context("Failed to ping MongoDB")?;

    println!("✅ Successfully connected to MongoDB replicaset!");

    Ok(client)
}

pub async fn get_mongo() -> Result<Database> {
    let config = MongoConfig::from_env()?;

    let client = connect_to_replicaset(&config).await?;

    let db = client.database(&config.database_name);
    Ok(db)
}
