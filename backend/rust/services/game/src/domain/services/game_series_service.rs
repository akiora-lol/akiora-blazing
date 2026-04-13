use chrono::Utc;
use shared::game::{Actor, GameSettings};
use std::sync::Arc;
use uuid::Uuid;

use crate::domain::models::{Game, GameSeries};
use crate::domain::services::game_service::GameService;

use crate::domain::value_objects::participant::TeamParticipant;
use crate::infra::{GameSeriesRepo, GameSeriesRepoExt};

pub struct GameSeriesService {
    repo: Arc<GameSeriesRepo>,
    game_service: Arc<GameService>,
}

impl GameSeriesService {
    pub fn new(repo: Arc<GameSeriesRepo>, game_service: Arc<GameService>) -> Self {
        Self { repo, game_service }
    }

    pub async fn create(
        &self,
        id: Uuid,
        participants: Vec<TeamParticipant>,
        settings: GameSettings,
    ) -> Result<GameSeries, Box<dyn std::error::Error + Send + Sync>> {
        let game_series = GameSeries::new(id, participants, settings);
        self.repo.insert(&game_series).await?;
        Ok(game_series)
    }

    pub async fn get_by_id(
        &self,
        id: Uuid,
    ) -> Result<Option<GameSeries>, Box<dyn std::error::Error + Send + Sync>> {
        self.repo.find_by_id(id).await.map_err(|e| e.into())
    }

    pub async fn get_by_ids(
        &self,
        ids: Vec<Uuid>,
    ) -> Result<Vec<GameSeries>, Box<dyn std::error::Error + Send + Sync>> {
        self.repo.find_by_ids(ids).await.map_err(|e| e.into())
    }

    pub async fn start(
        &self,
        id: Uuid,
    ) -> Result<GameSeries, Box<dyn std::error::Error + Send + Sync>> {
        let mut game_series = self
            .repo
            .find_by_id(id)
            .await?
            .ok_or("GameSeries not found")?;

        game_series.set_start(Utc::now());
        self.repo.update(&game_series).await?;
        Ok(game_series)
    }

    pub async fn finish(
        &self,
        id: Uuid,
    ) -> Result<GameSeries, Box<dyn std::error::Error + Send + Sync>> {
        let mut game_series = self
            .repo
            .find_by_id(id)
            .await?
            .ok_or("GameSeries not found")?;

        game_series.set_end(Utc::now());
        self.repo.update(&game_series).await?;
        Ok(game_series)
    }

    pub async fn add_game(
        &self,
        id: Uuid,
        game: Game,
    ) -> Result<GameSeries, Box<dyn std::error::Error + Send + Sync>> {
        let mut game_series = self
            .repo
            .find_by_id(id)
            .await?
            .ok_or("GameSeries not found")?;

        game_series.add_game(game);
        self.repo.update(&game_series).await?;
        Ok(game_series)
    }

    pub async fn delete(&self, id: Uuid) -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
        self.repo.delete(id).await.map_err(|e| e.into())
    }

    pub fn game_service(&self) -> &Arc<GameService> {
        &self.game_service
    }
}
