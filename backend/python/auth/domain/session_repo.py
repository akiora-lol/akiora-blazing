from domain.session import Session
from shared.redis import RedisService
from uuid import UUID
from datetime import datetime, UTC
from loguru import logger


class SessionRepo:
    def __init__(self, redis_service: RedisService):
        self.prefix = "sid:"
        self.redis = redis_service

    async def get(self, id: UUID | str) -> Session | None:
        logger.info(f"Getting session with id: {self.prefix}{id}")
        data = await self.redis.get(f"{self.prefix}{id}", obj_type=Session)
        if data:
            data.last_activity = datetime.now(tz=UTC)
            logger.info(
                f"Updating session last activity: {self.prefix}{id if id else data.id}"
            )
            await self.redis.create(
                key=f"{self.prefix}{id if id else data.id}",
                value=data.model_dump(),
                ttl=int(
                    (
                        data.exipres_at.astimezone(tz=UTC) - datetime.now(tz=UTC)
                    ).total_seconds()
                ),
            )
        return data

    async def create(self, sign: str, data: Session) -> Session:
        data.last_activity = datetime.now(tz=UTC)
        await self.redis.create(
            key=f"{self.prefix}{sign if sign else data.id}",
            value=data.model_dump(),
            ttl=int(
                (
                    data.exipres_at.astimezone(tz=UTC) - datetime.now(tz=UTC)
                ).total_seconds()
            ),
        )
        return data

    async def delete(self, id: UUID) -> None:
        await self.redis.delete(f"{self.prefix}{id}")
