from fastapi import APIRouter, HTTPException, status, Query
from uuid import UUID
from typing import Optional
import grpc
from loguru import logger

from shared.contracts.club import (
    ClubFilter,
    ClubMembersResponse,
    CreateClubRequest,
    DeleteClubRequest,
    GetClubRequest,
    GetMemberPermissionsRequest,
    GetMembersRequest,
    IsMemberRequest,
    IsMemberResponse,
    ListClubsRequest,
    ListClubsResponse,
    PaginationRequest,
    SearchMembersRequest,
    UpdateClubRequest,
    AddMemberRequest,
    RemoveMemberRequest,
    SetPermissionRequest,
    ClubResponse,
)
from stubs.club_stub import ClubStub
from dependencies import get_community_channel

router = APIRouter(prefix="/v1/clubs", tags=["clubs"])


def _get_stub() -> ClubStub:
    return ClubStub(get_community_channel())


@router.post(
    path="",
    response_model=ClubResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_club(request: CreateClubRequest):
    try:
        return await _get_stub().create_club(request)
    except grpc.RpcError as e:
        logger.warning("gRPC error in create_club: {} {}", e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="", response_model=ListClubsResponse)
async def list_clubs(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=100),
    search: Optional[str] = None,
    owner_id: Optional[UUID] = None,
    is_member: bool = False,
):
    try:
        return await _get_stub().list_clubs(
            ListClubsRequest(
                filter=ClubFilter(
                    search=search,
                    owner_id=owner_id,
                    is_member=is_member,
                ),
                pagination=PaginationRequest(page=page, page_size=page_size),
            )
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in list_clubs: {} {}", e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="/{club_id}", response_model=ClubResponse)
async def get_club(club_id: UUID):
    try:
        return await _get_stub().get_club(GetClubRequest(club_id=club_id))
    except grpc.RpcError as e:
        logger.warning("gRPC error in get_club({}): {} {}", club_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.patch(path="/{club_id}", response_model=ClubResponse)
async def update_club(club_id: UUID, request: UpdateClubRequest):
    if request.club_id != club_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Club ID in path does not match request body",
        )
    try:
        return await _get_stub().update_club(request)
    except grpc.RpcError as e:
        logger.warning("gRPC error in update_club({}): {} {}", club_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.delete(path="/{club_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_club(club_id: UUID, actor_id: UUID):
    try:
        await _get_stub().delete_club(DeleteClubRequest(club_id=club_id, actor_id=actor_id))
    except grpc.RpcError as e:
        logger.warning("gRPC error in delete_club({}): {} {}", club_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.post(path="/{club_id}/members", response_model=ClubResponse)
async def add_member(club_id: UUID, request: AddMemberRequest):
    if request.club_id != club_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Club ID in path does not match request body",
        )
    try:
        return await _get_stub().add_member(request)
    except grpc.RpcError as e:
        logger.warning("gRPC error in add_member(club={}): {} {}", club_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.delete(path="/{club_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(club_id: UUID, user_id: UUID, actor_id: Optional[UUID] = None):
    try:
        await _get_stub().remove_member(
            RemoveMemberRequest(club_id=club_id, user_id=user_id, actor_id=actor_id)
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in remove_member(club={}, user={}): {} {}", club_id, user_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="/{club_id}/members", response_model=ClubMembersResponse)
async def get_members(
    club_id: UUID,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=100),
    search: Optional[str] = None,
):
    try:
        if search:
            return await _get_stub().search_members(
                SearchMembersRequest(
                    club_id=club_id,
                    search=search,
                    pagination=PaginationRequest(page=page, page_size=page_size),
                )
            )
        return await _get_stub().get_members(
            GetMembersRequest(
                club_id=club_id,
                pagination=PaginationRequest(page=page, page_size=page_size),
            )
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in get_members(club={}): {} {}", club_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="/{club_id}/members/{user_id}", response_model=IsMemberResponse)
async def is_member(club_id: UUID, user_id: UUID):
    try:
        return await _get_stub().is_member(
            IsMemberRequest(club_id=club_id, user_id=user_id)
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in is_member(club={}, user={}): {} {}", club_id, user_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="/{club_id}/members/{user_id}/permissions")
async def get_member_permissions(club_id: UUID, user_id: UUID):
    try:
        return await _get_stub().get_member_permissions(
            GetMemberPermissionsRequest(club_id=club_id, user_id=user_id)
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in get_member_permissions(club={}, user={}): {} {}", club_id, user_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.put(path="/{club_id}/members/{target_user_id}/permissions", response_model=ClubResponse)
async def set_permission(club_id: UUID, target_user_id: UUID, request: SetPermissionRequest):
    if request.club_id != club_id or request.target_user_id != target_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="IDs in path do not match request body",
        )
    try:
        return await _get_stub().set_permission(request)
    except grpc.RpcError as e:
        logger.warning("gRPC error in set_permission(club={}): {} {}", club_id, e.code(), e.details())
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
