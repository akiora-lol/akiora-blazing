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

class MemberInfo(_message.Message):
    __slots__ = ("user_id", "nickname", "avatar", "permissions")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    AVATAR_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    nickname: str
    avatar: str
    permissions: ClubPermission
    def __init__(self, user_id: _Optional[str] = ..., nickname: _Optional[str] = ..., avatar: _Optional[str] = ..., permissions: _Optional[_Union[ClubPermission, _Mapping]] = ...) -> None: ...

class PaginationRequest(_message.Message):
    __slots__ = ("page", "page_size")
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    page: int
    page_size: int
    def __init__(self, page: _Optional[int] = ..., page_size: _Optional[int] = ...) -> None: ...

class ClubFilter(_message.Message):
    __slots__ = ("search", "owner_id", "is_member")
    SEARCH_FIELD_NUMBER: _ClassVar[int]
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    IS_MEMBER_FIELD_NUMBER: _ClassVar[int]
    search: str
    owner_id: str
    is_member: bool
    def __init__(self, search: _Optional[str] = ..., owner_id: _Optional[str] = ..., is_member: bool = ...) -> None: ...

class ListClubsRequest(_message.Message):
    __slots__ = ("filter", "pagination")
    FILTER_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    filter: ClubFilter
    pagination: PaginationRequest
    def __init__(self, filter: _Optional[_Union[ClubFilter, _Mapping]] = ..., pagination: _Optional[_Union[PaginationRequest, _Mapping]] = ...) -> None: ...

class ListClubsResponse(_message.Message):
    __slots__ = ("clubs", "total_count", "page", "page_size", "has_next")
    CLUBS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    HAS_NEXT_FIELD_NUMBER: _ClassVar[int]
    clubs: _containers.RepeatedCompositeFieldContainer[ClubResponse]
    total_count: int
    page: int
    page_size: int
    has_next: bool
    def __init__(self, clubs: _Optional[_Iterable[_Union[ClubResponse, _Mapping]]] = ..., total_count: _Optional[int] = ..., page: _Optional[int] = ..., page_size: _Optional[int] = ..., has_next: bool = ...) -> None: ...

class ClubMembersResponse(_message.Message):
    __slots__ = ("members", "total_count")
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    members: _containers.RepeatedCompositeFieldContainer[MemberInfo]
    total_count: int
    def __init__(self, members: _Optional[_Iterable[_Union[MemberInfo, _Mapping]]] = ..., total_count: _Optional[int] = ...) -> None: ...

class CreateClubRequest(_message.Message):
    __slots__ = ("owner_id", "name", "avatar", "description", "fields")
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    AVATAR_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    owner_id: str
    name: str
    avatar: str
    description: str
    fields: _containers.RepeatedCompositeFieldContainer[FieldGroup]
    def __init__(self, owner_id: _Optional[str] = ..., name: _Optional[str] = ..., avatar: _Optional[str] = ..., description: _Optional[str] = ..., fields: _Optional[_Iterable[_Union[FieldGroup, _Mapping]]] = ...) -> None: ...

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

class DeleteClubRequest(_message.Message):
    __slots__ = ("club_id", "actor_id")
    CLUB_ID_FIELD_NUMBER: _ClassVar[int]
    ACTOR_ID_FIELD_NUMBER: _ClassVar[int]
    club_id: str
    actor_id: str
    def __init__(self, club_id: _Optional[str] = ..., actor_id: _Optional[str] = ...) -> None: ...

class AddMemberRequest(_message.Message):
    __slots__ = ("club_id", "actor_id", "user_id", "tokens")
    CLUB_ID_FIELD_NUMBER: _ClassVar[int]
    ACTOR_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    TOKENS_FIELD_NUMBER: _ClassVar[int]
    club_id: str
    actor_id: str
    user_id: str
    tokens: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, club_id: _Optional[str] = ..., actor_id: _Optional[str] = ..., user_id: _Optional[str] = ..., tokens: _Optional[_Iterable[str]] = ...) -> None: ...

class RemoveMemberRequest(_message.Message):
    __slots__ = ("club_id", "actor_id", "user_id")
    CLUB_ID_FIELD_NUMBER: _ClassVar[int]
    ACTOR_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    club_id: str
    actor_id: str
    user_id: str
    def __init__(self, club_id: _Optional[str] = ..., actor_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

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

class GetMembersRequest(_message.Message):
    __slots__ = ("club_id", "pagination")
    CLUB_ID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    club_id: str
    pagination: PaginationRequest
    def __init__(self, club_id: _Optional[str] = ..., pagination: _Optional[_Union[PaginationRequest, _Mapping]] = ...) -> None: ...

class GetMemberPermissionsRequest(_message.Message):
    __slots__ = ("club_id", "user_id")
    CLUB_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    club_id: str
    user_id: str
    def __init__(self, club_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class MemberPermissionResponse(_message.Message):
    __slots__ = ("user_id", "tokens")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    TOKENS_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    tokens: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, user_id: _Optional[str] = ..., tokens: _Optional[_Iterable[str]] = ...) -> None: ...

class SearchMembersRequest(_message.Message):
    __slots__ = ("club_id", "search", "pagination")
    CLUB_ID_FIELD_NUMBER: _ClassVar[int]
    SEARCH_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    club_id: str
    search: str
    pagination: PaginationRequest
    def __init__(self, club_id: _Optional[str] = ..., search: _Optional[str] = ..., pagination: _Optional[_Union[PaginationRequest, _Mapping]] = ...) -> None: ...

class IsMemberRequest(_message.Message):
    __slots__ = ("club_id", "user_id")
    CLUB_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    club_id: str
    user_id: str
    def __init__(self, club_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class IsMemberResponse(_message.Message):
    __slots__ = ("is_member", "role", "permissions")
    IS_MEMBER_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    is_member: bool
    role: str
    permissions: ClubPermission
    def __init__(self, is_member: bool = ..., role: _Optional[str] = ..., permissions: _Optional[_Union[ClubPermission, _Mapping]] = ...) -> None: ...
