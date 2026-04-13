use crate::domain::value_objects::participant::TeamParticipant;
use chrono::{DateTime, Utc};
use prost_types::Timestamp;
use serde::{Deserialize, Serialize};
use shared::game::*;
use uuid::Uuid;

#[derive(Deserialize, Serialize, Clone)]
pub struct Game {
    #[serde(rename = "_id", with = "uuid::serde::hyphenated")]
    id: Uuid,
    #[serde(with = "uuid::serde::hyphenated")]
    game_series: Uuid,
    draft: Option<Draft>,
    results: Option<Vec<TeamParticipant>>,
    start: Option<DateTime<Utc>>,
    end: Option<DateTime<Utc>>,
}

impl Game {
    pub fn new(id: Uuid, game_series: Uuid) -> Self {
        Self {
            id,
            game_series,
            draft: None,
            results: None,
            start: None,
            end: None,
        }
    }

    pub fn id(&self) -> Uuid {
        self.id
    }

    pub fn game_series_id(&self) -> Uuid {
        self.game_series
    }

    pub fn draft(&self) -> Option<&Draft> {
        self.draft.as_ref()
    }

    pub fn set_draft(&mut self, draft: Draft) {
        self.draft = Some(draft);
    }

    pub fn results(&self) -> Option<&Vec<TeamParticipant>> {
        self.results.as_ref()
    }

    pub fn set_results(&mut self, results: Vec<TeamParticipant>) {
        self.results = Some(results);
    }

    pub fn start(&self) -> Option<DateTime<Utc>> {
        self.start
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

    pub fn set_start(&mut self, start: DateTime<Utc>) {
        self.start = Some(start);
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
