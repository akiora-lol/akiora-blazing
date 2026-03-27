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
    pub champion_id: u8,
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
    pub history: Vec<Command>,
    pub picks: Vec<ChampLock>,
    pub forbidden_champions: BitArray<[u8; 30], Lsb0>,
}

impl From<Draft> for Bson {
    fn from(draft: Draft) -> Self {
        bson::to_bson(&draft).unwrap() // или обработайте ошибку
    }
}
