import grpc
from uuid import UUID

from shared.contracts.messenger import (
    ChatResponse,
    CreateChatRequest,
    GetChatRequest,
    AddAllowedUserRequest,
    RemoveAllowedUserRequest,
    FreezeChatRequest,
    MessageResponse,
    SendMessageRequest,
    UpdateMessageRequest,
    DeleteMessageRequest,
    MarkAsReadRequest,
    AddReactionRequest,
    RemoveReactionRequest,
    GetMessagesRequest,
    GetMessagesResponse,
    ChatOwnerType,
    ChatType,
    ChatStatus,
    MessageStatus,
    Reaction,
    MessageShort,
)

import messenger.v1.messenger_service_pb2 as pb2_module
import messenger.v1.messenger_service_pb2_grpc as pb2_grpc_module


class MessengerMapper:
    """Mapper between gRPC protobuf messages and Pydantic models for Messenger service"""

    CHAT_OWNER_TYPE_MAP = {
        0: ChatOwnerType.OWNER_UNSPECIFIED,
        1: ChatOwnerType.SYSTEM,
        2: ChatOwnerType.CLUB,
        3: ChatOwnerType.TOURNAMENT,
        4: ChatOwnerType.GAMESERIES,
    }

    CHAT_OWNER_TYPE_TO_PROTO = {v: k for k, v in CHAT_OWNER_TYPE_MAP.items()}

    CHAT_TYPE_MAP = {
        0: ChatType.CHAT_TYPE_UNSPECIFIED,
        1: ChatType.PRIVATE,
        2: ChatType.PUBLIC,
    }

    CHAT_TYPE_TO_PROTO = {v: k for k, v in CHAT_TYPE_MAP.items()}

    CHAT_STATUS_MAP = {
        0: ChatStatus.CHAT_STATUS_UNSPECIFIED,
        1: ChatStatus.ACTIVE,
        2: ChatStatus.FROZEN,
    }

    MESSAGE_STATUS_MAP = {
        0: MessageStatus.MESSAGE_STATUS_UNSPECIFIED,
        1: MessageStatus.SENT,
        2: MessageStatus.READ,
    }

    @classmethod
    def to_pydantic_chat_response(cls, grpc_response) -> ChatResponse:
        return ChatResponse(
            id=UUID(grpc_response.id),
            owner_id=UUID(grpc_response.owner_id),
            owner_type=cls.CHAT_OWNER_TYPE_MAP.get(
                grpc_response.owner_type, ChatOwnerType.OWNER_UNSPECIFIED
            ),
            type=cls.CHAT_TYPE_MAP.get(grpc_response.type, ChatType.CHAT_TYPE_UNSPECIFIED),
            status=cls.CHAT_STATUS_MAP.get(
                grpc_response.status, ChatStatus.CHAT_STATUS_UNSPECIFIED
            ),
            timestamp=grpc_response.timestamp,
            allowed_users=list(grpc_response.allowed_users),
        )

    @classmethod
    def to_pydantic_message_response(cls, grpc_response) -> MessageResponse:
        history = [
            MessageShort(body=h.body, timestamp=h.timestamp) for h in grpc_response.history
        ]
        reactions = [
            Reaction(emote_id=r.emote_id, user_id=r.user_id)
            for r in grpc_response.reactions
        ]

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
            history=history,
            reply_to=grpc_response.reply_to if grpc_response.reply_to else None,
            reactions=reactions,
            spoiler=grpc_response.spoiler,
        )

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
    def to_grpc_send_message_request(cls, request: SendMessageRequest):
        return pb2_module.SendMessageRequest(
            chat_id=str(request.chat_id),
            creator_id=str(request.creator_id),
            body=request.body,
            reply_to=request.reply_to or "",
            spoiler=request.spoiler,
        )

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
        grpc_request = pb2_module.GetMessagesRequest(
            chat_id=str(request.chat_id),
            limit=request.limit,
        )
        if request.before_timestamp:
            grpc_request.before_timestamp = request.before_timestamp
        return grpc_request


class MessengerStub:
    """Stub for Messenger Service gRPC calls with pydantic mapping"""

    def __init__(self, channel: grpc.Channel):
        self.channel = channel
        self.stub = pb2_grpc_module.MessengerServiceStub(channel)
        self.mapper = MessengerMapper()

    async def create_chat(self, request: CreateChatRequest) -> ChatResponse:
        grpc_request = self.mapper.to_grpc_create_chat_request(request)
        response = await self.stub.CreateChat(grpc_request)
        return self.mapper.to_pydantic_chat_response(response)

    async def get_chat(self, request: GetChatRequest) -> ChatResponse:
        grpc_request = self.mapper.to_grpc_get_chat_request(request)
        response = await self.stub.GetChat(grpc_request)
        return self.mapper.to_pydantic_chat_response(response)

    async def send_message(self, request: SendMessageRequest) -> MessageResponse:
        grpc_request = self.mapper.to_grpc_send_message_request(request)
        response = await self.stub.SendMessage(grpc_request)
        return self.mapper.to_pydantic_message_response(response)

    async def update_message(self, request: UpdateMessageRequest) -> MessageResponse:
        grpc_request = self.mapper.to_grpc_update_message_request(request)
        response = await self.stub.UpdateMessage(grpc_request)
        return self.mapper.to_pydantic_message_response(response)

    async def delete_message(self, request: DeleteMessageRequest) -> MessageResponse:
        grpc_request = self.mapper.to_grpc_delete_message_request(request)
        response = await self.stub.DeleteMessage(grpc_request)
        return self.mapper.to_pydantic_message_response(response)

    async def get_messages(self, request: GetMessagesRequest) -> GetMessagesResponse:
        grpc_request = self.mapper.to_grpc_get_messages_request(request)
        response = await self.stub.GetMessages(grpc_request)
        messages = [
            self.mapper.to_pydantic_message_response(m) for m in response.messages
        ]
        return GetMessagesResponse(messages=messages)

    def create_chat_sync(self, request: CreateChatRequest) -> ChatResponse:
        grpc_request = self.mapper.to_grpc_create_chat_request(request)
        response = self.stub.CreateChat(grpc_request)
        return self.mapper.to_pydantic_chat_response(response)

    def get_chat_sync(self, request: GetChatRequest) -> ChatResponse:
        grpc_request = self.mapper.to_grpc_get_chat_request(request)
        response = self.stub.GetChat(grpc_request)
        return self.mapper.to_pydantic_chat_response(response)
