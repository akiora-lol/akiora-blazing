use mongodb::{Collection, Database};
use mongodb::bson::{doc, oid::ObjectId};
use mongodb::results::InsertOneResult;
use anyhow::Result;

use crate::user::persistence::User;

pub struct UserRepository {
    collection: Collection<User>,
}

impl UserRepository {
    pub async fn new(database: &Database) -> Self {
        let collection = database.collection::<User>("users");
        Self { collection }
    }

    pub async fn save(&self, user: User) -> Result<InsertOneResult> {
        let result = self.collection.insert_one(user, None).await?;
        Ok(result)
    }

    pub async fn find_by_email(&self, email: &str) -> Result<Option<User>> {
        let filter = doc! { "email": email };
        let user = self.collection.find_one(filter, None).await?;
        Ok(user)
    }

    pub async fn find_by_id(&self, id: &str) -> Result<Option<User>> {
        let object_id = ObjectId::parse_str(id)?;
        let filter = doc! { "_id": object_id };
        let user = self.collection.find_one(filter, None).await?;
        Ok(user)
    }

    pub async fn find_all(&self) -> Result<Vec<User>> {
        let mut cursor = self.collection.find(doc! {}, None).await?;
        let mut users = Vec::new();

        while cursor.advance().await? {
            users.push(cursor.deserialize_current()?);
        }

        Ok(users)
    }

    pub async fn delete_by_email(&self, email: &str) -> Result<u64> {
        let filter = doc! { "email": email };
        let result = self.collection.delete_one(filter, None).await?;
        Ok(result.deleted_count)
    }
}