use async_trait::async_trait;

use crate::user::domain::user_domain::UserDomain;

#[async_trait]
pub trait UserRepository: Send + Sync {
    async fn save(&self, user: &UserDomain) -> anyhow::Result<UserDomain>;
    async fn update_by_email(&self, email: &str, user: &UserDomain) -> anyhow::Result<Option<UserDomain>>;
    async fn find_by_id(&self, id: &str) -> anyhow::Result<Option<UserDomain>>;
    async fn find_by_email(&self, email: &str) -> anyhow::Result<Option<UserDomain>>;
    async fn find_all(&self) -> anyhow::Result<Vec<UserDomain>>;
    async fn delete_by_email(&self, email: &str) -> anyhow::Result<bool>;
}
