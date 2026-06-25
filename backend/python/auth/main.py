from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from routes import router
from dishka.integrations.fastapi import setup_dishka
from ioc import container
from settings import settings
from shared.logging import setup_logging
from shared.metrics import setup_fastapi_metrics
from loguru import logger
import time

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):

    yield


app = FastAPI(lifespan=lifespan)

setup_fastapi_metrics(app, service_name="auth")

_default_origins = [
    "http://185.88.101.251",
    "http://185.88.101.251:3000",
    "http://185.88.101.251:8000",
    "http://185.88.101.251:8001",
    "http://localhost:3000",
    "http://front:3000",
    "http://localhost:4173",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:4173",
    "http://127.0.0.1:5173",
]
_extra = (
    [o.strip() for o in (settings.allowed_origins or "").split(",") if o.strip()]
    if getattr(settings, "allowed_origins", None)
    else []
)
origins = _default_origins + _extra


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


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return "alive"


app.include_router(router)


setup_dishka(container=container, app=app)

if __name__ == "__main__":
    from granian import Granian

    Granian(
        "main:app",
        address="0.0.0.0",
        port=8000,
        interface="asgi",
    ).serve()
