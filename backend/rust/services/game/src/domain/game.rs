use core::str;

use crate::domain::value_objects::*;
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Deserialize, Serialize, Clone)]
pub struct Game {
    #[serde(rename = "_id")]
    id: Uuid,
    game_series: Uuid,
    draft: Option<Draft>,
    results: Option<Vec<TeamParticipant>>,
    started: Option<DateTime<Utc>>,
    ended: Option<DateTime<Utc>>,
}
