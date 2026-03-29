pub mod dto;
pub mod handler;

use axum::{
    routing::{delete, get, patch, post},
    Router,
};

use crate::constants::{ROUTE_USERS, ROUTE_USERS_BY_EMAIL, ROUTE_USERS_BY_ID};
use crate::state::AppState;
use handler::*;

pub fn user_router() -> Router<AppState> {
    Router::new()
        .route(ROUTE_USERS_BY_EMAIL, get(get_user_by_email))
        .route(ROUTE_USERS_BY_EMAIL, patch(update_user))
        .route(ROUTE_USERS_BY_EMAIL, delete(delete_user))
        .route(ROUTE_USERS_BY_ID, get(get_user_by_id))
        .route(ROUTE_USERS, post(create_user))
}
