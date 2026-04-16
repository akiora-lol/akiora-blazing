use proto_build::game::gameseries::{DraftAction, ToggleReadyRequest};
use std::sync::Arc;
use tonic::{Request, Response, Status};
use uuid::Uuid;

use proto_build::common::{Empty, Status as ProtoStatus};
use proto_build::game::gameseries::game_series_service_server::GameSeriesService as GrpcGameSeriesService;

use crate::app::mapper::{action_from_proto_to_domain, actor_from_proto_to_domain};
use crate::domain::services::{GameSeriesService as DomainGameSeriesService, TournamentService};
use shared::game::*;
#[derive(Clone)]
pub struct GrpcGameSeriesServiceImpl {
    domain_service: DomainGameSeriesService,
    domain_tourn_service: TournamentService,
}

impl GrpcGameSeriesServiceImpl {
    pub fn new(domain_service: DomainGameSeriesService, ts: TournamentService) -> Self {
        Self {
            domain_service,
            domain_tourn_service: ts,
        }
    }
}

#[tonic::async_trait]
impl GrpcGameSeriesService for GrpcGameSeriesServiceImpl {
    async fn draft_action(&self, request: Request<DraftAction>) -> Result<Response<Empty>, Status> {
        let req = request.into_inner();
        let id = Uuid::parse_str(&req.series_id)
            .map_err(|_| Status::invalid_argument("Invalid gameseries id"))?;
        let command = req
            .command
            .ok_or_else(|| Status::invalid_argument("Command should exist"))?;

        let actor = actor_from_proto_to_domain(
            command
                .actor
                .ok_or_else(|| Status::invalid_argument("Command actor should exist"))?,
        )
        .map_err(|e| Status::invalid_argument(e.to_string()))?;
        let action = action_from_proto_to_domain(
            command
                .action
                .ok_or_else(|| Status::invalid_argument("Command action should exist"))?,
        )
        .map_err(|e| Status::invalid_argument(e.to_string()))?;

        let gs = self
            .domain_service
            .get_by_id(id)
            .await
            .map_err(|_| Status::invalid_argument("Invalid gameseries id"))?;
        let tourn = self
            .domain_tourn_service
            .get_by_id(gs.tournament_id)
            .await
            .map_err(|_| Status::invalid_argument("Invalid gameseries id"))?;
        if let Some(t) = tourn {
            
            let teamp = t
                .participant_pool
                .get(&actor)
                .ok_or_else(|| Status::invalid_argument("Actor should exist"))?
                .clone();
            if let Some(tp) = teamp {
                self.clone()
                    .domain_service
                    .toggle_ready(id, tp)
                    .await
                    .map_err(|e| Status::invalid_argument(e.to_string()))?;
                return Ok(Response::new(Empty {}));
            }
        }

        Err(Status::invalid_argument("Smth Failed"))
    }
    async fn toggle_ready(
        &self,
        request: Request<ToggleReadyRequest>,
    ) -> Result<Response<Empty>, Status> {
        let req = request.into_inner();
        let id = Uuid::parse_str(&req.series_id)
            .map_err(|_| Status::invalid_argument("Invalid gameseries id"))?;
        let actor = req
            .actor
            .ok_or_else(|| Status::invalid_argument("Actor should exist"))?;

        let gs = self
            .domain_service
            .get_by_id(id)
            .await
            .map_err(|_| Status::invalid_argument("Invalid gameseries id"))?;
        let tourn = self
            .domain_tourn_service
            .get_by_id(gs.tournament_id)
            .await
            .map_err(|_| Status::invalid_argument("Invalid gameseries id"))?;
        if let Some(t) = tourn {
            let actor = actor_from_proto_to_domain(actor)
                .map_err(|e| Status::invalid_argument(e.to_string()))?;
            let teamp = t
                .participant_pool
                .get(&actor)
                .ok_or_else(|| Status::invalid_argument("Actor should exist"))?
                .clone();
            if let Some(tp) = teamp {
                self.clone()
                    .domain_service
                    .toggle_ready(id, tp)
                    .await
                    .map_err(|e| Status::invalid_argument(e.to_string()))?;
                return Ok(Response::new(Empty {}));
            }
        }

        Err(Status::invalid_argument("Smth Failed"))
    }
}
