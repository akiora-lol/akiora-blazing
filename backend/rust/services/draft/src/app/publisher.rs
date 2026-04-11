use anyhow::Result;
use redis::{AsyncCommands, aio::ConnectionManager};
use serde::Serialize;

pub struct Publisher {
    con: ConnectionManager,
}
impl Publisher {
    pub fn new(con: ConnectionManager) -> Self {
        Self { con }
    }

    pub async fn pub_sub_publish<T: Serialize>(&mut self, channel: &str, data: &T) -> Result<i64> {
        let json = serde_json::to_string(data)?;
        let subscribers: i64 = self.con.publish(channel, json).await?;
        Ok(subscribers)
    }
    pub async fn stream_publish<T: Serialize>(&mut self, stream: &str, data: &T) -> Result<String> {
        let json = serde_json::to_string(data)?;
        let id: String = self.con.xadd(stream, "*", &[("data", json)]).await?;
        Ok(id)
    }
}
