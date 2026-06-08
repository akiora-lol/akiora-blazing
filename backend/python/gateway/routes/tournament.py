from fastapi import APIRouter, HTTPException, status, Query
from uuid import UUID
from typing import Optional, List
import grpc
from loguru import logger

from shared.contracts.tournament import (
    AddParticipantToWaitListRequest,
    CreateTournamentRequest,
    DeleteTournamentRequest,
    FinishTournamentRequest,
    GetBracketRequest,
    GetBracketResponse,
    GetParticipantsRequest,
    GetParticipantsResponse,
    GetTournamentRequest,
    GetTournamentStatsRequest,
    GetWaitlistRequest,
    GetWaitlistResponse,
    IsParticipantRequest,
    IsParticipantResponse,
    ListTournamentsRequest,
    ListTournamentsResponse,
    LockRegistrationRequest,
    PaginationRequest,
    PreBuildBracketRequest,
    RemoveFromWaitListRequest,
    StartTournamentRequest,
    RescheduleTournamentRequest,
    TournamentFilter,
    TournamentStatsResponse,
    UpdateParticipantRequest,
    UpdateBracketMatchRequest,
    UpdateDraftPickOrderRequest,
    UpdateTournamentRequest,
    ChangeBracketRequest,
    AddParticipantRequest,
    AddTeamParticipantRequest,
    DraftPickPlayerRequest,
    RemoveParticipantRequest,
    SetDraftCaptainsRequest,
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


@router.get(path="/search", response_model=ListTournamentsResponse)
async def list_tournaments(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=100),
    game_type: Optional[GameType] = None,
    host_id: Optional[UUID] = None,
    is_participant: bool = False,
    min_start_time: Optional[int] = None,
    max_start_time: Optional[int] = None,
    is_open: bool = False,
):
    try:
        return await _get_stub().list_tournaments(
            ListTournamentsRequest(
                filter=TournamentFilter(
                    game_type=game_type,
                    host_id=host_id,
                    is_participant=is_participant,
                    min_start_time=min_start_time,
                    max_start_time=max_start_time,
                    is_open=is_open,
                ),
                pagination=PaginationRequest(page=page, page_size=page_size),
            )
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in list_tournaments: {} {}", e.code(), e.details())
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


@router.patch(path="/{tournament_id}", response_model=TournamentResponse)
async def update_tournament(tournament_id: str, request: UpdateTournamentRequest):
    if str(request.tournament_id) != tournament_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tournament ID in path does not match request body",
        )
    try:
        return await _get_stub().update_tournament(request)
    except grpc.RpcError as e:
        logger.warning("gRPC error in update_tournament({}): {} {}", tournament_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.delete(path="/{tournament_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tournament(tournament_id: str, actor_id: UUID):
    try:
        await _get_stub().delete_tournament(
            DeleteTournamentRequest(tournament_id=tournament_id, actor_id=actor_id)
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in delete_tournament({}): {} {}", tournament_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.post(path="/{tournament_id}/start", response_model=TournamentResponse)
async def start_tournament(tournament_id: str, actor_id: Optional[UUID] = None):
    try:
        return await _get_stub().start_tournament(
            StartTournamentRequest(tournament_id=tournament_id, actor_id=actor_id)
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in start_tournament({}): {} {}", tournament_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.post(path="/{tournament_id}/lock-registration", response_model=TournamentResponse)
async def lock_registration(tournament_id: str, request: LockRegistrationRequest):
    if str(request.tournament_id) != tournament_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tournament ID in path does not match request body")
    try:
        return await _get_stub().lock_registration(request)
    except grpc.RpcError as e:
        logger.warning("gRPC error in lock_registration({}): {} {}", tournament_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.post(path="/{tournament_id}/reschedule", response_model=TournamentResponse)
async def reschedule_tournament(tournament_id: str, request: RescheduleTournamentRequest):
    if str(request.tournament_id) != tournament_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tournament ID in path does not match request body")
    try:
        return await _get_stub().reschedule_tournament(request)
    except grpc.RpcError as e:
        logger.warning("gRPC error in reschedule_tournament({}): {} {}", tournament_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.post(path="/{tournament_id}/prebuild-bracket", response_model=TournamentResponse)
async def prebuild_bracket(tournament_id: str, request: PreBuildBracketRequest):
    if str(request.tournament_id) != tournament_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tournament ID in path does not match request body")
    try:
        return await _get_stub().prebuild_bracket(request)
    except grpc.RpcError as e:
        logger.warning("gRPC error in prebuild_bracket({}): {} {}", tournament_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.post(path="/{tournament_id}/draft/captains", response_model=TournamentResponse)
async def set_draft_captains(tournament_id: str, request: SetDraftCaptainsRequest):
    if str(request.tournament_id) != tournament_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tournament ID in path does not match request body")
    try:
        return await _get_stub().set_draft_captains(request)
    except grpc.RpcError as e:
        logger.warning("gRPC error in set_draft_captains({}): {} {}", tournament_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.post(path="/{tournament_id}/draft/pick-order", response_model=TournamentResponse)
async def update_draft_pick_order(tournament_id: str, request: UpdateDraftPickOrderRequest):
    if str(request.tournament_id) != tournament_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tournament ID in path does not match request body")
    try:
        return await _get_stub().update_draft_pick_order(request)
    except grpc.RpcError as e:
        logger.warning("gRPC error in update_draft_pick_order({}): {} {}", tournament_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.post(path="/{tournament_id}/draft/picks", response_model=TournamentResponse)
async def draft_pick_player(tournament_id: str, request: DraftPickPlayerRequest):
    if str(request.tournament_id) != tournament_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tournament ID in path does not match request body")
    try:
        return await _get_stub().draft_pick_player(request)
    except grpc.RpcError as e:
        logger.warning("gRPC error in draft_pick_player({}): {} {}", tournament_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.post(path="/{tournament_id}/finish", response_model=TournamentResponse)
async def finish_tournament(
    tournament_id: str,
    actor_id: Optional[UUID] = None,
    winner_id: Optional[str] = None,
):
    try:
        return await _get_stub().finish_tournament(
            FinishTournamentRequest(
                tournament_id=tournament_id,
                actor_id=actor_id,
                winner_id=winner_id,
            )
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in finish_tournament({}): {} {}", tournament_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.post(path="/{tournament_id}/participants", response_model=TournamentResponse)
async def add_participant(tournament_id: str, request: AddParticipantRequest):
    if str(request.tournament_id) != tournament_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tournament ID in path does not match request body",
        )
    try:
        return await _get_stub().add_participant(request)
    except grpc.RpcError as e:
        logger.warning("gRPC error in add_participant({}): {} {}", tournament_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="/{tournament_id}/participants", response_model=GetParticipantsResponse)
async def get_participants(
    tournament_id: str,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=100),
):
    try:
        return await _get_stub().get_participants(
            GetParticipantsRequest(
                tournament_id=tournament_id,
                pagination=PaginationRequest(page=page, page_size=page_size),
            )
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in get_participants({}): {} {}", tournament_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.post(path="/{tournament_id}/teams", response_model=TournamentResponse)
async def add_team(tournament_id: str, request: AddTeamParticipantRequest):
    if str(request.tournament_id) != tournament_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tournament ID in path does not match request body",
        )
    try:
        return await _get_stub().add_team(request)
    except grpc.RpcError as e:
        logger.warning("gRPC error in add_team({}): {} {}", tournament_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.post(path="/{tournament_id}/waitlist", response_model=TournamentResponse)
async def add_to_waitlist(tournament_id: str, request: AddParticipantToWaitListRequest):
    if str(request.tournament_id) != tournament_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tournament ID in path does not match request body",
        )
    try:
        return await _get_stub().add_to_waitlist(request)
    except grpc.RpcError as e:
        logger.warning("gRPC error in add_to_waitlist({}): {} {}", tournament_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="/{tournament_id}/waitlist", response_model=GetWaitlistResponse)
async def get_waitlist(
    tournament_id: str,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=100),
):
    try:
        return await _get_stub().get_waitlist(
            GetWaitlistRequest(
                tournament_id=tournament_id,
                pagination=PaginationRequest(page=page, page_size=page_size),
            )
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in get_waitlist({}): {} {}", tournament_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.delete(path="/{tournament_id}/waitlist/{participant_id}", response_model=TournamentResponse)
async def remove_from_waitlist(tournament_id: str, participant_id: str):
    try:
        return await _get_stub().remove_from_waitlist(
            RemoveFromWaitListRequest(
                tournament_id=tournament_id,
                participant_id=participant_id,
            )
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in remove_from_waitlist({}, {}): {} {}", tournament_id, participant_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.post(path="/{tournament_id}/bracket/swap", response_model=TournamentResponse)
async def change_bracket(tournament_id: str, request: ChangeBracketRequest):
    if str(request.tournament_id) != tournament_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tournament ID in path does not match request body",
        )
    try:
        return await _get_stub().change_bracket(request)
    except grpc.RpcError as e:
        logger.warning("gRPC error in change_bracket({}): {} {}", tournament_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.patch(path="/{tournament_id}/bracket/matches/{game_series_id}", response_model=TournamentResponse)
async def update_bracket_match(tournament_id: str, game_series_id: str, request: UpdateBracketMatchRequest):
    if str(request.tournament_id) != tournament_id or request.game_series_id != game_series_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="IDs in path do not match request body")
    try:
        return await _get_stub().update_bracket_match(request)
    except grpc.RpcError as e:
        logger.warning("gRPC error in update_bracket_match({}, {}): {} {}", tournament_id, game_series_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="/{tournament_id}/bracket", response_model=GetBracketResponse)
async def get_bracket(tournament_id: str):
    try:
        return await _get_stub().get_bracket(GetBracketRequest(tournament_id=tournament_id))
    except grpc.RpcError as e:
        logger.warning("gRPC error in get_bracket({}): {} {}", tournament_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.delete(path="/{tournament_id}/participants/{participant_id}", response_model=TournamentResponse)
async def remove_participant(
    tournament_id: str,
    participant_id: str,
    actor_id: Optional[UUID] = None,
):
    try:
        return await _get_stub().remove_participant(
            RemoveParticipantRequest(
                tournament_id=tournament_id,
                participant_id=participant_id,
                actor_id=actor_id,
            )
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in remove_participant({}, {}): {} {}", tournament_id, participant_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.patch(path="/{tournament_id}/participants/{participant_id}", response_model=TournamentResponse)
async def update_participant(
    tournament_id: str,
    participant_id: str,
    request: UpdateParticipantRequest,
):
    if str(request.tournament_id) != tournament_id or request.participant_id != participant_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="IDs in path do not match request body",
        )
    try:
        return await _get_stub().update_participant(request)
    except grpc.RpcError as e:
        logger.warning("gRPC error in update_participant({}, {}): {} {}", tournament_id, participant_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="/{tournament_id}/participants/{participant_id}", response_model=IsParticipantResponse)
async def is_participant(tournament_id: str, participant_id: str):
    try:
        return await _get_stub().is_participant(
            IsParticipantRequest(
                tournament_id=tournament_id,
                participant_id=participant_id,
            )
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in is_participant({}, {}): {} {}", tournament_id, participant_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="/{tournament_id}/stats", response_model=TournamentStatsResponse)
async def get_tournament_stats(tournament_id: str):
    try:
        return await _get_stub().get_tournament_stats(
            GetTournamentStatsRequest(tournament_id=tournament_id)
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in get_tournament_stats({}): {} {}", tournament_id, e.code(), e.details())
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
