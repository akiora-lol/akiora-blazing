from beanie import init_beanie
from pymongo import AsyncMongoClient
from shared.logging import setup_logging

from domain.entities.cold_form import ColdForm
from domain.entities.hot_form import HotForm
from settings import settings


async def setup():
    setup_logging()
    client = AsyncMongoClient(settings.mongo_url)
    await init_beanie(
        database=client[settings.mongo_db],
        document_models=[ColdForm, HotForm],
    )
