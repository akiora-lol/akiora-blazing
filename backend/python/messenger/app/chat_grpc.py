import grpc
from uuid import UUID

from dishka.integrations.grpcio import FromDishka, inject

from messenger.v1.messenger_service_pb2 import (
    AddAllowedUserRequest,
    CreateChatRequest,
    DeleteChatRequest,
    GetChatRequest,
    GetChatMembersRequest,
    GetUserChatsRequest,
    IsChatMemberRequest,
    ListChatsRequest,
    RemoveAllowedUserRequest,
    FreezeChatRequest,
    UnfreezeChatRequest,
    UpdateChatRequest,
    ChatResponse,
    ChatOwnerType,
    ChatType,
    ChatStatus,
)
from messenger.v1.messenger_service_pb2_grpc import ChatServiceServicer
from common.types_pb2 import Empty

from domain.services.chat import ChatService
from domain.entities.chat import Chat
from domain.entities.message import Message


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
_CHAT_STATUS_MAP = {v: k for k, v in _CHAT_STATUS_REVERSE.items()}


def _paginate(items, pagination):
    page = pagination.page or 1
    page_size = pagination.page_size or 50
    start = (page - 1) * page_size
    end = start + page_size
    return items[start:end], page, page_size, end < len(items)


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
    async def UpdateChat(
        self,
        request: UpdateChatRequest,
        context: grpc.aio.ServicerContext,
    ) -> ChatResponse:
        chat = await Chat.get(UUID(request.chat_id))
        if not chat:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Chat not found")
        patch = {}
        if request.HasField("status"):
            patch["status"] = _CHAT_STATUS_MAP.get(request.status, "active")
        if request.HasField("owner_id"):
            patch["owner_id"] = UUID(request.owner_id)
        if patch:
            await chat.update({"$set": patch})
            chat = await Chat.get(chat.id)
        return _chat_to_proto(chat)

    @inject
    async def DeleteChat(
        self,
        request: DeleteChatRequest,
        context: grpc.aio.ServicerContext,
    ):
        from common.types_pb2 import Empty
        chat = await Chat.get(UUID(request.chat_id))
        if not chat:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Chat not found")
        await Message.find(Message.chat_id == chat.id).delete()
        await chat.delete()
        return Empty()

    @inject
    async def ListChats(
        self,
        request: ListChatsRequest,
        context: grpc.aio.ServicerContext,
    ):
        from messenger.v1 import messenger_service_pb2 as pb2
        chats = await Chat.find_all().to_list()
        if request.HasField("filter"):
            filter_ = request.filter
            if filter_.owner_id:
                owner_id = UUID(filter_.owner_id)
                if filter_.is_member:
                    chats = [
                        chat for chat in chats
                        if owner_id == chat.owner_id or owner_id in chat.allowed_users
                    ]
                else:
                    chats = [chat for chat in chats if chat.owner_id == owner_id]
            if filter_.owner_type:
                owner_type = _OWNER_TYPE_MAP.get(filter_.owner_type)
                chats = [chat for chat in chats if chat.owner_type == owner_type]
            if filter_.type:
                chat_type = _CHAT_TYPE_MAP.get(filter_.type)
                chats = [chat for chat in chats if chat.type == chat_type]
            if filter_.status:
                chat_status = _CHAT_STATUS_MAP.get(filter_.status)
                chats = [chat for chat in chats if chat.status == chat_status]
        page_items, page, page_size, has_next = _paginate(chats, request.pagination)
        return pb2.ListChatsResponse(
            chats=[_chat_to_proto(chat) for chat in page_items],
            total_count=len(chats),
            page=page,
            page_size=page_size,
            has_next=has_next,
        )

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
    ) -> ChatResponse:
        chat = await ChatService.remove_allowed_user(
            chat_id=UUID(request.chat_id),
            user_id=UUID(request.user_id),
        )
        return _chat_to_proto(chat)

    @inject
    async def FreezeChat(
        self,
        request: FreezeChatRequest,
        context: grpc.aio.ServicerContext,
    ) -> ChatResponse:
        chat = await ChatService.freeze_chat(UUID(request.chat_id))
        return _chat_to_proto(chat)

    @inject
    async def UnfreezeChat(
        self,
        request: UnfreezeChatRequest,
        context: grpc.aio.ServicerContext,
    ) -> ChatResponse:
        chat = await Chat.get(UUID(request.chat_id))
        if not chat:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Chat not found")
        chat.status = "active"
        await chat.save()
        return _chat_to_proto(chat)

    @inject
    async def GetUserChats(
        self,
        request: GetUserChatsRequest,
        context: grpc.aio.ServicerContext,
    ):
        from messenger.v1 import messenger_service_pb2 as pb2
        user_id = UUID(request.user_id)
        chats = [
            chat for chat in await Chat.find_all().to_list()
            if chat.owner_id == user_id or user_id in chat.allowed_users
        ]
        page_items, page, page_size, has_next = _paginate(chats, request.pagination)
        return pb2.ListChatsResponse(
            chats=[_chat_to_proto(chat) for chat in page_items],
            total_count=len(chats),
            page=page,
            page_size=page_size,
            has_next=has_next,
        )

    @inject
    async def GetChatMembers(
        self,
        request: GetChatMembersRequest,
        context: grpc.aio.ServicerContext,
    ):
        from messenger.v1 import messenger_service_pb2 as pb2
        chat = await Chat.get(UUID(request.chat_id))
        if not chat:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Chat not found")
        member_ids = [chat.owner_id, *chat.allowed_users]
        members, _, _, _ = _paginate(member_ids, request.pagination)
        return pb2.GetChatMembersResponse(
            members=[pb2.ChatMemberInfo(user_id=str(user_id)) for user_id in members],
            total_count=len(member_ids),
        )

    @inject
    async def IsChatMember(
        self,
        request: IsChatMemberRequest,
        context: grpc.aio.ServicerContext,
    ):
        from messenger.v1 import messenger_service_pb2 as pb2
        chat = await Chat.get(UUID(request.chat_id))
        if not chat:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Chat not found")
        user_id = UUID(request.user_id)
        return pb2.IsChatMemberResponse(
            is_member=chat.owner_id == user_id or user_id in chat.allowed_users
        )
