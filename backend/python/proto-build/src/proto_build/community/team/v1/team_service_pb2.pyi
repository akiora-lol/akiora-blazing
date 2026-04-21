from google.api import annotations_pb2 as _annotations_pb2
from google.api import http_pb2 as _http_pb2
from common import types_pb2 as _types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class TeamResponse(_message.Message):
    __slots__ = ("id", "owner_id", "name", "avatar", "tag", "members", "created_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    AVATAR_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    owner_id: str
    name: str
    avatar: str
    tag: str
    members: _containers.RepeatedScalarFieldContainer[str]
    created_at: int
    def __init__(self, id: _Optional[str] = ..., owner_id: _Optional[str] = ..., name: _Optional[str] = ..., avatar: _Optional[str] = ..., tag: _Optional[str] = ..., members: _Optional[_Iterable[str]] = ..., created_at: _Optional[int] = ...) -> None: ...

class CreateTeamRequest(_message.Message):
    __slots__ = ("owner_id", "name", "tag")
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    owner_id: str
    name: str
    tag: str
    def __init__(self, owner_id: _Optional[str] = ..., name: _Optional[str] = ..., tag: _Optional[str] = ...) -> None: ...

class GetTeamRequest(_message.Message):
    __slots__ = ("team_id",)
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    team_id: str
    def __init__(self, team_id: _Optional[str] = ...) -> None: ...

class UpdateTeamRequest(_message.Message):
    __slots__ = ("team_id", "actor_id", "name", "avatar", "tag")
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    ACTOR_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    AVATAR_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    team_id: str
    actor_id: str
    name: str
    avatar: str
    tag: str
    def __init__(self, team_id: _Optional[str] = ..., actor_id: _Optional[str] = ..., name: _Optional[str] = ..., avatar: _Optional[str] = ..., tag: _Optional[str] = ...) -> None: ...

class AddTeamMemberRequest(_message.Message):
    __slots__ = ("team_id", "actor_id", "user_id")
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    ACTOR_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    team_id: str
    actor_id: str
    user_id: str
    def __init__(self, team_id: _Optional[str] = ..., actor_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class RemoveTeamMemberRequest(_message.Message):
    __slots__ = ("team_id", "actor_id", "user_id")
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    ACTOR_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    team_id: str
    actor_id: str
    user_id: str
    def __init__(self, team_id: _Optional[str] = ..., actor_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...
