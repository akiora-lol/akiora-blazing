use mongodb::{Collection, Database};
use redis::aio::{ConnectionManager, ConnectionManagerConfig};
use redis::{AsyncCommands, Client, RedisError, RedisResult};
use serde::Serialize;
use std::time::Duration;

use crate::errors::PublishError;

pub struct MongoRepository<T: Send + Sync> {
    collection: Collection<T>,
}

impl<T> MongoRepository<T>
where
    T: Send + Sync,
{
    pub fn new(db: &Database, collection_name: &str) -> Self {
        Self {
            collection: db.collection::<T>(collection_name),
        }
    }
    pub fn get_collection(&self) -> &Collection<T> {
        &self.collection
    }
}

pub async fn get_redis_manager(redis_uri: &str) -> RedisResult<ConnectionManager> {
    let client = Client::open(redis_uri)?;

    let config = ConnectionManagerConfig::new()
        .set_min_delay(Duration::from_millis(100)) // минимальная задержка между попытками
        .set_max_delay(Duration::from_secs(5)) // максимальная задержка
        .set_number_of_retries(10) // количество попыток переподключения
        .set_response_timeout(Some(Duration::from_secs(30))) // таймаут ответа
        .set_connection_timeout(Some(Duration::from_secs(5))); // таймаут соединения

    let manager = ConnectionManager::new_with_config(client, config).await?;
    Ok(manager)
}

pub struct Publisher {
    con: ConnectionManager,
}
impl Publisher {
    pub fn new(con: ConnectionManager) -> Self {
        Self { con }
    }

    pub async fn pub_sub_publish<T: Serialize>(
        &mut self,
        channel: &str,
        data: &T,
    ) -> Result<i64, PublishError> {
        let json = serde_json::to_string(data).map_err(|e| PublishError::ReadError)?;
        let subscribers: i64 = self
            .con
            .publish(channel, json)
            .await
            .map_err(|e| PublishError::WriteError)?;
        Ok(subscribers)
    }
    pub async fn stream_publish<T: Serialize>(
        &mut self,
        stream: &str,
        data: &T,
    ) -> Result<String, PublishError> {
        let json = serde_json::to_string(data).map_err(|e| PublishError::ReadError)?;
        let id: String = self
            .con
            .xadd(stream, "*", &[("data", json)])
            .await
            .map_err(|e| PublishError::WriteError)?;
        Ok(id)
    }
}
