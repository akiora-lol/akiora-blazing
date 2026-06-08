use crate::schemas::{Configuration, CreateLobby, CustomGameLobby, Mutator};
use irelia::{
    self,
    in_game::{GameClient, types::AllGameData},
    requests::RequestClientType,
};
use serde_derive::{Deserialize, Serialize};
use serde_json::{Value, json};
pub struct GameService {
    client: RequestClientType,
}
#[derive(Debug, thiserror::Error)]
pub enum DraftError {
    // ... другие ошибки
    #[error("LCU error: {0}")]
    LcuError(String),
}
impl GameService {
    pub async fn new() -> Self {
        let client = irelia::requests::new();
        GameService { client }
    }
    pub async fn get_current_summoner(&self) -> Result<CurrentSummoner, DraftError> {
        let lcu_client =
            irelia::rest::LcuClient::connect_with_request_client(&self.client).unwrap();
        let current_summoner: CurrentSummoner = lcu_client
            .get("/lol-summoner/v1/current-summoner")
            .await
            .map_err(|e| DraftError::LcuError(e.to_string()))?;
        Ok(current_summoner)
    }
    pub async fn get_ing_data(&self) {
        let active_player = self.client.active_player().await.unwrap();

        println!("{active_player:?}");

        let all_game_data = self.client.all_game_data().await;

        println!("{all_game_data:?}");
    }

    pub async fn create_lobby(&self) -> Result<serde_json::Value, DraftError> {
        let lcu_client = irelia::rest::LcuClient::connect_with_request_client(&self.client)
            .map_err(|e| DraftError::LcuError(e.to_string()))?;

        let request = json!({
            "queueId": 3100, //aram is 3200
            "isCustom": true,
            "customGameLobby": {
                "lobbyName": "test12349129034",
                "lobbyPassword": "123412355",
                "configuration": {



                    "mutators": {
                        "id": 2
                    },
                    "spectatorPolicy": "AllAllowed",
                    "teamSize": 3,
                    "maxPlayerCount": 0,
                    "gameServerRegion": "",
                    "spectatorDelayEnabled": false,
                    "hidePublicly": true
                }
            }
        });

        let response: serde_json::Value = lcu_client
            .post("/lol-lobby/v2/lobby", &request)
            .await
            .map_err(|e| DraftError::LcuError(format!("LCU error: {e}")))?;

        // Извлекаем полезную информацию из ответа
        let party_id = response
            .get("partyId")
            .and_then(|v| v.as_str())
            .unwrap_or("unknown");

        let is_leader = response
            .get("localMember")
            .and_then(|v| v.get("isLeader"))
            .and_then(|v| v.as_bool())
            .unwrap_or(false);

        let can_start = response
            .get("canStartActivity")
            .and_then(|v| v.as_bool())
            .unwrap_or(false);

        Ok(response)
    }
}

#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct CreateGame {
    pub map_id: i64,
    pub team_size: i64,
    pub lobby_name: String,
    pub lobby_password: String,
}

#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct CurrentSummoner {
    pub account_id: i64,
    pub display_name: String,
    pub game_name: String,
    pub internal_name: String,

    pub puuid: String,

    pub summoner_id: i64,

    pub tag_line: String,
}
