from typing import Annotated, Optional

from fastapi import APIRouter, Cookie, Depends, HTTPException, status, Query
from uuid import UUID
import grpc
from loguru import logger
from dishka.integrations.fastapi import DishkaRoute, FromDishka, inject
from schemas.cookie import CookieSchema
from shared.contracts.user import (
    BlockUserRequest,
    CreateUserRequest,
    DeleteUserRequest,
    FriendResponse,
    Gender,
    GetFriendStatusRequest,
    GetFriendStatusResponse,
    GetUserRequest,
    GetUserByEmailRequest,
    ListFriendsRequest,
    ListFriendsResponse,
    ListUsersRequest,
    ListUsersResponse,
    PaginationRequest,
    RemoveFriendRequest,
    RespondFriendRequestRequest,
    SendFriendRequestRequest,
    UnblockUserRequest,
    UpdateUserRequest,
    UserResponse,
    UserFilter,
    UserType,
)
from stubs.user_stub import UserStub
from dependencies import get_community_channel

from redis_invalidator import RedisInvalidator
from shared.redis import RedisService

router = APIRouter(prefix="/v1/users", tags=["users"], route_class=DishkaRoute)
NOTIFICATION_STREAM = "notification_stream"


async def verify_cookie(
    sid: Optional[str] = Cookie(None, alias="sid"),
):
    if not sid:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return sid


def _get_stub() -> UserStub:
    return UserStub(get_community_channel())


async def _publish_friend_event(redis: RedisService, event_type: str, user_ids: list[UUID], friendship: FriendResponse):
    try:
        await redis.publish_stream(
            NOTIFICATION_STREAM,
            {
                "type": event_type,
                "user_ids": [str(user_id) for user_id in user_ids],
                "friendship": friendship.model_dump(mode="json"),
            },
        )
    except Exception as e:
        logger.warning("Failed to publish {} for friendship={}: {}", event_type, friendship.id, e)


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


@router.get(path="", response_model=ListUsersResponse)
async def list_users(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=100),
    search: Optional[str] = None,
    user_type: Optional[UserType] = None,
    gender: Optional[Gender] = None,
    has_avatar: bool = False,
    min_created_at: Optional[int] = None,
    max_created_at: Optional[int] = None,
):
    try:
        return await _get_stub().list_users(
            ListUsersRequest(
                filter=UserFilter(
                    search=search,
                    user_type=user_type,
                    gender=gender,
                    has_avatar=has_avatar,
                    min_created_at=min_created_at,
                    max_created_at=max_created_at,
                ),
                pagination=PaginationRequest(page=page, page_size=page_size),
            )
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in list_users: {} {}", e.code(), e.details())
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


@router.delete(path="/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, actor_id: UUID):
    try:
        await _get_stub().delete_user(DeleteUserRequest(user_id=user_id, actor_id=actor_id))
    except grpc.RpcError as e:
        logger.warning("gRPC error in delete_user({}): {} {}", user_id, e.code(), e.details())
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


@router.post(path="/friend-requests", response_model=FriendResponse)
async def send_friend_request(
    request: SendFriendRequestRequest,
    redis: FromDishka[RedisService],
):
    try:
        friendship = await _get_stub().send_friend_request(request)
        await _publish_friend_event(
            redis,
            "friend.request.created",
            [request.request.receiver_id],
            friendship,
        )
        return friendship
    except grpc.RpcError as e:
        logger.warning("gRPC error in send_friend_request: {} {}", e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.post(path="/friend-requests/respond", response_model=FriendResponse)
async def respond_friend_request(
    request: RespondFriendRequestRequest,
    redis: FromDishka[RedisService],
):
    try:
        friendship = await _get_stub().respond_friend_request(request)
        await _publish_friend_event(
            redis,
            "friend.request.accepted" if request.response.accept else "friend.request.rejected",
            [friendship.user_id_1, friendship.user_id_2],
            friendship,
        )
        return friendship
    except grpc.RpcError as e:
        logger.warning("gRPC error in respond_friend_request: {} {}", e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="/{user_id}/friend-requests/pending", response_model=ListFriendsResponse)
async def get_pending_friend_requests(user_id: UUID):
    try:
        return await _get_stub().get_pending_friend_requests(GetUserRequest(id=user_id))
    except grpc.RpcError as e:
        logger.warning("gRPC error in get_pending_friend_requests({}): {} {}", user_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="/{user_id}/friends", response_model=ListFriendsResponse)
async def get_friends(
    user_id: UUID,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=100),
    friend_status: str = "ACCEPTED",
):
    try:
        return await _get_stub().get_friends(
            ListFriendsRequest(
                user_id=user_id,
                status=friend_status,
                pagination=PaginationRequest(page=page, page_size=page_size),
            )
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in get_friends({}): {} {}", user_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.delete(path="/{user_id}/friends/{friend_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_friend(user_id: UUID, friend_id: UUID, actor_id: UUID):
    try:
        await _get_stub().remove_friend(
            RemoveFriendRequest(user_id_1=user_id, user_id_2=friend_id, actor_id=actor_id)
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in remove_friend({}, {}): {} {}", user_id, friend_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.post(path="/{user_id}/blocks/{blocked_id}", response_model=FriendResponse)
async def block_user(user_id: UUID, blocked_id: UUID):
    try:
        return await _get_stub().block_user(
            BlockUserRequest(blocker_id=user_id, blocked_id=blocked_id)
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in block_user({}, {}): {} {}", user_id, blocked_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.delete(path="/{user_id}/blocks/{blocked_id}", response_model=FriendResponse)
async def unblock_user(user_id: UUID, blocked_id: UUID):
    try:
        return await _get_stub().unblock_user(
            UnblockUserRequest(blocker_id=user_id, blocked_id=blocked_id)
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in unblock_user({}, {}): {} {}", user_id, blocked_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="/{user_id}/friends/{other_user_id}/status", response_model=GetFriendStatusResponse)
async def get_friend_status(user_id: UUID, other_user_id: UUID):
    try:
        return await _get_stub().get_friend_status(
            GetFriendStatusRequest(user_id_1=user_id, user_id_2=other_user_id)
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in get_friend_status({}, {}): {} {}", user_id, other_user_id, e.code(), e.details())
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
