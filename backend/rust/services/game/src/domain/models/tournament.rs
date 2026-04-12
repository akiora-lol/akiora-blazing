use chrono::{DateTime, Utc};
use prost_types::Timestamp;
use serde::{Deserialize, Serialize};
use shared::game::{Actor, LolGameSettings};
use uuid::Uuid;

use crate::domain::GameSeries;
use crate::domain::value_objects::participant::TeamParticipant;
use crate::domain::value_objects::*;

#[derive(Deserialize, Serialize, Clone)]
pub struct Tournament {
    #[serde(rename = "_id", with = "uuid::serde::simple")]
    pub id: Uuid,
    pub status: TournamentStatus,
    pub host: Actor,
    pub teams: Vec<TeamParticipant>,
    pub participant_pool: Vec<Actor>,
    pub wait_list: Vec<Actor>,
    pub settings: TournamentSettings,
    #[serde(skip_deserializing)]
    pub games: Option<Vec<GameSeries>>,
    pub start_time: DateTime<Utc>,
    pub end_time: Option<DateTime<Utc>>,
    pub prizepool: Option<String>,
}

impl Tournament {
    pub fn new(
        host: Actor,
        settings: TournamentSettings,
        start: DateTime<Utc>,
        prizepool: Option<String>,
    ) -> Self {
        let id = Uuid::new_v4();
        let teams = Vec::new();
        let participant_pool = Vec::new();
        let wait_list = Vec::new();
        Self {
            id,
            host,
            status: TournamentStatus::Sheduled,
            teams,
            participant_pool,
            settings,
            games: None,
            wait_list,
            start_time: start,
            end_time: None,
            prizepool,
        }
    }

    pub fn id(&self) -> Uuid {
        self.id
    }

    pub fn host(&self) -> &Actor {
        &self.host
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

    pub fn start_timestamp(&self) -> i64 {
        self.start_time.timestamp()
    }
    pub fn end_timestamp(&self) -> Option<i64> {
        match self.end_time {
            Some(st) => Some(st.timestamp()),
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
        self.start_time
    }

    pub fn end(&self) -> Option<DateTime<Utc>> {
        self.end_time
    }

    pub fn set_end(&mut self, end: DateTime<Utc>) {
        self.end_time = Some(end);
    }

    pub fn is_finished(&self) -> bool {
        self.end_time.is_some()
    }

    pub fn prizepool(&self) -> Option<&str> {
        self.prizepool.as_deref()
    }

    pub fn set_prizepool(&mut self, prizepool: String) {
        self.prizepool = Some(prizepool);
    }

    pub fn add_participant(&mut self, participant: Actor) {
        self.participant_pool.push(participant);
    }

    pub fn add_team(&mut self, team: TeamParticipant) {
        self.teams.push(team);
    }

    pub fn add_to_waitlist(&mut self, participant: Actor) {
        self.wait_list.push(participant);
    }
}
