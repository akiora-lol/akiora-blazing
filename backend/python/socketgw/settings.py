from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    redis_url: str = "redis://localhost:6379/0"
    redis_ttl: int = 0
    allowed_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:4173",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:4173",
        "http://127.0.0.1:5173",
    ]
    presence_ttl_seconds: int = 30

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}
