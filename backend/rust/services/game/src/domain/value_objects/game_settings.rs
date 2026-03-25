use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Clone, Copy)]
pub enum GameSettings {
    Lol(LolGameSettings),
    Tft,
    Valo,
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
    mode: LolGameMode,
    team_size: u8,
    map: u8,
    best_of: u8,
}
