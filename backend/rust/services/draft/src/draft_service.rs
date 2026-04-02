use crate::{errors::DraftError, loldraft::Draft};

use redis::AsyncCommands;
use redis::aio::ConnectionManager;
use redis_macros;
use redis_macros::{FromRedisValue, ToRedisArgs};
pub struct DraftService {
    redis: ConnectionManager,
}

impl DraftService {
    pub fn new(r: ConnectionManager) -> Self {
        Self { redis: r.clone() }
    }

    pub async fn load_draft(&mut self, game_id: &str) -> Result<Draft, DraftError> {
        let d: Option<Draft> = self.redis.get(game_id).await.unwrap_or(None);
        d.ok_or(DraftError::NotFound {
            game_id: game_id.to_string(),
        })
    }
    pub async fn save_draft(&mut self, draft: &Draft) -> () {
        let set: Draft = self.redis.set(draft.game_id(), draft).await.unwrap();
        todo!()
    }
}
