from contextlib import asynccontextmanager
from fastapi import FastAPI
from loguru import logger

from routes.user import router as user_router
from routes.club import router as club_router
from routes.team import router as team_router
from routes.group import router as group_router
from routes.messenger import router as messenger_router
from routes.tournament import router as tournament_router
from routes.gameseries import router as gameseries_router
from dependencies import close_all_channels
from settings import Settings

settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Gateway starting...")
    logger.info(f"Community service: {settings.community_service_address}")
    logger.info(f"Messenger service: {settings.messenger_service_address}")
    logger.info(f"Game service: {settings.game_service_address}")
    yield
    logger.info("Gateway shutting down...")
    await close_all_channels()


app = FastAPI(title="Akiora Gateway", lifespan=lifespan)

# Community routes
app.include_router(user_router)
app.include_router(club_router)
app.include_router(team_router)
app.include_router(group_router)

# Messenger routes
app.include_router(messenger_router)

# Game routes
app.include_router(tournament_router)
app.include_router(gameseries_router)


if __name__ == "__main__":
    from granian import Granian

    Granian(
        "main:app",
        address="0.0.0.0",
        port=8001,
        interface="asgi",
    ).serve()
