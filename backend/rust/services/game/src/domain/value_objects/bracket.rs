use crate::domain::value_objects::{LolTournamentSettings, participant::TeamParticipant};

#[derive(Debug, Clone)]
pub struct Match {
    pub game_series_id: Option<String>,
    pub team1: Option<TeamParticipant>,
    pub team2: Option<TeamParticipant>,
    pub winner: Option<TeamParticipant>,
    pub round: usize,
    pub match_number: usize,
    pub next_match_id: Option<usize>, // ссылка на следующий матч (номер матча в следующем раунде)
    pub is_bye: bool,                 // является ли матч техническим (bye)
}

#[derive(Debug, Clone)]
pub struct Bracket {
    pub rounds: Vec<Vec<Match>>, // rounds[round_index][match_index]
    pub total_rounds: usize,
    pub total_matches: usize,
}
