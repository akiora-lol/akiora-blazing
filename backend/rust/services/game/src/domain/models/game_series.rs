use core::str;

use crate::domain::Game;
use crate::domain::value_objects::*;
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Deserialize, Serialize, Clone)]
pub struct GameSeries {
    #[serde(rename = "_id")]
    id: Uuid,
    teams: Vec<Participant>,
    settings: GameSettings,
    #[serde(skip_serializing)]
    games: Option<Vec<Game>>,
    started: Option<DateTime<Utc>>,
    ended: Option<DateTime<Utc>>,
}
