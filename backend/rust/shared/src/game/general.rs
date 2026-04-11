use crate::game::LolGameSettings;
use serde::{Deserialize, Serialize};
#[derive(Serialize, Debug, Deserialize, Clone, Copy)]
pub enum GameSettings {
    Lol(LolGameSettings),
    Tft(LolGameSettings),
    Valo(LolGameSettings),
}
