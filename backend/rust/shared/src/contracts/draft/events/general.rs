use super::PrepareDraft;

use super::draft::DraftAction;
use super::redo::RedoAction;
use redis_macros::{FromRedisValue, ToRedisArgs};
use serde::{Deserialize, Serialize};

use uuid::Uuid;

#[derive(Serialize, Debug, Deserialize, Clone, FromRedisValue, ToRedisArgs)]
#[serde(tag = "type", content = "data")]
pub enum Event {
    PrepareDraft(PrepareDraft),
    Draft(DraftAction),
    Redo(RedoAction),
}
#[derive(Serialize, Deserialize, Clone, FromRedisValue, ToRedisArgs)]
pub enum Action {
    Draft(DraftAction),
    Redo(RedoAction),
}

#[derive(Serialize, Deserialize, Clone, FromRedisValue, ToRedisArgs)]
pub struct BadAction {
    pub game_id: Uuid,
}
