use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize)]
pub struct CreateUserDto {
    pub email: String,
    pub name: String,
    pub gender: String,
}

#[derive(Debug, Deserialize)]
pub struct UpdateUserDto {
    pub name: Option<String>,
    pub gender: Option<String>,
}

#[derive(Debug, Serialize)]
pub struct UserResponseDto {
    pub id: Option<String>,
    pub email: String,
    pub name: String,
    pub gender: String,
    pub social: Vec<SocialDto>,
}

#[derive(Debug, Serialize)]
pub struct SocialDto {
    pub link: String,
    pub is_hide: bool,
}
