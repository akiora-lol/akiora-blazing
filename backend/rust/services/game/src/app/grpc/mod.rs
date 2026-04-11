// pub mod game_series_service;
// pub mod game_service;
pub mod tournament_service;

// pub use game_series_service::GrpcGameSeriesServiceImpl;
// pub use game_service::GrpcGameServiceImpl;
pub use tournament_service::GrpcTournamentServiceImpl;
async fn setup_grpc_gameseries() -> () {
    ()
}
