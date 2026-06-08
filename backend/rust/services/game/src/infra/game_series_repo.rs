use futures::stream::TryStreamExt;
use mongodb::{
    IndexModel,
    bson::{self, doc},
    options::IndexOptions,
};
use uuid::Uuid;

use crate::domain::models::GameSeries;
use shared::MongoRepository;

pub type GameSeriesRepo = MongoRepository<GameSeries>;

pub trait GameSeriesRepoExt {
    async fn create_indexes(
        &self,
    ) -> Result<mongodb::results::CreateIndexesResult, mongodb::error::Error>;

    async fn find_by_id(&self, id: Uuid) -> Result<Option<GameSeries>, mongodb::error::Error>;

    async fn find_by_ids(&self, ids: Vec<Uuid>) -> Result<Vec<GameSeries>, mongodb::error::Error>;

    async fn insert(&self, game_series: &GameSeries) -> Result<(), mongodb::error::Error>;

    async fn update(&self, game_series: &GameSeries) -> Result<(), mongodb::error::Error>;

    async fn delete(&self, id: Uuid) -> Result<(), mongodb::error::Error>;
}

impl GameSeriesRepoExt for GameSeriesRepo {
    async fn create_indexes(
        &self,
    ) -> Result<mongodb::results::CreateIndexesResult, mongodb::error::Error> {
        let keys = doc! { "start": 1 };
        let start_index = IndexModel::builder()
            .keys(keys)
            .options(
                IndexOptions::builder()
                    .name("start_idx".to_string())
                    .build(),
            )
            .build();

        self.get_collection()
            .create_indexes(vec![start_index])
            .await
    }

    async fn find_by_id(&self, id: Uuid) -> Result<Option<GameSeries>, mongodb::error::Error> {
        use mongodb::bson::doc;

        let filter = doc! { "_id": id.to_string() };
        self.get_collection().find_one(filter).await
    }

    async fn find_by_ids(&self, ids: Vec<Uuid>) -> Result<Vec<GameSeries>, mongodb::error::Error> {
        let ids_str: Vec<String> = ids.into_iter().map(|id| id.to_string()).collect();
        let filter = doc! { "_id": { "$in": ids_str } };
        let cursor = self.get_collection().find(filter).await?;
        Ok(cursor.try_collect().await?)
    }

    async fn insert(&self, game_series: &GameSeries) -> Result<(), mongodb::error::Error> {
        self.get_collection().insert_one(game_series).await?;
        Ok(())
    }

    async fn update(&self, game_series: &GameSeries) -> Result<(), mongodb::error::Error> {
        let filter = doc! { "_id": game_series.id.to_string() };
        let update = doc! {
            "$set": {
                "start":bson::to_bson(&game_series.start).unwrap() ,
                "teams": game_series.teams.clone(),


            }
        };
        self.get_collection().update_one(filter, update).await?;
        Ok(())
    }

    async fn delete(&self, id: Uuid) -> Result<(), mongodb::error::Error> {
        use mongodb::bson::doc;

        let filter = doc! { "_id": id.to_string() };
        self.get_collection().delete_one(filter).await?;
        Ok(())
    }
}
