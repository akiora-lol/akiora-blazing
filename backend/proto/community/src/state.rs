use std::sync::Arc;

use crate::group::domain::group_service::GroupService;
use crate::user::domain::user_service::UserService;

#[derive(Clone)]
pub struct AppState {
    pub user_service: Arc<UserService>,
    pub group_service: Arc<GroupService>,
}
