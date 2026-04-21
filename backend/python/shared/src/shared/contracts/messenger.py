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


class Reaction(BaseModel):
    emote_id: str
    user_id: str


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


class AddAllowedUserRequest(BaseModel):
    chat_id: UUID
    user_id: UUID


class RemoveAllowedUserRequest(BaseModel):
    chat_id: UUID
    user_id: UUID


class FreezeChatRequest(BaseModel):
    chat_id: UUID


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
