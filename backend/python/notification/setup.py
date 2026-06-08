from beanie import init_beanie
from pymongo import AsyncMongoClient
from shared.logging import setup_logging

from notification_model import Notification
from settings import Settings


async def setup():
    settings = Settings()
    setup_logging()
    client = AsyncMongoClient(settings.mongo_url)
    await init_beanie(
        database=client[settings.mongo_db],
        document_models=[Notification],
    )
