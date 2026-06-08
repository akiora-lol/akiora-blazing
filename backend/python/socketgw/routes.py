import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from loguru import logger
from shared.redis import RedisService

from session import require_session


router = APIRouter()
NOTIFICATION_STREAM = "notification_stream"


class NotificationConnectionManager:
    def __init__(self):
        self._connections: dict[str, dict[str, WebSocket]] = {}
        self._lock = asyncio.Lock()

    async def connect(self, user_id: str, connection_id: str, websocket: WebSocket):
        async with self._lock:
            self._connections.setdefault(user_id, {})[connection_id] = websocket

    async def disconnect(self, user_id: str, connection_id: str):
        async with self._lock:
            sessions = self._connections.get(user_id)
            if not sessions:
                return
            sessions.pop(connection_id, None)
            if not sessions:
                self._connections.pop(user_id, None)

    async def send_to_user(self, user_id: str, payload: dict):
        async with self._lock:
            sessions = dict(self._connections.get(user_id, {}))

        stale_connection_ids: list[str] = []
        for connection_id, websocket in sessions.items():
            try:
                await websocket.send_json(payload)
            except Exception as e:
                logger.debug("Dropping stale notification websocket user_id={} connection={}: {}", user_id, connection_id, e)
                stale_connection_ids.append(connection_id)

        for connection_id in stale_connection_ids:
            await self.disconnect(user_id, connection_id)

    async def dispatch(self, payload: dict):
        user_ids = _event_user_ids(payload)
        if not user_ids:
            return

        for user_id in user_ids:
            await self.send_to_user(user_id, payload)


notification_connections = NotificationConnectionManager()


async def _auth(websocket: WebSocket):
    redis: RedisService = websocket.app.state.redis
    auth = await require_session(websocket, redis)
    if not auth:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Unauthorized")
        return None
    return auth


def _session_user_id(session) -> str | None:
    user = session.custom_data.get("user")
    if isinstance(user, dict):
        value = user.get("id")
    else:
        value = getattr(user, "id", None)
    if value is None:
        value = session.custom_data.get("user_id")
    return str(value) if value else None


def _event_user_ids(event: dict) -> set[str]:
    event_user_id = event.get("user_id")
    if event_user_id:
        return {str(event_user_id)}

    user_ids = event.get("user_ids")
    if isinstance(user_ids, list):
        return {str(value) for value in user_ids}

    return set()


async def notification_stream_worker(redis: RedisService):
    last_id = "$"
    logger.info("Notification stream worker started stream={}", NOTIFICATION_STREAM)
    while True:
        try:
            messages = await redis.read_stream(NOTIFICATION_STREAM, last_id=last_id)
            for message_id, event in messages:
                last_id = message_id
                await notification_connections.dispatch({"event_id": message_id, **event})
        except asyncio.CancelledError:
            raise
        except Exception as e:
            logger.warning("Notification stream worker failed: {}", e)
            await asyncio.sleep(2)


@router.websocket("/ws/v1/ping")
async def ping(websocket: WebSocket):
    auth = await _auth(websocket)
    if not auth:
        return
    _, session = auth
    await websocket.accept()
    await websocket.send_json(
        {
            "type": "pong",
            "email": session.email,
            "user": session.custom_data.get("user"),
        }
    )
    await websocket.close()


@router.websocket("/ws/v1/echo")
async def echo(websocket: WebSocket):
    auth = await _auth(websocket)
    if not auth:
        return
    sid, session = auth
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_text()
            await websocket.send_json(
                {
                    "type": "echo",
                    "sid": sid,
                    "email": session.email,
                    "message": message,
                }
            )
    except WebSocketDisconnect:
        logger.debug("Echo websocket disconnected email={}", session.email)


@router.websocket("/ws/v1/notifications")
async def notifications(websocket: WebSocket):
    auth = await _auth(websocket)
    if not auth:
        return
    sid, session = auth
    user_id = _session_user_id(session)
    if not user_id:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="User is not attached to session")
        return

    connection_id = f"{sid}:{id(websocket)}"
    await websocket.accept()
    await notification_connections.connect(user_id, connection_id, websocket)
    await websocket.send_json({"type": "notification.connected", "user_id": user_id})
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        logger.debug("Notifications websocket disconnected email={}", session.email)
    except Exception as e:
        logger.warning("Notifications websocket failed email={}: {}", session.email, e)
    finally:
        await notification_connections.disconnect(user_id, connection_id)
