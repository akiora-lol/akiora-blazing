use chrono::Utc;
use std::sync::Arc;
use uuid::Uuid;

use crate::domain::models::{GameSeries, Tournament};
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
        id: Uuid,
        host: Actor,
        participants: Vec<Actor>,
        settings: TournamentSettings,
        start: chrono::DateTime<Utc>,
        prizepool: Option<String>,
    ) -> Result<Tournament, Box<dyn std::error::Error + Send + Sync>> {
        let tournament = Tournament::new(id, host, participants, settings, start, prizepool);
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

        // Tournament already has start time set at creation
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

    pub async fn remove_participant(
        &self,
        id: Uuid,
        participant_id: Uuid,
    ) -> Result<Tournament, Box<dyn std::error::Error + Send + Sync>> {
        let mut tournament = self
            .repo
            .find_by_id(id)
            .await?
            .ok_or("Tournament not found")?;

        tournament.remove_participant(participant_id);
        self.repo.update(&tournament).await?;
        Ok(tournament)
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
