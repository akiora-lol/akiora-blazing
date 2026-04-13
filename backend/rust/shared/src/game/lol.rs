use mongodb::bson::{self, Bson};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Serialize, Debug, Deserialize, Clone, PartialEq, Eq)]
pub enum Team {
    Red(Option<Uuid>),
    Blue(Option<Uuid>),
}
#[derive(Serialize, Deserialize, Clone)]
pub struct ChampLock {
    pub champion_id: usize,
    pub player: Uuid,
}

#[derive(Serialize, Debug, Deserialize, Clone, PartialEq, Eq)]
pub enum Action {
    Pick(Option<usize>),
    Ban(Option<usize>),
}

#[derive(Serialize, Debug, Deserialize, Clone, PartialEq, Eq)]
pub struct Command(pub Team, pub Action);

#[derive(Serialize, Deserialize, Clone)]
pub struct Draft {
    pub game_id: Uuid,
    pub history: Vec<Command>,
    pub picks: Vec<ChampLock>,
    pub forbidden_champions: Vec<u8>,
    pub teams: Vec<Team>,
}

#[derive(Serialize, PartialEq, Hash, Eq, Debug, Deserialize, Clone, Copy)]
pub enum Actor {
    #[serde(with = "uuid::serde::hyphenated")]
    User(Uuid),
    #[serde(with = "uuid::serde::hyphenated")]
    Team(Uuid),
    #[serde(with = "uuid::serde::hyphenated")]
    Club(Uuid),
}

#[derive(Serialize, Debug, Deserialize, Default, Clone, Copy)]
pub enum LolGameMode {
    #[default]
    Classic,
    Fearless,
    IronMan,
    AllRandom,
}

#[derive(Serialize, Debug, Deserialize, Default, Clone, Copy)]
pub struct LolGameSettings {
    pub mode: LolGameMode,
    pub team_size: u8,
    pub map: u8,
    pub best_of: u8,
}

impl From<Draft> for Bson {
    fn from(draft: Draft) -> Self {
        bson::to_bson(&draft).unwrap()
    }
}

impl From<Actor> for Bson {
    fn from(tp: Actor) -> Self {
        let st = match tp {
            Actor::Club(id) => format!("Club:{id}"),
            Actor::User(id) => format!("User:{id}"),
            Actor::Team(id) => format!("Team:{id}"),
        };
        bson::to_bson(&st).unwrap()
    }
}
