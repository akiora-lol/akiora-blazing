from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Service addresses
    community_service_address: str = Field(default="localhost:50051")
    messenger_service_address: str = Field(default="localhost:50052")
    game_service_address: str = Field(default="localhost:50053")

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}
