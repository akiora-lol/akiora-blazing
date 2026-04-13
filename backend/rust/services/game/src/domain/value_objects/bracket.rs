use mongodb::bson::{self, Bson};
use serde::{Deserialize, Serialize};
use shared::game::Actor;
use uuid::Uuid;

use crate::domain::value_objects::{LolTournamentSettings, participant::TeamParticipant};

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Match {
    pub game_series_id: Uuid,
    pub team1: Option<Actor>,
    pub team2: Option<Actor>,
    pub winner: Option<Actor>,
    pub round: usize,
    pub match_number: usize,
    pub next_match_id: Option<usize>, // ссылка на следующий матч (номер матча в следующем раунде)
    pub is_bye: bool,                 // является ли матч техническим (bye)
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Bracket {
    pub rounds: Vec<Vec<Match>>, // rounds[round_index][match_index]
    pub total_rounds: usize,
    pub total_matches: usize,
}

impl From<Bracket> for Bson {
    fn from(tp: Bracket) -> Self {
        bson::to_bson(&tp).unwrap()
    }
}
