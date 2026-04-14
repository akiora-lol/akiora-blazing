use std::collections::HashMap;

use anyhow::{Context, Result, bail};
use chrono::{DateTime, Utc};
use prost_types::Timestamp;
use serde::{Deserialize, Serialize};
use serde_with::serde_as;
use shared::game::{Actor, LolGameSettings};
use uuid::Uuid;

use crate::domain::GameSeries;
use crate::domain::value_objects::bracket::Bracket;
use crate::domain::value_objects::participant::TeamParticipant;
use crate::domain::value_objects::*;

#[serde_as]
#[derive(Deserialize, Serialize, Clone)]
pub struct Tournament {
    #[serde(rename = "_id", with = "uuid::serde::hyphenated")]
    pub id: Uuid,
    pub status: TournamentStatus,
    pub host: Actor,
    #[serde_as(as = "Vec<(_,_)>")]
    pub participant_pool: HashMap<Actor, Option<TeamParticipant>>,
    pub wait_list: Vec<Actor>,
    pub settings: TournamentSettings,
    pub bracket: Option<Bracket>,
    pub start_time: DateTime<Utc>,
    pub end_time: Option<DateTime<Utc>>,
    pub prizepool: Option<String>,
    pub is_open: bool,
}

impl Tournament {
    pub fn new(
        host: Actor,
        settings: TournamentSettings,
        start: DateTime<Utc>,
        is_open: bool,
        prizepool: Option<String>,
    ) -> Self {
        let id = Uuid::new_v4();

        let wait_list = Vec::new();
        Self {
            id,
            host,
            status: TournamentStatus::Scheduled,

            participant_pool: HashMap::new(),
            settings,
            is_open,
            wait_list,
            start_time: start,
            end_time: None,
            bracket: None,
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

    pub fn start_timestamp(&self) -> i64 {
        self.start_time.timestamp()
    }
    pub fn end_timestamp(&self) -> Option<i64> {
        match self.end_time {
            Some(st) => Some(st.timestamp()),
            _ => None,
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

    pub fn add_participant(&mut self, participant: Actor) -> Result<()> {
        if !matches!(self.status, TournamentStatus::Scheduled) {
            bail!("Can only add participants while tournament is scheduled");
        }
        self.participant_pool.entry(participant).or_insert(None);
        Ok(())
    }

    pub fn remove_participant(&mut self, participant_id: Uuid) -> Result<()> {
        if !matches!(self.status, TournamentStatus::Scheduled) {
            bail!("Can only remove participants while tournament is scheduled");
        }

        self.participant_pool.retain(|&part, _| match part {
            Actor::Club(id) | Actor::Team(id) | Actor::User(id) => id != participant_id,
        });
        Ok(())
    }

    pub fn add_team(&mut self, team: TeamParticipant) -> Result<()> {
        if !matches!(self.status, TournamentStatus::Scheduled) {
            bail!("Can only add teams while tournament is scheduled");
        }
        if !self.participant_pool.contains_key(&team.participant) {
            bail!("Can only add teams if it's in participant_pool");
        }

        self.participant_pool.insert(team.participant, Some(team));

        Ok(())
    }

    pub fn add_to_waitlist(&mut self, participant: Actor) -> Result<()> {
        if !matches!(self.status, TournamentStatus::Scheduled) {
            bail!("Can only add to waitlist while tournament is scheduled");
        }
        self.wait_list.push(participant);
        Ok(())
    }

    pub fn remove_from_waitlist(&mut self, participant_id: Uuid) -> Result<()> {
        if !matches!(self.status, TournamentStatus::Scheduled) {
            bail!("Can only remove from waitlist while tournament is scheduled");
        }
        self.wait_list.retain(|p| match p {
            Actor::User(id) | Actor::Team(id) | Actor::Club(id) => *id != participant_id,
        });
        Ok(())
    }

    pub fn set_start_time(&mut self, start: DateTime<Utc>) -> Result<()> {
        if !matches!(self.status, TournamentStatus::Scheduled) {
            bail!("Can only change start time while tournament is scheduled");
        }
        self.start_time = start;
        Ok(())
    }

    pub fn activate(&mut self) -> Result<()> {
        if !matches!(self.status, TournamentStatus::Scheduled) {
            bail!("Can only activate scheduled tournament");
        }
        self.status = TournamentStatus::Active;
        Ok(())
    }

    pub fn cancel(&mut self) -> Result<()> {
        if matches!(self.status, TournamentStatus::Finished) {
            bail!("Cannot cancel finished tournament");
        }
        self.status = TournamentStatus::Cancelled;
        Ok(())
    }

    pub fn mark_finished(&mut self) -> Result<()> {
        if !matches!(self.status, TournamentStatus::Active) {
            bail!("Can only finish active tournament");
        }
        self.status = TournamentStatus::Finished;
        self.end_time = Some(Utc::now());
        Ok(())
    }
}
