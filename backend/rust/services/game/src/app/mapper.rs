use anyhow::{Result, bail};
use chrono::{DateTime, Utc};
use prost_types::Timestamp;
pub trait TimestampExt {
    fn to_prost(&self) -> Timestamp;
    fn from_prost(ts: Timestamp) -> Self;
}

impl TimestampExt for DateTime<Utc> {
    fn to_prost(&self) -> Timestamp {
        Timestamp {
            seconds: self.timestamp(),
            nanos: self.timestamp_subsec_nanos() as i32,
        }
    }

    fn from_prost(ts: Timestamp) -> Self {
        DateTime::from_timestamp(ts.seconds, ts.nanos as u32).expect("Invalid timestamp")
    }
}

use proto_build::common::{Actor as ProtoActor, ActorType};
use shared::game::Actor;
use uuid::Uuid;

pub fn actor_from_proto_to_domain(ac: ProtoActor) -> Result<Actor> {
    match ac.actor_type() {
        ActorType::Team => Ok(Actor::Team(Uuid::parse_str(&ac.id).unwrap_or_default())),
        ActorType::User => Ok(Actor::User(Uuid::parse_str(&ac.id).unwrap_or_default())),
        ActorType::Club => Ok(Actor::Club(Uuid::parse_str(&ac.id).unwrap_or_default())),
        _ => bail!("doesnt exist"),
    }
}
