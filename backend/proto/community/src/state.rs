use std::sync::Arc;

use crate::user::domain::user_service::UserService;

#[derive(Clone)]
pub struct AppState {
    pub user_service: Arc<UserService>,
}
