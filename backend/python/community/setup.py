from shared.logging import setup_logging
from beanie import init_beanie
from domain.entites.user import User
from domain.entites.club import Club
from domain.entites.team import Team
from pymongo import AsyncMongoClient
from settings import settings


async def setup():
    setup_logging()
    client = AsyncMongoClient(settings.mongo_url)
    await init_beanie(
        database=client[settings.mongo_db],
        document_models=[User, Club, Team],
    )
