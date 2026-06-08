from fastapi import WebSocket
from shared.contracts.auth import Session
from shared.redis import RedisService


def get_sid(websocket: WebSocket) -> str | None:
    return websocket.cookies.get("sid") or websocket.query_params.get("sid")


async def get_session_by_sid(redis: RedisService, sid: str) -> Session | None:
    try:
        return await redis.get(f"sid:{sid}", obj_type=Session)
    except Exception:
        return None


async def require_session(websocket: WebSocket, redis: RedisService) -> tuple[str, Session] | None:
    sid = get_sid(websocket)
    if not sid:
        return None
    session = await get_session_by_sid(redis, sid)
    if not session:
        return None
    return sid, session
