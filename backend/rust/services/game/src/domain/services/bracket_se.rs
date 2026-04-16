use shared::game::Actor;
use uuid::Uuid;

use crate::domain::{
    interfaces::BracketBuilder,
    value_objects::{
        bracket::{Bracket, Match},
        participant::TeamParticipant,
    },
};

#[derive(Clone)]
pub struct SingleEliminationBuilder;
impl SingleEliminationBuilder {
    fn create_next_round(prev_round_matches: &[Match], round: usize) -> Vec<Match> {
        let mut matches = Vec::new();
        let mut match_counter = 0;
        let matches_per_round = prev_round_matches.len() / 2;

        for i in 0..matches_per_round {
            let match_node = Match {
                game_series_id: Uuid::new_v4(),
                team1: None,
                team2: None,
                winner: None,
                round,
                match_number: match_counter,
                next_match_id: None,
                is_bye: false,
            };

            matches.push(match_node);
            match_counter += 1;
        }

        matches
    }
    fn create_first_round(teams: Vec<Option<Actor>>) -> Vec<Match> {
        let total_slots = teams.len();
        let mut matches = Vec::new();
        let mut match_counter = 0;

        for i in (0..total_slots).step_by(2) {
            let team1 = teams[i].clone();
            let team2 = if i + 1 < total_slots {
                teams[i + 1].clone()
            } else {
                None
            };

            let is_bye = team1.is_none() || team2.is_none();

            let match_node = Match {
                game_series_id: Uuid::new_v4(),
                team1,
                team2,
                winner: None,
                round: 1,
                match_number: match_counter,
                next_match_id: None,
                is_bye,
            };

            matches.push(match_node);
            match_counter += 1;
        }

        matches
    }
    fn calculate_bye_positions(total_slots: usize, byes: usize) -> Vec<usize> {
        if byes == 0 {
            return vec![];
        }

        let mut positions = Vec::new();

        if byes % 2 == 0 {
            let half_byes = byes / 2;

            for i in 0..half_byes {
                positions.push(i);
            }

            for i in 0..half_byes {
                positions.push(total_slots - 1 - i);
            }
        } else {
            let half_byes = byes / 2;

            for i in 0..half_byes {
                positions.push(i);
            }

            for i in 0..half_byes {
                positions.push(total_slots - 1 - i);
            }

            let center = total_slots / 2;
            if !positions.contains(&center) {
                positions.push(center);
            } else {
                positions.push(center + 1);
            }
        }

        positions.sort();
        positions
    }
}
fn next_power_of_two(n: usize) -> usize {
    if n == 0 {
        return 1;
    }
    let mut power = 1;
    while power < n {
        power <<= 1;
    }
    power
}
impl BracketBuilder for SingleEliminationBuilder {
    fn build_bracket(&self, teams: &Vec<Actor>) -> Option<Bracket> {
        let number_of_teams = teams.len();

        if number_of_teams < 2 {
            return None;
        }

        let bracket_size = next_power_of_two(number_of_teams);
        let total_rounds = (bracket_size as f64).log2() as usize;
        let byes = bracket_size - number_of_teams;

        // Подготавливаем команды с bye-слотами
        let mut bracket_teams = Vec::with_capacity(bracket_size);
        let bye_positions = Self::calculate_bye_positions(bracket_size, byes);
        let mut team_iter = teams.into_iter();

        for i in 0..bracket_size {
            if bye_positions.contains(&i) {
                bracket_teams.push(None);
            } else {
                bracket_teams.push(Some(team_iter.next().unwrap().clone()));
            }
        }

        // Строим сетку
        let mut rounds: Vec<Vec<Match>> = Vec::new();

        // Первый раунд
        let mut current_round_matches = Self::create_first_round(bracket_teams);
        rounds.push(current_round_matches.clone());

        for round in 2..=total_rounds {
            let next_round_matches = Self::create_next_round(&current_round_matches, round);
            rounds.push(next_round_matches.clone());
            current_round_matches = next_round_matches;
        }

        let mut bracket = Bracket {
            rounds,
            total_rounds,
            total_matches: bracket_size - 1,
        };

        bracket.link_matches();

        Some(bracket)
    }
}
