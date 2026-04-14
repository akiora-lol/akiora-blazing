use crate::domain::{
    GameSeries,
    value_objects::{game_status::GameStatus, participant::TeamParticipant},
};
use anyhow::{Context, Result};
use chrono::{DateTime, Utc};
use prost_types::Timestamp;
use serde::{Deserialize, Serialize};
use shared::game::*;
use uuid::Uuid;

#[derive(Deserialize, Serialize, Clone)]
pub struct Game {
    #[serde(rename = "_id", with = "uuid::serde::hyphenated")]
    pub id: Uuid,
    #[serde(with = "uuid::serde::hyphenated")]
    pub game_series: Uuid,
    pub draft: Option<Draft>,
    pub teams: Vec<TeamParticipant>,
    pub results: Option<Vec<TeamParticipant>>,
    pub start: Option<DateTime<Utc>>,
    pub end: Option<DateTime<Utc>>,
    pub settings: GameSettings,
    pub status: GameStatus,
}

impl Game {
    pub fn new(
        id: Uuid,
        game_series: Uuid,
        teams: Vec<TeamParticipant>,
        settings: GameSettings,
    ) -> Self {
        Self {
            id,
            game_series,
            teams,
            settings,
            draft: None,
            results: None,
            start: None,
            status: GameStatus::Scheduled,
            end: None,
        }
    }

    pub fn choose_side(&mut self, actor: TeamParticipant, side: usize) -> Result<()> {
        if self.status != GameStatus::Scheduled {
            anyhow::bail!("Can only swap in scheduled games");
        }
        if !self.teams.contains(&actor) {
            anyhow::bail!("No such team in game");
        }
        if side > 1 {
            anyhow::bail!("Side should be 0 or 1");
        }
        // BAD LOGIC ONLY FOR 2 TEAMS LEAUGUE ONLY RN
        if self.teams[side] != actor {
            self.teams.swap(side, 1 - side);
        }
        Ok(())
    }
}
