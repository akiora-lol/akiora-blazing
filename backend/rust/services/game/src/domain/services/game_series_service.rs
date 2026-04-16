use chrono::Utc;
use proto_build::common::TeamType;
use serde_json::json;
use shared::Publisher;
use shared::contracts::draft::events::PrepareDraft;
use shared::game::{self, Actor, GameSettings, Team};
use std::ops::Deref;
use std::sync::Arc;
use uuid::Uuid;

use crate::domain::models::{Game, GameSeries};
use crate::domain::services::game_service::GameService;
use crate::domain::value_objects::game_status::GameStatus;
use crate::domain::value_objects::participant::TeamParticipant;
use crate::infra::{GameSeriesRepo, GameSeriesRepoExt};
use anyhow::{Context, Result, bail};

#[derive(Clone)]
pub struct GameSeriesService {
    repo: Arc<GameSeriesRepo>,
    game_service: GameService,
    redis_publisher: Publisher,
}

impl GameSeriesService {
    pub fn new(
        repo: Arc<GameSeriesRepo>,
        game_service: GameService,
        redis_publisher: Publisher,
    ) -> Self {
        Self {
            repo,
            game_service,
            redis_publisher,
        }
    }

    pub async fn create(
        &self,
        id: Uuid,
        tournament_id: Uuid,
        participants: Vec<TeamParticipant>,
        settings: GameSettings,
        forbidden_champions: Vec<i32>,
    ) -> Result<GameSeries> {
        let game_series = GameSeries::new(
            id,
            tournament_id,
            participants.clone(),
            settings,
            forbidden_champions,
        );
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

        self.repo
            .insert(&game_series)
            .await
            .context("Failed to insert game series")?;
        Ok(game_series)
    }

    pub async fn toggle_ready(&mut self, id: Uuid, tp: TeamParticipant) -> Result<GameSeries> {
        let mut game_series = self
            .get_by_id(id)
            .await
            .context("Failed to get game series")?;
        let games = self.game_service.get_by_game_series_id(id).await?;
        game_series.games = Some(games);
        if game_series.start.is_none() {
            game_series.start = Some(Utc::now());
        }
        match &game_series.games {
            Some(games) => {
                if !games.is_empty() {
                    let game = games
                        .iter()
                        .filter(|g| g.results.is_none() || g.results.as_ref().unwrap().is_empty())
                        .next()
                        .context("Games list is empty despite check")?;
                    let game = self
                        .game_service
                        .toggle_ready(game.id, tp)
                        .await
                        .context("failed to toggle ready on game ")?;
                    if !(game.status == GameStatus::Active) {
                        bail!("Game toggled but didnt start yet");
                    }
                    let blue_id = match game.teams[0].participant {
                        Actor::Club(id) | Actor::User(id) | Actor::Team(id) => id,
                    };
                    let red_id = match game.teams[1].participant {
                        Actor::Club(id) | Actor::User(id) | Actor::Team(id) => id,
                    };
                    let sets = match game.settings {
                        GameSettings::Lol(s) => s,
                        _ => todo!(),
                    };
                    let prep_draft = PrepareDraft {
                        game_id: game.id,
                        teams: vec![Team::Blue(Some(blue_id)), Team::Red(Some(red_id))],
                        settings: sets,
                        allow_redo: true,       // HARD_CODED
                        seconds_per_action: 30, // HARD_CODED
                        forbidden_champions: self.get_forbidden_champs(id).await?,
                    };
                    self.redis_publisher
                        .stream_publish("draft", &prep_draft)
                        .await?;
                    self.redis_publisher
                        .pub_sub_publish(
                            "notification",
                            &json!({
                                "start_draft":id,
                            }),
                        )
                        .await?;
                }
            }
            None => bail!("Games list is empty"),
        }
        self.repo
            .update(&game_series)
            .await
            .context("Failed to update game series")?;
        Ok(game_series)
    }

    fn get_forbidden_classic(&self, games: Vec<Game>) -> Result<Vec<i32>> {
        let forbc: Vec<i32> = vec![];
        Ok(forbc)
    }

    fn get_forbidden_all_random(&self, games: Vec<Game>) -> Result<Vec<i32>> {
        let forbc: Vec<i32> = vec![];
        Ok(forbc)
    }

    fn get_forbidden_fearless(&self, games: Vec<Game>) -> Result<Vec<i32>> {
        let mut forbc: Vec<i32> = vec![];
        if games.is_empty() {
            return Ok(forbc);
        }
        for game in games {
            if let Some(draft) = game.draft {
                let mut forbcs: Vec<i32> =
                    draft.picks.iter().map(|el| el.champion_id as i32).collect();
                forbc.append(&mut forbcs);
            }
        }

        Ok(forbc)
    }

    fn get_forbidden_iron_man(&self, games: Vec<Game>) -> Result<Vec<i32>> {
        let mut forbc: Vec<i32> = vec![];
        if games.is_empty() {
            return Ok(forbc);
        }
        for game in games {
            if let Some(draft) = game.draft {
                let mut forbcs: Vec<i32> =
                    draft.picks.iter().map(|el| el.champion_id as i32).collect();
                forbc.append(&mut forbcs);
                let mut forbcs: Vec<i32> = draft.bans;
                forbc.append(&mut forbcs);
            }
        }

        Ok(forbc)
    }

    pub async fn get_forbidden_champs(&self, id: Uuid) -> Result<Vec<i32>> {
        let mut game_series = self
            .get_by_id(id)
            .await
            .context("Failed to get game series")?;
        let games = self.game_service.get_by_game_series_id(id).await?;
        game_series.games = Some(games);
        match game_series.settings {
            GameSettings::Lol(set) => match set.mode {
                game::LolGameMode::Fearless => {
                    let mut fbc = game_series.forbidden_champions;
                    fbc.append(
                        &mut self
                            .get_forbidden_fearless(game_series.games.context("No games")?)
                            .context("Failed to get foribdden_fearless")?,
                    );
                    return Ok(fbc);
                }
                game::LolGameMode::Classic => {
                    let mut fbc = game_series.forbidden_champions;
                    fbc.append(
                        &mut self
                            .get_forbidden_classic(game_series.games.context("No games")?)
                            .context("Failed to get foribdden_classic")?,
                    );
                    return Ok(fbc);
                }
                game::LolGameMode::AllRandom => {
                    let mut fbc = game_series.forbidden_champions;
                    fbc.append(
                        &mut self
                            .get_forbidden_all_random(game_series.games.context("No games")?)
                            .context("Failed to get foribdden_all_random")?,
                    );
                    return Ok(fbc);
                }
                game::LolGameMode::IronMan => {
                    let mut fbc = game_series.forbidden_champions;
                    fbc.append(
                        &mut self
                            .get_forbidden_iron_man(game_series.games.context("No games")?)
                            .context("Failed to get foribdden_iron_man")?,
                    );
                    return Ok(fbc);
                }
            },
            _ => todo!(),
        }
    }

    pub async fn choose_side(&self, actor: Actor, side: usize, id: Uuid) -> Result<()> {
        let mut game_series = self
            .get_by_id(id)
            .await
            .context("Failed to get game series")?;
        let games = self.game_service.get_by_game_series_id(id).await?;
        game_series.games = Some(games);
        match &game_series.games {
            Some(games) if !games.is_empty() => {
                let game = games
                    .iter()
                    .filter(|g| g.results.is_none() || g.results.as_ref().unwrap().is_empty())
                    .next()
                    .context("Games list is empty despite check")?;
                if games[0] == *game {
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

    pub async fn update_teams(
        &self,
        id: Uuid,
        to_replace: TeamParticipant,
        replacement: TeamParticipant,
    ) -> Result<()> {
        let mut gs = self
            .repo
            .find_by_id(id)
            .await
            .context("Failed to find game series by id")?
            .context("Game series not found")?;
        let idx = gs
            .teams
            .iter()
            .position(|el| *el == to_replace)
            .context("REPLACE GS ERROR")?;
        gs.teams[idx] = replacement;

        self.repo.update(&gs).await?;
        Ok(())
    }

    pub async fn get_by_id(&self, id: Uuid) -> Result<GameSeries> {
        let gs = self
            .repo
            .find_by_id(id)
            .await
            .context("Failed to find game series by id")?;
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
        self.repo
            .find_by_ids(ids)
            .await
            .context("Failed to find game series by ids")
    }
}
