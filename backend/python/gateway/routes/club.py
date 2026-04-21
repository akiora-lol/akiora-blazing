from fastapi import APIRouter, HTTPException, status
from uuid import UUID
import grpc

from shared.contracts.club import (
    CreateClubRequest,
    GetClubRequest,
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
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="/{club_id}", response_model=ClubResponse)
async def get_club(club_id: UUID):
    try:
        return await _get_stub().get_club(GetClubRequest(club_id=club_id))
    except grpc.RpcError as e:
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
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.delete(path="/{club_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(club_id: UUID, user_id: UUID):
    try:
        await _get_stub().remove_member(RemoveMemberRequest(club_id=club_id, user_id=user_id))
    except grpc.RpcError as e:
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
