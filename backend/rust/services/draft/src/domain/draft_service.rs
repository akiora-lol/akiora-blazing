use crate::domain::{draft::Draft, errors::DraftError};
use shared::contracts::draft::events::PrepareDraft;

use chrono::{DateTime, Duration, Utc};
use redis::aio::ConnectionManager;
use redis::{AsyncCommands, Value};

use shared::game::{Command, Team};
use uuid::Uuid;
pub struct DraftService {
    redis: ConnectionManager,
}

impl DraftService {
    pub fn new(r: ConnectionManager) -> Self {
        Self { redis: r.clone() }
    }

    pub async fn load_draft(&mut self, game_id: &str) -> Result<Draft, DraftError> {
        let d: Option<Draft> = self.redis.get(game_id).await.unwrap_or(None);
        d.ok_or(DraftError::NotFound {
            game_id: game_id.to_string(),
        })
    }

    pub async fn prepare_draft(&mut self, pd: &PrepareDraft) -> Result<Draft, DraftError> {
        let mut team_uuids = Vec::with_capacity(2);

        for team in &pd.teams {
            match team {
                Team::Blue(Some(uuid)) => team_uuids.push(*uuid),
                Team::Red(Some(uuid)) => team_uuids.push(*uuid),
                _ => {
                    return Err(DraftError::InvalidCommand);
                }
            }
        }
        if team_uuids.len() != 2 {
            return Err(DraftError::InvalidCommand);
        }

        let dr = Draft::new(
            pd.game_id,
            team_uuids, // теперь Vec<Uuid>
            pd.settings,
            pd.seconds_per_action as usize,
            pd.allow_redo,
            pd.forbidden_champions.clone(),
        );
        let d = self.save_draft(&dr).await;
        dbg!(&d);
        let d = d?;
        Ok(dr)
    }

    pub async fn save_draft(&mut self, draft: &Draft) -> Result<(), DraftError> {
        let _: Value = self
            .redis
            .set_ex(
                format!("draft-{}", draft.game_id.to_string()),
                draft,
                60 * 60 * 48,
            )
            .await
            .map_err(|e| {
                dbg!(e);
                DraftError::SaveError
            })
            .unwrap();
        Ok(())
    }

    pub async fn command(
        &mut self,
        command: &Command,
        game_id: &str,
    ) -> Result<Option<Command>, DraftError> {
        let mut draft = self.load_draft(game_id).await?;
        let new_draft_state = draft.perform_command(command).await?;
        let res = self.save_draft(new_draft_state.0).await?;

        Ok(new_draft_state.1)
    }
    
    pub async fn generate_next_command(
        &mut self,
        command: &Command,
        game_id: &str,
    ) -> Result<Option<Command>, DraftError> {
        let mut draft = self.load_draft(game_id).await?;
        let new_draft_state = draft.perform_command(command).await?;
        let res = self.save_draft(new_draft_state.0).await?;

        Ok(new_draft_state.1)
    }
}
