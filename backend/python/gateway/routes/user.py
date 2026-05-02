from typing import Annotated, Optional

from fastapi import APIRouter, Cookie, Depends, HTTPException, status
from uuid import UUID
import grpc
from loguru import logger
from dishka.integrations.fastapi import DishkaRoute, FromDishka, inject
from schemas.cookie import CookieSchema
from shared.contracts.user import (
    CreateUserRequest,
    GetUserRequest,
    GetUserByEmailRequest,
    UpdateUserRequest,
    UserResponse,
)
from stubs.user_stub import UserStub
from dependencies import get_community_channel

from redis_invalidator import RedisInvalidator

router = APIRouter(prefix="/v1/users", tags=["users"], route_class=DishkaRoute)


async def verify_cookie(
    sid: Optional[str] = Cookie(None, alias="sid"),
):
    if not sid:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return sid


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
        logger.warning("gRPC error in create_user: {} {}", e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID):
    try:
        return await _get_stub().get_user(GetUserRequest(id=user_id))
    except grpc.RpcError as e:
        logger.warning(
            "gRPC error in get_user({}): {} {}", user_id, e.code(), e.details()
        )
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="/by-email/{email}", response_model=UserResponse)
async def get_user_by_email(email: str):
    try:
        return await _get_stub().get_user_by_email(GetUserByEmailRequest(email=email))
    except grpc.RpcError as e:
        logger.warning(
            "gRPC error in get_user_by_email({}): {} {}", email, e.code(), e.details()
        )
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.patch(path="/{user_id}", response_model=UserResponse)
async def update_user(
    cookie_data: Annotated[CookieSchema, Cookie()],
    user_id: UUID,
    request: UpdateUserRequest,
    rinvd: FromDishka[RedisInvalidator],
):

    if request.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID in path does not match request body",
        )
    try:
        data = await _get_stub().update_user(request)
        await rinvd.update_session_user(cookie_data.sid, data.model_dump())
        return data
    except grpc.RpcError as e:
        logger.warning(
            "gRPC error in update_user({}): {} {}", user_id, e.code(), e.details()
        )
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())
    except ValueError as e:
        logger.warning("Value error  in update_user({}): {}", user_id, e)
        raise HTTPException(status_code=400, detail=str(e))


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
