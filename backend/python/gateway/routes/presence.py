from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel, Field
from dishka.integrations.fastapi import DishkaRoute, FromDishka

from shared.redis import RedisService


router = APIRouter(tags=["presence"], route_class=DishkaRoute)

PRESENCE_KEY_PREFIX = "presence:user:"
MAX_BATCH = 500


class PresenceCheckRequest(BaseModel):
    user_ids: list[UUID] = Field(default_factory=list)


class PresenceCheckResponse(BaseModel):
    online: dict[str, bool]


def _key(user_id: str) -> str:
    return f"{PRESENCE_KEY_PREFIX}{user_id}"


@router.post("/v1/presence/check", response_model=PresenceCheckResponse)
async def check_presence(
    request: PresenceCheckRequest,
    redis: FromDishka[RedisService],
):
    ids = [str(uid) for uid in request.user_ids[:MAX_BATCH]]
    if not ids:
        return PresenceCheckResponse(online={})
    values = await redis.redis.mget(*[_key(uid) for uid in ids])
    return PresenceCheckResponse(
        online={uid: bool(value) for uid, value in zip(ids, values)}
    )
