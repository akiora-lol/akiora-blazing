use prost_types::Timestamp;

use chrono::{DateTime, Utc};
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
