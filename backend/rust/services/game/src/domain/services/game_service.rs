use chrono::Utc;
use shared::game::{Draft, GameSettings};
use std::sync::Arc;
use uuid::Uuid;

use crate::domain::models::Game;
use crate::domain::value_objects::participant::TeamParticipant;
use crate::infra::{GameRepo, GameRepoExt};
use anyhow::{Context, Result, bail};

pub struct GameService {
    repo: Arc<GameRepo>,
}

impl GameService {
    pub fn new(repo: Arc<GameRepo>) -> Self {
        Self { repo }
    }

    pub async fn create(
        &self,
        game_series_id: Uuid,
        teams: Vec<TeamParticipant>,
        settings: GameSettings,
    ) -> Result<Game> {
        let id = Uuid::new_v4();
        let game = Game::new(id, game_series_id, teams, settings);
        self.repo.insert(&game).await.context("Failed to insert game")?;
        Ok(game)
    }

    pub async fn get_by_id(&self, id: Uuid) -> Result<Option<Game>> {
        self.repo.find_by_id(id).await.context("Failed to find game by id")
    }

    pub async fn choose_side(&self, id: Uuid, tp: TeamParticipant, side: usize) -> Result<()> {
        let mut game = self
            .repo
            .find_by_id(id)
            .await
            .context("Failed to find game")?
            .context("Game not found")?;
        game.choose_side(tp, side).context("Failed to choose side")?;
        self.repo.update(&game).await.context("Failed to update game")?;
        Ok(())
    }

    pub async fn get_by_ids(&self, ids: Vec<Uuid>) -> Result<Vec<Game>> {
        self.repo.find_by_ids(ids).await.context("Failed to find games by ids")
    }

    pub async fn get_by_game_series_id(&self, game_series_id: Uuid) -> Result<Vec<Game>> {
        self.repo
            .find_by_game_series_id(game_series_id)
            .await
            .context("Failed to find games by game series id")
    }

    pub async fn update_result(&self, id: Uuid, results: Vec<TeamParticipant>) -> Result<Game> {
        let mut game = self
            .repo
            .find_by_id(id)
            .await
            .context("Failed to find game")?
            .context("Game not found")?;

        game.results = Some(results);
        self.repo.update(&game).await.context("Failed to update game")?;
        Ok(game)
    }

    pub async fn finish(&self, id: Uuid) -> Result<Game> {
        let mut game = self
            .repo
            .find_by_id(id)
            .await
            .context("Failed to find game")?
            .context("Game not found")?;

        game.end = Some(Utc::now());
        self.repo.update(&game).await.context("Failed to update game")?;
        Ok(game)
    }

    pub async fn delete(&self, id: Uuid) -> Result<()> {
        self.repo.delete(id).await.context("Failed to delete game")
    }
}
