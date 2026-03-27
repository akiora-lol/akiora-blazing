use std::sync::Arc;
use uuid::Uuid;
use tonic::{Request, Response, Status};

use proto_build::game::gameseries::{
    self,
    game_series_service::GameSeriesService as GrpcGameSeriesService,
    CreateGameSeriesRequest, GameSeriesResponse, GetGameSeriesRequest,
    ManyGameSeriesResponse,
};
use proto_build::common::Status as ProtoStatus;

use crate::domain::services::GameSeriesService as DomainGameSeriesService;
use crate::domain::value_objects::*;

pub struct GrpcGameSeriesServiceImpl {
    domain_service: Arc<DomainGameSeriesService>,
}

impl GrpcGameSeriesServiceImpl {
    pub fn new(domain_service: Arc<DomainGameSeriesService>) -> Self {
        Self { domain_service }
    }
}

#[tonic::async_trait]
impl GrpcGameSeriesService for GrpcGameSeriesServiceImpl {
    async fn create_game_series(
        &self,
        request: Request<CreateGameSeriesRequest>,
    ) -> Result<Response<GameSeriesResponse>, Status> {
        let req = request.into_inner();
        
        let participants: Vec<Actor> = req.participants.into_iter().map(|p| {
            match p.r#type {
                1 => Actor::User(Uuid::parse_str(&p.id).unwrap_or_default()),
                2 => Actor::Group(Uuid::parse_str(&p.id).unwrap_or_default()),
                3 => Actor::Club(Uuid::parse_str(&p.id).unwrap_or_default()),
                _ => Actor::User(Uuid::new_v4()),
            }
        }).collect();
        
        let settings = req.settings
            .ok_or_else(|| Status::invalid_argument("Settings are required"))?;
        
        let game_settings = game_settings_from_proto(settings.settings.ok_or_else(|| Status::invalid_argument("Game settings are required"))?)?;
        
        let id = Uuid::new_v4();
        
        let game_series = self.domain_service.create(id, participants, game_settings)
            .await
            .map_err(|e| Status::internal(e.to_string()))?;
        
        Ok(Response::new(game_series_to_proto(game_series)))
    }

    async fn get_game_series(
        &self,
        request: Request<GetGameSeriesRequest>,
    ) -> Result<Response<GameSeriesResponse>, Status> {
        let req = request.into_inner();
        
        let ids: Vec<Uuid> = req.ids.iter()
            .filter_map(|id| Uuid::parse_str(id).ok())
            .collect();
        
        if ids.len() == 1 {
            let game_series = self.domain_service.get_by_id(ids[0])
                .await
                .map_err(|e| Status::internal(e.to_string()))?
                .ok_or_else(|| Status::not_found("GameSeries not found"))?;
            
            Ok(Response::new(game_series_to_proto(game_series)))
        } else {
            let game_series_list = self.domain_service.get_by_ids(ids)
                .await
                .map_err(|e| Status::internal(e.to_string()))?;
            
            let first = game_series_list.into_iter().next()
                .ok_or_else(|| Status::not_found("GameSeries not found"))?;
            
            Ok(Response::new(game_series_to_proto(first)))
        }
    }

    async fn get_game_series_list(
        &self,
        request: Request<GetGameSeriesRequest>,
    ) -> Result<Response<ManyGameSeriesResponse>, Status> {
        let req = request.into_inner();
        
        let ids: Vec<Uuid> = req.ids.iter()
            .filter_map(|id| Uuid::parse_str(id).ok())
            .collect();
        
        let game_series_list = if !ids.is_empty() {
            self.domain_service.get_by_ids(ids)
                .await
                .map_err(|e| Status::internal(e.to_string()))?
        } else {
            vec![]
        };
        
        let proto_series: Vec<GameSeriesResponse> = game_series_list
            .into_iter()
            .map(game_series_to_proto)
            .collect();
        
        Ok(Response::new(ManyGameSeriesResponse { series: proto_series }))
    }

    async fn start_game_series(
        &self,
        request: Request<GetGameSeriesRequest>,
    ) -> Result<Response<GameSeriesResponse>, Status> {
        let req = request.into_inner();
        
        let id = req.ids.first()
            .ok_or_else(|| Status::invalid_argument("ID is required"))?;
        let id = Uuid::parse_str(id)
            .map_err(|_| Status::invalid_argument("Invalid id"))?;
        
        let game_series = self.domain_service.start(id)
            .await
            .map_err(|e| Status::internal(e.to_string()))?;
        
        Ok(Response::new(game_series_to_proto(game_series)))
    }

    async fn finish_game_series(
        &self,
        request: Request<GetGameSeriesRequest>,
    ) -> Result<Response<GameSeriesResponse>, Status> {
        let req = request.into_inner();
        
        let id = req.ids.first()
            .ok_or_else(|| Status::invalid_argument("ID is required"))?;
        let id = Uuid::parse_str(id)
            .map_err(|_| Status::invalid_argument("Invalid id"))?;
        
        let game_series = self.domain_service.finish(id)
            .await
            .map_err(|e| Status::internal(e.to_string()))?;
        
        Ok(Response::new(game_series_to_proto(game_series)))
    }
}

fn game_settings_from_proto(settings: proto_build::game::gameseries::game_series_settings::Settings) -> Result<GameSettings, Status> {
    match settings {
        proto_build::game::gameseries::game_series_settings::Settings::Lol(lol) => {
            let mode = match lol.mode {
                1 => LolGameMode::Classic,
                2 => LolGameMode::Fearless,
                3 => LolGameMode::IronMan,
                4 => LolGameMode::AllRandom,
                _ => LolGameMode::Classic,
            };
            Ok(GameSettings::Lol(LolGameSettings {
                mode,
                team_size: lol.team_size as u8,
                map: lol.map as u8,
                best_of: lol.best_of as u8,
            }))
        }
        _ => Err(Status::invalid_argument("Only LoL settings are supported")),
    }
}

fn game_series_to_proto(game_series: crate::domain::models::GameSeries) -> GameSeriesResponse {
    let status = if game_series.is_finished() {
        ProtoStatus::Finished as i32
    } else if game_series.start().is_some() {
        ProtoStatus::Active as i32
    } else {
        ProtoStatus::Scheduled as i32
    };
    
    let game_ids = game_series.games()
        .map(|games| games.iter().map(|g| g.id().to_string()).collect())
        .unwrap_or_default();
    
    GameSeriesResponse {
        id: game_series.id().to_string(),
        participants: game_series.teams().iter().map(|actor| {
            proto_build::common::Actor {
                id: match actor {
                    Actor::User(id) | Actor::Group(id) | Actor::Club(id) => id.to_string(),
                },
                r#type: match actor {
                    Actor::User(_) => proto_build::common::ActorType::User as i32,
                    Actor::Group(_) => proto_build::common::ActorType::Group as i32,
                    Actor::Club(_) => proto_build::common::ActorType::Club as i32,
                },
            }
        }).collect(),
        settings: Some(game_series_settings_to_proto(game_series.settings())),
        game_ids,
        start: game_series.start().map(|t| t.into()),
        end: game_series.end().map(|t| t.into()),
        status,
    }
}

fn game_series_settings_to_proto(settings: &GameSettings) -> proto_build::game::gameseries::GameSeriesSettings {
    proto_build::game::gameseries::GameSeriesSettings {
        game_type: proto_build::game::gameseries::GameType::Lol as i32,
        settings: Some(proto_build::game::gameseries::game_series_settings::Settings::Lol(
            proto_build::game::gameseries::LolGameSettings {
                mode: match settings {
                    GameSettings::Lol(lol) => match lol.mode {
                        LolGameMode::Classic => proto_build::game::gameseries::LolGameMode::Classic as i32,
                        LolGameMode::Fearless => proto_build::game::gameseries::LolGameMode::Fearless as i32,
                        LolGameMode::IronMan => proto_build::game::gameseries::LolGameMode::IronMan as i32,
                        LolGameMode::AllRandom => proto_build::game::gameseries::LolGameMode::AllRandom as i32,
                    },
                    _ => proto_build::game::gameseries::LolGameMode::Classic as i32,
                },
                team_size: match settings {
                    GameSettings::Lol(lol) => lol.team_size as u32,
                    _ => 5,
                },
                map: match settings {
                    GameSettings::Lol(lol) => lol.map as u32,
                    _ => 11,
                },
                best_of: match settings {
                    GameSettings::Lol(lol) => lol.best_of as u32,
                    _ => 1,
                },
            }
        )),
    }
}
