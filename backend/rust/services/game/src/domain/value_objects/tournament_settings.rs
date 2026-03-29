use bitvec::{array::BitArray, order::Lsb0};

use serde::{Deserialize, Serialize};
use shared::game::LolGameMode;

#[derive(Serialize, Deserialize, Clone)]
pub enum TournamentSettings {
    Lol(LolTournamentSettings),
    Tft,
    Valo,
}
#[derive(Serialize, Deserialize, Clone)]
pub enum TournamentType {
    Classic,
    PickEm,
}

#[derive(Serialize, Deserialize, Clone, Copy)]
pub enum LolBracketMode {
    SingleElim(bool), //bool for 3rd place
    DoubleElim,
    Swiss,
    RoundRobin,
}

#[derive(Serialize, Deserialize, Clone)]
pub struct LolTournamentSettings {
    pub bracket_mode: LolBracketMode,
    pub draft_mode: LolGameMode,
    pub team_size: u8,
    pub tournament_type: TournamentType,
    pub map: u8,
    pub forbidden_champions: BitArray<[u8; 30], Lsb0>,
    pub series_best_of: Option<Vec<u8>>, // n=0..last is finals:boX, semifinals:boX, quarter:boX .... 1/2^n:boX
}
