use chrono::Utc;
use shared::game::{Actor, GameSettings};
use std::sync::Arc;
use uuid::Uuid;

use crate::domain::models::{Game, GameSeries};

use crate::infra::{GameSeriesRepo, GameSeriesRepoExt};

pub struct GameSeriesService {
    repo: Arc<GameSeriesRepo>,
}

impl GameSeriesService {
    pub fn new(repo: Arc<GameSeriesRepo>) -> Self {
        Self { repo }
    }

    pub async fn create(
        &self,
        participants: Vec<Actor>,
        settings: GameSettings,
    ) -> Result<GameSeries, Box<dyn std::error::Error + Send + Sync>> {
        let id = Uuid::new_v4();
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
}
