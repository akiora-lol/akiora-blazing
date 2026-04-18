from domain.session import Session
from shared.redis import RedisService
from uuid import UUID
from datetime import datetime, UTC


class SessionRepo:
    def __init__(self, redis_service: RedisService):
        self.prefix = "sid:"
        self.redis = redis_service

    async def get(self, id: UUID) -> Session | None:
        data = await self.redis.get(f"{self.prefix}{id}", obj_type=Session)
        if data:
            data.last_activity = datetime.now(tz=UTC)
            await self.redis.create(
                prefix=self.prefix,
                key=str(data.id),
                value=data.model_dump(),
                ttl=int(
                    (
                        data.exipres_at.astimezone(tz=UTC) - datetime.now(tz=UTC)
                    ).total_seconds()
                ),
            )
        return data

    async def create(self, data: Session) -> Session:
        data.last_activity = datetime.now(tz=UTC)
        await self.redis.create(
            prefix=self.prefix,
            key=str(data.id),
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
