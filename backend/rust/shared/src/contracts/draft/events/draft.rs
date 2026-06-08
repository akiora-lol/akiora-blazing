use crate::game::{Command, GameSettings, LolGameSettings, Team};
use redis_macros::{FromRedisValue, ToRedisArgs};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Serialize, Debug, Deserialize, Clone, FromRedisValue, ToRedisArgs)]
pub struct PrepareDraft {
    pub game_id: Uuid,
    pub forbidden_champions: Vec<i32>,
    pub teams: Vec<Team>,
    pub seconds_per_action: i32,
    pub settings: LolGameSettings,
    pub allow_redo: bool,
}

#[derive(Serialize, Debug, Deserialize, Clone, FromRedisValue, ToRedisArgs)]
pub struct DraftAction {
    pub game_id: Uuid,
    pub command: Command,
}

#[derive(Serialize, Deserialize, Clone, FromRedisValue, ToRedisArgs)]
pub struct DraftEnded {
    pub game_id: Uuid,
}

#[derive(Serialize, Deserialize, Clone, FromRedisValue, ToRedisArgs)]
pub struct DraftNextCommand {
    pub game_id: Uuid,
    pub command: Command,
}
