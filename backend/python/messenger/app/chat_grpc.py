import grpc
from uuid import UUID

from dishka.integrations.grpcio import FromDishka, inject

from messenger.v1.messenger_service_pb2 import (
    CreateChatRequest,
    GetChatRequest,
    AddAllowedUserRequest,
    RemoveAllowedUserRequest,
    FreezeChatRequest,
    ChatResponse,
    ChatOwnerType,
    ChatType,
    ChatStatus,
)
from messenger.v1.messenger_service_pb2_grpc import ChatServiceServicer
from common.types_pb2 import Empty

from domain.services.chat import ChatService
from domain.entities.chat import Chat


_OWNER_TYPE_MAP = {
    ChatOwnerType.SYSTEM: "system",
    ChatOwnerType.CLUB: "club",
    ChatOwnerType.TOURNAMENT: "tournament",
    ChatOwnerType.GAMESERIES: "gameseries",
}

_CHAT_TYPE_MAP = {
    ChatType.PRIVATE: "private",
    ChatType.PUBLIC: "public",
}

_OWNER_TYPE_REVERSE = {v: k for k, v in _OWNER_TYPE_MAP.items()}
_CHAT_TYPE_REVERSE = {v: k for k, v in _CHAT_TYPE_MAP.items()}
_CHAT_STATUS_REVERSE = {
    "active": ChatStatus.ACTIVE,
    "frozen": ChatStatus.FROZEN,
}


def _chat_to_proto(chat: Chat) -> ChatResponse:
    return ChatResponse(
        id=str(chat.id),
        owner_id=str(chat.owner_id),
        owner_type=_OWNER_TYPE_REVERSE.get(chat.owner_type, ChatOwnerType.SYSTEM),
        type=_CHAT_TYPE_REVERSE.get(chat.type, ChatType.PRIVATE),
        status=_CHAT_STATUS_REVERSE.get(chat.status, ChatStatus.ACTIVE),
        timestamp=int(chat.timestamp.timestamp()),
        allowed_users=[str(u) for u in chat.allowed_users],
    )


class ChatGrpc(ChatServiceServicer):
    @inject
    async def CreateChat(
        self,
        request: CreateChatRequest,
        context: grpc.aio.ServicerContext,
    ) -> ChatResponse:
        owner_type = _OWNER_TYPE_MAP.get(request.owner_type, "system")
        chat_type = _CHAT_TYPE_MAP.get(request.type, "private")
        allowed_users = [UUID(uid) for uid in request.allowed_users]
        chat = await ChatService.create_chat(
            owner_id=UUID(request.owner_id),
            owner_type=owner_type,
            chat_type=chat_type,
            allowed_users=allowed_users,
        )
        return _chat_to_proto(chat)

    @inject
    async def GetChat(
        self,
        request: GetChatRequest,
        context: grpc.aio.ServicerContext,
    ) -> ChatResponse:
        chat = await ChatService.get_chat(UUID(request.chat_id))
        if not chat:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Chat not found")
        return _chat_to_proto(chat)

    @inject
    async def AddAllowedUser(
        self,
        request: AddAllowedUserRequest,
        context: grpc.aio.ServicerContext,
    ) -> ChatResponse:
        chat = await ChatService.add_allowed_user(
            chat_id=UUID(request.chat_id),
            user_id=UUID(request.user_id),
        )
        return _chat_to_proto(chat)

    @inject
    async def RemoveAllowedUser(
        self,
        request: RemoveAllowedUserRequest,
        context: grpc.aio.ServicerContext,
    ) -> Empty:
        await ChatService.remove_allowed_user(
            chat_id=UUID(request.chat_id),
            user_id=UUID(request.user_id),
        )
        return Empty()

    @inject
    async def FreezeChat(
        self,
        request: FreezeChatRequest,
        context: grpc.aio.ServicerContext,
    ) -> ChatResponse:
        chat = await ChatService.freeze_chat(UUID(request.chat_id))
        return _chat_to_proto(chat)
