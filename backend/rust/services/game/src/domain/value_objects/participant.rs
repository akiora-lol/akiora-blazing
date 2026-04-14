use mongodb::bson::{self, Bson};
use serde::{Deserialize, Serialize};
use serde_with::{DisplayFromStr, serde_as};
use shared::game::Actor;
use uuid::Uuid;

#[serde_as]
#[derive(Serialize, PartialEq, Eq, Debug, Deserialize, Clone)]
pub struct TeamParticipant {
    pub participant: Actor,

    #[serde_as(as = "Vec<DisplayFromStr>")]
    pub users: Vec<Uuid>,
}

impl From<TeamParticipant> for Bson {
    fn from(tp: TeamParticipant) -> Self {
        bson::to_bson(&tp).unwrap()
    }
}
