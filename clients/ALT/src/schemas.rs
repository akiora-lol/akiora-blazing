use serde_derive::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct CreateLobby {
    pub customg_game_lobby: CustomGameLobby,
    pub is_custom: bool,
}

#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct CustomGameLobby {
    pub configuration: Configuration,
    pub lobby_name: String,
    pub lobby_password: String,
}

#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct Configuration {
    pub game_mode: String, //CLASSIC \ PRACTICETOOL
    pub game_mutator: String,
    pub game_server_region: String,
    pub map_id: i64,
    pub mutators: Mutator,
    pub team_size: i64,
    pub spectator_policy: String,
}

#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct Mutator {
    pub id: i64,
}
