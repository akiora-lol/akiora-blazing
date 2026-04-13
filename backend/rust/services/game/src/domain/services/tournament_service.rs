use crate::domain::interfaces::BracketBuilder;
use crate::domain::models::{GameSeries, Tournament};
use crate::domain::services::bracket_se::SingleEliminationBuilder;
use crate::domain::services::game_series_service::GameSeriesService;
use crate::domain::value_objects::bracket::Bracket;
use crate::domain::value_objects::participant::TeamParticipant;
use crate::domain::value_objects::*;
use crate::infra::{TournamentRepo, TournamentRepoExt};
use anyhow::Result;
use bitvec::bitarr;
use bitvec::order::Lsb0;
use chrono::Utc;
use shared::game::{Actor, GameSettings, LolGameSettings};
use std::sync::Arc;
use uuid::Uuid;

pub struct TournamentService {
    repo: Arc<TournamentRepo>,
    game_series_service: Arc<GameSeriesService>,
    single_elim_bracket_builder: SingleEliminationBuilder,
}

impl TournamentService {
    pub fn new(repo: Arc<TournamentRepo>, game_series_service: Arc<GameSeriesService>) -> Self {
        Self {
            repo,
            game_series_service,
            single_elim_bracket_builder: SingleEliminationBuilder {},
        }
    }

    pub async fn create(
        &self,

        host: Actor,
        is_open: bool,
        settings: TournamentSettings,
        start: chrono::DateTime<Utc>,
        prizepool: Option<String>,
    ) -> Result<Tournament, Box<dyn std::error::Error + Send + Sync>> {
        let tournament = Tournament::new(host, settings, start, is_open, prizepool);
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

        tournament.mark_finished()?;
        self.repo.update_status(id, &tournament.status).await?;
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

        tournament.add_participant(participant.clone())?;
        self.repo
            .update_participant_pool(id, &tournament.participant_pool)
            .await
            .map_err(|e| {
                dbg!(&e);
                e
            })?;
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

        tournament.remove_participant(participant_id)?;
        self.repo
            .update_participant_pool(id, &tournament.participant_pool)
            .await?;
        Ok(tournament)
    }

    pub async fn add_team(
        &self,
        id: Uuid,
        team: TeamParticipant,
    ) -> Result<Tournament, Box<dyn std::error::Error + Send + Sync>> {
        let mut tournament = self
            .repo
            .find_by_id(id)
            .await?
            .ok_or("Tournament not found")?;

        tournament.add_team(team.clone())?;
        self.repo
            .update_participant_pool(id, &tournament.participant_pool)
            .await?;
        Ok(tournament)
    }

    pub async fn add_to_wait_list(
        &self,
        id: Uuid,
        participant: Actor,
    ) -> Result<Tournament, Box<dyn std::error::Error + Send + Sync>> {
        let mut tournament = self
            .repo
            .find_by_id(id)
            .await?
            .ok_or("Tournament not found")?;

        tournament.add_to_waitlist(participant.clone())?;
        self.repo
            .update_wait_list(id, &tournament.wait_list)
            .await?;
        Ok(tournament)
    }

    pub async fn remove_from_wait_list(
        &self,
        id: Uuid,
        participant_id: Uuid,
    ) -> Result<Tournament, Box<dyn std::error::Error + Send + Sync>> {
        let mut tournament = self
            .repo
            .find_by_id(id)
            .await?
            .ok_or("Tournament not found")?;

        tournament.remove_from_waitlist(participant_id)?;
        self.repo
            .update_wait_list(id, &tournament.wait_list)
            .await?;
        Ok(tournament)
    }

    pub async fn prebuild_bracket(
        &self,
        id: Uuid,
    ) -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
        let mut tournament = self
            .repo
            .find_by_id(id)
            .await?
            .ok_or("Tournament not found")?;

        let participant_vec: Vec<Actor> = tournament.participant_pool.into_keys().collect();
        match &tournament.settings {
            TournamentSettings::Lol(settings) => {
                let bracket = self.build_bracket(&settings, &participant_vec);

                self.repo.update_bracket(id, bracket).await?;
            }
            _ => todo!(),
        }
        Ok(())
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

        let pp_clone = tournament.participant_pool.clone();
        let participant_vec: Vec<Actor> = tournament.participant_pool.into_keys().collect();
        let bracket = match &tournament.settings {
            TournamentSettings::Lol(settings) => {
                let bracket = self.build_bracket(settings, &participant_vec);
                if bracket.is_none() {
                    return Err("Failed to build bracket".into());
                }
                bracket.unwrap()
            }
            _ => return Err("Only LoL tournaments are supported".into()),
        };

        // Создаём GameSeries для каждого матча в каждом раунде
        for round in &bracket.rounds {
            for match_node in round {
                let participants: Vec<Actor> = match_node
                    .team1
                    .iter()
                    .chain(match_node.team2.iter())
                    .map(|t| t.clone())
                    .collect();

                if participants.is_empty() {
                    continue;
                }

                let settings = match &tournament.settings {
                    TournamentSettings::Lol(lol_settings) => {
                        self.lol_settings_to_game_settings(lol_settings)
                    }
                    _ => return Err("Unsupported tournament type".into()),
                };
                let mut teams = Vec::new();
                for part in participants {
                    let tp = pp_clone.get(&part).unwrap();
                    teams.push(tp.clone().unwrap());
                }
                self.game_series_service
                    .create(match_node.game_series_id, teams, settings)
                    .await?;
            }
        }

        self.repo.update_bracket(id, Some(bracket)).await?;
        Ok(())
    }

    fn lol_settings_to_game_settings(&self, lol_settings: &LolTournamentSettings) -> GameSettings {
        let best_of = lol_settings
            .series_best_of
            .as_ref()
            .and_then(|v| v.first())
            .copied()
            .unwrap_or(1);

        GameSettings::Lol(LolGameSettings {
            mode: lol_settings.draft_mode.first().copied().unwrap_or_default(),
            team_size: lol_settings.team_size,
            map: lol_settings.map,
            best_of,
        })
    }

    fn build_bracket(
        &self,
        settings: &LolTournamentSettings,
        teams: &Vec<Actor>,
    ) -> Option<Bracket> {
        match settings.bracket_mode {
            LolBracketMode::DoubleElim => {
                todo!()
            }
            LolBracketMode::Scrim => {
                todo!()
            }
            LolBracketMode::SingleElim => self.single_elim_bracket_builder.build_bracket(teams),
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

    pub fn game_series_service(&self) -> &Arc<GameSeriesService> {
        &self.game_series_service
    }

    pub async fn delete(&self, id: Uuid) -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
        self.repo.delete(id).await.map_err(|e| e.into())
    }
}
