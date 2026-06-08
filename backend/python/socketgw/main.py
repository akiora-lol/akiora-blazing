import asyncio
from contextlib import asynccontextmanager, suppress

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from redis.asyncio import Redis

from routes import notification_stream_worker, router
from settings import Settings
from shared.redis import RedisService


settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("SocketGW starting...")
    redis_client = Redis.from_url(
        settings.redis_url,
        encoding="utf-8",
        decode_responses=True,
    )
    app.state.redis_client = redis_client
    app.state.redis = RedisService(redis_client, settings.redis_ttl)
    app.state.notification_worker = asyncio.create_task(notification_stream_worker(app.state.redis))
    try:
        yield
    finally:
        logger.info("SocketGW shutting down...")
        app.state.notification_worker.cancel()
        with suppress(asyncio.CancelledError):
            await app.state.notification_worker
        await redis_client.close()


app = FastAPI(title="Akiora SocketGW", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    from granian import Granian

    Granian(
        "main:app",
        address="0.0.0.0",
        port=8000,
        interface="asgi",
    ).serve()
