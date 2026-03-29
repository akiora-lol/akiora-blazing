use bitvec::prelude::*;
use chrono::{DateTime, Utc};

use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Serialize, Deserialize, Clone)]
pub struct Draft {
    history: Vec<Command>,
    deadline: DateTime<Utc>,
    game_id: Uuid,
    forbidden_champions: BitArray<[u8; 30], Lsb0>,
    settings: Settings,
    stage: usize,
}

impl Draft {
    fn perform_command(&mut self, command: &Command) -> bool {
        //should publish next move to redis pubsub for socket
        if self.valid_classic(command) {
            self.stage += 1;
            let cid = match command.1 {
                Action::Ban(c) => c,
                Action::Pick(c) => c,
            };
            self.forbidden_champions.set(cid, true);
            self.history.push(command.clone());

            return true;
        }
        return false;
    }

    fn valid_classic(&self, command: &Command) -> bool {
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

#[derive(Serialize, Deserialize, Clone)]
pub enum Team {
    Red(Uuid),
    Blue(Uuid),
}

#[derive(Serialize, Deserialize, Clone)]
pub enum Action {
    Pick(usize),
    Ban(usize),
}

#[derive(Serialize, Deserialize, Clone)]
pub struct Command(Team, Action);

#[derive(Serialize, Deserialize, Clone)]
pub enum GameType {
    Fearless,
    Classic,
}

#[derive(Serialize, Deserialize, Clone)]
pub struct Settings {
    team_size: usize,
    ban_size: usize,
    game_type: GameType,
}
