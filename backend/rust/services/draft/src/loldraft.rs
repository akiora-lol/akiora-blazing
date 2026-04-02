use crate::errors::DraftError;
use bitvec::prelude::*;
use chrono::{DateTime, Utc};
use redis::AsyncTypedCommands;
use redis::aio::ConnectionManager;
use redis_macros::{FromRedisValue, ToRedisArgs};
use serde::{Deserialize, Serialize};
use shared::game::*;
use shared::get_redis_manager;
use uuid::Uuid;
#[derive(Serialize, Deserialize, Clone, FromRedisValue, ToRedisArgs)]
pub struct Draft {
    history: Vec<Command>,
    deadline: DateTime<Utc>,
    game_id: Uuid,
    forbidden_champions: BitArray<[u8; 30], Lsb0>,
    settings: LolGameSettings,
    stage: usize,
}

impl Draft {
    pub fn game_id(&self) -> String {
        self.game_id.to_string()
    }
    async fn perform_command(&mut self, command: &Command) -> Result<&Self, DraftError> {
        match self.settings.mode {
            LolGameMode::Classic => {
                if self.valid_classic_command(command) {
                    self.stage += 1;
                    let champ_id = match command.1 {
                        Action::Ban(c) | Action::Pick(c) => c,
                    };
                    self.forbidden_champions.set(champ_id, true);
                    self.history.push(command.clone());
                    Ok(self)

                    // save self to redis
                    // update deadline
                    // push info for redis pub\sub
                } else {
                    Err(DraftError::InvalidCommand)
                }
            }
            _ => Err(DraftError::InvalidCommand),
        }
    }

    fn valid_classic_command(&self, command: &Command) -> bool {
        match (self.stage, command) {
            (1, Command(Team::Blue(_x), Action::Ban(_c))) => true,
            (2, Command(Team::Red(_x), Action::Ban(_c))) => true,
            (3, Command(Team::Blue(_x), Action::Ban(_c))) => true,
            (4, Command(Team::Red(_x), Action::Ban(_c))) => true,
            (5, Command(Team::Blue(_x), Action::Ban(_c))) => true,
            (6, Command(Team::Red(_x), Action::Ban(_c))) => true,
            (7, Command(Team::Blue(_x), Action::Pick(_c))) => true,
            (8, Command(Team::Red(_x), Action::Pick(_c))) => true,
            (9, Command(Team::Red(_x), Action::Pick(_c))) => true,
            (10, Command(Team::Blue(_x), Action::Pick(_c))) => true,
            (11, Command(Team::Blue(_x), Action::Pick(_c))) => true,
            (12, Command(Team::Red(_x), Action::Pick(_c))) => true,
            (13, Command(Team::Red(_x), Action::Ban(_c))) => true,
            (14, Command(Team::Blue(_x), Action::Ban(_c))) => true,
            (15, Command(Team::Red(_x), Action::Ban(_c))) => true,
            (16, Command(Team::Blue(_x), Action::Ban(_c))) => true,
            (17, Command(Team::Red(_x), Action::Pick(_c))) => true,
            (18, Command(Team::Blue(_x), Action::Pick(_c))) => true,
            (19, Command(Team::Blue(_x), Action::Pick(_c))) => true,
            (20, Command(Team::Red(_x), Action::Pick(_c))) => true,
            (_, _) => false,
        }
    }
}
