use bitvec::array::BitArray;
use bitvec::order::Lsb0;
use chrono::{DateTime, Utc};
use shared::game::{Actor, LolGameMode};
use std::sync::Arc;
use tonic::{Request, Response, Status};
use uuid::Uuid;

use crate::domain::services::TournamentService as DomainTournamentService;
use crate::domain::value_objects::*;

use proto_build::common::Status as ProtoStatus;
use proto_build::game::tournament::{
    self, AddParticipantRequest, CreateTournamentRequest, GetTournamentRequest,
    ManyTournamentsResponse, RemoveParticipantRequest, TournamentResponse,
    tournament_service_server::TournamentService as GrpcTournamentService,
};
#[derive(Clone)]
pub struct GrpcTournamentServiceImpl {
    domain_service: Arc<DomainTournamentService>,
}

impl GrpcTournamentServiceImpl {
    pub fn new(domain_service: Arc<DomainTournamentService>) -> Self {
        Self { domain_service }
    }
}

#[tonic::async_trait]
impl GrpcTournamentService for GrpcTournamentServiceImpl {
    async fn create_tournament(
        &self,
        request: Request<CreateTournamentRequest>,
    ) -> Result<Response<TournamentResponse>, Status> {
        let req = request.into_inner();

        let host = req
            .host
            .ok_or_else(|| Status::invalid_argument("Host is required"))
            .map(|h| match h.r#type {
                1 => Actor::User(Uuid::parse_str(&h.id).unwrap_or_default()),
                2 => Actor::Team(Uuid::parse_str(&h.id).unwrap_or_default()),
                3 => Actor::Club(Uuid::parse_str(&h.id).unwrap_or_default()),
                _ => Actor::User(Uuid::new_v4()),
            })?;

        let participants: Vec<Actor> = req
            .participants
            .into_iter()
            .map(|p| match p.r#type {
                1 => Actor::User(Uuid::parse_str(&p.id).unwrap_or_default()),
                2 => Actor::Team(Uuid::parse_str(&p.id).unwrap_or_default()),
                3 => Actor::Club(Uuid::parse_str(&p.id).unwrap_or_default()),
                _ => Actor::User(Uuid::new_v4()),
            })
            .collect();

        let settings = req
            .settings
            .ok_or_else(|| Status::invalid_argument("Settings are required"))?;

        let tournament_settings = tournament_settings_from_proto(
            settings
                .settings
                .ok_or_else(|| Status::invalid_argument("Tournament settings are required"))?,
        )?;

        let start = req
            .start
            .ok_or_else(|| Status::invalid_argument("Start time is required"))?;
        let start =
            DateTime::from_timestamp(start.seconds, start.nanos as u32).expect("Invalid timestamp");

        let tournament = self
            .domain_service
            .create(
                host,
                participants,
                tournament_settings,
                start,
                Some(req.prizepool),
            )
            .await
            .map_err(|e| Status::internal(e.to_string()))?;

        Ok(Response::new(tournament_to_proto(tournament)))
    }

    async fn get_tournament(
        &self,
        request: Request<GetTournamentRequest>,
    ) -> Result<Response<TournamentResponse>, Status> {
        let req = request.into_inner();

        let ids: Vec<Uuid> = req
            .ids
            .iter()
            .filter_map(|id| Uuid::parse_str(id).ok())
            .collect();

        if ids.len() == 1 {
            let tournament = self
                .domain_service
                .get_by_id(ids[0])
                .await
                .map_err(|e| Status::internal(e.to_string()))?
                .ok_or_else(|| Status::not_found("Tournament not found"))?;

            Ok(Response::new(tournament_to_proto(tournament)))
        } else {
            let tournament_list = self
                .domain_service
                .get_by_ids(ids)
                .await
                .map_err(|e| Status::internal(e.to_string()))?;

            let first = tournament_list
                .into_iter()
                .next()
                .ok_or_else(|| Status::not_found("Tournament not found"))?;

            Ok(Response::new(tournament_to_proto(first)))
        }
    }

    async fn get_tournaments(
        &self,
        request: Request<GetTournamentRequest>,
    ) -> Result<Response<ManyTournamentsResponse>, Status> {
        let req = request.into_inner();

        let ids: Vec<Uuid> = req
            .ids
            .iter()
            .filter_map(|id| Uuid::parse_str(id).ok())
            .collect();

        let tournament_list = if !ids.is_empty() {
            self.domain_service
                .get_by_ids(ids)
                .await
                .map_err(|e| Status::internal(e.to_string()))?
        } else {
            vec![]
        };

        let proto_tournaments: Vec<TournamentResponse> = tournament_list
            .into_iter()
            .map(tournament_to_proto)
            .collect();

        Ok(Response::new(ManyTournamentsResponse {
            tournaments: proto_tournaments,
        }))
    }

    async fn start_tournament(
        &self,
        request: Request<GetTournamentRequest>,
    ) -> Result<Response<TournamentResponse>, Status> {
        let req = request.into_inner();

        let id = req
            .ids
            .first()
            .ok_or_else(|| Status::invalid_argument("ID is required"))?;
        let id = Uuid::parse_str(id).map_err(|_| Status::invalid_argument("Invalid id"))?;

        let tournament = self
            .domain_service
            .start(id)
            .await
            .map_err(|e| Status::internal(e.to_string()))?;

        Ok(Response::new(tournament_to_proto(tournament)))
    }

    async fn finish_tournament(
        &self,
        request: Request<GetTournamentRequest>,
    ) -> Result<Response<TournamentResponse>, Status> {
        let req = request.into_inner();

        let id = req
            .ids
            .first()
            .ok_or_else(|| Status::invalid_argument("ID is required"))?;
        let id = Uuid::parse_str(id).map_err(|_| Status::invalid_argument("Invalid id"))?;

        let tournament = self
            .domain_service
            .finish(id)
            .await
            .map_err(|e| Status::internal(e.to_string()))?;

        Ok(Response::new(tournament_to_proto(tournament)))
    }

    async fn add_participant(
        &self,
        request: Request<AddParticipantRequest>,
    ) -> Result<Response<TournamentResponse>, Status> {
        let req = request.into_inner();

        let tournament_id = Uuid::parse_str(&req.tournament_id)
            .map_err(|_| Status::invalid_argument("Invalid tournament_id"))?;

        let participant = req
            .participant
            .ok_or_else(|| Status::invalid_argument("Participant is required"))
            .map(|p| match p.r#type {
                1 => Actor::User(Uuid::parse_str(&p.id).unwrap_or_default()),
                2 => Actor::Team(Uuid::parse_str(&p.id).unwrap_or_default()),
                3 => Actor::Club(Uuid::parse_str(&p.id).unwrap_or_default()),
                _ => Actor::User(Uuid::new_v4()),
            })?;

        let tournament = self
            .domain_service
            .add_participant(tournament_id, participant)
            .await
            .map_err(|e| Status::internal(e.to_string()))?;

        Ok(Response::new(tournament_to_proto(tournament)))
    }

    async fn remove_participant(
        &self,
        request: Request<RemoveParticipantRequest>,
    ) -> Result<Response<TournamentResponse>, Status> {
        let req = request.into_inner();

        let tournament_id = Uuid::parse_str(&req.tournament_id)
            .map_err(|_| Status::invalid_argument("Invalid tournament_id"))?;

        let participant_id = Uuid::parse_str(&req.participant_id)
            .map_err(|_| Status::invalid_argument("Invalid participant_id"))?;

        let tournament = self
            .domain_service
            .remove_participant(tournament_id, participant_id)
            .await
            .map_err(|e| Status::internal(e.to_string()))?;

        Ok(Response::new(tournament_to_proto(tournament)))
    }
}

fn tournament_settings_from_proto(
    settings: proto_build::game::tournament::tournament_settings::Settings,
) -> Result<TournamentSettings, Status> {
    match settings {
        proto_build::game::tournament::tournament_settings::Settings::Lol(lol) => {
            let bracket_mode = match lol.bracket_mode {
                1 => LolBracketMode::DoubleElim,
                2 => LolBracketMode::SingleElim(true),
                3 => LolBracketMode::SingleElim(false),
                4 => LolBracketMode::Swiss,
                5 => LolBracketMode::RoundRobin,
                _ => LolBracketMode::SingleElim(false),
            };

            let draft_mode = match lol.draft_mode {
                1 => LolGameMode::Classic,
                2 => LolGameMode::Fearless,
                3 => LolGameMode::IronMan,
                4 => LolGameMode::AllRandom,
                _ => LolGameMode::Classic,
            };

            let series_best_of = lol.series_best_of.iter().map(|&x| x as u8).collect();

            let forbidden_champs = lol.forbidden_champions.iter().fold(
                BitArray::<[u8; 30], Lsb0>::ZERO,
                |mut acc, &idx| {
                    acc.set(idx as usize, true);
                    acc
                },
            );
            Ok(TournamentSettings::Lol(LolTournamentSettings {
                bracket_mode,
                draft_mode,
                team_size: lol.team_size as u8,
                tournament_type: TournamentType::Classic,
                map: lol.map as u8,
                forbidden_champions: forbidden_champs,
                series_best_of: Some(series_best_of),
            }))
        }
        _ => Err(Status::invalid_argument("Only LoL settings are supported")),
    }
}

fn tournament_to_proto(tournament: crate::domain::models::Tournament) -> TournamentResponse {
    let status = if tournament.is_finished() {
        ProtoStatus::Finished as i32
    } else if tournament.start() < Utc::now() {
        ProtoStatus::Active as i32
    } else {
        ProtoStatus::Scheduled as i32
    };

    let game_series_ids = tournament
        .games()
        .map(|games| games.iter().map(|g| g.id().to_string()).collect())
        .unwrap_or_default();

    TournamentResponse {
        id: tournament.id().to_string(),
        host: Some(proto_build::common::Actor {
            id: match tournament.host() {
                Actor::User(id) | Actor::Team(id) | Actor::Club(id) => id.to_string(),
            },
            r#type: match tournament.host() {
                Actor::User(_) => proto_build::common::ActorType::User as i32,
                Actor::Team(_) => proto_build::common::ActorType::Team as i32,
                Actor::Club(_) => proto_build::common::ActorType::Club as i32,
            },
        }),
        participants: tournament
            .teams()
            .iter()
            .map(|actor| proto_build::common::Actor {
                id: match actor {
                    Actor::User(id) | Actor::Team(id) | Actor::Club(id) => id.to_string(),
                },
                r#type: match actor {
                    Actor::User(_) => proto_build::common::ActorType::User as i32,
                    Actor::Team(_) => proto_build::common::ActorType::Team as i32,
                    Actor::Club(_) => proto_build::common::ActorType::Club as i32,
                },
            })
            .collect(),
        settings: Some(tournament_settings_to_proto(tournament.settings())),
        game_series_ids,
        start: Some(tournament.start_timestamp().into()),
        end: tournament.end_timestamp().map(|t| t.into()),
        status,
        prizepool: tournament.prizepool().map(String::from).unwrap(),
    }
}

fn tournament_settings_to_proto(
    settings: &TournamentSettings,
) -> proto_build::game::tournament::TournamentSettings {
    proto_build::game::tournament::TournamentSettings {
        game_type: proto_build::game::gameseries::GameType::Lol as i32,
        settings: Some(
            proto_build::game::tournament::tournament_settings::Settings::Lol(
                proto_build::game::tournament::LolTournamentSettings {
                    bracket_mode: match settings {
                        TournamentSettings::Lol(lol) => match lol.bracket_mode {
                            LolBracketMode::DoubleElim => 1,
                            LolBracketMode::SingleElim(true) => 2,
                            LolBracketMode::SingleElim(false) => 3,
                            LolBracketMode::Swiss => 4,
                            LolBracketMode::RoundRobin => 5,
                        },
                        _ => 3,
                    },
                    draft_mode: match settings {
                        TournamentSettings::Lol(lol) => match lol.draft_mode {
                            LolGameMode::Classic => {
                                proto_build::game::gameseries::LolGameMode::Classic as i32
                            }
                            LolGameMode::Fearless => {
                                proto_build::game::gameseries::LolGameMode::Fearless as i32
                            }
                            LolGameMode::IronMan => {
                                proto_build::game::gameseries::LolGameMode::IronMan as i32
                            }
                            LolGameMode::AllRandom => {
                                proto_build::game::gameseries::LolGameMode::AllRandom as i32
                            }
                        },
                        _ => proto_build::game::gameseries::LolGameMode::Classic as i32,
                    },
                    team_size: match settings {
                        TournamentSettings::Lol(lol) => lol.team_size as u32,
                        _ => 5,
                    },
                    map: match settings {
                        TournamentSettings::Lol(lol) => lol.map as u32,
                        _ => 11,
                    },
                    forbidden_champions: match settings {
                        TournamentSettings::Lol(lol) => lol
                            .forbidden_champions
                            .iter_ones()
                            .map(|index| index as u32)
                            .collect(),
                        _ => vec![0; 30],
                    },
                    series_best_of: match settings {
                        TournamentSettings::Lol(lol) => lol
                            .series_best_of
                            .iter()
                            .flatten()
                            .map(|&x| x as u32)
                            .collect(),
                        _ => vec![1],
                    },
                },
            ),
        ),
    }
}
