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
    pub mode: LolGameMode,
    pub team_size: u8,
    pub map: u8,
    pub best_of: u8,
}
