use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Clone, PartialEq, Eq)]
pub struct DraftCommand(pub Team, pub Action, pub Option<usize>);

#[derive(Serialize, Deserialize, Clone, PartialEq, Eq)]
pub enum Team {
    Red,
    Blue,
}
#[derive(Serialize, Deserialize, Clone, PartialEq, Eq)]
pub enum Action {
    Pick,
    Ban,
}
