from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="ignore",
        env_file=".env",
    )

    redis_url: str = "redis://localhost:6379/0"
    redis_ttl: int = 0

    env_type: str = "IGNORE"


settings = Settings()
