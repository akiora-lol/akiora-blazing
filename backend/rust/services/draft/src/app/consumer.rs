use crate::{app::publisher::Publisher, domain::draft_service::DraftService};
use anyhow::Result;
use redis::{
    AsyncCommands, FromRedisValue,
    aio::ConnectionManager,
    streams::{StreamId, StreamReadOptions, StreamReadReply},
};
use shared::contracts::draft::events::{
    BadAction, DraftAction, DraftEnded, DraftNextCommand, Event, PrepareDraft, RedoAction,
};
use shared::game::{Action, Command, LolGameSettings, Team};
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
        let event = Event::PrepareDraft(PrepareDraft {
            game_id: Uuid::new_v4(),
            forbidden_champions: vec![1, 2, 3, 4, 5],
            teams: vec![
                Team::Blue(Some(Uuid::new_v4())),
                Team::Red(Some(Uuid::new_v4())),
            ],
            allow_redo: false,
            seconds_per_action: 30,
            settings: LolGameSettings {
                mode: shared::game::LolGameMode::Classic,
                team_size: 5,
                map: 12,
                best_of: 3,
            },
        });
        self.publisher.stream_publish("draft", &event).await?;

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
        dbg!(raw_event.clone());
        let event: Event = Event::from_redis_value(raw_event.clone())?;
        dbg!(event.clone());

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
            self.publisher
                .pub_sub_publish(
                    "notification",
                    &BadAction {
                        game_id: da.game_id,
                    },
                )
                .await?;
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
}
