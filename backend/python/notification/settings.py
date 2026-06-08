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
    mongo_url: str = "mongodb://localhost:27017"
    mongo_db: str = "akiora-notification"
    stream_name: str = "notification_stream"
    stream_group: str = "notification-group"
    stream_consumer: str = "notification-consumer-1"
    channel_name: str = "notification_channel"
