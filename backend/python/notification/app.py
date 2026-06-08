from faststream import FastStream
from faststream.redis import RedisBroker, StreamSub
from dishka.integrations.faststream import FromDishka, setup_dishka
from loguru import logger

from ioc import container
from notification_service import NotificationService
from settings import Settings


settings = Settings()
broker = RedisBroker(settings.redis_url)
app = FastStream(broker)

setup_dishka(container=container, app=app, auto_inject=True)


@broker.subscriber(
    stream=StreamSub(
        settings.stream_name,
        group=settings.stream_group,
        consumer=settings.stream_consumer,
    )
)
async def handle_notification_stream(
    msg: dict,
    notification_service: FromDishka[NotificationService],
):
    logger.debug("Received notification event: {}", msg)
    notification = await notification_service.handle_event(msg)
    if notification:
        logger.info(
            "Notification processed id={} type={} status={}",
            notification.id,
            notification.type,
            notification.status,
        )
        return
    logger.warning("Notification event ignored: {}", msg)
