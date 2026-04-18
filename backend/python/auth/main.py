from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.api import router
from dishka.integrations.fastapi import setup_dishka
from ioc import container
from shared.logging import setup_logging

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):

    yield


app = FastAPI(lifespan=lifespan)

origins = ["*"]


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
        "app",
        address="0.0.0.0",
        port=8000,
        interface="asgi",
    ).serve()
