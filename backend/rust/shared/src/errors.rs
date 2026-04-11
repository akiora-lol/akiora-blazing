use thiserror::Error;

#[derive(Error, Debug)]
pub enum PublishError {
    #[error("Failed to parse")]
    ReadError,
    #[error("Failed to write")]
    WriteError,
}
