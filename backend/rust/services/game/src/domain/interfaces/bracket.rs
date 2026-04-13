use shared::game::{Action, Actor};

use crate::domain::value_objects::{
    LolTournamentSettings,
    bracket::{Bracket, Match},
    participant::TeamParticipant,
};

impl Bracket {
    pub fn link_matches(&mut self) {
        // Проходим по всем раундам, кроме последнего
        for round_idx in 0..self.rounds.len() - 1 {
            let current_round = self.rounds[round_idx].clone();

            let next_round_len = self.rounds[round_idx + 1].len();
            // Каждые 2 матча текущего раунда ссылаются на 1 матч следующего
            for i in 0..current_round.len() {
                let next_match_index = i / 2;
                if next_match_index < next_round_len {
                    if let Some(match_node) = self.rounds[round_idx].get_mut(i) {
                        match_node.next_match_id = Some(next_match_index);
                    }
                }
            }
        }
    }

    // Получить все матчи определенного раунда
    pub fn get_matches_by_round(&self, round: usize) -> Option<&Vec<Match>> {
        if round > 0 && round <= self.rounds.len() {
            Some(&self.rounds[round - 1])
        } else {
            None
        }
    }
    pub fn fill_bracket(&mut self, teams: &Vec<Actor>) {}

    // Получить матч по номеру раунда и индексу матча
    pub fn get_match(&self, round: usize, match_index: usize) -> Option<&Match> {
        self.rounds.get(round - 1).and_then(|r| r.get(match_index))
    }

    pub fn get_match_mut(&mut self, round: usize, match_index: usize) -> Option<&mut Match> {
        self.rounds
            .get_mut(round - 1)
            .and_then(|r| r.get_mut(match_index))
    }

    pub fn set_match_winner(&mut self, round: usize, match_index: usize, winner: Actor) -> bool {
        let rounds_len = self.rounds.len();

        if let Some(match_node) = self.get_match_mut(round, match_index) {
            match_node.winner = Some(winner.clone());

            if round < rounds_len {
                if let Some(next_match_id) = match_node.next_match_id {
                    // Определяем, в какую позицию (team1 или team2) поставить победителя
                    let is_left_match = match_index % 2 == 0;

                    if let Some(next_match) = self.get_match_mut(round + 1, next_match_id) {
                        if is_left_match {
                            next_match.team1 = Some(winner);
                        } else {
                            next_match.team2 = Some(winner);
                        }
                    }
                }
            }
            return true;
        }
        false
    }

    // Получить всех победителей (для отладки)
    pub fn get_all_winners(&self) -> Vec<(usize, usize, &Actor)> {
        let mut winners = Vec::new();
        for (round_idx, round) in self.rounds.iter().enumerate() {
            for (match_idx, match_node) in round.iter().enumerate() {
                if let Some(winner) = &match_node.winner {
                    winners.push((round_idx + 1, match_idx, winner));
                }
            }
        }
        winners
    }
}

pub trait BracketBuilder {
    fn build_bracket(&self, teams: &Vec<Actor>) -> Option<Bracket>;
}
