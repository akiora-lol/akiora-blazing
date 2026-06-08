from fastapi import APIRouter, HTTPException, status, Query
from uuid import UUID
from typing import Optional
import grpc
from loguru import logger

from shared.contracts.team import (
    CheckCapacityRequest,
    CheckCapacityResponse,
    CreateTeamRequest,
    DeleteTeamRequest,
    GetMembersRequest,
    GetTeamRequest,
    IsMemberRequest,
    IsMemberResponse,
    ListTeamsRequest,
    ListTeamsResponse,
    PaginationRequest,
    SearchMembersRequest,
    TeamFilter,
    TeamMembersResponse,
    UpdateTeamRequest,
    AddTeamMemberRequest,
    RemoveTeamMemberRequest,
    TeamResponse,
)
from stubs.team_stub import TeamStub
from dependencies import get_community_channel

router = APIRouter(prefix="/v1/teams", tags=["teams"])


def _get_stub() -> TeamStub:
    return TeamStub(get_community_channel())


@router.post(
    path="",
    response_model=TeamResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_team(request: CreateTeamRequest):
    try:
        return await _get_stub().create_team(request)
    except grpc.RpcError as e:
        logger.warning("gRPC error in create_team: {} {}", e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="", response_model=ListTeamsResponse)
async def list_teams(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=100),
    search: Optional[str] = None,
    owner_id: Optional[UUID] = None,
    is_member: bool = False,
):
    try:
        return await _get_stub().list_teams(
            ListTeamsRequest(
                filter=TeamFilter(
                    search=search,
                    owner_id=owner_id,
                    is_member=is_member,
                ),
                pagination=PaginationRequest(page=page, page_size=page_size),
            )
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in list_teams: {} {}", e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="/{team_id}", response_model=TeamResponse)
async def get_team(team_id: UUID):
    try:
        return await _get_stub().get_team(GetTeamRequest(team_id=team_id))
    except grpc.RpcError as e:
        logger.warning("gRPC error in get_team({}): {} {}", team_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.patch(path="/{team_id}", response_model=TeamResponse)
async def update_team(team_id: UUID, request: UpdateTeamRequest):
    if request.team_id != team_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Team ID in path does not match request body",
        )
    try:
        return await _get_stub().update_team(request)
    except grpc.RpcError as e:
        logger.warning("gRPC error in update_team({}): {} {}", team_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.delete(path="/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(team_id: UUID, actor_id: UUID):
    try:
        await _get_stub().delete_team(DeleteTeamRequest(team_id=team_id, actor_id=actor_id))
    except grpc.RpcError as e:
        logger.warning("gRPC error in delete_team({}): {} {}", team_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.post(path="/{team_id}/members", response_model=TeamResponse)
async def add_member(team_id: UUID, request: AddTeamMemberRequest):
    if request.team_id != team_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Team ID in path does not match request body",
        )
    try:
        return await _get_stub().add_member(request)
    except grpc.RpcError as e:
        logger.warning("gRPC error in add_member(team={}): {} {}", team_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="/{team_id}/members", response_model=TeamMembersResponse)
async def get_members(
    team_id: UUID,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=100),
    search: Optional[str] = None,
):
    try:
        if search:
            return await _get_stub().search_members(
                SearchMembersRequest(
                    team_id=team_id,
                    search=search,
                    pagination=PaginationRequest(page=page, page_size=page_size),
                )
            )
        return await _get_stub().get_members(
            GetMembersRequest(
                team_id=team_id,
                pagination=PaginationRequest(page=page, page_size=page_size),
            )
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in get_members(team={}): {} {}", team_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.delete(path="/{team_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(team_id: UUID, user_id: UUID, actor_id: UUID):
    try:
        await _get_stub().remove_member(
            RemoveTeamMemberRequest(team_id=team_id, actor_id=actor_id, user_id=user_id)
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in remove_member(team={}, user={}): {} {}", team_id, user_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="/{team_id}/members/{user_id}", response_model=IsMemberResponse)
async def is_member(team_id: UUID, user_id: UUID):
    try:
        return await _get_stub().is_member(
            IsMemberRequest(team_id=team_id, user_id=user_id)
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in is_member(team={}, user={}): {} {}", team_id, user_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="/{team_id}/capacity", response_model=CheckCapacityResponse)
async def check_capacity(team_id: UUID):
    try:
        return await _get_stub().check_capacity(CheckCapacityRequest(team_id=team_id))
    except grpc.RpcError as e:
        logger.warning("gRPC error in check_capacity({}): {} {}", team_id, e.code(), e.details())
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
