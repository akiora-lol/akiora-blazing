use std::sync::Arc;
use tonic::{Request, Response, Status};
use uuid::Uuid;

use crate::domain::services::GameService as DomainGameService;
use crate::domain::value_objects::participant::TeamParticipant;
use proto_build::common::Status as ProtoStatus;
use proto_build::game::game::{
    self, CreateGameRequest, GameResponse, GetGameRequest, GetGamesRequest, ManyGamesResponse,
    UpdateGameResultRequest, game_service_server::GameService as GrpcGameService,
};
use shared::game::*;

#[derive(Clone)]
pub struct GrpcGameServiceImpl {
    domain_service: Arc<DomainGameService>,
}

impl GrpcGameServiceImpl {
    pub fn new(domain_service: Arc<DomainGameService>) -> Self {
        Self { domain_service }
    }

    fn to_proto_status(finished: bool) -> i32 {
        if finished {
            ProtoStatus::Finished as i32
        } else {
            ProtoStatus::Active as i32
        }
    }
}

#[tonic::async_trait]
impl GrpcGameService for GrpcGameServiceImpl {
    async fn create_game(
        &self,
        request: Request<CreateGameRequest>,
    ) -> Result<Response<GameResponse>, Status> {
        let req = request.into_inner();

        let game_series_id = Uuid::parse_str(&req.game_series_id)
            .map_err(|_| Status::invalid_argument("Invalid game_series_id"))?;

        let id = Uuid::new_v4();

        let draft = req.draft.map(|d| Draft {
            history: d
                .history
                .into_iter()
                .map(|cmd| {
                    Command(
                        match team_from_proto(cmd.team) {
                            Team::Red(id) => Team::Red(id),
                            Team::Blue(id) => Team::Blue(id),
                        },
                        match cmd.action {
                            Some(proto_build::game::game::Action {
                                action_type: Some(action),
                            }) => match action {
                                proto_build::game::game::action::ActionType::Pick(p) => {
                                    Action::Pick(p as usize)
                                }
                                proto_build::game::game::action::ActionType::Ban(b) => {
                                    Action::Ban(b as usize)
                                }
                            },
                            _ => Action::Pick(0),
                        },
                    )
                })
                .collect(),
            picks: d
                .picks
                .into_iter()
                .map(|lock| ChampLock {
                    champion_id: lock.champion_id as usize,
                    player: Uuid::parse_str(&lock.player_id).unwrap_or_default(),
                })
                .collect(),
            forbidden_champions: bitvec::array::BitArray::new(
                d.forbidden_champions.try_into().unwrap_or([0u8; 30]),
            ),
            game_id: Uuid::parse_str(&d.game_id).unwrap(),
        });

        let game = self
            .domain_service
            .create(id, game_series_id, draft)
            .await
            .map_err(|e| Status::internal(e.to_string()))?;

        Ok(Response::new(game_to_proto(game)))
    }

    async fn get_game(
        &self,
        request: Request<GetGameRequest>,
    ) -> Result<Response<GameResponse>, Status> {
        let req = request.into_inner();

        let id = Uuid::parse_str(&req.id).map_err(|_| Status::invalid_argument("Invalid id"))?;

        let game = self
            .domain_service
            .get_by_id(id)
            .await
            .map_err(|e| Status::internal(e.to_string()))?
            .ok_or_else(|| Status::not_found("Game not found"))?;

        Ok(Response::new(game_to_proto(game)))
    }

    async fn get_games(
        &self,
        request: Request<GetGamesRequest>,
    ) -> Result<Response<ManyGamesResponse>, Status> {
        let req = request.into_inner();

        let ids: Vec<Uuid> = req
            .ids
            .iter()
            .filter_map(|id| Uuid::parse_str(id).ok())
            .collect();

        let games = if !ids.is_empty() {
            self.domain_service
                .get_by_ids(ids)
                .await
                .map_err(|e| Status::internal(e.to_string()))?
        } else if let Some(game_series_id) = req.game_series_id {
            let gs_id = Uuid::parse_str(&game_series_id)
                .map_err(|_| Status::invalid_argument("Invalid game_series_id"))?;
            self.domain_service
                .get_by_game_series_id(gs_id)
                .await
                .map_err(|e| Status::internal(e.to_string()))?
        } else {
            vec![]
        };

        let proto_games: Vec<GameResponse> = games.into_iter().map(game_to_proto).collect();

        Ok(Response::new(ManyGamesResponse { games: proto_games }))
    }

    async fn update_game_result(
        &self,
        request: Request<UpdateGameResultRequest>,
    ) -> Result<Response<GameResponse>, Status> {
        let req = request.into_inner();

        let id = Uuid::parse_str(&req.id).map_err(|_| Status::invalid_argument("Invalid id"))?;

        let results: Vec<TeamParticipant> = req
            .results
            .into_iter()
            .map(|r| TeamParticipant {
                participant: match r.participant {
                    Some(p) => match p.r#type {
                        1 => Actor::User(Uuid::parse_str(&p.id).unwrap_or_default()),
                        2 => Actor::Team(Uuid::parse_str(&p.id).unwrap_or_default()),
                        3 => Actor::Club(Uuid::parse_str(&p.id).unwrap_or_default()),
                        _ => Actor::User(Uuid::new_v4()),
                    },
                    None => Actor::User(Uuid::new_v4()),
                },
                users: r
                    .user_ids
                    .iter()
                    .filter_map(|id| Uuid::parse_str(id).ok())
                    .collect(),
            })
            .collect();

        let game = self
            .domain_service
            .update_result(id, results)
            .await
            .map_err(|e| Status::internal(e.to_string()))?;

        Ok(Response::new(game_to_proto(game)))
    }

    async fn finish_game(
        &self,
        request: Request<GetGameRequest>,
    ) -> Result<Response<GameResponse>, Status> {
        let req = request.into_inner();

        let id = Uuid::parse_str(&req.id).map_err(|_| Status::invalid_argument("Invalid id"))?;

        let game = self
            .domain_service
            .finish(id)
            .await
            .map_err(|e| Status::internal(e.to_string()))?;

        Ok(Response::new(game_to_proto(game)))
    }
}

fn game_to_proto(game: crate::domain::models::Game) -> GameResponse {
    let status = if game.is_finished() {
        ProtoStatus::Finished as i32
    } else if game.start().is_some() {
        ProtoStatus::Active as i32
    } else {
        ProtoStatus::Scheduled as i32
    };

    GameResponse {
        id: game.id().to_string(),
        game_series_id: game.game_series_id().to_string(),
        draft: game.draft().map(|d| game::Draft {
            game_id: d.game_id.to_string(),
            history: d
                .history
                .iter()
                .map(|cmd| game::Command {
                    team: match &cmd.0 {
                        Team::Red(_) => game::Team::Red as i32,
                        Team::Blue(_) => game::Team::Blue as i32,
                    },
                    action: Some(game::Action {
                        action_type: Some(match &cmd.1 {
                            Action::Pick(idx) => game::action::ActionType::Pick(*idx as i32),
                            Action::Ban(idx) => game::action::ActionType::Ban(*idx as i32),
                        }),
                    }),
                })
                .collect(),
            picks: d
                .picks
                .iter()
                .map(|lock| game::ChampLock {
                    champion_id: lock.champion_id as i32,
                    player_id: lock.player.to_string(),
                })
                .collect(),
            forbidden_champions: d.forbidden_champions.as_raw_slice().to_vec(),
        }),
        results: game
            .results()
            .map(|results| {
                results
                    .iter()
                    .map(|r| proto_build::common::TeamParticipant {
                        participant: Some(match r.participant {
                            Actor::User(id) => proto_build::common::Actor {
                                id: id.to_string(),
                                r#type: proto_build::common::ActorType::User as i32,
                            },
                            Actor::Team(id) => proto_build::common::Actor {
                                id: id.to_string(),
                                r#type: proto_build::common::ActorType::Team as i32,
                            },
                            Actor::Club(id) => proto_build::common::Actor {
                                id: id.to_string(),
                                r#type: proto_build::common::ActorType::Club as i32,
                            },
                        }),
                        user_ids: r.users.iter().map(|u| u.to_string()).collect(),
                    })
                    .collect()
            })
            .unwrap_or_default(),
        start: game.start_timestamp().map(|t| t.into()),
        end: game.end_timestamp().map(|t| t.into()),
        status,
    }
}

fn team_from_proto(team: i32) -> Team {
    match team {
        1 => Team::Red(Uuid::new_v4()),
        2 => Team::Blue(Uuid::new_v4()),
        _ => Team::Red(Uuid::new_v4()),
    }
}
