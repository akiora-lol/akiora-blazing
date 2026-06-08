use crate::game::LolGameSettings;
use serde::{Deserialize, Serialize};
#[derive(Serialize, PartialEq, Eq, Debug, Deserialize, Clone, Copy)]
pub enum GameSettings {
    Lol(LolGameSettings),
    Tft(LolGameSettings),
    Valo(LolGameSettings),
}
