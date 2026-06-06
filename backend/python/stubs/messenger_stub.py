import grpc
from uuid import UUID

from shared.contracts.messenger import (
    AddAllowedUserRequest,
    AddReactionRequest,
    ChatFilter,
    ChatMemberInfo,
    ChatOwnerType,
    ChatResponse,
    ChatStatus,
    ChatType,
    CreateChatRequest,
    DeleteChatRequest,
    DeleteMessageRequest,
    FreezeChatRequest,
    GetChatMembersRequest,
    GetChatMembersResponse,
    GetChatRequest,
    GetMessageHistoryRequest,
    GetMessageRequest,
    GetMessagesRequest,
    GetMessagesResponse,
    GetReactionsRequest,
    GetReactionsResponse,
    GetUnreadCountRequest,
    GetUnreadCountResponse,
    GetUserChatsRequest,
    GetUserChatsResponse,
    GetUserMessagesRequest,
    IsChatMemberRequest,
    IsChatMemberResponse,
    ListChatsRequest,
    ListChatsResponse,
    MarkAsReadRequest,
    MessageFilter,
    MessageResponse,
    MessageShort,
    MessageStatus,
    PaginationRequest,
    Reaction,
    RemoveAllowedUserRequest,
    RemoveReactionRequest,
    SendMessageRequest,
    UnfreezeChatRequest,
    UpdateChatRequest,
    UpdateMessageRequest,
)

import messenger.v1.messenger_service_pb2 as pb2_module
import messenger.v1.messenger_service_pb2_grpc as pb2_grpc_module


class MessengerMapper:
    CHAT_OWNER_TYPE_MAP = {
        0: ChatOwnerType.OWNER_UNSPECIFIED,
        1: ChatOwnerType.SYSTEM,
        2: ChatOwnerType.CLUB,
        3: ChatOwnerType.TOURNAMENT,
        4: ChatOwnerType.GAMESERIES,
    }
    CHAT_OWNER_TYPE_TO_PROTO = {value: key for key, value in CHAT_OWNER_TYPE_MAP.items()}

    CHAT_TYPE_MAP = {
        0: ChatType.CHAT_TYPE_UNSPECIFIED,
        1: ChatType.PRIVATE,
        2: ChatType.PUBLIC,
    }
    CHAT_TYPE_TO_PROTO = {value: key for key, value in CHAT_TYPE_MAP.items()}

    CHAT_STATUS_MAP = {
        0: ChatStatus.CHAT_STATUS_UNSPECIFIED,
        1: ChatStatus.ACTIVE,
        2: ChatStatus.FROZEN,
    }
    CHAT_STATUS_TO_PROTO = {value: key for key, value in CHAT_STATUS_MAP.items()}

    MESSAGE_STATUS_MAP = {
        0: MessageStatus.MESSAGE_STATUS_UNSPECIFIED,
        1: MessageStatus.SENT,
        2: MessageStatus.READ,
    }
    MESSAGE_STATUS_TO_PROTO = {value: key for key, value in MESSAGE_STATUS_MAP.items()}

    @classmethod
    def to_pydantic_chat_response(cls, grpc_response) -> ChatResponse:
        return ChatResponse(
            id=UUID(grpc_response.id),
            owner_id=UUID(grpc_response.owner_id),
            owner_type=cls.CHAT_OWNER_TYPE_MAP.get(
                grpc_response.owner_type, ChatOwnerType.OWNER_UNSPECIFIED
            ),
            type=cls.CHAT_TYPE_MAP.get(
                grpc_response.type, ChatType.CHAT_TYPE_UNSPECIFIED
            ),
            status=cls.CHAT_STATUS_MAP.get(
                grpc_response.status, ChatStatus.CHAT_STATUS_UNSPECIFIED
            ),
            timestamp=grpc_response.timestamp,
            allowed_users=list(grpc_response.allowed_users),
        )

    @classmethod
    def to_pydantic_message_response(cls, grpc_response) -> MessageResponse:
        return MessageResponse(
            id=UUID(grpc_response.id),
            chat_id=UUID(grpc_response.chat_id),
            creator_id=UUID(grpc_response.creator_id),
            body=grpc_response.body,
            status=cls.MESSAGE_STATUS_MAP.get(
                grpc_response.status, MessageStatus.MESSAGE_STATUS_UNSPECIFIED
            ),
            read_by=list(grpc_response.read_by),
            timestamp=grpc_response.timestamp,
            history=[
                MessageShort(body=item.body, timestamp=item.timestamp)
                for item in grpc_response.history
            ],
            reply_to=grpc_response.reply_to or None,
            reactions=[
                Reaction(
                    emote_id=reaction.emote_id,
                    user_id=reaction.user_id,
                    timestamp=reaction.timestamp,
                )
                for reaction in grpc_response.reactions
            ],
            spoiler=grpc_response.spoiler,
        )

    @classmethod
    def to_pydantic_list_chats_response(cls, grpc_response) -> ListChatsResponse:
        return ListChatsResponse(
            chats=[cls.to_pydantic_chat_response(chat) for chat in grpc_response.chats],
            total_count=grpc_response.total_count,
            page=grpc_response.page,
            page_size=grpc_response.page_size,
            has_next=grpc_response.has_next,
        )

    @classmethod
    def to_pydantic_get_user_chats_response(
        cls, grpc_response
    ) -> GetUserChatsResponse:
        return GetUserChatsResponse(
            chats=[cls.to_pydantic_chat_response(chat) for chat in grpc_response.chats],
            total_count=grpc_response.total_count,
            page=grpc_response.page,
            page_size=grpc_response.page_size,
            has_next=grpc_response.has_next,
        )

    @classmethod
    def to_pydantic_chat_members_response(
        cls, grpc_response
    ) -> GetChatMembersResponse:
        return GetChatMembersResponse(
            members=[
                ChatMemberInfo(
                    user_id=member.user_id,
                    nickname=member.nickname or None,
                    avatar=member.avatar or None,
                )
                for member in grpc_response.members
            ],
            total_count=grpc_response.total_count,
        )

    @classmethod
    def to_pydantic_messages_response(cls, grpc_response) -> GetMessagesResponse:
        return GetMessagesResponse(
            messages=[
                cls.to_pydantic_message_response(message)
                for message in grpc_response.messages
            ],
            total_count=grpc_response.total_count,
        )

    @classmethod
    def to_pydantic_reactions_response(cls, grpc_response) -> GetReactionsResponse:
        return GetReactionsResponse(
            reactions=[
                Reaction(
                    emote_id=reaction.emote_id,
                    user_id=reaction.user_id,
                    timestamp=reaction.timestamp,
                )
                for reaction in grpc_response.reactions
            ]
        )

    @classmethod
    def to_grpc_pagination(cls, pagination: PaginationRequest):
        return pb2_module.PaginationRequest(
            page=pagination.page,
            page_size=pagination.page_size,
            before_timestamp=pagination.before_timestamp or 0,
        )

    @classmethod
    def to_grpc_chat_filter(cls, filter: ChatFilter):
        grpc_filter = pb2_module.ChatFilter(is_member=filter.is_member)
        if filter.owner_id:
            grpc_filter.owner_id = str(filter.owner_id)
        if filter.owner_type:
            grpc_filter.owner_type = cls.CHAT_OWNER_TYPE_TO_PROTO.get(
                filter.owner_type, 0
            )
        if filter.type:
            grpc_filter.type = cls.CHAT_TYPE_TO_PROTO.get(filter.type, 0)
        if filter.status:
            grpc_filter.status = cls.CHAT_STATUS_TO_PROTO.get(filter.status, 0)
        return grpc_filter

    @classmethod
    def to_grpc_message_filter(cls, filter: MessageFilter):
        grpc_filter = pb2_module.MessageFilter(has_reactions=filter.has_reactions)
        if filter.creator_id:
            grpc_filter.creator_id = str(filter.creator_id)
        if filter.status:
            grpc_filter.status = cls.MESSAGE_STATUS_TO_PROTO.get(filter.status, 0)
        return grpc_filter

    @classmethod
    def to_grpc_create_chat_request(cls, request: CreateChatRequest):
        return pb2_module.CreateChatRequest(
            owner_id=str(request.owner_id),
            owner_type=cls.CHAT_OWNER_TYPE_TO_PROTO.get(request.owner_type, 0),
            type=cls.CHAT_TYPE_TO_PROTO.get(request.type, 0),
            allowed_users=request.allowed_users,
        )

    @classmethod
    def to_grpc_get_chat_request(cls, request: GetChatRequest):
        return pb2_module.GetChatRequest(chat_id=str(request.chat_id))

    @classmethod
    def to_grpc_update_chat_request(cls, request: UpdateChatRequest):
        grpc_request = pb2_module.UpdateChatRequest(
            chat_id=str(request.chat_id),
            actor_id=str(request.actor_id),
        )
        if request.status:
            grpc_request.status = cls.CHAT_STATUS_TO_PROTO.get(request.status, 0)
        if request.owner_id:
            grpc_request.owner_id = str(request.owner_id)
        return grpc_request

    @classmethod
    def to_grpc_delete_chat_request(cls, request: DeleteChatRequest):
        return pb2_module.DeleteChatRequest(
            chat_id=str(request.chat_id),
            actor_id=str(request.actor_id),
        )

    @classmethod
    def to_grpc_list_chats_request(cls, request: ListChatsRequest):
        return pb2_module.ListChatsRequest(
            filter=cls.to_grpc_chat_filter(request.filter),
            pagination=cls.to_grpc_pagination(request.pagination),
        )

    @classmethod
    def to_grpc_add_allowed_user_request(cls, request: AddAllowedUserRequest):
        return pb2_module.AddAllowedUserRequest(
            chat_id=str(request.chat_id),
            actor_id=str(request.actor_id or ""),
            user_id=str(request.user_id),
        )

    @classmethod
    def to_grpc_remove_allowed_user_request(cls, request: RemoveAllowedUserRequest):
        return pb2_module.RemoveAllowedUserRequest(
            chat_id=str(request.chat_id),
            actor_id=str(request.actor_id or ""),
            user_id=str(request.user_id),
        )

    @classmethod
    def to_grpc_freeze_chat_request(cls, request: FreezeChatRequest):
        return pb2_module.FreezeChatRequest(
            chat_id=str(request.chat_id),
            actor_id=str(request.actor_id or ""),
        )

    @classmethod
    def to_grpc_unfreeze_chat_request(cls, request: UnfreezeChatRequest):
        return pb2_module.UnfreezeChatRequest(
            chat_id=str(request.chat_id),
            actor_id=str(request.actor_id or ""),
        )

    @classmethod
    def to_grpc_get_user_chats_request(cls, request: GetUserChatsRequest):
        return pb2_module.GetUserChatsRequest(
            user_id=str(request.user_id),
            pagination=cls.to_grpc_pagination(request.pagination),
        )

    @classmethod
    def to_grpc_get_chat_members_request(cls, request: GetChatMembersRequest):
        return pb2_module.GetChatMembersRequest(
            chat_id=str(request.chat_id),
            pagination=cls.to_grpc_pagination(request.pagination),
        )

    @classmethod
    def to_grpc_is_chat_member_request(cls, request: IsChatMemberRequest):
        return pb2_module.IsChatMemberRequest(
            chat_id=str(request.chat_id),
            user_id=str(request.user_id),
        )

    @classmethod
    def to_grpc_send_message_request(cls, request: SendMessageRequest):
        return pb2_module.SendMessageRequest(
            chat_id=str(request.chat_id),
            creator_id=str(request.creator_id),
            body=request.body,
            reply_to=request.reply_to or "",
            spoiler=request.spoiler,
        )

    @classmethod
    def to_grpc_get_message_request(cls, request: GetMessageRequest):
        return pb2_module.GetMessageRequest(message_id=str(request.message_id))

    @classmethod
    def to_grpc_update_message_request(cls, request: UpdateMessageRequest):
        return pb2_module.UpdateMessageRequest(
            message_id=str(request.message_id),
            editor_id=str(request.editor_id),
            new_body=request.new_body,
        )

    @classmethod
    def to_grpc_delete_message_request(cls, request: DeleteMessageRequest):
        return pb2_module.DeleteMessageRequest(
            message_id=str(request.message_id),
            deleter_id=str(request.deleter_id),
        )

    @classmethod
    def to_grpc_get_messages_request(cls, request: GetMessagesRequest):
        pagination = PaginationRequest(
            page=1,
            page_size=request.limit,
            before_timestamp=request.before_timestamp,
        )
        return pb2_module.ListMessagesRequest(
            chat_id=str(request.chat_id),
            pagination=cls.to_grpc_pagination(pagination),
        )

    @classmethod
    def to_grpc_mark_as_read_request(cls, request: MarkAsReadRequest):
        return pb2_module.MarkAsReadRequest(
            message_id=str(request.message_id),
            user_id=str(request.user_id),
        )

    @classmethod
    def to_grpc_unread_count_request(cls, request: GetUnreadCountRequest):
        return pb2_module.GetUnreadCountRequest(
            chat_id=str(request.chat_id),
            user_id=str(request.user_id),
        )

    @classmethod
    def to_grpc_add_reaction_request(cls, request: AddReactionRequest):
        return pb2_module.AddReactionRequest(
            message_id=str(request.message_id),
            user_id=str(request.user_id),
            emote_id=request.emote_id,
        )

    @classmethod
    def to_grpc_remove_reaction_request(cls, request: RemoveReactionRequest):
        return pb2_module.RemoveReactionRequest(
            message_id=str(request.message_id),
            user_id=str(request.user_id),
            emote_id=request.emote_id,
        )

    @classmethod
    def to_grpc_get_reactions_request(cls, request: GetReactionsRequest):
        return pb2_module.GetReactionsRequest(message_id=str(request.message_id))

    @classmethod
    def to_grpc_message_history_request(cls, request: GetMessageHistoryRequest):
        return pb2_module.GetMessageHistoryRequest(
            message_id=str(request.message_id),
            limit=request.limit,
        )

    @classmethod
    def to_grpc_user_messages_request(cls, request: GetUserMessagesRequest):
        grpc_request = pb2_module.GetUserMessagesRequest(
            user_id=str(request.user_id),
            pagination=cls.to_grpc_pagination(request.pagination),
        )
        if request.chat_id:
            grpc_request.chat_id = str(request.chat_id)
        return grpc_request


class MessengerStub:
    def __init__(self, channel: grpc.Channel):
        self.channel = channel
        self.chat_stub = pb2_grpc_module.ChatServiceStub(channel)
        self.message_stub = pb2_grpc_module.MessageServiceStub(channel)
        self.mapper = MessengerMapper()

    async def create_chat(self, request: CreateChatRequest) -> ChatResponse:
        response = await self.chat_stub.CreateChat(
            self.mapper.to_grpc_create_chat_request(request)
        )
        return self.mapper.to_pydantic_chat_response(response)

    async def get_chat(self, request: GetChatRequest) -> ChatResponse:
        response = await self.chat_stub.GetChat(
            self.mapper.to_grpc_get_chat_request(request)
        )
        return self.mapper.to_pydantic_chat_response(response)

    async def update_chat(self, request: UpdateChatRequest) -> ChatResponse:
        response = await self.chat_stub.UpdateChat(
            self.mapper.to_grpc_update_chat_request(request)
        )
        return self.mapper.to_pydantic_chat_response(response)

    async def delete_chat(self, request: DeleteChatRequest):
        return await self.chat_stub.DeleteChat(
            self.mapper.to_grpc_delete_chat_request(request)
        )

    async def list_chats(self, request: ListChatsRequest) -> ListChatsResponse:
        response = await self.chat_stub.ListChats(
            self.mapper.to_grpc_list_chats_request(request)
        )
        return self.mapper.to_pydantic_list_chats_response(response)

    async def add_allowed_user(self, request: AddAllowedUserRequest) -> ChatResponse:
        response = await self.chat_stub.AddAllowedUser(
            self.mapper.to_grpc_add_allowed_user_request(request)
        )
        return self.mapper.to_pydantic_chat_response(response)

    async def remove_allowed_user(
        self, request: RemoveAllowedUserRequest
    ) -> ChatResponse:
        response = await self.chat_stub.RemoveAllowedUser(
            self.mapper.to_grpc_remove_allowed_user_request(request)
        )
        return self.mapper.to_pydantic_chat_response(response)

    async def freeze_chat(self, request: FreezeChatRequest) -> ChatResponse:
        response = await self.chat_stub.FreezeChat(
            self.mapper.to_grpc_freeze_chat_request(request)
        )
        return self.mapper.to_pydantic_chat_response(response)

    async def unfreeze_chat(self, request: UnfreezeChatRequest) -> ChatResponse:
        response = await self.chat_stub.UnfreezeChat(
            self.mapper.to_grpc_unfreeze_chat_request(request)
        )
        return self.mapper.to_pydantic_chat_response(response)

    async def get_user_chats(self, request: GetUserChatsRequest) -> GetUserChatsResponse:
        response = await self.chat_stub.GetUserChats(
            self.mapper.to_grpc_get_user_chats_request(request)
        )
        return self.mapper.to_pydantic_get_user_chats_response(response)

    async def get_chat_members(
        self, request: GetChatMembersRequest
    ) -> GetChatMembersResponse:
        response = await self.chat_stub.GetChatMembers(
            self.mapper.to_grpc_get_chat_members_request(request)
        )
        return self.mapper.to_pydantic_chat_members_response(response)

    async def is_chat_member(
        self, request: IsChatMemberRequest
    ) -> IsChatMemberResponse:
        response = await self.chat_stub.IsChatMember(
            self.mapper.to_grpc_is_chat_member_request(request)
        )
        return IsChatMemberResponse(is_member=response.is_member)

    async def send_message(self, request: SendMessageRequest) -> MessageResponse:
        response = await self.message_stub.SendMessage(
            self.mapper.to_grpc_send_message_request(request)
        )
        return self.mapper.to_pydantic_message_response(response)

    async def get_message(self, request: GetMessageRequest) -> MessageResponse:
        response = await self.message_stub.GetMessage(
            self.mapper.to_grpc_get_message_request(request)
        )
        return self.mapper.to_pydantic_message_response(response)

    async def update_message(self, request: UpdateMessageRequest) -> MessageResponse:
        response = await self.message_stub.UpdateMessage(
            self.mapper.to_grpc_update_message_request(request)
        )
        return self.mapper.to_pydantic_message_response(response)

    async def delete_message(self, request: DeleteMessageRequest):
        return await self.message_stub.DeleteMessage(
            self.mapper.to_grpc_delete_message_request(request)
        )

    async def get_messages(self, request: GetMessagesRequest) -> GetMessagesResponse:
        response = await self.message_stub.ListMessages(
            self.mapper.to_grpc_get_messages_request(request)
        )
        return self.mapper.to_pydantic_messages_response(response)

    async def mark_as_read(self, request: MarkAsReadRequest) -> MessageResponse:
        response = await self.message_stub.MarkAsRead(
            self.mapper.to_grpc_mark_as_read_request(request)
        )
        return self.mapper.to_pydantic_message_response(response)

    async def get_unread_count(
        self, request: GetUnreadCountRequest
    ) -> GetUnreadCountResponse:
        response = await self.message_stub.GetUnreadCount(
            self.mapper.to_grpc_unread_count_request(request)
        )
        return GetUnreadCountResponse(count=response.count)

    async def add_reaction(self, request: AddReactionRequest) -> MessageResponse:
        response = await self.message_stub.AddReaction(
            self.mapper.to_grpc_add_reaction_request(request)
        )
        return self.mapper.to_pydantic_message_response(response)

    async def remove_reaction(self, request: RemoveReactionRequest) -> MessageResponse:
        response = await self.message_stub.RemoveReaction(
            self.mapper.to_grpc_remove_reaction_request(request)
        )
        return self.mapper.to_pydantic_message_response(response)

    async def get_reactions(self, request: GetReactionsRequest) -> GetReactionsResponse:
        response = await self.message_stub.GetReactions(
            self.mapper.to_grpc_get_reactions_request(request)
        )
        return self.mapper.to_pydantic_reactions_response(response)

    async def get_message_history(
        self, request: GetMessageHistoryRequest
    ) -> GetMessagesResponse:
        response = await self.message_stub.GetMessageHistory(
            self.mapper.to_grpc_message_history_request(request)
        )
        return self.mapper.to_pydantic_messages_response(response)

    async def get_user_messages(
        self, request: GetUserMessagesRequest
    ) -> GetMessagesResponse:
        response = await self.message_stub.GetUserMessages(
            self.mapper.to_grpc_user_messages_request(request)
        )
        return self.mapper.to_pydantic_messages_response(response)

    def create_chat_sync(self, request: CreateChatRequest) -> ChatResponse:
        response = self.chat_stub.CreateChat(
            self.mapper.to_grpc_create_chat_request(request)
        )
        return self.mapper.to_pydantic_chat_response(response)

    def get_chat_sync(self, request: GetChatRequest) -> ChatResponse:
        response = self.chat_stub.GetChat(self.mapper.to_grpc_get_chat_request(request))
        return self.mapper.to_pydantic_chat_response(response)
