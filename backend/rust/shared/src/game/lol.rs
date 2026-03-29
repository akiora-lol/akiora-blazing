use bitvec::{array::BitArray, order::Lsb0};
use mongodb::bson::{self, Bson};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Serialize, Deserialize, Clone)]
pub enum Team {
    Red(Uuid),
    Blue(Uuid),
}
#[derive(Serialize, Deserialize, Clone)]
pub struct ChampLock {
    pub champion_id: usize,
    pub player: Uuid,
}

#[derive(Serialize, Deserialize, Clone)]
pub enum Action {
    Pick(usize),
    Ban(usize),
}

#[derive(Serialize, Deserialize, Clone)]
pub struct Command(pub Team, pub Action);

#[derive(Serialize, Deserialize, Clone)]
pub struct Draft {
    pub game_id: Uuid,
    pub history: Vec<Command>,
    pub picks: Vec<ChampLock>,
    pub forbidden_champions: BitArray<[u8; 30], Lsb0>,
}

#[derive(Serialize, Deserialize, Clone, Copy)]

pub enum Actor {
    #[serde(with = "uuid::serde::simple")]
    User(Uuid),
    #[serde(with = "uuid::serde::simple")]
    Team(Uuid),
    #[serde(with = "uuid::serde::simple")]
    Club(Uuid),
}

#[derive(Serialize, Deserialize, Default, Clone, Copy)]
pub enum LolGameMode {
    #[default]
    Classic,
    Fearless,
    IronMan,
    AllRandom,
}

#[derive(Serialize, Deserialize, Default, Clone, Copy)]
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
        bson::to_bson(&tp).unwrap()
    }
}
