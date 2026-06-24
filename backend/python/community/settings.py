from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="ignore",
        env_file=".env",
    )

    mongo_url: str = "mongodb://localhost:27017/?replicaSet=rs0"
    mongo_db: str = "community_db"

    env_type: str = "IGNORE"

    grpc_port: int = 50051

    # How often (in seconds) the background LolRefresher re-queries OP.GG
    # for every user's verified league accounts. Default: 30 minutes.
    lol_refresh_interval_seconds: int = 30 * 60


settings = Settings()
