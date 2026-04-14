use chrono::Utc;
use shared::game::{self, Actor, GameSettings};
use std::sync::Arc;
use uuid::Uuid;

use crate::domain::models::{Game, GameSeries};
use crate::domain::services::game_service::GameService;
use crate::domain::value_objects::participant::TeamParticipant;
use crate::infra::{GameSeriesRepo, GameSeriesRepoExt};
use anyhow::{Context, Result, bail};

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
    ) -> Result<GameSeries> {
        let game_series = GameSeries::new(id, participants.clone(), settings);
        match settings {
            GameSettings::Lol(sets) => {
                for _ in 0..sets.best_of {
                    self.game_service
                        .create(id, participants.clone(), settings.clone())
                        .await
                        .context("Failed to create game")?;
                }
            }
            _ => bail!("Unsupported game settings"),
        }

        self.repo.insert(&game_series).await.context("Failed to insert game series")?;
        Ok(game_series)
    }

    pub async fn start(&self, id: Uuid) -> Result<GameSeries> {
        let mut game_series = self
            .get_by_id(id)
            .await
            .context("Failed to get game series")?;
        game_series.start = Some(Utc::now());
        self.repo.update(&game_series).await.context("Failed to update game series")?;
        Ok(game_series)
    }

    pub async fn start_next_game(&self, id: Uuid) -> Result<GameSeries> {
        let mut game_series = self
            .get_by_id(id)
            .await
            .context("Failed to get game series")?;
        if game_series.start.is_none() {
            game_series.start = Some(Utc::now());
        }
        match &game_series.games {
            Some(games) => {
                if !games.is_empty() {
                    let game = games.last().context("Games list is empty")?;
                    let loser = game.results.as_ref().context("Results are missing")?.last();
                    if let Some(loser) = loser {
                        // ask in pubsub for loser to select side
                    }
                }
            }
            None => bail!("Games list is empty"),
        }
        self.repo.update(&game_series).await.context("Failed to update game series")?;
        Ok(game_series)
    }

    pub async fn choose_side(&self, actor: Actor, side: usize, id: Uuid) -> Result<()> {
        let game_series = self
            .get_by_id(id)
            .await
            .context("Failed to get game series")?;

        match &game_series.games {
            Some(games) if !games.is_empty() => {
                let game = games.last().context("Games list is empty despite check")?;
                if games.len() == 1 {
                    if actor == game.teams[0].participant {
                        self.game_service
                            .choose_side(game.id, game.teams[0].clone(), side)
                            .await?;
                        return Ok(());
                    }
                }
                let loser = game
                    .results
                    .as_ref()
                    .context("Game results are missing")?
                    .last()
                    .context("Results list is empty")?;
                if actor == loser.participant {
                    self.game_service
                        .choose_side(game.id, loser.clone(), side)
                        .await?;
                    return Ok(());
                }

                bail!("No Permission");
            }
            Some(_) => Ok(()),
            None => bail!("GameSeries games are missing (None)"),
        }
    }

    pub async fn get_by_id(&self, id: Uuid) -> Result<GameSeries> {
        let gs = self.repo.find_by_id(id).await.context("Failed to find game series by id")?;
        let mut gss = gs.context("Game series not found")?;
        let games = self
            .game_service
            .get_by_game_series_id(id)
            .await
            .context("Failed to get games by game series id")?;
        gss.games = Some(games);
        Ok(gss)
    }

    pub async fn get_by_ids(&self, ids: Vec<Uuid>) -> Result<Vec<GameSeries>> {
        self.repo.find_by_ids(ids).await.context("Failed to find game series by ids")
    }
}
