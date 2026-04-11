use crate::domain::{errors::DraftError, rules::CLASSIC_5_DRAFT};
use bitvec::prelude::*;
use chrono::{DateTime, Duration, Utc};

use redis_macros::{FromRedisValue, ToRedisArgs};
use serde::{Deserialize, Serialize};
use shared::game::*;
use uuid::Uuid;

#[derive(Serialize, Deserialize, Clone, FromRedisValue, ToRedisArgs)]
pub struct Draft {
    pub history: Vec<Command>,
    pub deadline: DateTime<Utc>,
    pub game_id: Uuid,
    pub teams: Vec<Uuid>, // 1st is blue 2nd is red
    pub forbidden_champions: BitArray<[u8; 30], Lsb0>,
    pub settings: LolGameSettings,
    pub stage: isize,
    pub seconds_per_action: usize,
    pub allow_redo: bool,
}

impl Draft {
    pub fn new(
        game_id: Uuid,
        teams: Vec<Uuid>,
        settings: LolGameSettings,
        seconds_per_action: usize,
        allow_redo: bool,
        forb_champions: Vec<i32>,
    ) -> Self {
        let history = Vec::new();
        let stage = -1;
        let deadline = Utc::now() + Duration::hours(48);
        let mut forbidden_champions = bitarr![u8, Lsb0; 0; 240];
        forb_champions
            .iter()
            .filter(|&&id| id >= 0 && id < 240)
            .for_each(|&id| {
                forbidden_champions.set(id as usize, true);
            });
        Self {
            game_id,
            allow_redo,
            teams,
            settings,
            seconds_per_action,
            history,
            stage,
            deadline,
            forbidden_champions,
        }
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

        let mut new_forbidden = self.forbidden_champions.clone();
        new_forbidden.set(champ_id, true);
        let mut new_history = self.history.clone();
        new_history.push(command.clone());

        let coms = self.get_command_sl().ok_or(DraftError::InvalidCommand)?;

        let next_command = if let Some(next_move) = coms.get(self.stage as usize) {
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
        if let Some(c) = vec.get(self.stage as usize + 1) {
            if c == command {
                return true;
            }
        }
        return false;
    }
}
