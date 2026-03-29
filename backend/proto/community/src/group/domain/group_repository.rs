use async_trait::async_trait;

use crate::group::domain::group_domain::GroupDomain;

/// Port (interface) for group persistence.
#[async_trait]
pub trait GroupRepository: Send + Sync {
    async fn save(&self, group: &GroupDomain) -> anyhow::Result<GroupDomain>;
    async fn update(&self, id: &str, group: &GroupDomain) -> anyhow::Result<Option<GroupDomain>>;
    async fn find_by_id(&self, id: &str) -> anyhow::Result<Option<GroupDomain>>;
    async fn find_by_owner_id(&self, owner_id: &str) -> anyhow::Result<Option<GroupDomain>>;
    async fn delete(&self, id: &str) -> anyhow::Result<bool>;
    /// Returns the group that contains `user_id` as a member, if any.
    async fn find_by_member_id(&self, user_id: &str) -> anyhow::Result<Option<GroupDomain>>;
}
