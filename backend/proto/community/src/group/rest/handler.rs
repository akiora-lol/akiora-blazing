use axum::{
    extract::State,
    http::StatusCode,
    response::IntoResponse,
    Json,
};

use crate::group::domain::GroupDomain;
use crate::state::AppState;
use super::dto::{CreateGroupDto, GroupResponseDto, UpdateGroupDto};

fn to_response_dto(g: GroupDomain) -> GroupResponseDto {
    GroupResponseDto {
        id: g.id,
        owner_id: g.owner_id,
        name: g.name,
        members: g.members,
    }
}

pub async fn create_group(
    State(state): State<AppState>,
    Json(body): Json<CreateGroupDto>,
) -> impl IntoResponse {
    match state.group_service.create_group(body.owner_id, body.name).await {
        Ok(g) => (StatusCode::CREATED, Json(to_response_dto(g))).into_response(),
        Err(e) => (StatusCode::BAD_REQUEST, e.to_string()).into_response(),
    }
}

pub async fn get_group(
    State(state): State<AppState>,
    axum::extract::Path(id): axum::extract::Path<String>,
) -> impl IntoResponse {
    match state.group_service.get_group(&id).await {
        Ok(Some(g)) => (StatusCode::OK, Json(to_response_dto(g))).into_response(),
        Ok(None) => StatusCode::NOT_FOUND.into_response(),
        Err(e) => (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()).into_response(),
    }
}

pub async fn update_group(
    State(state): State<AppState>,
    axum::extract::Path(id): axum::extract::Path<String>,
    Json(body): Json<UpdateGroupDto>,
) -> impl IntoResponse {
    match state
        .group_service
        .update_group(
            &id,
            body.owner_id,
            body.name,
            body.add_users.unwrap_or_default(),
            body.delete_users.unwrap_or_default(),
        )
        .await
    {
        Ok(Some(g)) => (StatusCode::OK, Json(to_response_dto(g))).into_response(),
        Ok(None) => StatusCode::NOT_FOUND.into_response(),
        Err(e) => (StatusCode::BAD_REQUEST, e.to_string()).into_response(),
    }
}

pub async fn delete_group(
    State(state): State<AppState>,
    axum::extract::Path(id): axum::extract::Path<String>,
) -> impl IntoResponse {
    match state.group_service.delete_group(&id).await {
        Ok(true) => StatusCode::NO_CONTENT.into_response(),
        Ok(false) => StatusCode::NOT_FOUND.into_response(),
        Err(e) => (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()).into_response(),
    }
}
