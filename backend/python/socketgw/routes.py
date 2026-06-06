from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from loguru import logger
from shared.redis import RedisService

from session import require_session


router = APIRouter()


async def _auth(websocket: WebSocket):
    redis: RedisService = websocket.app.state.redis
    auth = await require_session(websocket, redis)
    if not auth:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Unauthorized")
        return None
    return auth


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
    _, session = auth
    await websocket.accept()
    await websocket.send_json(
        {
            "type": "notification.stub",
            "message": "Notifications socket connected",
            "email": session.email,
        }
    )
    await websocket.close()
