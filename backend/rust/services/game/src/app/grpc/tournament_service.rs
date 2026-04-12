use crate::domain::services::TournamentService as DomainTournamentService;
use crate::domain::value_objects::LolBracketMode as DomainBracketMode;
use crate::domain::value_objects::TournamentType as DomainTournamentType;
use crate::domain::value_objects::*;
use bitvec::array::BitArray;
use bitvec::order::Lsb0;
use chrono::{DateTime, Utc};
use proto_build::common::{LolBracketMode, LolGameMode, Status as ProtoStatus};
use proto_build::game::tournament::TournamentType;
use proto_build::game::tournament::{
    AddParticipantRequest, CreateTournamentRequest, GetTournamentRequest, ManyTournamentsResponse,
    RemoveParticipantRequest, TournamentResponse,
    tournament_service_server::TournamentService as GrpcTournamentService,
};
use shared::game::{Actor, LolGameMode as DomainLolGameMode};
use std::sync::Arc;
use tonic::{Request, Response, Status};
use uuid::Uuid;
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
            .map(|h| match h.actor_type {
                1 => Actor::User(Uuid::parse_str(&h.id).unwrap_or_default()),
                2 => Actor::Team(Uuid::parse_str(&h.id).unwrap_or_default()),
                3 => Actor::Club(Uuid::parse_str(&h.id).unwrap_or_default()),
                _ => Actor::User(Uuid::new_v4()),
            })?;

        let settings = req
            .settings
            .ok_or_else(|| Status::invalid_argument("Settings are required"))?;

        let tournament_settings = tournament_settings_from_proto(
            settings
                .settings
                .ok_or_else(|| Status::invalid_argument("Tournament settings are required"))?,
        )?;

        let start = req.start;
        let start = DateTime::from_timestamp(start, 0).expect("Invalid timestamp");

        let tournament = self
            .domain_service
            .create(host, tournament_settings, start, Some(req.prizepool))
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
            .map(|p| match p.actor_type {
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

    async fn add_participant_to_wait_list(
        &self,
        request: Request<AddParticipantRequest>,
    ) -> Result<Response<TournamentResponse>, Status> {
        let req = request.into_inner();

        let tournament_id = Uuid::parse_str(&req.tournament_id)
            .map_err(|_| Status::invalid_argument("Invalid tournament_id"))?;

        let participant = req
            .participant
            .ok_or_else(|| Status::invalid_argument("Participant is required"))
            .map(|p| match p.actor_type {
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
            let lbm = lol.bracket_mode();
            let bracket_mode = match lbm {
                LolBracketMode::DoubleElim => DomainBracketMode::DoubleElim,
                LolBracketMode::SingleElimNoThirdPlace => DomainBracketMode::SingleElim,
                LolBracketMode::SingleElimThirdPlace => DomainBracketMode::SingleElimWithThird,
                LolBracketMode::Scrim => DomainBracketMode::Scrim,
                LolBracketMode::Swiss => DomainBracketMode::Swiss,
                LolBracketMode::RoundRobin => DomainBracketMode::RoundRobin,
                _ => DomainBracketMode::DoubleElim,
            };

            let ldm = lol.draft_mode();
            let draft_mode: Vec<DomainLolGameMode> = ldm
                .map(|el| match el {
                    LolGameMode::AllRandom => DomainLolGameMode::AllRandom,
                    LolGameMode::Classic => DomainLolGameMode::Classic,
                    LolGameMode::Fearless => DomainLolGameMode::Fearless,
                    LolGameMode::IronMan => DomainLolGameMode::IronMan,
                    _ => DomainLolGameMode::Classic,
                })
                .collect();

            let series_best_of = lol.series_best_of.iter().map(|&x| x as u8).collect();

            let forbidden_champs = lol.forbidden_champions.iter().fold(
                BitArray::<[u8; 30], Lsb0>::ZERO,
                |mut acc, &idx| {
                    acc.set(idx as usize, true);
                    acc
                },
            );

            let tournament_type = match lol.tournament_type() {
                TournamentType::Pickem => DomainTournamentType::PickEm,
                TournamentType::Presign => DomainTournamentType::Presign,
                _ => DomainTournamentType::Presign,
            };
            Ok(TournamentSettings::Lol(LolTournamentSettings {
                bracket_mode,
                draft_mode,
                team_size: lol.team_size as u8,
                tournament_type,
                map: lol.map as u8,
                forbidden_champions: forbidden_champs,
                series_best_of: Some(series_best_of),
            }))
        }
        _ => Err(Status::invalid_argument("Only LoL settings are supported")),
    }
}

fn tournament_to_proto(tournament: crate::domain::models::Tournament) -> TournamentResponse {
    let status = match tournament.status {
        TournamentStatus::Sheduled => ProtoStatus::Scheduled,
        TournamentStatus::Active => ProtoStatus::Active,
        TournamentStatus::Finished => ProtoStatus::Finished,
        TournamentStatus::Cancelled => ProtoStatus::Cancelled,
        _ => ProtoStatus::Unspecified,
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
            actor_type: match tournament.host() {
                Actor::User(_) => proto_build::common::ActorType::User as i32,
                Actor::Team(_) => proto_build::common::ActorType::Team as i32,
                Actor::Club(_) => proto_build::common::ActorType::Club as i32,
            },
        }),
        participants: tournament
            .teams
            .iter()
            .map(|actor| proto_build::common::Actor {
                id: match actor {
                    Actor::User(id) | Actor::Team(id) | Actor::Club(id) => id.to_string(),
                },
                actor_type: match actor {
                    Actor::User(_) => proto_build::common::ActorType::User as i32,
                    Actor::Team(_) => proto_build::common::ActorType::Team as i32,
                    Actor::Club(_) => proto_build::common::ActorType::Club as i32,
                },
            })
            .collect(),
        settings: Some(tournament_settings_to_proto(tournament.settings())),
        game_series_ids,
        start: tournament.start_timestamp(),
        end: tournament.end_timestamp(),
        status: status as i32,
        prizepool: tournament.prizepool().map(String::from).unwrap(),
    }
}

fn tournament_settings_to_proto(
    settings: &TournamentSettings,
) -> proto_build::game::tournament::TournamentSettings {
    proto_build::game::tournament::TournamentSettings {
        game_type: proto_build::common::GameType::Lol as i32,
        settings: Some(
            proto_build::game::tournament::tournament_settings::Settings::Lol(
                proto_build::game::tournament::LolTournamentSettings {
                    tournament_type: match settings {
                        TournamentSettings::Lol(lol) => match lol.tournament_type {
                            DomainTournamentType::PickEm => {
                                proto_build::game::tournament::TournamentType::Pickem as i32
                            }
                            DomainTournamentType::Presign => {
                                proto_build::game::tournament::TournamentType::Presign as i32
                            }
                        },
                        _ => 0,
                    },
                    bracket_mode: match settings {
                        TournamentSettings::Lol(lol) => match lol.bracket_mode {
                            DomainBracketMode::DoubleElim => LolBracketMode::DoubleElim as i32,
                            DomainBracketMode::SingleElim => {
                                LolBracketMode::SingleElimNoThirdPlace as i32
                            }
                            DomainBracketMode::SingleElimWithThird => {
                                LolBracketMode::SingleElimThirdPlace as i32
                            }
                            DomainBracketMode::Swiss => LolBracketMode::Swiss as i32,
                            DomainBracketMode::RoundRobin => LolBracketMode::RoundRobin as i32,
                            DomainBracketMode::Scrim => LolBracketMode::Scrim as i32,
                        },
                        _ => 0,
                    },
                    draft_mode: match settings {
                        TournamentSettings::Lol(lol) => lol
                            .draft_mode
                            .iter()
                            .map(|el| match el {
                                DomainLolGameMode::AllRandom => LolGameMode::AllRandom as i32,
                                DomainLolGameMode::Fearless => LolGameMode::Fearless as i32,
                                DomainLolGameMode::IronMan => LolGameMode::IronMan as i32,
                                DomainLolGameMode::Classic => LolGameMode::Classic as i32,
                            })
                            .collect(),

                        _ => vec![],
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
