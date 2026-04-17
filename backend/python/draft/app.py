import uuid

from faststream import FastStream
from faststream.redis import RedisBroker, StreamSub
from draft_schemas import Command, PrepareDraft, Team
from draft_service import DraftService
from settings import Settings
import msgspec
from dishka.integrations.faststream import FromDishka, setup_dishka
from ioc import container

settings = Settings()
broker = RedisBroker(settings.redis_url)
app = FastStream(broker)
setup_dishka(container=container, app=app, auto_inject=True)


@broker.subscriber(
    stream=StreamSub("my-stream", group="my-group", consumer="consumer-1")
)
async def handle_stream(msg: dict, draft_service: FromDishka[DraftService]):
    print("RECEIVED DATA:")

    print(msg)
    if msg.get("type") == "prepare_draft":
        prepare_draft = PrepareDraft(**msg.get("data"))

        await draft_service.prepare_draft(prepare_draft)
    if msg.get("type") == "draft_action":
        prepare_draft = msgspec.json.decode(msg.get("data"), type=Command)
        await draft_service.perform_command(prepare_draft)


@app.after_startup
async def send_msg():
    dt = {
        "type": "prepare_draft",
        "data": PrepareDraft(
            game_id=uuid.uuid4(),
            forbidden_champions=[],
            teams=[
                Team(id=uuid.uuid4(), type="red"),
                Team(id=uuid.uuid4(), type="blue"),
            ],
            team_size=5,
            seconds_per_action=30,
        ).model_dump(),
    }

    await broker.publish(dt, stream="my-stream")
