from fastapi import APIRouter, HTTPException, status
from uuid import UUID
import grpc

from shared.contracts.user import (
    CreateUserRequest,
    GetUserRequest,
    GetUserByEmailRequest,
    UpdateUserRequest,
    UserResponse,
)
from stubs.user_stub import UserStub
from dependencies import get_community_channel

router = APIRouter(prefix="/v1/users", tags=["users"])


def _get_stub() -> UserStub:
    return UserStub(get_community_channel())


@router.post(
    path="",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(request: CreateUserRequest):
    try:
        return await _get_stub().create_user(request)
    except grpc.RpcError as e:
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID):
    try:
        return await _get_stub().get_user(GetUserRequest(id=user_id))
    except grpc.RpcError as e:
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="/by-email/{email}", response_model=UserResponse)
async def get_user_by_email(email: str):
    try:
        return await _get_stub().get_user_by_email(GetUserByEmailRequest(email=email))
    except grpc.RpcError as e:
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.patch(path="/{user_id}", response_model=UserResponse)
async def update_user(user_id: UUID, request: UpdateUserRequest):
    if request.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID in path does not match request body",
        )
    try:
        return await _get_stub().update_user(request)
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
