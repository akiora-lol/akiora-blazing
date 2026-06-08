use serde_derive::{Deserialize, Serialize};
use std::fs;
use std::path::PathBuf;

#[derive(Debug, thiserror::Error)]
pub enum BackendError {
    #[error("HTTP error: {0}")]
    Http(#[from] reqwest::Error),
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),
    #[error("JSON error: {0}")]
    Json(#[from] serde_json::Error),
}

#[derive(Debug, Serialize)]
struct EmailLoginStartRequest {
    email: String,
}

#[derive(Debug, Deserialize)]
pub struct EmailLoginStartResponse {
    pub verification_id: String,
}

#[derive(Debug, Serialize)]
struct EmailLoginFinishRequest {
    verification_id: String,
    code: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct DesktopSession {
    pub sid: String,
    pub user: serde_json::Value,
}

#[derive(Debug, Deserialize)]
struct EmailLoginFinishResponse {
    sid: String,
    user: serde_json::Value,
}

pub struct BackendClient {
    base_url: String,
    client: reqwest::Client,
}

impl BackendClient {
    pub fn new(base_url: impl Into<String>) -> Self {
        Self {
            base_url: base_url.into().trim_end_matches('/').to_string(),
            client: reqwest::Client::new(),
        }
    }

    pub async fn start_email_login(
        &self,
        email: String,
    ) -> Result<EmailLoginStartResponse, BackendError> {
        let response = self
            .client
            .post(format!("{}/desktop/email/login/start", self.base_url))
            .json(&EmailLoginStartRequest { email })
            .send()
            .await?
            .error_for_status()?;

        Ok(response.json().await?)
    }

    pub async fn finish_email_login(
        &self,
        verification_id: String,
        code: String,
    ) -> Result<DesktopSession, BackendError> {
        let response = self
            .client
            .post(format!("{}/desktop/email/login/finish", self.base_url))
            .json(&EmailLoginFinishRequest {
                verification_id,
                code,
            })
            .send()
            .await?
            .error_for_status()?;

        let auth: EmailLoginFinishResponse = response.json().await?;
        Ok(DesktopSession {
            sid: auth.sid,
            user: auth.user,
        })
    }

    pub fn session_path() -> Result<PathBuf, BackendError> {
        Ok(std::env::current_dir()?.join(".alt-session.json"))
    }

    pub fn save_session(session: &DesktopSession) -> Result<PathBuf, BackendError> {
        let path = Self::session_path()?;
        fs::write(&path, serde_json::to_vec_pretty(session)?)?;
        Ok(path)
    }
}
