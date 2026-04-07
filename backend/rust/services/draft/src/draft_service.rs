use crate::{draft::Draft, errors::DraftError};

use redis::AsyncCommands;
use redis::aio::ConnectionManager;

use shared::game::Command;
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
    pub async fn save_draft(&mut self, draft: &Draft) -> Result<Draft, DraftError> {
        let set: Draft = self
            .redis
            .set(draft.game_id(), draft)
            .await
            .map_err(|e| DraftError::SaveError)
            .unwrap();
        Ok(set)
    }

    pub async fn command(&mut self, command: &Command, game_id: &str) -> Result<Draft, DraftError> {
        let mut draft = self.load_draft(game_id).await?;
        let res = draft.perform_command(command).await?;
        // if res.1 is Some, send action to pubsub, else send finish action to pubsub
        todo!()
    }
}
