from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Example: GRPC_SERVICES='{"game": "localhost:50051", "community": "localhost:50052"}'
    grpc_services: dict[str, str] = Field(default_factory=dict)

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}
