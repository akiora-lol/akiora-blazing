use crate::domain::{Game, value_objects::participant::TeamParticipant};

use chrono::{DateTime, Utc};
use prost_types::Timestamp;
use serde::{Deserialize, Serialize};
use shared::game::*;
use uuid::Uuid;

#[derive(Deserialize, Serialize, Clone)]
pub struct GameSeries {
    #[serde(rename = "_id")]
    #[serde(with = "uuid::serde::hyphenated")]
    pub id: Uuid,
    pub teams: Vec<TeamParticipant>,
    pub settings: GameSettings,
    #[serde(skip_deserializing)]
    pub games: Option<Vec<Game>>,
    pub start: Option<DateTime<Utc>>,
    pub end: Option<DateTime<Utc>>,
}

impl GameSeries {
    pub fn new(id: Uuid, teams: Vec<TeamParticipant>, settings: GameSettings) -> Self {
        Self {
            id,
            teams,
            settings,
            games: None,
            start: None,
            end: None,
        }
    }
}
