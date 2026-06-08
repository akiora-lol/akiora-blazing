from shared.logging import setup_logging
from beanie import init_beanie
from domain.entities.chat import Chat
from domain.entities.message import Message

from pymongo import AsyncMongoClient
from settings import settings


async def setup():
    setup_logging()
    client = AsyncMongoClient(settings.mongo_url)
    await init_beanie(
        database=client[settings.mongo_db],
        document_models=[Chat, Message],
    )
