use crate::domain::Game;

use chrono::{DateTime, Utc};
use prost_types::Timestamp;
use serde::{Deserialize, Serialize};
use shared::game::*;
use uuid::Uuid;

#[derive(Deserialize, Serialize, Clone)]
pub struct GameSeries {
    #[serde(rename = "_id")]
    id: Uuid,
    teams: Vec<Actor>,
    settings: GameSettings,
    #[serde(skip_deserializing)]
    games: Option<Vec<Game>>,

    start: Option<DateTime<Utc>>,

    end: Option<DateTime<Utc>>,
}

impl GameSeries {
    pub fn new(id: Uuid, teams: Vec<Actor>, settings: GameSettings) -> Self {
        Self {
            id,
            teams,
            settings,
            games: None,
            start: None,
            end: None,
        }
    }

    pub fn id(&self) -> Uuid {
        self.id
    }

    pub fn teams(&self) -> &[Actor] {
        &self.teams
    }

    pub fn settings(&self) -> &GameSettings {
        &self.settings
    }

    pub fn games(&self) -> Option<&Vec<Game>> {
        self.games.as_ref()
    }

    pub fn set_games(&mut self, games: Vec<Game>) {
        self.games = Some(games);
    }

    pub fn add_game(&mut self, game: Game) {
        if let Some(ref mut games) = self.games {
            games.push(game);
        } else {
            self.games = Some(vec![game]);
        }
    }

    pub fn start(&self) -> Option<DateTime<Utc>> {
        self.start
    }

    pub fn set_start(&mut self, start: DateTime<Utc>) {
        self.start = Some(start);
    }
    pub fn start_timestamp(&self) -> Option<Timestamp> {
        match self.start {
            Some(st) => Some(Timestamp {
                seconds: st.timestamp(),
                nanos: st.timestamp_subsec_nanos() as i32,
            }),
            _ => None,
        }
    }
    pub fn end_timestamp(&self) -> Option<Timestamp> {
        match self.end {
            Some(st) => Some(Timestamp {
                seconds: st.timestamp(),
                nanos: st.timestamp_subsec_nanos() as i32,
            }),
            _ => None,
        }
    }

    pub fn end(&self) -> Option<DateTime<Utc>> {
        self.end
    }

    pub fn set_end(&mut self, end: DateTime<Utc>) {
        self.end = Some(end);
    }

    pub fn is_finished(&self) -> bool {
        self.end.is_some()
    }
}
