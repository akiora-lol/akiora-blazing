from google.api import annotations_pb2 as _annotations_pb2
from google.api import http_pb2 as _http_pb2
from common import game_actors_pb2 as _game_actors_pb2
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

class AddAllowedUserRequest(_message.Message):
    __slots__ = ("chat_id", "user_id")
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    chat_id: str
    user_id: str
    def __init__(self, chat_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class RemoveAllowedUserRequest(_message.Message):
    __slots__ = ("chat_id", "user_id")
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    chat_id: str
    user_id: str
    def __init__(self, chat_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class FreezeChatRequest(_message.Message):
    __slots__ = ("chat_id",)
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    chat_id: str
    def __init__(self, chat_id: _Optional[str] = ...) -> None: ...

class ReactionProto(_message.Message):
    __slots__ = ("emote_id", "user_id")
    EMOTE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    emote_id: str
    user_id: str
    def __init__(self, emote_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

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

class GetMessagesRequest(_message.Message):
    __slots__ = ("chat_id", "limit", "before_timestamp")
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    BEFORE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    chat_id: str
    limit: int
    before_timestamp: int
    def __init__(self, chat_id: _Optional[str] = ..., limit: _Optional[int] = ..., before_timestamp: _Optional[int] = ...) -> None: ...

class GetMessagesResponse(_message.Message):
    __slots__ = ("messages",)
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    messages: _containers.RepeatedCompositeFieldContainer[MessageResponse]
    def __init__(self, messages: _Optional[_Iterable[_Union[MessageResponse, _Mapping]]] = ...) -> None: ...
