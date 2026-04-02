use thiserror::Error;

#[derive(Error, Debug)]
pub enum DraftError {
    #[error("Invalid command")]
    InvalidCommand,
    #[error("Draft for game_id {game_id:?} not found")]
    NotFound { game_id: String },
}
