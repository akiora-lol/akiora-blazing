use anyhow::Context;
use axum::{
    Router,
    body::Body,
    extract::{Path, Query, State},
    http::{Request, StatusCode},
    response::{IntoResponse, Response},
    routing::{delete, get, post},
};
use tonic::transport::Channel;
use tower_http::cors::CorsLayer;
use tower_http::trace::TraceLayer;
use tracing_subscriber::EnvFilter;

use proto_build::game::{
    gameseries::{
        DraftActionRequest, ToggleReadyRequest, game_series_service_client::GameSeriesServiceClient,
    },
    tournament::{
        AddParticipantRequest, AddTeamParticipantRequest, ChangeBracketRequest,
        CreateTournamentRequest, GetTournamentRequest, RemoveParticipantRequest,
        tournament_service_client::TournamentServiceClient,
    },
};

// ── config ─────────────────────────────────────────────────────────────────────

struct Config {
    listen_addr: String,
    game_addr: String,
}

impl Config {
    fn from_env() -> anyhow::Result<Self> {
        let game_port = std::env::var("GAME_PORT").unwrap_or_else(|_| "50051".to_string());
        let game_host = std::env::var("GAME_HOST").unwrap_or_else(|_| "127.0.0.1".to_string());
        let http_port = std::env::var("GATEWAY_PORT").unwrap_or_else(|_| "8080".to_string());

        Ok(Self {
            listen_addr: format!("0.0.0.0:{http_port}"),
            game_addr: format!("http://{game_host}:{game_port}"),
        })
    }
}

// ── app state ──────────────────────────────────────────────────────────────────

#[derive(Clone)]
struct AppState {
    tournament: TournamentServiceClient<Channel>,
    gameseries: GameSeriesServiceClient<Channel>,
}

impl AppState {
    async fn connect(cfg: &Config) -> anyhow::Result<Self> {
        let channel = Channel::from_shared(cfg.game_addr.clone())
            .context("invalid game_addr")?
            .connect()
            .await
            .context("connect to game service")?;

        Ok(Self {
            tournament: TournamentServiceClient::new(channel.clone()),
            gameseries: GameSeriesServiceClient::new(channel),
        })
    }
}

// ── helpers ────────────────────────────────────────────────────────────────────

/// Deserialise request body JSON into prost message T.
async fn json_body<T: prost::Message + Default + serde::de::DeserializeOwned>(
    req: Request<Body>,
) -> anyhow::Result<T> {
    let bytes = axum::body::to_bytes(req.into_body(), 4 * 1024 * 1024).await?;
    let val: T = serde_json::from_slice(&bytes)?;
    Ok(val)
}

fn grpc_err(e: tonic::Status) -> Response {
    let code = match e.code() {
        tonic::Code::NotFound => StatusCode::NOT_FOUND,
        tonic::Code::AlreadyExists => StatusCode::CONFLICT,
        tonic::Code::InvalidArgument => StatusCode::BAD_REQUEST,
        tonic::Code::PermissionDenied => StatusCode::FORBIDDEN,
        tonic::Code::Unauthenticated => StatusCode::UNAUTHORIZED,
        _ => StatusCode::INTERNAL_SERVER_ERROR,
    };
    (code, e.message().to_string()).into_response()
}

fn ok_empty() -> Response {
    StatusCode::NO_CONTENT.into_response()
}

// ── tournament handlers ────────────────────────────────────────────────────────

async fn create_tournament(State(mut s): State<AppState>, req: Request<Body>) -> Response {
    let Ok(body) = json_body::<CreateTournamentRequest>(req).await else {
        return (StatusCode::BAD_REQUEST, "invalid body").into_response();
    };
    match s.tournament.create_tournament(body).await {
        Ok(_) => ok_empty(),
        Err(e) => grpc_err(e),
    }
}

async fn get_tournament(State(mut s): State<AppState>, Path(ids): Path<String>) -> Response {
    let req = GetTournamentRequest {
        ids: ids.split(',').map(String::from).collect(),
        game_type: None,
    };
    match s.tournament.get_tournament(req).await {
        Ok(r) => axum::Json(serde_json::to_value(format!("{:?}", r.into_inner())).unwrap())
            .into_response(),
        Err(e) => grpc_err(e),
    }
}

async fn get_tournaments(
    State(mut s): State<AppState>,
    Query(params): Query<std::collections::HashMap<String, String>>,
) -> Response {
    let game_type = params.get("game_type").and_then(|v| v.parse::<i32>().ok());
    let req = GetTournamentRequest {
        ids: vec![],
        game_type,
    };
    match s.tournament.get_tournaments(req).await {
        Ok(r) => axum::Json(serde_json::to_value(format!("{:?}", r.into_inner())).unwrap())
            .into_response(),
        Err(e) => grpc_err(e),
    }
}

async fn start_tournament(State(mut s): State<AppState>, Path(ids): Path<String>) -> Response {
    let req = GetTournamentRequest {
        ids: ids.split(',').map(String::from).collect(),
        game_type: None,
    };
    match s.tournament.start_tournament(req).await {
        Ok(_) => ok_empty(),
        Err(e) => grpc_err(e),
    }
}

async fn prebuild_bracket(State(mut s): State<AppState>, Path(ids): Path<String>) -> Response {
    let req = GetTournamentRequest {
        ids: ids.split(',').map(String::from).collect(),
        game_type: None,
    };
    match s.tournament.pre_build_bracket(req).await {
        Ok(_) => ok_empty(),
        Err(e) => grpc_err(e),
    }
}

async fn finish_tournament(State(mut s): State<AppState>, Path(ids): Path<String>) -> Response {
    let req = GetTournamentRequest {
        ids: ids.split(',').map(String::from).collect(),
        game_type: None,
    };
    match s.tournament.finish_tournament(req).await {
        Ok(_) => ok_empty(),
        Err(e) => grpc_err(e),
    }
}

async fn add_participant(
    State(mut s): State<AppState>,
    Path(tournament_id): Path<String>,
    req: Request<Body>,
) -> Response {
    let Ok(mut body) = json_body::<AddParticipantRequest>(req).await else {
        return (StatusCode::BAD_REQUEST, "invalid body").into_response();
    };
    body.tournament_id = tournament_id;
    match s.tournament.add_participant(body).await {
        Ok(_) => ok_empty(),
        Err(e) => grpc_err(e),
    }
}

async fn add_team(
    State(mut s): State<AppState>,
    Path(tournament_id): Path<String>,
    req: Request<Body>,
) -> Response {
    let Ok(mut body) = json_body::<AddTeamParticipantRequest>(req).await else {
        return (StatusCode::BAD_REQUEST, "invalid body").into_response();
    };
    body.tournament_id = tournament_id;
    match s.tournament.add_team(body).await {
        Ok(_) => ok_empty(),
        Err(e) => grpc_err(e),
    }
}

async fn add_to_waitlist(
    State(mut s): State<AppState>,
    Path(tournament_id): Path<String>,
    req: Request<Body>,
) -> Response {
    let Ok(mut body) = json_body::<AddParticipantRequest>(req).await else {
        return (StatusCode::BAD_REQUEST, "invalid body").into_response();
    };
    body.tournament_id = tournament_id;
    match s.tournament.add_participant_to_wait_list(body).await {
        Ok(_) => ok_empty(),
        Err(e) => grpc_err(e),
    }
}

async fn change_bracket(
    State(mut s): State<AppState>,
    Path(tournament_id): Path<String>,
    req: Request<Body>,
) -> Response {
    let Ok(mut body) = json_body::<ChangeBracketRequest>(req).await else {
        return (StatusCode::BAD_REQUEST, "invalid body").into_response();
    };
    body.tournament_id = tournament_id;
    match s.tournament.change_bracket(body).await {
        Ok(_) => ok_empty(),
        Err(e) => grpc_err(e),
    }
}

async fn remove_participant(
    State(mut s): State<AppState>,
    Path((tournament_id, participant_id)): Path<(String, String)>,
) -> Response {
    let req = RemoveParticipantRequest {
        tournament_id,
        participant_id,
    };
    match s.tournament.remove_participant(req).await {
        Ok(_) => ok_empty(),
        Err(e) => grpc_err(e),
    }
}

// ── gameseries handlers ────────────────────────────────────────────────────────

async fn draft_action(
    State(mut s): State<AppState>,
    Path(series_id): Path<String>,
    req: Request<Body>,
) -> Response {
    let Ok(mut body) = json_body::<DraftActionRequest>(req).await else {
        return (StatusCode::BAD_REQUEST, "invalid body").into_response();
    };
    body.series_id = series_id;
    match s.gameseries.draft_action(body).await {
        Ok(_) => ok_empty(),
        Err(e) => grpc_err(e),
    }
}

async fn toggle_ready(
    State(mut s): State<AppState>,
    Path(series_id): Path<String>,
    req: Request<Body>,
) -> Response {
    let Ok(mut body) = json_body::<ToggleReadyRequest>(req).await else {
        return (StatusCode::BAD_REQUEST, "invalid body").into_response();
    };
    body.series_id = series_id;
    match s.gameseries.toggle_ready(body).await {
        Ok(_) => ok_empty(),
        Err(e) => grpc_err(e),
    }
}

// ── router ─────────────────────────────────────────────────────────────────────

fn build_router(state: AppState) -> Router {
    Router::new()
        // tournaments
        .route("/v1/tournaments", post(create_tournament))
        .route("/v1/tournaments", get(get_tournaments))
        .route("/v1/tournaments/{ids}", get(get_tournament))
        .route("/v1/tournaments/{ids}/start", post(start_tournament))
        .route(
            "/v1/tournaments/{ids}/prebuild-bracket",
            post(prebuild_bracket),
        )
        .route("/v1/tournaments/{ids}/finish", post(finish_tournament))
        .route(
            "/v1/tournaments/{tournament_id}/participants",
            post(add_participant),
        )
        .route("/v1/tournaments/{tournament_id}/teams", post(add_team))
        .route(
            "/v1/tournaments/{tournament_id}/waitlist",
            post(add_to_waitlist),
        )
        .route(
            "/v1/tournaments/{tournament_id}/bracket/swap",
            post(change_bracket),
        )
        .route(
            "/v1/tournaments/{tournament_id}/participants/{participant_id}",
            delete(remove_participant),
        )
        // game-series
        .route(
            "/v1/game-series/{series_id}/draft/action",
            post(draft_action),
        )
        .route("/v1/game-series/{series_id}/ready", post(toggle_ready))
        // middleware
        .layer(CorsLayer::permissive())
        .layer(TraceLayer::new_for_http())
        .with_state(state)
}

// ── entry point ────────────────────────────────────────────────────────────────

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let _ = dotenvy::dotenv();

    tracing_subscriber::fmt()
        .with_env_filter(EnvFilter::from_default_env())
        .init();

    let cfg = Config::from_env()?;

    tracing::info!("connecting to game service at {}", cfg.game_addr);
    let state = AppState::connect(&cfg).await?;

    let addr: std::net::SocketAddr = cfg.listen_addr.parse()?;
    tracing::info!("gateway listening on {addr}");

    let listener = tokio::net::TcpListener::bind(addr).await?;
    axum::serve(listener, build_router(state)).await?;

    Ok(())
}
