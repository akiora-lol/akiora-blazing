from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Service addresses
    community_service_address: str = Field(default="localhost:50051")
    messenger_service_address: str = Field(default="localhost:50052")
    game_service_address: str = Field(default="localhost:50053")
    search_service_address: str = Field(default="localhost:50054")
    redis_url: str = "redis://localhost:6379/0"
    redis_ttl: int = 0
    allowed_origins: str = ""  # comma-separated extra CORS origins
    presence_ttl_seconds: int = 30
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}
