from google.api import annotations_pb2 as _annotations_pb2
from google.api import http_pb2 as _http_pb2
from common import types_pb2 as _types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ClubPermission(_message.Message):
    __slots__ = ("tokens",)
    TOKENS_FIELD_NUMBER: _ClassVar[int]
    tokens: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, tokens: _Optional[_Iterable[str]] = ...) -> None: ...

class FieldGroup(_message.Message):
    __slots__ = ("fields",)
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    fields: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, fields: _Optional[_Iterable[str]] = ...) -> None: ...

class ClubResponse(_message.Message):
    __slots__ = ("id", "owner_id", "name", "avatar", "description", "members", "fields", "permissions", "created_at")
    class PermissionsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ClubPermission
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ClubPermission, _Mapping]] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    AVATAR_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    owner_id: str
    name: str
    avatar: str
    description: str
    members: _containers.RepeatedScalarFieldContainer[str]
    fields: _containers.RepeatedCompositeFieldContainer[FieldGroup]
    permissions: _containers.MessageMap[str, ClubPermission]
    created_at: int
    def __init__(self, id: _Optional[str] = ..., owner_id: _Optional[str] = ..., name: _Optional[str] = ..., avatar: _Optional[str] = ..., description: _Optional[str] = ..., members: _Optional[_Iterable[str]] = ..., fields: _Optional[_Iterable[_Union[FieldGroup, _Mapping]]] = ..., permissions: _Optional[_Mapping[str, ClubPermission]] = ..., created_at: _Optional[int] = ...) -> None: ...

class CreateClubRequest(_message.Message):
    __slots__ = ("owner_id", "name", "fields")
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    owner_id: str
    name: str
    fields: _containers.RepeatedCompositeFieldContainer[FieldGroup]
    def __init__(self, owner_id: _Optional[str] = ..., name: _Optional[str] = ..., fields: _Optional[_Iterable[_Union[FieldGroup, _Mapping]]] = ...) -> None: ...

class GetClubRequest(_message.Message):
    __slots__ = ("club_id",)
    CLUB_ID_FIELD_NUMBER: _ClassVar[int]
    club_id: str
    def __init__(self, club_id: _Optional[str] = ...) -> None: ...

class UpdateClubRequest(_message.Message):
    __slots__ = ("club_id", "actor_id", "name", "avatar", "description", "fields")
    CLUB_ID_FIELD_NUMBER: _ClassVar[int]
    ACTOR_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    AVATAR_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    club_id: str
    actor_id: str
    name: str
    avatar: str
    description: str
    fields: _containers.RepeatedCompositeFieldContainer[FieldGroup]
    def __init__(self, club_id: _Optional[str] = ..., actor_id: _Optional[str] = ..., name: _Optional[str] = ..., avatar: _Optional[str] = ..., description: _Optional[str] = ..., fields: _Optional[_Iterable[_Union[FieldGroup, _Mapping]]] = ...) -> None: ...

class AddMemberRequest(_message.Message):
    __slots__ = ("club_id", "user_id", "tokens")
    CLUB_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    TOKENS_FIELD_NUMBER: _ClassVar[int]
    club_id: str
    user_id: str
    tokens: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, club_id: _Optional[str] = ..., user_id: _Optional[str] = ..., tokens: _Optional[_Iterable[str]] = ...) -> None: ...

class RemoveMemberRequest(_message.Message):
    __slots__ = ("club_id", "user_id")
    CLUB_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    club_id: str
    user_id: str
    def __init__(self, club_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class SetPermissionRequest(_message.Message):
    __slots__ = ("club_id", "actor_id", "target_user_id", "tokens")
    CLUB_ID_FIELD_NUMBER: _ClassVar[int]
    ACTOR_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_USER_ID_FIELD_NUMBER: _ClassVar[int]
    TOKENS_FIELD_NUMBER: _ClassVar[int]
    club_id: str
    actor_id: str
    target_user_id: str
    tokens: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, club_id: _Optional[str] = ..., actor_id: _Optional[str] = ..., target_user_id: _Optional[str] = ..., tokens: _Optional[_Iterable[str]] = ...) -> None: ...
