use mongodb::bson::{self, Bson};
use serde::{Deserialize, Serialize};

#[derive(Serialize, PartialEq, Eq, Debug, Deserialize, Clone)]
pub enum GameStatus {
    Scheduled,
    Active,
    Finished,
    Cancelled,
}

impl From<GameStatus> for Bson {
    fn from(tp: GameStatus) -> Self {
        bson::to_bson(&tp).unwrap()
    }
}
