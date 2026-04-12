use chrono::Utc;
use shared::game::Actor;
use std::sync::Arc;
use uuid::Uuid;

use crate::domain::models::{GameSeries, Tournament};
use crate::domain::value_objects::participant::TeamParticipant;
use crate::domain::value_objects::*;
use crate::infra::{TournamentRepo, TournamentRepoExt};

pub struct TournamentService {
    repo: Arc<TournamentRepo>,
}

impl TournamentService {
    pub fn new(repo: Arc<TournamentRepo>) -> Self {
        Self { repo }
    }

    pub async fn create(
        &self,

        host: Actor,

        settings: TournamentSettings,
        start: chrono::DateTime<Utc>,
        prizepool: Option<String>,
    ) -> Result<Tournament, Box<dyn std::error::Error + Send + Sync>> {
        let tournament = Tournament::new(host, settings, start, prizepool);
        self.repo.insert(&tournament).await?;
        Ok(tournament)
    }

    pub async fn get_by_id(
        &self,
        id: Uuid,
    ) -> Result<Option<Tournament>, Box<dyn std::error::Error + Send + Sync>> {
        self.repo.find_by_id(id).await.map_err(|e| e.into())
    }

    pub async fn get_by_ids(
        &self,
        ids: Vec<Uuid>,
    ) -> Result<Vec<Tournament>, Box<dyn std::error::Error + Send + Sync>> {
        self.repo.find_by_ids(ids).await.map_err(|e| e.into())
    }

    pub async fn start(
        &self,
        id: Uuid,
    ) -> Result<Tournament, Box<dyn std::error::Error + Send + Sync>> {
        let tournament = self
            .repo
            .find_by_id(id)
            .await?
            .ok_or("Tournament not found")?;

        Ok(tournament)
    }

    pub async fn finish(
        &self,
        id: Uuid,
    ) -> Result<Tournament, Box<dyn std::error::Error + Send + Sync>> {
        let mut tournament = self
            .repo
            .find_by_id(id)
            .await?
            .ok_or("Tournament not found")?;

        tournament.set_end(Utc::now());
        self.repo.update(&tournament).await?;
        Ok(tournament)
    }

    pub async fn add_participant(
        &self,
        id: Uuid,
        participant: Actor,
    ) -> Result<Tournament, Box<dyn std::error::Error + Send + Sync>> {
        let mut tournament = self
            .repo
            .find_by_id(id)
            .await?
            .ok_or("Tournament not found")?;

        tournament.add_participant(participant);
        self.repo.update(&tournament).await?;
        Ok(tournament)
    }

    pub async fn add_team(
        &self,
        id: Uuid,
        participant: Actor,
    ) -> Result<Tournament, Box<dyn std::error::Error + Send + Sync>> {
        let mut tournament = self
            .repo
            .find_by_id(id)
            .await?
            .ok_or("Tournament not found")?;

        tournament.add_participant(participant);
        self.repo.update(&tournament).await?;
        Ok(tournament)
    }

    pub async fn start_tournament(
        &self,
        id: Uuid,
    ) -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
        let mut tournament = self
            .repo
            .find_by_id(id)
            .await?
            .ok_or("Tournament not found")?;
        match tournament.settings {
            TournamentSettings::Lol(settings) => self.build_bracket(&settings, &tournament.teams),

            _ => todo!(),
        }
        Ok(())
    }
    fn build_bracket(&self, settings: &LolTournamentSettings, teams: &Vec<TeamParticipant>) {
        match settings.bracket_mode {
            LolBracketMode::DoubleElim => {
                todo!()
            }
            LolBracketMode::Scrim => {
                todo!()
            }
            LolBracketMode::SingleElim => {
                self.build_bracket_se(settings, teams);
            }
            LolBracketMode::SingleElimWithThird => {
                todo!()
            }
            LolBracketMode::RoundRobin => {
                todo!()
            }
            LolBracketMode::Swiss => {
                todo!()
            }
        }
    }

    fn build_bracket_se(&self, settings: &LolTournamentSettings, teams: &Vec<TeamParticipant>) {
        let number_of_teams = teams.len();
        let mut log_n = number_of_teams.ilog2();
        let base_2: i32 = 2;
        if base_2.pow(log_n) < number_of_teams as i32 {
            log_n += 1;
        }
    }

    pub async fn add_game_series(
        &self,
        id: Uuid,
        game_series: GameSeries,
    ) -> Result<Tournament, Box<dyn std::error::Error + Send + Sync>> {
        let mut tournament = self
            .repo
            .find_by_id(id)
            .await?
            .ok_or("Tournament not found")?;

        tournament.add_game_series(game_series);
        self.repo.update(&tournament).await?;
        Ok(tournament)
    }

    pub async fn delete(&self, id: Uuid) -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
        self.repo.delete(id).await.map_err(|e| e.into())
    }
}
