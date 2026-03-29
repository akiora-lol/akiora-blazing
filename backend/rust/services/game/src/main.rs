mod app;
mod domain;
mod infra;
use std::sync::Arc;

use app::GrpcGameSeriesServiceImpl;
use app::GrpcGameServiceImpl;
use app::GrpcTournamentServiceImpl;
use infra::get_mongo;
use infra::*;
use proto_build::game::game::game_service_server::GameServiceServer;
use proto_build::game::gameseries::game_series_service_server::GameSeriesServiceServer;
use proto_build::game::tournament::tournament_service_server::TournamentServiceServer;
use tonic::transport::Server;

use crate::domain::services::{GameSeriesService, GameService, TournamentService};
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let db = get_mongo().await?;

    let game_repo = Arc::new(GameRepo::new(&db.clone(), "games"));
    let game_series_repo = Arc::new(GameSeriesRepo::new(&db.clone(), "gameseries"));
    let tournament_repo = Arc::new(TournamentRepo::new(&db.clone(), "tournaments"));

    let game_service = Arc::new(GameService::new(game_repo));
    let game_series_service = Arc::new(GameSeriesService::new(game_series_repo));
    let tournament_service = Arc::new(TournamentService::new(tournament_repo));

    let address = "0.0.0.0:50051".parse()?;
    let grpc_gs = GrpcGameServiceImpl::new(game_service);
    let grpc_gss = GrpcGameSeriesServiceImpl::new(game_series_service);
    let grpc_ts = GrpcTournamentServiceImpl::new(tournament_service);

    println!("Listening at {}", address);

    Server::builder()
        .add_service(GameServiceServer::new(grpc_gs))
        .add_service(GameSeriesServiceServer::new(grpc_gss))
        .add_service(TournamentServiceServer::new(grpc_ts))
        .serve(address)
        .await?;

    Ok(())
}
