use std::sync::Arc;

use mongodb::{Collection, Database, IndexModel, results::CreateIndexesResult};

pub struct MongoRepository<T: Send + Sync> {
    collection: Collection<T>,
}

impl<T> MongoRepository<T>
where
    T: Send + Sync,
{
    pub fn new(db: &Database, collection_name: &str) -> Self {
        Self {
            collection: db.collection::<T>(collection_name),
        }
    }
    pub fn get_collection(&self) -> &Collection<T> {
        &self.collection
    }
}
