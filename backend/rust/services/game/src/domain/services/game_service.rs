use chrono::Utc;
use shared::game::Draft;
use std::sync::Arc;
use uuid::Uuid;

use crate::domain::models::Game;
use crate::domain::value_objects::participant::TeamParticipant;
use crate::infra::{GameRepo, GameRepoExt};

pub struct GameService {
    repo: Arc<GameRepo>,
}

impl GameService {
    pub fn new(repo: Arc<GameRepo>) -> Self {
        Self { repo }
    }

    pub async fn create(
        &self,
        id: Uuid,
        game_series_id: Uuid,
        draft: Option<Draft>,
    ) -> Result<Game, Box<dyn std::error::Error + Send + Sync>> {
        let mut game = Game::new(id, game_series_id);
        if let Some(d) = draft {
            game.set_draft(d);
        }
        game.set_start(Utc::now());

        self.repo.insert(&game).await?;
        Ok(game)
    }

    pub async fn get_by_id(
        &self,
        id: Uuid,
    ) -> Result<Option<Game>, Box<dyn std::error::Error + Send + Sync>> {
        self.repo.find_by_id(id).await.map_err(|e| e.into())
    }

    pub async fn get_by_ids(
        &self,
        ids: Vec<Uuid>,
    ) -> Result<Vec<Game>, Box<dyn std::error::Error + Send + Sync>> {
        self.repo.find_by_ids(ids).await.map_err(|e| e.into())
    }

    pub async fn get_by_game_series_id(
        &self,
        game_series_id: Uuid,
    ) -> Result<Vec<Game>, Box<dyn std::error::Error + Send + Sync>> {
        self.repo
            .find_by_game_series_id(game_series_id)
            .await
            .map_err(|e| e.into())
    }

    pub async fn update_result(
        &self,
        id: Uuid,
        results: Vec<TeamParticipant>,
    ) -> Result<Game, Box<dyn std::error::Error + Send + Sync>> {
        let mut game = self.repo.find_by_id(id).await?.ok_or("Game not found")?;

        game.set_results(results);
        self.repo.update(&game).await?;
        Ok(game)
    }

    pub async fn finish(&self, id: Uuid) -> Result<Game, Box<dyn std::error::Error + Send + Sync>> {
        let mut game = self.repo.find_by_id(id).await?.ok_or("Game not found")?;

        game.set_end(Utc::now());
        self.repo.update(&game).await?;
        Ok(game)
    }

    pub async fn delete(&self, id: Uuid) -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
        self.repo.delete(id).await.map_err(|e| e.into())
    }
}
