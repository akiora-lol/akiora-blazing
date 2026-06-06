from fastapi import APIRouter, HTTPException, status, Query
from uuid import UUID
from typing import Optional
import grpc
from loguru import logger

from shared.contracts.messenger import (
    ChatFilter,
    ChatOwnerType,
    ChatStatus,
    ChatType,
    CreateChatRequest,
    DeleteChatRequest,
    GetChatRequest,
    GetChatMembersRequest,
    GetChatMembersResponse,
    GetMessageHistoryRequest,
    GetMessageRequest,
    GetReactionsRequest,
    GetReactionsResponse,
    GetUnreadCountRequest,
    GetUnreadCountResponse,
    GetUserMessagesRequest,
    AddAllowedUserRequest,
    RemoveAllowedUserRequest,
    FreezeChatRequest,
    IsChatMemberRequest,
    IsChatMemberResponse,
    ListChatsRequest,
    ListChatsResponse,
    PaginationRequest,
    UnfreezeChatRequest,
    UpdateChatRequest,
    ChatResponse,
    SendMessageRequest,
    UpdateMessageRequest,
    DeleteMessageRequest,
    MarkAsReadRequest,
    AddReactionRequest,
    RemoveReactionRequest,
    GetMessagesRequest,
    GetMessagesResponse,
    GetUserChatsRequest,
    GetUserChatsResponse,
    MessageResponse,
)
from stubs.messenger_stub import MessengerStub
from dependencies import get_messenger_channel

router = APIRouter(tags=["messenger"])


def _get_stub() -> MessengerStub:
    return MessengerStub(get_messenger_channel())


# Chat endpoints
@router.post(
    path="/v1/chats",
    response_model=ChatResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_chat(request: CreateChatRequest):
    try:
        return await _get_stub().create_chat(request)
    except grpc.RpcError as e:
        logger.warning("gRPC error in create_chat: {} {}", e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="/v1/chats", response_model=ListChatsResponse)
async def list_chats(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=100),
    owner_id: Optional[UUID] = None,
    owner_type: Optional[ChatOwnerType] = None,
    chat_type: Optional[ChatType] = None,
    chat_status: Optional[ChatStatus] = None,
    is_member: bool = False,
):
    try:
        filter = ChatFilter(
            owner_id=owner_id,
            owner_type=owner_type,
            type=chat_type,
            status=chat_status,
            is_member=is_member,
        )
        return await _get_stub().list_chats(
            ListChatsRequest(
                filter=filter,
                pagination=PaginationRequest(page=page, page_size=page_size),
            )
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in list_chats: {} {}", e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="/v1/chats/{chat_id}", response_model=ChatResponse)
async def get_chat(chat_id: UUID):
    try:
        return await _get_stub().get_chat(GetChatRequest(chat_id=chat_id))
    except grpc.RpcError as e:
        logger.warning("gRPC error in get_chat({}): {} {}", chat_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.patch(path="/v1/chats/{chat_id}", response_model=ChatResponse)
async def update_chat(chat_id: UUID, request: UpdateChatRequest):
    if request.chat_id != chat_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chat ID in path does not match request body",
        )
    try:
        return await _get_stub().update_chat(request)
    except grpc.RpcError as e:
        logger.warning("gRPC error in update_chat({}): {} {}", chat_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.delete(path="/v1/chats/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(chat_id: UUID, actor_id: UUID):
    try:
        await _get_stub().delete_chat(DeleteChatRequest(chat_id=chat_id, actor_id=actor_id))
    except grpc.RpcError as e:
        logger.warning("gRPC error in delete_chat({}): {} {}", chat_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="/v1/users/{user_id}/chats", response_model=GetUserChatsResponse)
async def get_user_chats(
    user_id: UUID,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=100),
):
    try:
        return await _get_stub().get_user_chats(
            GetUserChatsRequest(
                user_id=user_id,
                pagination=PaginationRequest(page=page, page_size=page_size),
            )
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in get_user_chats({}): {} {}", user_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.post(path="/v1/chats/{chat_id}/members", response_model=ChatResponse)
async def add_allowed_user(chat_id: UUID, request: AddAllowedUserRequest):
    if request.chat_id != chat_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chat ID in path does not match request body",
        )
    try:
        return await _get_stub().add_allowed_user(request)
    except grpc.RpcError as e:
        logger.warning("gRPC error in add_allowed_user(chat={}): {} {}", chat_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.delete(path="/v1/chats/{chat_id}/members/{user_id}", response_model=ChatResponse)
async def remove_allowed_user(chat_id: UUID, user_id: UUID, actor_id: Optional[UUID] = None):
    try:
        return await _get_stub().remove_allowed_user(
            RemoveAllowedUserRequest(chat_id=chat_id, user_id=user_id, actor_id=actor_id)
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in remove_allowed_user(chat={}, user={}): {} {}", chat_id, user_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="/v1/chats/{chat_id}/members", response_model=GetChatMembersResponse)
async def get_chat_members(
    chat_id: UUID,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=100),
):
    try:
        return await _get_stub().get_chat_members(
            GetChatMembersRequest(
                chat_id=chat_id,
                pagination=PaginationRequest(page=page, page_size=page_size),
            )
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in get_chat_members({}): {} {}", chat_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="/v1/chats/{chat_id}/members/{user_id}", response_model=IsChatMemberResponse)
async def is_chat_member(chat_id: UUID, user_id: UUID):
    try:
        return await _get_stub().is_chat_member(
            IsChatMemberRequest(chat_id=chat_id, user_id=user_id)
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in is_chat_member(chat={}, user={}): {} {}", chat_id, user_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.post(path="/v1/chats/{chat_id}/freeze", response_model=ChatResponse)
async def freeze_chat(chat_id: UUID, actor_id: Optional[UUID] = None):
    try:
        return await _get_stub().freeze_chat(FreezeChatRequest(chat_id=chat_id, actor_id=actor_id))
    except grpc.RpcError as e:
        logger.warning("gRPC error in freeze_chat({}): {} {}", chat_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.post(path="/v1/chats/{chat_id}/unfreeze", response_model=ChatResponse)
async def unfreeze_chat(chat_id: UUID, actor_id: Optional[UUID] = None):
    try:
        return await _get_stub().unfreeze_chat(UnfreezeChatRequest(chat_id=chat_id, actor_id=actor_id))
    except grpc.RpcError as e:
        logger.warning("gRPC error in unfreeze_chat({}): {} {}", chat_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


# Message endpoints
@router.post(
    path="/v1/chats/{chat_id}/messages",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def send_message(chat_id: UUID, request: SendMessageRequest):
    if request.chat_id != chat_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chat ID in path does not match request body",
        )
    try:
        return await _get_stub().send_message(request)
    except grpc.RpcError as e:
        logger.warning("gRPC error in send_message(chat={}): {} {}", chat_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="/v1/chats/{chat_id}/messages", response_model=GetMessagesResponse)
async def get_messages(
    chat_id: UUID,
    limit: int = Query(default=50, ge=1, le=100),
    before_timestamp: Optional[int] = None,
):
    try:
        return await _get_stub().get_messages(
            GetMessagesRequest(chat_id=chat_id, limit=limit, before_timestamp=before_timestamp)
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in get_messages(chat={}): {} {}", chat_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="/v1/messages/{message_id}", response_model=MessageResponse)
async def get_message(message_id: UUID):
    try:
        return await _get_stub().get_message(GetMessageRequest(message_id=message_id))
    except grpc.RpcError as e:
        logger.warning("gRPC error in get_message({}): {} {}", message_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.patch(path="/v1/messages/{message_id}", response_model=MessageResponse)
async def update_message(message_id: UUID, request: UpdateMessageRequest):
    if request.message_id != message_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message ID in path does not match request body",
        )
    try:
        return await _get_stub().update_message(request)
    except grpc.RpcError as e:
        logger.warning("gRPC error in update_message({}): {} {}", message_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.delete(path="/v1/messages/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(message_id: UUID, deleter_id: UUID):
    try:
        await _get_stub().delete_message(
            DeleteMessageRequest(message_id=message_id, deleter_id=deleter_id)
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in delete_message({}): {} {}", message_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.post(path="/v1/messages/{message_id}/read", response_model=MessageResponse)
async def mark_as_read(message_id: UUID, request: MarkAsReadRequest):
    if request.message_id != message_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message ID in path does not match request body",
        )
    try:
        return await _get_stub().mark_as_read(request)
    except grpc.RpcError as e:
        logger.warning("gRPC error in mark_as_read({}): {} {}", message_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="/v1/chats/{chat_id}/unread-count", response_model=GetUnreadCountResponse)
async def get_unread_count(chat_id: UUID, user_id: UUID):
    try:
        return await _get_stub().get_unread_count(
            GetUnreadCountRequest(chat_id=chat_id, user_id=user_id)
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in get_unread_count(chat={}): {} {}", chat_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.post(path="/v1/messages/{message_id}/reactions", response_model=MessageResponse)
async def add_reaction(message_id: UUID, request: AddReactionRequest):
    if request.message_id != message_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message ID in path does not match request body",
        )
    try:
        return await _get_stub().add_reaction(request)
    except grpc.RpcError as e:
        logger.warning("gRPC error in add_reaction({}): {} {}", message_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="/v1/messages/{message_id}/reactions", response_model=GetReactionsResponse)
async def get_reactions(message_id: UUID):
    try:
        return await _get_stub().get_reactions(GetReactionsRequest(message_id=message_id))
    except grpc.RpcError as e:
        logger.warning("gRPC error in get_reactions({}): {} {}", message_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.delete(path="/v1/messages/{message_id}/reactions/{emote_id}", response_model=MessageResponse)
async def remove_reaction(message_id: UUID, emote_id: str, user_id: UUID):
    try:
        return await _get_stub().remove_reaction(
            RemoveReactionRequest(message_id=message_id, emote_id=emote_id, user_id=user_id)
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in remove_reaction({}): {} {}", message_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="/v1/messages/{message_id}/history", response_model=GetMessagesResponse)
async def get_message_history(
    message_id: UUID,
    limit: int = Query(default=50, ge=1, le=100),
):
    try:
        return await _get_stub().get_message_history(
            GetMessageHistoryRequest(message_id=message_id, limit=limit)
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in get_message_history({}): {} {}", message_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="/v1/users/{user_id}/messages", response_model=GetMessagesResponse)
async def get_user_messages(
    user_id: UUID,
    chat_id: Optional[UUID] = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=100),
):
    try:
        return await _get_stub().get_user_messages(
            GetUserMessagesRequest(
                user_id=user_id,
                chat_id=chat_id,
                pagination=PaginationRequest(page=page, page_size=page_size),
            )
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in get_user_messages({}): {} {}", user_id, e.code(), e.details())
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
