use crate::game::Team;
use redis_macros::{FromRedisValue, ToRedisArgs};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Serialize, Debug, Deserialize, Clone, FromRedisValue, ToRedisArgs)]
pub struct RedoAction {
    pub game_id: Uuid,
    pub team: Team,
}
