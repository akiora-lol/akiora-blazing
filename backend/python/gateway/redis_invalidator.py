from datetime import datetime, UTC
from shared.contracts.auth import Session
from shared.redis import RedisService


class RedisInvalidator:
    def __init__(self, redis_service: RedisService):
        self.redis = redis_service

    async def invalidate_session(self, session_id: str) -> None:
        await self.redis.delete(f"sid:{session_id}")

    async def update_session_user(self, sign: str, user: dict) -> Session:
        data = await self.redis.get(f"sid:{sign}", obj_type=Session)
        if not data:
            raise ValueError("Session not found for invalidation")
        data.last_activity = datetime.now(tz=UTC)
        data.custom_data["user"] = user
        await self.redis.create(
            key=f"sid:{sign}",
            value=data.model_dump(),
            ttl=int(
                (
                    data.exipres_at.astimezone(tz=UTC) - datetime.now(tz=UTC)
                ).total_seconds()
            ),
        )
        return data
