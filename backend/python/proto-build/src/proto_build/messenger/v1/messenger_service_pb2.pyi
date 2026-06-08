from google.api import annotations_pb2 as _annotations_pb2
from common import types_pb2 as _types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChatOwnerType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OWNER_UNSPECIFIED: _ClassVar[ChatOwnerType]
    SYSTEM: _ClassVar[ChatOwnerType]
    CLUB: _ClassVar[ChatOwnerType]
    TOURNAMENT: _ClassVar[ChatOwnerType]
    GAMESERIES: _ClassVar[ChatOwnerType]

class ChatType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CHAT_TYPE_UNSPECIFIED: _ClassVar[ChatType]
    PRIVATE: _ClassVar[ChatType]
    PUBLIC: _ClassVar[ChatType]

class ChatStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CHAT_STATUS_UNSPECIFIED: _ClassVar[ChatStatus]
    ACTIVE: _ClassVar[ChatStatus]
    FROZEN: _ClassVar[ChatStatus]

class MessageStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MESSAGE_STATUS_UNSPECIFIED: _ClassVar[MessageStatus]
    SENT: _ClassVar[MessageStatus]
    READ: _ClassVar[MessageStatus]
OWNER_UNSPECIFIED: ChatOwnerType
SYSTEM: ChatOwnerType
CLUB: ChatOwnerType
TOURNAMENT: ChatOwnerType
GAMESERIES: ChatOwnerType
CHAT_TYPE_UNSPECIFIED: ChatType
PRIVATE: ChatType
PUBLIC: ChatType
CHAT_STATUS_UNSPECIFIED: ChatStatus
ACTIVE: ChatStatus
FROZEN: ChatStatus
MESSAGE_STATUS_UNSPECIFIED: MessageStatus
SENT: MessageStatus
READ: MessageStatus

class ChatResponse(_message.Message):
    __slots__ = ("id", "owner_id", "owner_type", "type", "status", "timestamp", "allowed_users")
    ID_FIELD_NUMBER: _ClassVar[int]
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    OWNER_TYPE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_USERS_FIELD_NUMBER: _ClassVar[int]
    id: str
    owner_id: str
    owner_type: ChatOwnerType
    type: ChatType
    status: ChatStatus
    timestamp: int
    allowed_users: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., owner_id: _Optional[str] = ..., owner_type: _Optional[_Union[ChatOwnerType, str]] = ..., type: _Optional[_Union[ChatType, str]] = ..., status: _Optional[_Union[ChatStatus, str]] = ..., timestamp: _Optional[int] = ..., allowed_users: _Optional[_Iterable[str]] = ...) -> None: ...

class PaginationRequest(_message.Message):
    __slots__ = ("page", "page_size", "before_timestamp")
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    BEFORE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    page: int
    page_size: int
    before_timestamp: int
    def __init__(self, page: _Optional[int] = ..., page_size: _Optional[int] = ..., before_timestamp: _Optional[int] = ...) -> None: ...

class ChatFilter(_message.Message):
    __slots__ = ("owner_id", "owner_type", "type", "status", "is_member")
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    OWNER_TYPE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    IS_MEMBER_FIELD_NUMBER: _ClassVar[int]
    owner_id: str
    owner_type: ChatOwnerType
    type: ChatType
    status: ChatStatus
    is_member: bool
    def __init__(self, owner_id: _Optional[str] = ..., owner_type: _Optional[_Union[ChatOwnerType, str]] = ..., type: _Optional[_Union[ChatType, str]] = ..., status: _Optional[_Union[ChatStatus, str]] = ..., is_member: bool = ...) -> None: ...

class ListChatsRequest(_message.Message):
    __slots__ = ("filter", "pagination")
    FILTER_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    filter: ChatFilter
    pagination: PaginationRequest
    def __init__(self, filter: _Optional[_Union[ChatFilter, _Mapping]] = ..., pagination: _Optional[_Union[PaginationRequest, _Mapping]] = ...) -> None: ...

class ListChatsResponse(_message.Message):
    __slots__ = ("chats", "total_count", "page", "page_size", "has_next")
    CHATS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    HAS_NEXT_FIELD_NUMBER: _ClassVar[int]
    chats: _containers.RepeatedCompositeFieldContainer[ChatResponse]
    total_count: int
    page: int
    page_size: int
    has_next: bool
    def __init__(self, chats: _Optional[_Iterable[_Union[ChatResponse, _Mapping]]] = ..., total_count: _Optional[int] = ..., page: _Optional[int] = ..., page_size: _Optional[int] = ..., has_next: bool = ...) -> None: ...

class ChatMemberInfo(_message.Message):
    __slots__ = ("user_id", "nickname", "avatar")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    AVATAR_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    nickname: str
    avatar: str
    def __init__(self, user_id: _Optional[str] = ..., nickname: _Optional[str] = ..., avatar: _Optional[str] = ...) -> None: ...

class GetChatMembersRequest(_message.Message):
    __slots__ = ("chat_id", "pagination")
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    chat_id: str
    pagination: PaginationRequest
    def __init__(self, chat_id: _Optional[str] = ..., pagination: _Optional[_Union[PaginationRequest, _Mapping]] = ...) -> None: ...

class GetChatMembersResponse(_message.Message):
    __slots__ = ("members", "total_count")
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    members: _containers.RepeatedCompositeFieldContainer[ChatMemberInfo]
    total_count: int
    def __init__(self, members: _Optional[_Iterable[_Union[ChatMemberInfo, _Mapping]]] = ..., total_count: _Optional[int] = ...) -> None: ...

class IsChatMemberRequest(_message.Message):
    __slots__ = ("chat_id", "user_id")
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    chat_id: str
    user_id: str
    def __init__(self, chat_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class IsChatMemberResponse(_message.Message):
    __slots__ = ("is_member",)
    IS_MEMBER_FIELD_NUMBER: _ClassVar[int]
    is_member: bool
    def __init__(self, is_member: bool = ...) -> None: ...

class CreateChatRequest(_message.Message):
    __slots__ = ("owner_id", "owner_type", "type", "allowed_users")
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    OWNER_TYPE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_USERS_FIELD_NUMBER: _ClassVar[int]
    owner_id: str
    owner_type: ChatOwnerType
    type: ChatType
    allowed_users: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, owner_id: _Optional[str] = ..., owner_type: _Optional[_Union[ChatOwnerType, str]] = ..., type: _Optional[_Union[ChatType, str]] = ..., allowed_users: _Optional[_Iterable[str]] = ...) -> None: ...

class GetChatRequest(_message.Message):
    __slots__ = ("chat_id",)
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    chat_id: str
    def __init__(self, chat_id: _Optional[str] = ...) -> None: ...

class UpdateChatRequest(_message.Message):
    __slots__ = ("chat_id", "actor_id", "status", "owner_id")
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    ACTOR_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    chat_id: str
    actor_id: str
    status: ChatStatus
    owner_id: str
    def __init__(self, chat_id: _Optional[str] = ..., actor_id: _Optional[str] = ..., status: _Optional[_Union[ChatStatus, str]] = ..., owner_id: _Optional[str] = ...) -> None: ...

class DeleteChatRequest(_message.Message):
    __slots__ = ("chat_id", "actor_id")
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    ACTOR_ID_FIELD_NUMBER: _ClassVar[int]
    chat_id: str
    actor_id: str
    def __init__(self, chat_id: _Optional[str] = ..., actor_id: _Optional[str] = ...) -> None: ...

class AddAllowedUserRequest(_message.Message):
    __slots__ = ("chat_id", "actor_id", "user_id")
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    ACTOR_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    chat_id: str
    actor_id: str
    user_id: str
    def __init__(self, chat_id: _Optional[str] = ..., actor_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class RemoveAllowedUserRequest(_message.Message):
    __slots__ = ("chat_id", "actor_id", "user_id")
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    ACTOR_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    chat_id: str
    actor_id: str
    user_id: str
    def __init__(self, chat_id: _Optional[str] = ..., actor_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class FreezeChatRequest(_message.Message):
    __slots__ = ("chat_id", "actor_id")
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    ACTOR_ID_FIELD_NUMBER: _ClassVar[int]
    chat_id: str
    actor_id: str
    def __init__(self, chat_id: _Optional[str] = ..., actor_id: _Optional[str] = ...) -> None: ...

class UnfreezeChatRequest(_message.Message):
    __slots__ = ("chat_id", "actor_id")
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    ACTOR_ID_FIELD_NUMBER: _ClassVar[int]
    chat_id: str
    actor_id: str
    def __init__(self, chat_id: _Optional[str] = ..., actor_id: _Optional[str] = ...) -> None: ...

class GetUserChatsRequest(_message.Message):
    __slots__ = ("user_id", "pagination")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    pagination: PaginationRequest
    def __init__(self, user_id: _Optional[str] = ..., pagination: _Optional[_Union[PaginationRequest, _Mapping]] = ...) -> None: ...

class ReactionProto(_message.Message):
    __slots__ = ("emote_id", "user_id", "timestamp")
    EMOTE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    emote_id: str
    user_id: str
    timestamp: int
    def __init__(self, emote_id: _Optional[str] = ..., user_id: _Optional[str] = ..., timestamp: _Optional[int] = ...) -> None: ...

class MessageShortProto(_message.Message):
    __slots__ = ("body", "timestamp")
    BODY_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    body: str
    timestamp: int
    def __init__(self, body: _Optional[str] = ..., timestamp: _Optional[int] = ...) -> None: ...

class MessageResponse(_message.Message):
    __slots__ = ("id", "chat_id", "creator_id", "body", "status", "read_by", "timestamp", "history", "reply_to", "reactions", "spoiler")
    ID_FIELD_NUMBER: _ClassVar[int]
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    CREATOR_ID_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    READ_BY_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    HISTORY_FIELD_NUMBER: _ClassVar[int]
    REPLY_TO_FIELD_NUMBER: _ClassVar[int]
    REACTIONS_FIELD_NUMBER: _ClassVar[int]
    SPOILER_FIELD_NUMBER: _ClassVar[int]
    id: str
    chat_id: str
    creator_id: str
    body: str
    status: MessageStatus
    read_by: _containers.RepeatedScalarFieldContainer[str]
    timestamp: int
    history: _containers.RepeatedCompositeFieldContainer[MessageShortProto]
    reply_to: str
    reactions: _containers.RepeatedCompositeFieldContainer[ReactionProto]
    spoiler: bool
    def __init__(self, id: _Optional[str] = ..., chat_id: _Optional[str] = ..., creator_id: _Optional[str] = ..., body: _Optional[str] = ..., status: _Optional[_Union[MessageStatus, str]] = ..., read_by: _Optional[_Iterable[str]] = ..., timestamp: _Optional[int] = ..., history: _Optional[_Iterable[_Union[MessageShortProto, _Mapping]]] = ..., reply_to: _Optional[str] = ..., reactions: _Optional[_Iterable[_Union[ReactionProto, _Mapping]]] = ..., spoiler: bool = ...) -> None: ...

class MessageFilter(_message.Message):
    __slots__ = ("creator_id", "status", "has_reactions")
    CREATOR_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    HAS_REACTIONS_FIELD_NUMBER: _ClassVar[int]
    creator_id: str
    status: MessageStatus
    has_reactions: bool
    def __init__(self, creator_id: _Optional[str] = ..., status: _Optional[_Union[MessageStatus, str]] = ..., has_reactions: bool = ...) -> None: ...

class ListMessagesRequest(_message.Message):
    __slots__ = ("chat_id", "filter", "pagination")
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    chat_id: str
    filter: MessageFilter
    pagination: PaginationRequest
    def __init__(self, chat_id: _Optional[str] = ..., filter: _Optional[_Union[MessageFilter, _Mapping]] = ..., pagination: _Optional[_Union[PaginationRequest, _Mapping]] = ...) -> None: ...

class ListMessagesResponse(_message.Message):
    __slots__ = ("messages", "total_count")
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    messages: _containers.RepeatedCompositeFieldContainer[MessageResponse]
    total_count: int
    def __init__(self, messages: _Optional[_Iterable[_Union[MessageResponse, _Mapping]]] = ..., total_count: _Optional[int] = ...) -> None: ...

class SendMessageRequest(_message.Message):
    __slots__ = ("chat_id", "creator_id", "body", "reply_to", "spoiler")
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    CREATOR_ID_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    REPLY_TO_FIELD_NUMBER: _ClassVar[int]
    SPOILER_FIELD_NUMBER: _ClassVar[int]
    chat_id: str
    creator_id: str
    body: str
    reply_to: str
    spoiler: bool
    def __init__(self, chat_id: _Optional[str] = ..., creator_id: _Optional[str] = ..., body: _Optional[str] = ..., reply_to: _Optional[str] = ..., spoiler: bool = ...) -> None: ...

class UpdateMessageRequest(_message.Message):
    __slots__ = ("message_id", "editor_id", "new_body")
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    EDITOR_ID_FIELD_NUMBER: _ClassVar[int]
    NEW_BODY_FIELD_NUMBER: _ClassVar[int]
    message_id: str
    editor_id: str
    new_body: str
    def __init__(self, message_id: _Optional[str] = ..., editor_id: _Optional[str] = ..., new_body: _Optional[str] = ...) -> None: ...

class DeleteMessageRequest(_message.Message):
    __slots__ = ("message_id", "deleter_id")
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    DELETER_ID_FIELD_NUMBER: _ClassVar[int]
    message_id: str
    deleter_id: str
    def __init__(self, message_id: _Optional[str] = ..., deleter_id: _Optional[str] = ...) -> None: ...

class MarkAsReadRequest(_message.Message):
    __slots__ = ("message_id", "user_id")
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    message_id: str
    user_id: str
    def __init__(self, message_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class GetUnreadCountRequest(_message.Message):
    __slots__ = ("chat_id", "user_id")
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    chat_id: str
    user_id: str
    def __init__(self, chat_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class GetUnreadCountResponse(_message.Message):
    __slots__ = ("count",)
    COUNT_FIELD_NUMBER: _ClassVar[int]
    count: int
    def __init__(self, count: _Optional[int] = ...) -> None: ...

class AddReactionRequest(_message.Message):
    __slots__ = ("message_id", "user_id", "emote_id")
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    EMOTE_ID_FIELD_NUMBER: _ClassVar[int]
    message_id: str
    user_id: str
    emote_id: str
    def __init__(self, message_id: _Optional[str] = ..., user_id: _Optional[str] = ..., emote_id: _Optional[str] = ...) -> None: ...

class RemoveReactionRequest(_message.Message):
    __slots__ = ("message_id", "user_id", "emote_id")
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    EMOTE_ID_FIELD_NUMBER: _ClassVar[int]
    message_id: str
    user_id: str
    emote_id: str
    def __init__(self, message_id: _Optional[str] = ..., user_id: _Optional[str] = ..., emote_id: _Optional[str] = ...) -> None: ...

class GetReactionsRequest(_message.Message):
    __slots__ = ("message_id",)
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    message_id: str
    def __init__(self, message_id: _Optional[str] = ...) -> None: ...

class GetReactionsResponse(_message.Message):
    __slots__ = ("reactions",)
    REACTIONS_FIELD_NUMBER: _ClassVar[int]
    reactions: _containers.RepeatedCompositeFieldContainer[ReactionProto]
    def __init__(self, reactions: _Optional[_Iterable[_Union[ReactionProto, _Mapping]]] = ...) -> None: ...

class GetMessageHistoryRequest(_message.Message):
    __slots__ = ("message_id", "limit")
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    message_id: str
    limit: int
    def __init__(self, message_id: _Optional[str] = ..., limit: _Optional[int] = ...) -> None: ...

class GetMessageRequest(_message.Message):
    __slots__ = ("message_id",)
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    message_id: str
    def __init__(self, message_id: _Optional[str] = ...) -> None: ...

class GetUserMessagesRequest(_message.Message):
    __slots__ = ("user_id", "pagination", "chat_id")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    pagination: PaginationRequest
    chat_id: str
    def __init__(self, user_id: _Optional[str] = ..., pagination: _Optional[_Union[PaginationRequest, _Mapping]] = ..., chat_id: _Optional[str] = ...) -> None: ...
