use std::time::Duration;

use crate::domain::draft_service::DraftService;
use anyhow::Result;
use chrono::Utc;
use redis::{
    AsyncCommands, FromRedisValue,
    aio::ConnectionManager,
    streams::{StreamId, StreamReadOptions, StreamReadReply},
};
use shared::Publisher;
use shared::contracts::draft::events::{
    DraftAction, DraftEnded, DraftNextCommand, Event, PrepareDraft, RedoAction,
};
use shared::game::{Action, Command, LolGameSettings, Team};
use tokio::time::sleep;
use uuid::Uuid;

pub struct Consumer {
    con: ConnectionManager,
    opts: StreamReadOptions,
    draft_service: DraftService,
    publisher: Publisher,
}
impl Consumer {
    pub fn new(con: ConnectionManager, opts: StreamReadOptions) -> Self {
        let draft_service = DraftService::new(con.clone());
        let publisher = Publisher::new(con.clone());
        Self {
            con,
            opts,
            draft_service,
            publisher,
        }
    }
    pub async fn consume(&mut self) -> Result<()> {
        loop {
            let reply: StreamReadReply = self
                .con
                .xread_options(&["draft"], &[">"], &self.opts)
                .await?;

            for key in &reply.keys {
                for entry in &key.ids {
                    println!("b4 handle");
                    let _ = self.handle(entry).await.map_err(|e| dbg!(e));
                    println!("after handle");

                    let _: () = self
                        .con
                        .xack("draft", "draft-workers", &[entry.id.as_str()])
                        .await?;
                }
            }
        }
    }

    async fn handle(&mut self, entry: &StreamId) -> Result<()> {
        let raw_event = entry.map.get("data").unwrap();
        let event: Event = Event::from_redis_value(raw_event.clone())?;

        match event {
            Event::Draft(data) => {
                println!(
                    "Draft: game_id={}, command={:?}",
                    data.game_id, data.command
                );
                self.handle_draft_action(&data).await?
            }
            Event::Redo(data) => {
                println!("Redo: game_id={}, team={:?}", data.game_id, data.team);
                self.handle_redo(&data).await?
            }
            Event::PrepareDraft(data) => self.handle_draft_prepare(&data).await?,
        }

        Ok(())
    }

    async fn handle_draft_action(&mut self, da: &DraftAction) -> Result<()> {
        let command = self
            .draft_service
            .command(&da.command, da.game_id.to_string().as_str())
            .await;
        if let Ok(com) = command {
            match com {
                Some(next_com) => {
                    self.publisher
                        .pub_sub_publish(
                            "notification",
                            &DraftNextCommand {
                                game_id: da.game_id,
                                command: next_com,
                            },
                        )
                        .await?;
                }
                None => {
                    self.publisher
                        .pub_sub_publish(
                            "notification",
                            &DraftEnded {
                                game_id: da.game_id,
                            },
                        )
                        .await?;
                }
            }
        } else {
            println!("Bad action");
        }

        Ok(())
    }
    async fn handle_redo(&mut self, ra: &RedoAction) -> Result<()> {
        Ok(())
    }
    async fn handle_draft_prepare(&mut self, pd: &PrepareDraft) -> Result<()> {
        self.draft_service.prepare_draft(pd).await?;
        Ok(())
    }
    async fn handle_draft_action_with_abort_simple(&mut self, da: &DraftAction) -> Result<()> {
        let game_id = da.game_id;
        let command = da.command.clone();

        let draft = self
            .draft_service
            .load_draft(game_id.to_string().as_str())
            .await?;
        let deadline = draft.deadline;
        let now = Utc::now();
        let time_to_deadline = if deadline > now {
            (deadline - now).num_seconds().max(1) as u64
        } else {
            1
        };

        let (cancel_tx, mut cancel_rx) = tokio::sync::mpsc::channel(1);

        let mut publisher_clone = self.publisher.clone();
        let mut draft_service_clone = self.draft_service;

        let process_handle = tokio::spawn(async move {
            tokio::select! {
                result = async {
                    let command_result = draft_service_clone
                        .command(&command, &game_id.to_string())
                        .await;

                    if let Ok(com) = command_result {
                        match com {
                            Some(next_com) => {
                                publisher_clone
                                    .pub_sub_publish(
                                        "notification",
                                        &DraftNextCommand {
                                            game_id,
                                            command: next_com,
                                        },
                                    )
                                    .await?;
                            }
                            None => {
                                publisher_clone
                                    .pub_sub_publish(
                                        "notification",
                                        &DraftEnded { game_id },
                                    )
                                    .await?;
                            }
                        }
                    } else {
                        println!("Bad action for game_id: {}", game_id);
                    }
                    Ok::<_, anyhow::Error>(())
                } => result,
                _ = cancel_rx.recv() => {
                    println!("Process cancelled for game_id: {}", game_id);
                    Ok(())
                }
            }
        });
        process_handle.await?;

        let timeout_handle = tokio::spawn(async move {
            sleep(Duration::from_secs(time_to_deadline)).await;
            println!(
                "⏰ Deadline reached for game_id: {}, generating random action",
                game_id
            );

            let _ = cancel_tx.send(()).await;

            // Ждем немного, чтобы основная задача успела отреагировать
            sleep(Duration::from_millis(100)).await;

            // Принудительно абортируем, если основная задача еще висит
            process_handle.abort();

            // Генерируем и отправляем случайное действие
            if let Ok(random_command) = draft_service_clone
                .generate_random_command(&game_id.to_string())
                .await
            {
                let _ = publisher_clone
                    .pub_sub_publish(
                        "notification",
                        &DraftAction {
                            game_id,
                            command: random_command,
                        },
                    )
                    .await;
            }
        });

        timeout_handle.await?;
        Ok(())
    }
}
