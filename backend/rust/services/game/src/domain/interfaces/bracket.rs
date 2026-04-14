use shared::game::{Action, Actor};
use uuid::Uuid;

use crate::domain::value_objects::{
    LolTournamentSettings,
    bracket::{Bracket, Match},
    participant::TeamParticipant,
};
use anyhow::{Context, Result, bail};
impl Bracket {
    pub fn update_first_round(
        &mut self,
        swap_initiator: Actor,
        swap_victim: Actor,
    ) -> Result<(Uuid, Uuid)> {
        let mut i1: Option<(usize, usize)> = None;
        let mut i2: Option<(usize, usize)> = None;
        let mut game_series_id1: Option<Uuid> = None;
        let mut game_series_id2: Option<Uuid> = None;
        for m in self.rounds[0].iter() {
            for (pos, team_opt) in [m.team1, m.team2].iter().enumerate() {
                if let Some(team) = team_opt {
                    if *team == swap_initiator {
                        i1 = Some((m.match_number, pos));
                        game_series_id1 = Some(m.game_series_id);
                    }
                    if *team == swap_victim {
                        i2 = Some((m.match_number, pos));
                        game_series_id2 = Some(m.game_series_id);
                    }
                }
            }
        }
        let gameseries_to_change = (
            game_series_id1.context("GS_ID not found")?,
            game_series_id2.context("GS_ID not found")?,
        );

        let i1 = i1.context("Swap initiator not found in round 0")?;
        let i2 = i2.context("Swap victim not found in round 0")?;

        self.swap_actors_in_matches(i1, i2)?;
        Ok(gameseries_to_change)
    }
    fn swap_actors_in_matches(&mut self, t1: (usize, usize), t2: (usize, usize)) -> Result<()> {
        let round = self.rounds.get_mut(1).context("Round not found")?;

        let (m1, m2) = if t1.0 < t2.0 {
            let (left, right) = round.split_at_mut(t2.0);
            (&mut left[t1.0], &mut right[0])
        } else {
            let (left, right) = round.split_at_mut(t1.0);
            (&mut right[0], &mut left[t2.0])
        };

        let team_a = if t1.1 == 0 {
            &mut m1.team1
        } else {
            &mut m1.team2
        };
        let team_b = if t2.1 == 0 {
            &mut m2.team1
        } else {
            &mut m2.team2
        };

        std::mem::swap(team_a, team_b);

        Ok(())
    }

    pub fn link_matches(&mut self) {
        for round_idx in 0..self.rounds.len() - 1 {
            let current_round = self.rounds[round_idx].clone();

            let next_round_len = self.rounds[round_idx + 1].len();

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
