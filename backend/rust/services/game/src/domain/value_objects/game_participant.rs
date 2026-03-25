use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Serialize, Deserialize, Clone, Copy)]
pub enum Participant {
    User(Uuid),
    Group(Uuid),
    Club(Uuid),
}

#[derive(Serialize, Deserialize, Clone)]
pub struct TeamParticipant {
    participant: Participant,
    users: Vec<Uuid>,
}
