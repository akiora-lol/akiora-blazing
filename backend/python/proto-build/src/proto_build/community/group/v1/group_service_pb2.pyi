from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CreateGroupRequest(_message.Message):
    __slots__ = ("owner_id", "name")
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    owner_id: str
    name: str
    def __init__(self, owner_id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class PatchGroupRequest(_message.Message):
    __slots__ = ("owner_id", "name", "add_users", "delete_users")
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ADD_USERS_FIELD_NUMBER: _ClassVar[int]
    DELETE_USERS_FIELD_NUMBER: _ClassVar[int]
    owner_id: str
    name: str
    add_users: _containers.RepeatedScalarFieldContainer[str]
    delete_users: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, owner_id: _Optional[str] = ..., name: _Optional[str] = ..., add_users: _Optional[_Iterable[str]] = ..., delete_users: _Optional[_Iterable[str]] = ...) -> None: ...

class GroupResponse(_message.Message):
    __slots__ = ("id", "owner_id", "name", "users")
    ID_FIELD_NUMBER: _ClassVar[int]
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    USERS_FIELD_NUMBER: _ClassVar[int]
    id: str
    owner_id: str
    name: str
    users: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., owner_id: _Optional[str] = ..., name: _Optional[str] = ..., users: _Optional[_Iterable[str]] = ...) -> None: ...

class GetGroupRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...
