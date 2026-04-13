use std::collections::HashMap;

use futures::stream::TryStreamExt;
use mongodb::bson;
use mongodb::{IndexModel, bson::doc, options::IndexOptions};
use shared::game::Actor;
use uuid::Uuid;

use crate::domain::models::Tournament;
use crate::domain::value_objects::TournamentStatus;
use crate::domain::value_objects::bracket::Bracket;
use crate::domain::value_objects::participant::TeamParticipant;
use shared::MongoRepository;

pub type TournamentRepo = MongoRepository<Tournament>;

pub trait TournamentRepoExt {
    async fn create_indexes(
        &self,
    ) -> Result<mongodb::results::CreateIndexesResult, mongodb::error::Error>;

    async fn find_by_id(&self, id: Uuid) -> Result<Option<Tournament>, mongodb::error::Error>;

    async fn find_by_ids(&self, ids: Vec<Uuid>) -> Result<Vec<Tournament>, mongodb::error::Error>;

    async fn insert(&self, tournament: &Tournament) -> Result<(), mongodb::error::Error>;

    async fn update(&self, tournament: &Tournament) -> Result<(), mongodb::error::Error>;

    async fn update_participant_pool(
        &self,
        id: Uuid,
        participants: &HashMap<Actor, Option<TeamParticipant>>,
    ) -> Result<(), mongodb::error::Error>;

    async fn update_wait_list(
        &self,
        id: Uuid,
        wait_list: &[Actor],
    ) -> Result<(), mongodb::error::Error>;

    async fn update_teams(
        &self,
        id: Uuid,
        teams: &[TeamParticipant],
    ) -> Result<(), mongodb::error::Error>;

    async fn update_status(
        &self,
        id: Uuid,
        status: &TournamentStatus,
    ) -> Result<(), mongodb::error::Error>;

    async fn update_start_time(
        &self,
        id: Uuid,
        start_time: &chrono::DateTime<chrono::Utc>,
    ) -> Result<(), mongodb::error::Error>;
    async fn update_bracket(
        &self,
        id: Uuid,
        bracket: Option<Bracket>,
    ) -> Result<(), mongodb::error::Error>;

    async fn delete(&self, id: Uuid) -> Result<(), mongodb::error::Error>;
}

impl TournamentRepoExt for TournamentRepo {
    async fn create_indexes(
        &self,
    ) -> Result<mongodb::results::CreateIndexesResult, mongodb::error::Error> {
        // Индекс на host
        let host_index = IndexModel::builder()
            .keys(doc! { "host": 1 })
            .options(IndexOptions::builder().name("host_idx".to_string()).build())
            .build();

        // Индекс на start
        let start_index = IndexModel::builder()
            .keys(doc! { "start": 1 })
            .options(
                IndexOptions::builder()
                    .name("start_idx".to_string())
                    .build(),
            )
            .build();

        // Индекс на teams
        let teams_index = IndexModel::builder()
            .keys(doc! { "teams": 1 })
            .options(
                IndexOptions::builder()
                    .name("teams_idx".to_string())
                    .build(),
            )
            .build();

        self.get_collection()
            .create_indexes(vec![host_index, start_index, teams_index])
            .await
    }

    async fn find_by_id(&self, id: Uuid) -> Result<Option<Tournament>, mongodb::error::Error> {
        let filter = doc! { "_id": id.to_string() };
        self.get_collection().find_one(filter).await.map_err(|e| {
            dbg!(&e);
            e
        })
    }

    async fn find_by_ids(&self, ids: Vec<Uuid>) -> Result<Vec<Tournament>, mongodb::error::Error> {
        let ids_str: Vec<String> = ids.into_iter().map(|id| id.to_string()).collect();
        let filter = doc! { "_id": { "$in": ids_str } };
        let cursor = self.get_collection().find(filter).await?;
        Ok(cursor.try_collect().await?)
    }

    async fn insert(&self, tournament: &Tournament) -> Result<(), mongodb::error::Error> {
        self.get_collection().insert_one(tournament).await?;
        Ok(())
    }

    async fn update(&self, tournament: &Tournament) -> Result<(), mongodb::error::Error> {
        todo!();
        Ok(())
    }

    async fn update_participant_pool(
        &self,
        id: Uuid,
        participants: &HashMap<Actor, Option<TeamParticipant>>,
    ) -> Result<(), mongodb::error::Error> {
        let mut to_be_saved = Vec::new();
        for (key, value) in participants {
            to_be_saved.push((key, value));
        }

        let filter = doc! { "_id": id.to_string() };
        let update = doc! { "$set": { "participant_pool": bson::to_bson(&to_be_saved).map_err(|e|{
            dbg!(&e);
            e
        }).unwrap() }};
        self.get_collection()
            .update_one(filter, update)
            .await
            .map_err(|e| {
                dbg!(&e);
                e
            })?;
        Ok(())
    }

    async fn update_bracket(
        &self,
        id: Uuid,
        bracket: Option<Bracket>,
    ) -> Result<(), mongodb::error::Error> {
        let filter = doc! { "_id": id.to_string() };
        let update = doc! { "$set": { "bracket": bracket } };
        self.get_collection().update_one(filter, update).await?;
        Ok(())
    }

    async fn update_wait_list(
        &self,
        id: Uuid,
        wait_list: &[Actor],
    ) -> Result<(), mongodb::error::Error> {
        let filter = doc! { "_id": id.to_string() };
        let update = doc! { "$set": { "wait_list": wait_list.to_vec() } };
        self.get_collection().update_one(filter, update).await?;
        Ok(())
    }

    async fn update_teams(
        &self,
        id: Uuid,
        teams: &[TeamParticipant],
    ) -> Result<(), mongodb::error::Error> {
        let filter = doc! { "_id": id.to_string() };
        let update = doc! { "$set": { "teams": teams.to_vec() } };
        self.get_collection().update_one(filter, update).await?;
        Ok(())
    }

    async fn update_status(
        &self,
        id: Uuid,
        status: &TournamentStatus,
    ) -> Result<(), mongodb::error::Error> {
        let filter = doc! { "_id": id.to_string() };
        let update = doc! { "$set": { "status": bson::to_bson(status).unwrap() } };
        self.get_collection().update_one(filter, update).await?;
        Ok(())
    }

    async fn update_start_time(
        &self,
        id: Uuid,
        start_time: &chrono::DateTime<chrono::Utc>,
    ) -> Result<(), mongodb::error::Error> {
        let filter = doc! { "_id": id.to_string() };
        let update = doc! { "$set": { "start_time": bson::to_bson(start_time).unwrap() } };
        self.get_collection().update_one(filter, update).await?;
        Ok(())
    }

    async fn delete(&self, id: Uuid) -> Result<(), mongodb::error::Error> {
        let filter = doc! { "_id": id.to_string() };
        self.get_collection().delete_one(filter).await?;
        Ok(())
    }
}
