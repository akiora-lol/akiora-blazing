use async_trait::async_trait;
use mongodb::{Collection, Database};
use mongodb::bson::{doc, oid::ObjectId};
use anyhow::Result;

use crate::constants::COLLECTION_GROUPS;
use crate::group::domain::GroupDomain;
use crate::group::domain::group_repository::GroupRepository;
use crate::group::mapper::GroupMapper;
use crate::group::persistence::Group;

pub struct MongoGroupRepository {
    collection: Collection<Group>,
}

impl MongoGroupRepository {
    pub fn new(database: &Database) -> Self {
        Self { collection: database.collection::<Group>(COLLECTION_GROUPS) }
    }
}

#[async_trait]
impl GroupRepository for MongoGroupRepository {
    async fn save(&self, domain: &GroupDomain) -> Result<GroupDomain> {
        let mut model = GroupMapper::domain_to_data(domain);
        model.id = None;
        let result = self.collection.insert_one(model.clone(), None).await?;
        model.id = result.inserted_id.as_object_id();
        Ok(GroupMapper::data_to_domain(model))
    }

    async fn update(&self, id: &str, domain: &GroupDomain) -> Result<Option<GroupDomain>> {
        let object_id = ObjectId::parse_str(id)?;
        let filter = doc! { "_id": object_id };
        let mut model = GroupMapper::domain_to_data(domain);
        model.id = None;
        self.collection.replace_one(filter.clone(), model, None).await?;
        let updated = self.collection.find_one(filter, None).await?;
        Ok(updated.map(GroupMapper::data_to_domain))
    }

    async fn find_by_id(&self, id: &str) -> Result<Option<GroupDomain>> {
        let object_id = ObjectId::parse_str(id)?;
        let group = self.collection.find_one(doc! { "_id": object_id }, None).await?;
        Ok(group.map(GroupMapper::data_to_domain))
    }

    async fn find_by_owner_id(&self, owner_id: &str) -> Result<Option<GroupDomain>> {
        let group = self.collection.find_one(doc! { "owner_id": owner_id }, None).await?;
        Ok(group.map(GroupMapper::data_to_domain))
    }

    async fn delete(&self, id: &str) -> Result<bool> {
        let object_id = ObjectId::parse_str(id)?;
        let result = self.collection.delete_one(doc! { "_id": object_id }, None).await?;
        Ok(result.deleted_count > 0)
    }

    async fn find_by_member_id(&self, user_id: &str) -> Result<Option<GroupDomain>> {
        // MongoDB matches array element: { members: "user_id" }
        let group = self.collection.find_one(doc! { "members": user_id }, None).await?;
        Ok(group.map(GroupMapper::data_to_domain))
    }
}
