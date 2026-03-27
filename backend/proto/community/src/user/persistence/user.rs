use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct User {
    #[serde(rename = "_id", skip_serializing_if = "Option::is_none")]
    pub id: Option<bson::oid::ObjectId>,
    pub email: String,
    pub name: String,
    pub gender: String,
    pub social: Vec<Social>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Social {
    pub link: String,
    pub is_hide: bool,
}