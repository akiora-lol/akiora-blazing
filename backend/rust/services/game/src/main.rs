// mod app;
// mod domain;
// mod infra;
// use app::GrpcGameSeriesServiceImpl;
// use std::{env, sync::Arc};
// // use app::GrpcGameServiceImpl;
// use app::GrpcTournamentServiceImpl;
// use infra::get_mongo;
// use infra::*;
// // use proto_build::game::game::game_service_server::GameServiceServer;
// use proto_build::game::gameseries::game_series_service_server::GameSeriesServiceServer;
// use proto_build::game::tournament::tournament_service_server::TournamentServiceServer;
// use shared::{Publisher, get_redis_manager};
// use tonic::transport::Server;
fn main() {}
// use crate::domain::services::{GameSeriesService, GameService, TournamentService};
// #[tokio::main]
// async fn main() -> Result<(), Box<dyn std::error::Error>> {
//     let db = get_mongo().await?;
//     let game_repo = Arc::new(GameRepo::new(&db.clone(), "games"));
//     let game_series_repo = Arc::new(GameSeriesRepo::new(&db.clone(), "gameseries"));
//     let tournament_repo = Arc::new(TournamentRepo::new(&db.clone(), "tournaments"));

//     let connection_string = env::var("REDIS_URI").unwrap_or("redis://localhost:6379".to_string());

//     let mut con = get_redis_manager(connection_string.as_str()).await?;

//     let redis_publisher = Publisher::new(con);

//     let game_service = GameService::new(game_repo);
//     let game_series_service =
//         GameSeriesService::new(game_series_repo, game_service, redis_publisher);
//     let tournament_service = TournamentService::new(tournament_repo, game_series_service.clone());

//     let address = "0.0.0.0:50051".parse()?;
//     // let grpc_gs = GrpcGameServiceImpl::new(game_service);
//     let grpc_gss = GrpcGameSeriesServiceImpl::new(game_series_service, tournament_service.clone());
//     let grpc_ts = GrpcTournamentServiceImpl::new(tournament_service);

//     println!("Listening at {}", address);

//     Server::builder()
//         // .add_service(GameServiceServer::new(grpc_gs))
//         .add_service(GameSeriesServiceServer::new(grpc_gss))
//         .add_service(TournamentServiceServer::new(grpc_ts))
//         .serve(address)
//         .await?;

//     Ok(())
// }
