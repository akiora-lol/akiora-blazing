use crate::domain::value_objects::LolGameMode;
use bitvec::{array::BitArray, order::Lsb0};
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

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
    bracket_mode: LolBracketMode,
    draft_mode: LolGameMode,
    team_size: u8,
    tournament_type: TournamentType,
    map: u8,
    forbidden_champions: BitArray<[u8; 30], Lsb0>,
    series_best_of: Option<Vec<u8>>, // n=0..last is finals:boX, semifinals:boX, quarter:boX .... 1/2^n:boX
}
