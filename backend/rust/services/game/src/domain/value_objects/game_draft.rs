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
    champion_id: u8,
    player: Uuid,
}

#[derive(Serialize, Deserialize, Clone)]
pub enum Action {
    Pick(usize),
    Ban(usize),
}

#[derive(Serialize, Deserialize, Clone)]
pub struct Command(Team, Action);

#[derive(Serialize, Deserialize, Clone)]
pub struct Draft {
    history: Vec<Command>,
    picks: Vec<ChampLock>,
    forbidden_champions: BitArray<[u8; 30], Lsb0>,
}

impl From<Draft> for Bson {
    fn from(draft: Draft) -> Self {
        bson::to_bson(&draft).unwrap() // или обработайте ошибку
    }
}
