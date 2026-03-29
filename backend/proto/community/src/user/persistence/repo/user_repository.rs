use async_trait::async_trait;
use mongodb::{Collection, Database};
use mongodb::bson::{doc, oid::ObjectId};
use anyhow::Result;

use crate::constants::COLLECTION_USERS;
use crate::user::domain::UserDomain;
use crate::user::domain::user_repository::UserRepository;
use crate::user::mapper::UserMapper;
use crate::user::persistence::User;

pub struct MongoUserRepository {
    collection: Collection<User>,
}

impl MongoUserRepository {
    pub fn new(database: &Database) -> Self {
        let collection = database.collection::<User>(COLLECTION_USERS);
        Self { collection }
    }
}

#[async_trait]
impl UserRepository for MongoUserRepository {
    async fn save(&self, domain: &UserDomain) -> Result<UserDomain> {
        let mut model = UserMapper::domain_to_data(domain);
        model.id = None;
        let result = self.collection.insert_one(model.clone(), None).await?;
        model.id = result.inserted_id.as_object_id();
        Ok(UserMapper::data_to_domain(model))
    }

    async fn update_by_email(&self, email: &str, domain: &UserDomain) -> Result<Option<UserDomain>> {
        let filter = doc! { "email": email };
        let mut model = UserMapper::domain_to_data(domain);
        model.id = None;
        self.collection.replace_one(filter.clone(), model, None).await?;
        let updated = self.collection.find_one(filter, None).await?;
        Ok(updated.map(UserMapper::data_to_domain))
    }

    async fn find_by_id(&self, id: &str) -> Result<Option<UserDomain>> {
        let object_id = ObjectId::parse_str(id)?;
        let filter = doc! { "_id": object_id };
        let user = self.collection.find_one(filter, None).await?;
        Ok(user.map(UserMapper::data_to_domain))
    }

    async fn find_by_email(&self, email: &str) -> Result<Option<UserDomain>> {
        let filter = doc! { "email": email };
        let user = self.collection.find_one(filter, None).await?;
        Ok(user.map(UserMapper::data_to_domain))
    }

    async fn find_all(&self) -> Result<Vec<UserDomain>> {
        let mut cursor = self.collection.find(doc! {}, None).await?;
        let mut users = Vec::new();
        while cursor.advance().await? {
            users.push(UserMapper::data_to_domain(cursor.deserialize_current()?));
        }
        Ok(users)
    }

    async fn delete_by_email(&self, email: &str) -> Result<bool> {
        let filter = doc! { "email": email };
        let result = self.collection.delete_one(filter, None).await?;
        Ok(result.deleted_count > 0)
    }
}