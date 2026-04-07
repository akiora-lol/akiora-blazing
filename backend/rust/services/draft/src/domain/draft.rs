use crate::domain::errors::DraftError;
use bitvec::prelude::*;
use chrono::{DateTime, Utc};

use redis_macros::{FromRedisValue, ToRedisArgs};
use serde::{Deserialize, Serialize};
use shared::game::*;
use uuid::Uuid;

const BP: Command = Command(Team::Blue(None), Action::Pick(None));
const BB: Command = Command(Team::Blue(None), Action::Ban(None));
const RP: Command = Command(Team::Red(None), Action::Pick(None));
const RB: Command = Command(Team::Red(None), Action::Ban(None));

const CLASSIC_5_DRAFT: [Command; 20] = [
    BB, RB, BB, RB, BB, RB, BP, RP, RP, BP, BP, RP, RB, BB, RB, BB, RP, BP, BP, RP,
];

#[derive(Serialize, Deserialize, Clone, FromRedisValue, ToRedisArgs)]
pub struct Draft {
    history: Vec<Command>,
    deadline: DateTime<Utc>,
    game_id: Uuid,
    teams: Vec<Uuid>,
    forbidden_champions: BitArray<[u8; 30], Lsb0>,
    settings: LolGameSettings,
    stage: usize,
}

impl Draft {
    pub fn game_id(&self) -> String {
        self.game_id.to_string()
    }
    fn get_command_sl(&self) -> Option<&[Command]> {
        match self.settings.team_size {
            5 => Some(&CLASSIC_5_DRAFT),
            _ => None,
        }
    }

    pub async fn perform_command(
        &mut self,
        command: &Command,
    ) -> Result<(&Self, Option<Command>), DraftError> {
        if !self.valid_command(command) {
            return Err(DraftError::InvalidCommand);
        }

        let (team_blue, team_red) = match &command.0 {
            Team::Blue(Some(id)) => {
                let other_id = self
                    .teams
                    .iter()
                    .find(|&&x| x != *id)
                    .ok_or(DraftError::InvalidCommand)?;
                (Team::Blue(Some(*id)), Team::Red(Some(*other_id)))
            }
            Team::Red(Some(id)) => {
                let other_id = self
                    .teams
                    .iter()
                    .find(|&&x| x != *id)
                    .ok_or(DraftError::InvalidCommand)?;
                (Team::Blue(Some(*other_id)), Team::Red(Some(*id)))
            }
            _ => return Err(DraftError::InvalidCommand),
        };

        self.stage += 1;

        let champ_id = match &command.1 {
            Action::Ban(Some(c)) | Action::Pick(Some(c)) => *c,
            _ => return Err(DraftError::InvalidCommand),
        };

        if let Some(&true) = self.forbidden_champions.get(champ_id).as_deref() {
            return Err(DraftError::InvalidCommand);
        }

        self.forbidden_champions.set(champ_id, true);
        self.history.push(command.clone());

        let coms = self.get_command_sl().ok_or(DraftError::InvalidCommand)?;

        let next_command = if let Some(next_move) = coms.get(self.stage) {
            let team = match &next_move.0 {
                Team::Blue(_) => team_blue.clone(),
                Team::Red(_) => team_red.clone(),
            };

            Some(Command(
                team,
                match &next_move.1 {
                    Action::Pick(_) => Action::Pick(None),
                    Action::Ban(_) => Action::Ban(None),
                },
            ))
        } else {
            None
        };

        Ok((self, next_command))
    }
    fn valid_command(&self, command: &Command) -> bool {
        match self.settings.team_size {
            5 => self.valid_command_5(command),
            _ => false,
        }
    }

    fn valid_command_5(&self, command: &Command) -> bool {
        let vec = self.get_command_sl().unwrap();
        if let Some(c) = vec.get(self.stage + 1) {
            if c == command {
                return true;
            }
        }
        return false;
    }
}
