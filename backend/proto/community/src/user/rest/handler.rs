use axum::{
    extract::State,
    http::StatusCode,
    response::IntoResponse,
    Json,
};

use crate::state::AppState;
use crate::user::domain::{Gender, UserDomain};
use super::dto::{CreateUserDto, SocialDto, UpdateUserDto, UserResponseDto};

fn str_to_gender(s: &str) -> Gender {
    match s {
        "male" => Gender::Male,
        "female" => Gender::Female,
        _ => Gender::Helicopter,
    }
}

fn gender_to_str(g: &Gender) -> &'static str {
    match g {
        Gender::Male => "male",
        Gender::Female => "female",
        Gender::Helicopter => "helicopter",
    }
}

fn to_response_dto(user: UserDomain) -> UserResponseDto {
    UserResponseDto {
        id: user.id,
        email: user.email,
        name: user.name,
        gender: gender_to_str(&user.gender).to_string(),
        social: user.social.into_iter().map(|s| SocialDto { link: s.link, is_hide: s.is_hide }).collect(),
    }
}

pub async fn create_user(
    State(state): State<AppState>,
    Json(body): Json<CreateUserDto>,
) -> impl IntoResponse {
    match state.user_service.create_user(body.email, body.name, str_to_gender(&body.gender)).await {
        Ok(user) => (StatusCode::CREATED, Json(to_response_dto(user))).into_response(),
        Err(e) => (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()).into_response(),
    }
}

pub async fn get_user_by_id(
    State(state): State<AppState>,
    axum::extract::Path(id): axum::extract::Path<String>,
) -> impl IntoResponse {
    match state.user_service.get_user_by_id(&id).await {
        Ok(Some(user)) => (StatusCode::OK, Json(to_response_dto(user))).into_response(),
        Ok(None) => StatusCode::NOT_FOUND.into_response(),
        Err(e) => (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()).into_response(),
    }
}

pub async fn get_user_by_email(
    State(state): State<AppState>,
    axum::extract::Path(email): axum::extract::Path<String>,
) -> impl IntoResponse {
    match state.user_service.get_user_by_email(&email).await {
        Ok(Some(user)) => (StatusCode::OK, Json(to_response_dto(user))).into_response(),
        Ok(None) => StatusCode::NOT_FOUND.into_response(),
        Err(e) => (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()).into_response(),
    }
}

pub async fn update_user(
    State(state): State<AppState>,
    axum::extract::Path(email): axum::extract::Path<String>,
    Json(body): Json<UpdateUserDto>,
) -> impl IntoResponse {
    let existing = match state.user_service.get_user_by_email(&email).await {
        Ok(Some(u)) => u,
        Ok(None) => return StatusCode::NOT_FOUND.into_response(),
        Err(e) => return (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()).into_response(),
    };

    let updated = UserDomain {
        id: existing.id,
        email: existing.email.clone(),
        name: body.name.unwrap_or(existing.name),
        gender: body.gender.as_deref().map(str_to_gender).unwrap_or(existing.gender),
        social: existing.social,
    };

    match state.user_service.update_user(&email, updated).await {
        Ok(Some(u)) => (StatusCode::OK, Json(to_response_dto(u))).into_response(),
        Ok(None) => StatusCode::NOT_FOUND.into_response(),
        Err(e) => (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()).into_response(),
    }
}

pub async fn delete_user(
    State(state): State<AppState>,
    axum::extract::Path(email): axum::extract::Path<String>,
) -> impl IntoResponse {
    match state.user_service.delete_user(&email).await {
        Ok(true) => StatusCode::NO_CONTENT.into_response(),
        Ok(false) => StatusCode::NOT_FOUND.into_response(),
        Err(e) => (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()).into_response(),
    }
}
