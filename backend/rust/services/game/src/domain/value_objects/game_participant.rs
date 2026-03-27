use chrono::{DateTime, Utc};
use mongodb::bson::{self, Bson};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Serialize, Deserialize, Clone, Copy)]
pub enum Actor {
    User(Uuid),
    Group(Uuid),
    Club(Uuid),
}

#[derive(Serialize, Deserialize, Clone)]
pub struct TeamParticipant {
    participant: Actor,
    users: Vec<Uuid>,
}
impl From<TeamParticipant> for Bson {
    fn from(tp: TeamParticipant) -> Self {
        bson::to_bson(&tp).unwrap()
    }
}

impl From<Actor> for Bson {
    fn from(tp: Actor) -> Self {
        bson::to_bson(&tp).unwrap()
    }
}
