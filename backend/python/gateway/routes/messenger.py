from fastapi import APIRouter, HTTPException, status, Query
from uuid import UUID
from typing import Optional
import grpc

from shared.contracts.messenger import (
    CreateChatRequest,
    GetChatRequest,
    AddAllowedUserRequest,
    RemoveAllowedUserRequest,
    FreezeChatRequest,
    ChatResponse,
    SendMessageRequest,
    UpdateMessageRequest,
    DeleteMessageRequest,
    MarkAsReadRequest,
    AddReactionRequest,
    RemoveReactionRequest,
    GetMessagesRequest,
    GetMessagesResponse,
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
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="/v1/chats/{chat_id}", response_model=ChatResponse)
async def get_chat(chat_id: UUID):
    try:
        return await _get_stub().get_chat(GetChatRequest(chat_id=chat_id))
    except grpc.RpcError as e:
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.post(path="/v1/chats/{chat_id}/members", response_model=ChatResponse)
async def add_allowed_user(chat_id: UUID, request: AddAllowedUserRequest):
    if request.chat_id != chat_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chat ID in path does not match request body",
        )
    # TODO: implement add_allowed_user in stub
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete(path="/v1/chats/{chat_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_allowed_user(chat_id: UUID, user_id: UUID):
    # TODO: implement remove_allowed_user in stub
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post(path="/v1/chats/{chat_id}/freeze", response_model=ChatResponse)
async def freeze_chat(chat_id: UUID):
    # TODO: implement freeze_chat in stub
    raise HTTPException(status_code=501, detail="Not implemented")


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
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.delete(path="/v1/messages/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(message_id: UUID, deleter_id: UUID):
    try:
        await _get_stub().delete_message(
            DeleteMessageRequest(message_id=message_id, deleter_id=deleter_id)
        )
    except grpc.RpcError as e:
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.post(path="/v1/messages/{message_id}/read", response_model=MessageResponse)
async def mark_as_read(message_id: UUID, request: MarkAsReadRequest):
    if request.message_id != message_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message ID in path does not match request body",
        )
    # TODO: implement mark_as_read in stub
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post(path="/v1/messages/{message_id}/reactions", response_model=MessageResponse)
async def add_reaction(message_id: UUID, request: AddReactionRequest):
    if request.message_id != message_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message ID in path does not match request body",
        )
    # TODO: implement add_reaction in stub
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete(path="/v1/messages/{message_id}/reactions/{emote_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_reaction(message_id: UUID, emote_id: str, user_id: UUID):
    # TODO: implement remove_reaction in stub
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
