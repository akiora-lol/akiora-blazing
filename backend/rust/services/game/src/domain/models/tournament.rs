use chrono::{DateTime, Utc};
use prost_types::Timestamp;
use serde::{Deserialize, Serialize};
use shared::game::Actor;
use uuid::Uuid;

use crate::domain::GameSeries;
use crate::domain::value_objects::*;

#[derive(Deserialize, Serialize, Clone)]
pub struct Tournament {
    #[serde(rename = "_id", with = "uuid::serde::simple")]
    id: Uuid,

    host: Actor,
    teams: Vec<Actor>,
    settings: TournamentSettings,
    #[serde(skip_deserializing)]
    games: Option<Vec<GameSeries>>,
    start: DateTime<Utc>,
    end: Option<DateTime<Utc>>,
    prizepool: Option<String>,
}

impl Tournament {
    pub fn new(
        id: Uuid,
        host: Actor,
        teams: Vec<Actor>,
        settings: TournamentSettings,
        start: DateTime<Utc>,
        prizepool: Option<String>,
    ) -> Self {
        Self {
            id,
            host,
            teams,
            settings,
            games: None,
            start,
            end: None,
            prizepool,
        }
    }

    pub fn id(&self) -> Uuid {
        self.id
    }

    pub fn host(&self) -> &Actor {
        &self.host
    }

    pub fn teams(&self) -> &[Actor] {
        &self.teams
    }

    pub fn settings(&self) -> &TournamentSettings {
        &self.settings
    }

    pub fn games(&self) -> Option<&Vec<GameSeries>> {
        self.games.as_ref()
    }

    pub fn set_games(&mut self, games: Vec<GameSeries>) {
        self.games = Some(games);
    }

    pub fn start_timestamp(&self) -> Timestamp {
        Timestamp {
            seconds: self.start.timestamp(),
            nanos: self.start.timestamp_subsec_nanos() as i32,
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
    pub fn add_game_series(&mut self, game_series: GameSeries) {
        if let Some(ref mut games) = self.games {
            games.push(game_series);
        } else {
            self.games = Some(vec![game_series]);
        }
    }

    pub fn start(&self) -> DateTime<Utc> {
        self.start
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

    pub fn prizepool(&self) -> Option<&str> {
        self.prizepool.as_deref()
    }

    pub fn set_prizepool(&mut self, prizepool: String) {
        self.prizepool = Some(prizepool);
    }

    pub fn add_participant(&mut self, participant: Actor) {
        self.teams.push(participant);
    }

    pub fn remove_participant(&mut self, participant_id: Uuid) -> bool {
        if let Some(pos) = self.teams.iter().position(|t| match t {
            Actor::User(id) | Actor::Team(id) | Actor::Club(id) => *id == participant_id,
        }) {
            self.teams.remove(pos);
            true
        } else {
            false
        }
    }
}
