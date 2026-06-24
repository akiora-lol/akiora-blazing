from contextlib import asynccontextmanager
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from dishka.integrations.fastapi import setup_dishka
from ioc import container
from shared.metrics import setup_fastapi_metrics
from routes.user import router as user_router
from routes.club import router as club_router
from routes.team import router as team_router
from routes.group import router as group_router
from routes.messenger import router as messenger_router
from routes.tournament import router as tournament_router
from routes.gameseries import router as gameseries_router
from routes.search import router as search_router
from routes.presence import router as presence_router
from dependencies import close_all_channels
from settings import Settings

settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Gateway starting...")
    logger.info(f"Community service: {settings.community_service_address}")
    logger.info(f"Messenger service: {settings.messenger_service_address}")
    logger.info(f"Game service: {settings.game_service_address}")
    logger.info(f"Search service: {settings.search_service_address}")
    yield
    logger.info("Gateway shutting down...")
    await close_all_channels()


app = FastAPI(title="Akiora Gateway", lifespan=lifespan)

setup_fastapi_metrics(app, service_name="gateway")


@app.get("/health")
async def health():
    return {"status": "ok"}


_default_origins = [
    "http://localhost:3000",
    "http://localhost:4173",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:4173",
    "http://127.0.0.1:5173",
]
_extra = [o.strip() for o in (settings.allowed_origins or "").split(",") if o.strip()] if getattr(settings, "allowed_origins", None) else []
app.add_middleware(
    CORSMiddleware,
    allow_origins=_default_origins + _extra,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    logger.info(
        "{method} {path} → {status} ({duration:.1f}ms)",
        method=request.method,
        path=request.url.path,
        status=response.status_code,
        duration=duration_ms,
    )
    return response


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
app.include_router(search_router)

# Presence
app.include_router(presence_router)

setup_dishka(container=container, app=app)

if __name__ == "__main__":
    from granian import Granian

    Granian(
        "main:app",
        address="0.0.0.0",
        port=8000,
        interface="asgi",
    ).serve()
