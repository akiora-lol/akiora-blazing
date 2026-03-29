use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize)]
pub struct CreateGroupDto {
    pub owner_id: String,
    pub name: String,
}

#[derive(Debug, Deserialize)]
pub struct UpdateGroupDto {
    pub owner_id: Option<String>,
    pub name: Option<String>,
    pub add_users: Option<Vec<String>>,
    pub delete_users: Option<Vec<String>>,
}

#[derive(Debug, Serialize)]
pub struct GroupResponseDto {
    pub id: Option<String>,
    pub owner_id: String,
    pub name: String,
    pub members: Vec<String>,
}
