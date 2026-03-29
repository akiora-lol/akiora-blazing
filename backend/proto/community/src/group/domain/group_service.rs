use std::sync::Arc;

use crate::group::domain::group_domain::GroupDomain;
use crate::group::domain::group_repository::GroupRepository;

pub struct GroupService {
    repository: Arc<dyn GroupRepository>,
}

impl GroupService {
    pub fn new(repository: Arc<dyn GroupRepository>) -> Self {
        Self { repository }
    }

    /// Creates a group. The owner becomes the first (and only) member.
    /// The owner must not already be in another group.
    pub async fn create_group(&self, owner_id: String, name: String) -> anyhow::Result<GroupDomain> {
        if self.repository.find_by_member_id(&owner_id).await?.is_some() {
            return Err(anyhow::anyhow!("User '{}' is already a member of a group", owner_id));
        }
        let group = GroupDomain::new(owner_id, name);
        self.repository.save(&group).await
    }

    pub async fn get_group(&self, id: &str) -> anyhow::Result<Option<GroupDomain>> {
        self.repository.find_by_id(id).await
    }

    /// Updates a group by its MongoDB ID.
    /// - `new_owner_id`: transfers ownership; new owner must already be a member.
    /// - `new_name`: renames the group.
    /// - `add_user_ids`: adds new members; each must not be in any other group.
    /// - `delete_user_ids`: removes members; the owner cannot be removed.
    pub async fn update_group(
        &self,
        id: &str,
        new_owner_id: Option<String>,
        new_name: Option<String>,
        add_user_ids: Vec<String>,
        delete_user_ids: Vec<String>,
    ) -> anyhow::Result<Option<GroupDomain>> {
        let mut group = match self.repository.find_by_id(id).await? {
            Some(g) => g,
            None => return Ok(None),
        };

        // Validate users to add: none may be in a different group
        for user_id in &add_user_ids {
            if let Some(existing) = self.repository.find_by_member_id(user_id).await? {
                if existing.id.as_deref() != Some(id) {
                    return Err(anyhow::anyhow!(
                        "User '{}' is already a member of another group", user_id
                    ));
                }
            }
        }

        // Remove members (owner cannot be removed)
        for user_id in &delete_user_ids {
            if *user_id == group.owner_id {
                return Err(anyhow::anyhow!("Cannot remove the owner from the group"));
            }
            group.members.retain(|m| m != user_id);
        }

        // Add new members (deduplicate)
        for user_id in add_user_ids {
            if !group.members.contains(&user_id) {
                group.members.push(user_id);
            }
        }

        if let Some(name) = new_name {
            if !name.is_empty() {
                group.name = name;
            }
        }

        if let Some(owner_id) = new_owner_id {
            if !owner_id.is_empty() {
                if !group.members.contains(&owner_id) {
                    return Err(anyhow::anyhow!("New owner must already be a member of the group"));
                }
                group.owner_id = owner_id;
            }
        }

        self.repository.update(id, &group).await
    }

    /// Used by gRPC: finds the group by current owner_id, then applies the patch.
    pub async fn update_group_by_owner(
        &self,
        owner_id: &str,
        new_name: Option<String>,
        add_user_ids: Vec<String>,
        delete_user_ids: Vec<String>,
    ) -> anyhow::Result<Option<GroupDomain>> {
        let group = match self.repository.find_by_owner_id(owner_id).await? {
            Some(g) => g,
            None => return Ok(None),
        };
        let id = group.id.clone().unwrap_or_default();
        self.update_group(&id, None, new_name, add_user_ids, delete_user_ids).await
    }

    pub async fn delete_group(&self, id: &str) -> anyhow::Result<bool> {
        self.repository.delete(id).await
    }
}
