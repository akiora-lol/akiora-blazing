from fastapi import APIRouter, HTTPException, status
from uuid import UUID
import grpc

from shared.contracts.gameseries import ToggleReadyRequest
from stubs.gameseries_stub import GameSeriesStub
from dependencies import get_game_channel

router = APIRouter(prefix="/v1/game-series", tags=["game-series"])


def _get_stub() -> GameSeriesStub:
    return GameSeriesStub(get_game_channel())


@router.post(path="/{series_id}/ready", status_code=status.HTTP_204_NO_CONTENT)
async def toggle_ready(series_id: UUID, request: ToggleReadyRequest):
    if request.series_id != series_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Series ID in path does not match request body",
        )
    try:
        await _get_stub().toggle_ready(request)
    except grpc.RpcError as e:
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.post(path="/{series_id}/draft/action", status_code=status.HTTP_204_NO_CONTENT)
async def draft_action(series_id: UUID):
    # TODO: implement draft_action in stub
    raise HTTPException(status_code=501, detail="Not implemented")


def _grpc_to_http(code: grpc.StatusCode) -> int:
    mapping = {
        grpc.StatusCode.OK: 200,
        grpc.StatusCode.NOT_FOUND: 404,
        grpc.StatusCode.ALREADY_EXISTS: 409,
        grpc.StatusCode.PERMISSION_DENIED: 403,
        grpc.StatusCode.UNAUTHENTICATED: 401,
        grpc.StatusCode.INVALID_ARGUMENT: 400,
        grpc.StatusCode.UNAVAILABLE: 503,
    }
    return mapping.get(code, 500)
