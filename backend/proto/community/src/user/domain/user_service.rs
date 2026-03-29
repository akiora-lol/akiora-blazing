
use std::sync::Arc;

use crate::user::domain::user_domain::{Gender, UserDomain};
use crate::user::domain::user_repository::UserRepository;

pub struct UserService {
    repository: Arc<dyn UserRepository>,
}

impl UserService {
    pub fn new(repository: Arc<dyn UserRepository>) -> Self {
        Self { repository }
    }

    pub async fn create_user(&self, email: String, name: String, gender: Gender) -> anyhow::Result<UserDomain> {
        let user = UserDomain::new(email, name, gender);
        self.repository.save(&user).await
    }

    pub async fn get_user_by_id(&self, id: &str) -> anyhow::Result<Option<UserDomain>> {
        self.repository.find_by_id(id).await
    }

    pub async fn get_user_by_email(&self, email: &str) -> anyhow::Result<Option<UserDomain>> {
        self.repository.find_by_email(email).await
    }

    pub async fn update_user(&self, email: &str, updated: UserDomain) -> anyhow::Result<Option<UserDomain>> {
        self.repository.update_by_email(email, &updated).await
    }

    pub async fn list_users(&self) -> anyhow::Result<Vec<UserDomain>> {
        self.repository.find_all().await
    }

    pub async fn delete_user(&self, email: &str) -> anyhow::Result<bool> {
        self.repository.delete_by_email(email).await
    }
}