pub mod dto;
pub mod handler;

use axum::{
    routing::{delete, get, patch, post},
    Router,
};

use crate::constants::{ROUTE_GROUPS, ROUTE_GROUPS_BY_ID};
use crate::state::AppState;
use handler::*;

pub fn group_router() -> Router<AppState> {
    Router::new()
        .route(ROUTE_GROUPS, post(create_group))
        .route(ROUTE_GROUPS_BY_ID, get(get_group))
        .route(ROUTE_GROUPS_BY_ID, patch(update_group))
        .route(ROUTE_GROUPS_BY_ID, delete(delete_group))
}
