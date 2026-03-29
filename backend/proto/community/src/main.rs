mod constants;
mod db;
mod group;
mod state;
mod user;

use std::sync::Arc;

use axum::Router;
use tower_http::cors::CorsLayer;
use tonic::transport::Server;

use proto_build::community::group_v1::group_service_server::GroupServiceServer;
use proto_build::community::user_v1::user_service_server::UserServiceServer;
use state::AppState;
use group::domain::{GroupRepository, GroupService};
use group::grpc::GroupGrpcService;
use group::persistence::repo::MongoGroupRepository;
use group::rest::group_router;
use user::domain::{UserRepository, UserService};
use user::grpc::UserGrpcService;
use user::persistence::repo::MongoUserRepository;
use user::rest::user_router;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let database = db::connect_to_db().await?;

    let repository: Arc<dyn UserRepository> = Arc::new(MongoUserRepository::new(&database));
    let user_service = Arc::new(UserService::new(repository));

    let group_repo: Arc<dyn GroupRepository> = Arc::new(MongoGroupRepository::new(&database));
    let group_service = Arc::new(GroupService::new(group_repo));

    let app_state = AppState {
        user_service: Arc::clone(&user_service),
        group_service: Arc::clone(&group_service),
    };

    // ── REST (axum) ──────────────────────────────────────────────
    let rest_app = Router::new()
        .merge(user_router())
        .merge(group_router())
        .layer(CorsLayer::permissive())
        .with_state(app_state);

    // ── gRPC (tonic) ─────────────────────────────────────────────
    let grpc_addr = constants::GRPC_ADDR.parse()?;
    let grpc_user_svc = UserGrpcService::new(Arc::clone(&user_service));
    let grpc_group_svc = GroupGrpcService::new(Arc::clone(&group_service));

    println!("REST  → http://{}", constants::REST_ADDR);
    println!("gRPC  → {}", grpc_addr);

    let rest_handle = tokio::spawn(async move {
        let listener = tokio::net::TcpListener::bind(constants::REST_ADDR).await.unwrap();
        axum::serve(listener, rest_app).await.unwrap();
    });

    let grpc_handle = tokio::spawn(async move {
        Server::builder()
            .add_service(UserServiceServer::new(grpc_user_svc))
            .add_service(GroupServiceServer::new(grpc_group_svc))
            .serve(grpc_addr)
            .await
            .unwrap();
    });

    let (r1, r2) = tokio::join!(rest_handle, grpc_handle);
    r1?;
    r2?;
    Ok(())
}