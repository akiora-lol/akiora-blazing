from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field
from uuid import UUID


class ChatOwnerType(str, Enum):
    OWNER_UNSPECIFIED = "OWNER_UNSPECIFIED"
    SYSTEM = "SYSTEM"
    CLUB = "CLUB"
    TOURNAMENT = "TOURNAMENT"
    GAMESERIES = "GAMESERIES"


class ChatType(str, Enum):
    CHAT_TYPE_UNSPECIFIED = "CHAT_TYPE_UNSPECIFIED"
    PRIVATE = "PRIVATE"
    PUBLIC = "PUBLIC"


class ChatStatus(str, Enum):
    CHAT_STATUS_UNSPECIFIED = "CHAT_STATUS_UNSPECIFIED"
    ACTIVE = "ACTIVE"
    FROZEN = "FROZEN"


class MessageStatus(str, Enum):
    MESSAGE_STATUS_UNSPECIFIED = "MESSAGE_STATUS_UNSPECIFIED"
    SENT = "SENT"
    READ = "READ"


class PaginationRequest(BaseModel):
    page: int = 1
    page_size: int = 50
    before_timestamp: Optional[int] = None


class Reaction(BaseModel):
    emote_id: str
    user_id: str
    timestamp: Optional[int] = None


class MessageShort(BaseModel):
    body: str
    timestamp: int


class ChatResponse(BaseModel):
    id: UUID
    owner_id: UUID
    owner_type: ChatOwnerType
    type: ChatType
    status: ChatStatus
    timestamp: int
    allowed_users: List[str] = Field(default_factory=list)

    class Config:
        from_attributes = True


class CreateChatRequest(BaseModel):
    owner_id: UUID
    owner_type: ChatOwnerType
    type: ChatType
    allowed_users: List[str] = Field(default_factory=list)


class GetChatRequest(BaseModel):
    chat_id: UUID


class UpdateChatRequest(BaseModel):
    chat_id: UUID
    actor_id: UUID
    status: Optional[ChatStatus] = None
    owner_id: Optional[UUID] = None


class DeleteChatRequest(BaseModel):
    chat_id: UUID
    actor_id: UUID


class AddAllowedUserRequest(BaseModel):
    chat_id: UUID
    actor_id: Optional[UUID] = None
    user_id: UUID


class RemoveAllowedUserRequest(BaseModel):
    chat_id: UUID
    actor_id: Optional[UUID] = None
    user_id: UUID


class FreezeChatRequest(BaseModel):
    chat_id: UUID
    actor_id: Optional[UUID] = None


class UnfreezeChatRequest(BaseModel):
    chat_id: UUID
    actor_id: Optional[UUID] = None


class ChatFilter(BaseModel):
    owner_id: Optional[UUID] = None
    owner_type: Optional[ChatOwnerType] = None
    type: Optional[ChatType] = None
    status: Optional[ChatStatus] = None
    is_member: bool = False


class ListChatsRequest(BaseModel):
    filter: ChatFilter = Field(default_factory=ChatFilter)
    pagination: PaginationRequest = Field(default_factory=PaginationRequest)


class ListChatsResponse(BaseModel):
    chats: List[ChatResponse] = Field(default_factory=list)
    total_count: int = 0
    page: int = 1
    page_size: int = 50
    has_next: bool = False


class ChatMemberInfo(BaseModel):
    user_id: str
    nickname: Optional[str] = None
    avatar: Optional[str] = None


class GetChatMembersRequest(BaseModel):
    chat_id: UUID
    pagination: PaginationRequest = Field(default_factory=PaginationRequest)


class GetChatMembersResponse(BaseModel):
    members: List[ChatMemberInfo] = Field(default_factory=list)
    total_count: int = 0


class IsChatMemberRequest(BaseModel):
    chat_id: UUID
    user_id: UUID


class IsChatMemberResponse(BaseModel):
    is_member: bool = False


class MessageResponse(BaseModel):
    id: UUID
    chat_id: UUID
    creator_id: UUID
    body: str
    status: MessageStatus
    read_by: List[str] = Field(default_factory=list)
    timestamp: int
    history: List[MessageShort] = Field(default_factory=list)
    reply_to: Optional[str] = None
    reactions: List[Reaction] = Field(default_factory=list)
    spoiler: bool = False

    class Config:
        from_attributes = True


class SendMessageRequest(BaseModel):
    chat_id: UUID
    creator_id: UUID
    body: str
    reply_to: Optional[str] = None
    spoiler: bool = False


class UpdateMessageRequest(BaseModel):
    message_id: UUID
    editor_id: UUID
    new_body: str


class DeleteMessageRequest(BaseModel):
    message_id: UUID
    deleter_id: UUID


class MarkAsReadRequest(BaseModel):
    message_id: UUID
    user_id: UUID


class AddReactionRequest(BaseModel):
    message_id: UUID
    user_id: UUID
    emote_id: str


class RemoveReactionRequest(BaseModel):
    message_id: UUID
    user_id: UUID
    emote_id: str


class GetMessagesRequest(BaseModel):
    chat_id: UUID
    limit: int = 50
    before_timestamp: Optional[int] = None


class GetMessagesResponse(BaseModel):
    messages: List[MessageResponse] = Field(default_factory=list)
    total_count: int = 0


class GetUserChatsRequest(BaseModel):
    user_id: UUID
    pagination: PaginationRequest = Field(default_factory=PaginationRequest)


class GetUserChatsResponse(BaseModel):
    chats: List[ChatResponse] = Field(default_factory=list)
    total_count: int = 0
    page: int = 1
    page_size: int = 50
    has_next: bool = False


class GetMessageRequest(BaseModel):
    message_id: UUID


class GetUnreadCountRequest(BaseModel):
    chat_id: UUID
    user_id: UUID


class GetUnreadCountResponse(BaseModel):
    count: int = 0


class GetReactionsRequest(BaseModel):
    message_id: UUID


class GetReactionsResponse(BaseModel):
    reactions: List[Reaction] = Field(default_factory=list)


class GetMessageHistoryRequest(BaseModel):
    message_id: UUID
    limit: int = 50


class MessageFilter(BaseModel):
    creator_id: Optional[UUID] = None
    status: Optional[MessageStatus] = None
    has_reactions: bool = False


class GetUserMessagesRequest(BaseModel):
    user_id: UUID
    pagination: PaginationRequest = Field(default_factory=PaginationRequest)
    chat_id: Optional[UUID] = None
