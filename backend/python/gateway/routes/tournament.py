from fastapi import APIRouter, HTTPException, status, Query
from uuid import UUID
from typing import Optional, List
import grpc
from loguru import logger

from shared.contracts.tournament import (
    CreateTournamentRequest,
    GetTournamentRequest,
    ChangeBracketRequest,
    AddParticipantRequest,
    AddTeamParticipantRequest,
    RemoveParticipantRequest,
    TournamentResponse,
    ManyTournamentsResponse,
    GameType,
)
from stubs.tournament_stub import TournamentStub
from dependencies import get_game_channel

router = APIRouter(prefix="/v1/tournaments", tags=["tournaments"])


def _get_stub() -> TournamentStub:
    return TournamentStub(get_game_channel())


@router.post(
    path="",
    response_model=TournamentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_tournament(request: CreateTournamentRequest):
    try:
        return await _get_stub().create_tournament(request)
    except grpc.RpcError as e:
        logger.warning("gRPC error in create_tournament: {} {}", e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="/{tournament_id}", response_model=ManyTournamentsResponse)
async def get_tournament(tournament_id: str):
    try:
        return await _get_stub().get_tournament(GetTournamentRequest(ids=[tournament_id]))
    except grpc.RpcError as e:
        logger.warning("gRPC error in get_tournament({}): {} {}", tournament_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="", response_model=ManyTournamentsResponse)
async def get_tournaments(
    ids: Optional[List[str]] = Query(default=None),
    game_type: Optional[GameType] = None,
):
    try:
        return await _get_stub().get_tournament(
            GetTournamentRequest(ids=ids or [], game_type=game_type)
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in get_tournaments: {} {}", e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.post(path="/{tournament_id}/start", status_code=status.HTTP_204_NO_CONTENT)
async def start_tournament(tournament_id: str):
    # TODO: implement start_tournament in stub
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post(path="/{tournament_id}/prebuild-bracket", status_code=status.HTTP_204_NO_CONTENT)
async def prebuild_bracket(tournament_id: str):
    # TODO: implement prebuild_bracket in stub
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post(path="/{tournament_id}/finish", status_code=status.HTTP_204_NO_CONTENT)
async def finish_tournament(tournament_id: str):
    # TODO: implement finish_tournament in stub
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post(path="/{tournament_id}/participants", status_code=status.HTTP_204_NO_CONTENT)
async def add_participant(tournament_id: str, request: AddParticipantRequest):
    if str(request.tournament_id) != tournament_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tournament ID in path does not match request body",
        )
    # TODO: implement add_participant in stub
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post(path="/{tournament_id}/teams", status_code=status.HTTP_204_NO_CONTENT)
async def add_team(tournament_id: str, request: AddTeamParticipantRequest):
    if str(request.tournament_id) != tournament_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tournament ID in path does not match request body",
        )
    # TODO: implement add_team in stub
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post(path="/{tournament_id}/waitlist", status_code=status.HTTP_204_NO_CONTENT)
async def add_to_waitlist(tournament_id: str, request: AddParticipantRequest):
    if str(request.tournament_id) != tournament_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tournament ID in path does not match request body",
        )
    # TODO: implement add_to_waitlist in stub
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post(path="/{tournament_id}/bracket/swap", status_code=status.HTTP_204_NO_CONTENT)
async def change_bracket(tournament_id: str, request: ChangeBracketRequest):
    if str(request.tournament_id) != tournament_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tournament ID in path does not match request body",
        )
    # TODO: implement change_bracket in stub
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete(path="/{tournament_id}/participants/{participant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_participant(tournament_id: str, participant_id: str):
    # TODO: implement remove_participant in stub
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
