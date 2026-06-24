from fastapi import APIRouter, HTTPException, status
from uuid import UUID
import grpc
from loguru import logger

from shared.contracts.gameseries import (
    DraftActionRequest,
    ToggleReadyRequest,
    SetGameWinnerRequest,
    GetSeriesResponse,
)
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
        logger.warning("gRPC error in toggle_ready({}): {} {}", series_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.post(path="/{series_id}/draft/action", status_code=status.HTTP_204_NO_CONTENT)
async def draft_action(series_id: UUID, request: DraftActionRequest):
    if request.series_id != series_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Series ID in path does not match request body",
        )
    try:
        await _get_stub().draft_action(request)
    except grpc.RpcError as e:
        logger.warning("gRPC error in draft_action({}): {} {}", series_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(
    path="/{series_id}",
    response_model=GetSeriesResponse,
)
async def get_series(series_id: UUID):
    try:
        return await _get_stub().get_series(series_id)
    except grpc.RpcError as e:
        logger.warning(
            "gRPC error in get_series({}): {} {}", series_id, e.code(), e.details()
        )
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.post(
    path="/{series_id}/games/{game_id}/winner",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def set_game_winner(series_id: UUID, game_id: UUID, request: SetGameWinnerRequest):
    if request.series_id != series_id or request.game_id != game_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Series/Game ID in path does not match request body",
        )
    try:
        await _get_stub().set_game_winner(request)
    except grpc.RpcError as e:
        logger.warning(
            "gRPC error in set_game_winner({}/{}): {} {}",
            series_id,
            game_id,
            e.code(),
            e.details(),
        )
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


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
