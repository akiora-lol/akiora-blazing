use crate::domain::services::TournamentService as DomainTournamentService;
use crate::domain::value_objects::LolBracketMode as DomainBracketMode;
use crate::domain::value_objects::TournamentType as DomainTournamentType;
use crate::domain::value_objects::participant::TeamParticipant;
use crate::domain::value_objects::*;
use anyhow::Context;
use bitvec::array::BitArray;
use bitvec::order::Lsb0;
use chrono::DateTime;
use proto_build::common::ActorType;
use proto_build::common::{LolBracketMode, LolGameMode};
use proto_build::game::tournament::AddTeamParticipantRequest;
use proto_build::game::tournament::ChangeBracketRequest;
use proto_build::game::tournament::Empty;

use proto_build::game::tournament::TournamentType;

use proto_build::game::tournament::{
    AddParticipantRequest, CreateTournamentRequest, GetTournamentRequest, RemoveParticipantRequest,
    tournament_service_server::TournamentService as GrpcTournamentService,
};
use shared::game::{Actor, LolGameMode as DomainLolGameMode};
use std::sync::Arc;
use tonic::{Request, Response, Status};
use uuid::Uuid;
#[derive(Clone)]
pub struct GrpcTournamentServiceImpl {
    domain_service: DomainTournamentService,
}

impl GrpcTournamentServiceImpl {
    pub fn new(domain_service: DomainTournamentService) -> Self {
        Self { domain_service }
    }
}

#[tonic::async_trait]
impl GrpcTournamentService for GrpcTournamentServiceImpl {
    async fn create_tournament(
        &self,
        request: Request<CreateTournamentRequest>,
    ) -> Result<Response<Empty>, Status> {
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
            .create(
                host,
                req.is_open,
                tournament_settings,
                start,
                Some(req.prizepool),
            )
            .await
            .map_err(|e| Status::internal(e.to_string()))?;

        Ok(Response::new(Empty {}))
    }

    async fn get_tournament(
        &self,
        request: Request<GetTournamentRequest>,
    ) -> Result<Response<Empty>, Status> {
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

            Ok(Response::new(Empty {}))
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

            Ok(Response::new(Empty {}))
        }
    }

    async fn get_tournaments(
        &self,
        request: Request<GetTournamentRequest>,
    ) -> Result<Response<Empty>, Status> {
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
        Ok(Response::new(Empty {}))
    }

    async fn start_tournament(
        &self,
        request: Request<GetTournamentRequest>,
    ) -> Result<Response<Empty>, Status> {
        let req = request.into_inner();

        let id = req
            .ids
            .first()
            .ok_or_else(|| Status::invalid_argument("ID is required"))?;
        let id = Uuid::parse_str(id).map_err(|_| Status::invalid_argument("Invalid id"))?;

        self.domain_service
            .start_tournament(id)
            .await
            .map_err(|e| Status::internal(e.to_string()))?;

        Ok(Response::new(Empty {}))
    }

    async fn pre_build_bracket(
        &self,
        request: Request<GetTournamentRequest>,
    ) -> Result<Response<Empty>, Status> {
        let req = request.into_inner();

        let id = req
            .ids
            .first()
            .ok_or_else(|| Status::invalid_argument("ID is required"))?;
        let id = Uuid::parse_str(id).map_err(|_| Status::invalid_argument("Invalid id"))?;

        self.domain_service
            .prebuild_bracket(id)
            .await
            .map_err(|e| Status::internal(e.to_string()))?;

        Ok(Response::new(Empty {}))
    }

    async fn finish_tournament(
        &self,
        request: Request<GetTournamentRequest>,
    ) -> Result<Response<Empty>, Status> {
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

        Ok(Response::new(Empty {}))
    }

    async fn add_participant(
        &self,
        request: Request<AddParticipantRequest>,
    ) -> Result<Response<Empty>, Status> {
        let req = request.into_inner();

        let tournament_id = Uuid::parse_str(&req.tournament_id)
            .map_err(|_| Status::invalid_argument("Invalid tournament_id"))?;

        let participant = req
            .participant
            .ok_or_else(|| Status::invalid_argument("Participant is required"))
            .map(|p| match p.actor_type() {
                ActorType::Team => Actor::Team(Uuid::parse_str(&p.id).unwrap_or_default()),
                ActorType::User => Actor::User(Uuid::parse_str(&p.id).unwrap_or_default()),
                ActorType::Club => Actor::Club(Uuid::parse_str(&p.id).unwrap_or_default()),
                _ => Actor::User(Uuid::parse_str(&p.id).unwrap_or_default()),
            })?;

        let tournament = self
            .domain_service
            .add_participant(tournament_id, participant)
            .await
            .map_err(|e| Status::internal(e.to_string()))?;

        Ok(Response::new(Empty {}))
    }

    async fn add_team(
        &self,
        request: Request<AddTeamParticipantRequest>,
    ) -> Result<Response<Empty>, Status> {
        let req = request.into_inner();
        let tournament_id = Uuid::parse_str(&req.tournament_id)
            .map_err(|_| Status::invalid_argument("Invalid tournament_id"))?;
        let team_part = req
            .team_participant
            .ok_or_else(|| Status::invalid_argument("Participant is required"))
            .map(|tp| TeamParticipant {
                participant: to_domain_actor(tp.participant.unwrap()).unwrap(),
                users: tp
                    .user_ids
                    .iter()
                    .map(|str_id| {
                        Uuid::parse_str(str_id)
                            .map_err(|e| {
                                dbg!(&e);
                                e
                            })
                            .unwrap()
                    })
                    .collect(),
            })?;
        dbg!(&tournament_id);
        let tournament = self
            .domain_service
            .add_team(tournament_id, team_part)
            .await
            .map_err(|e| Status::internal(e.to_string()))?;

        Ok(Response::new(Empty {}))
    }

    async fn change_bracket(
        &self,
        request: Request<ChangeBracketRequest>,
    ) -> Result<Response<Empty>, Status> {
        let req = request.into_inner();
        let tournament_id = Uuid::parse_str(&req.tournament_id)
            .map_err(|_| Status::invalid_argument("Invalid tournament_id"))?;
        let s1 = req
            .swap_initiator
            .ok_or_else(|| Status::internal("Initiator required"))?;
        let s2 = req
            .swap_victim
            .ok_or_else(|| Status::internal("Target required"))?;
        let s1 = match &s1.actor_type() {
            ActorType::Club => Actor::Club(
                Uuid::parse_str(&s1.id).map_err(|e| Status::internal("Target required"))?,
            ),
            ActorType::User => Actor::User(
                Uuid::parse_str(&s1.id).map_err(|e| Status::internal("Target required"))?,
            ),
            ActorType::Team => Actor::Team(
                Uuid::parse_str(&s1.id).map_err(|e| Status::internal("Target required"))?,
            ),
            _ => Actor::Team(
                Uuid::parse_str("qwer").map_err(|e| Status::internal("Target required"))?,
            ),
        };

        let s2 = match &s2.actor_type() {
            ActorType::Club => Actor::Club(
                Uuid::parse_str(&s2.id).map_err(|e| Status::internal("Target required"))?,
            ),
            ActorType::User => Actor::User(
                Uuid::parse_str(&s2.id).map_err(|e| Status::internal("Target required"))?,
            ),
            ActorType::Team => Actor::Team(
                Uuid::parse_str(&s2.id).map_err(|e| Status::internal("Target required"))?,
            ),
            _ => Actor::Team(
                Uuid::parse_str("qwer").map_err(|e| Status::internal("Target required"))?,
            ),
        };
        let tournament = self
            .domain_service
            .change_bracket(tournament_id, s1, s2)
            .await
            .map_err(|e| Status::internal(e.to_string()))?;

        Ok(Response::new(Empty {}))
    }

    async fn add_participant_to_wait_list(
        &self,
        request: Request<AddParticipantRequest>,
    ) -> Result<Response<Empty>, Status> {
        let req = request.into_inner();

        let tournament_id = Uuid::parse_str(&req.tournament_id)
            .map_err(|_| Status::invalid_argument("Invalid tournament_id"))?;

        let participant = req
            .participant
            .ok_or_else(|| Status::invalid_argument("Participant is required"))?;

        let participant = to_domain_actor(participant)
            .ok_or_else(|| Status::invalid_argument("Participant is required"))?;
        self.domain_service
            .add_to_wait_list(tournament_id, participant)
            .await
            .map_err(|e| Status::internal(e.to_string()))?;

        Ok(Response::new(Empty {}))
    }

    async fn remove_participant(
        &self,
        request: Request<RemoveParticipantRequest>,
    ) -> Result<Response<Empty>, Status> {
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

        Ok(Response::new(Empty {}))
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

            let forbidden_champs = lol.forbidden_champions.iter().map(|e| *e as i32).collect();

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
                            .iter()
                            .map(|el| *el as u32)
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
fn to_domain_actor(act: proto_build::common::Actor) -> Option<Actor> {
    match &act.actor_type() {
        proto_build::common::ActorType::Club => Some(Actor::Club(
            Uuid::parse_str(&act.id)
                .map_err(|e| {
                    dbg!(&e);
                    e
                })
                .unwrap(),
        )),
        proto_build::common::ActorType::User => Some(Actor::User(
            Uuid::parse_str(&act.id)
                .map_err(|e| {
                    dbg!(&e);
                    e
                })
                .unwrap(),
        )),
        proto_build::common::ActorType::Team => Some(Actor::Team(
            Uuid::parse_str(&act.id)
                .map_err(|e| {
                    dbg!(&e);
                    e
                })
                .unwrap(),
        )),
        proto_build::common::ActorType::ActorUnspecified => None,
    }
}
