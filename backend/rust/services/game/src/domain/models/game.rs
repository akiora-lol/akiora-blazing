use std::collections::HashSet;

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

#[derive(Deserialize, PartialEq, Eq, Serialize, Clone, Debug)]
pub struct Game {
    #[serde(rename = "_id", with = "uuid::serde::hyphenated")]
    pub id: Uuid,
    #[serde(with = "uuid::serde::hyphenated")]
    pub game_series: Uuid,
    pub draft: Option<Draft>,
    pub teams: Vec<TeamParticipant>,
    pub ready_check: Vec<TeamParticipant>,
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
            ready_check: Vec::new(),
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

    pub fn toggle_ready(&mut self, actor: TeamParticipant) -> Result<()> {
        if self.status != GameStatus::Scheduled {
            anyhow::bail!("Can only toggle in scheduled games");
        }
        if !self.ready_check.contains(&actor) {
            self.ready_check.push(actor);
        } else {
            self.ready_check.retain(|f| *f != actor);
        }

        let set1: HashSet<_> = self.ready_check.iter().collect();
        let set2: HashSet<_> = self.teams.iter().collect();
        if set1 == set2 {
            self.status = GameStatus::Active;
        }
        Ok(())
    }
}
