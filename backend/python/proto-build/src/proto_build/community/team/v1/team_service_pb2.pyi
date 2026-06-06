from google.api import annotations_pb2 as _annotations_pb2
from google.api import http_pb2 as _http_pb2
from common import types_pb2 as _types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

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

class MemberInfo(_message.Message):
    __slots__ = ("user_id", "nickname", "avatar")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    AVATAR_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    nickname: str
    avatar: str
    def __init__(self, user_id: _Optional[str] = ..., nickname: _Optional[str] = ..., avatar: _Optional[str] = ...) -> None: ...

class PaginationRequest(_message.Message):
    __slots__ = ("page", "page_size")
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    page: int
    page_size: int
    def __init__(self, page: _Optional[int] = ..., page_size: _Optional[int] = ...) -> None: ...

class TeamFilter(_message.Message):
    __slots__ = ("search", "owner_id", "is_member")
    SEARCH_FIELD_NUMBER: _ClassVar[int]
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    IS_MEMBER_FIELD_NUMBER: _ClassVar[int]
    search: str
    owner_id: str
    is_member: bool
    def __init__(self, search: _Optional[str] = ..., owner_id: _Optional[str] = ..., is_member: bool = ...) -> None: ...

class ListTeamsRequest(_message.Message):
    __slots__ = ("filter", "pagination")
    FILTER_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    filter: TeamFilter
    pagination: PaginationRequest
    def __init__(self, filter: _Optional[_Union[TeamFilter, _Mapping]] = ..., pagination: _Optional[_Union[PaginationRequest, _Mapping]] = ...) -> None: ...

class ListTeamsResponse(_message.Message):
    __slots__ = ("teams", "total_count", "page", "page_size", "has_next")
    TEAMS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    HAS_NEXT_FIELD_NUMBER: _ClassVar[int]
    teams: _containers.RepeatedCompositeFieldContainer[TeamResponse]
    total_count: int
    page: int
    page_size: int
    has_next: bool
    def __init__(self, teams: _Optional[_Iterable[_Union[TeamResponse, _Mapping]]] = ..., total_count: _Optional[int] = ..., page: _Optional[int] = ..., page_size: _Optional[int] = ..., has_next: bool = ...) -> None: ...

class TeamMembersResponse(_message.Message):
    __slots__ = ("members", "total_count")
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    members: _containers.RepeatedCompositeFieldContainer[MemberInfo]
    total_count: int
    def __init__(self, members: _Optional[_Iterable[_Union[MemberInfo, _Mapping]]] = ..., total_count: _Optional[int] = ...) -> None: ...

class CreateTeamRequest(_message.Message):
    __slots__ = ("owner_id", "name", "avatar", "tag")
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    AVATAR_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    owner_id: str
    name: str
    avatar: str
    tag: str
    def __init__(self, owner_id: _Optional[str] = ..., name: _Optional[str] = ..., avatar: _Optional[str] = ..., tag: _Optional[str] = ...) -> None: ...

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

class DeleteTeamRequest(_message.Message):
    __slots__ = ("team_id", "actor_id")
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    ACTOR_ID_FIELD_NUMBER: _ClassVar[int]
    team_id: str
    actor_id: str
    def __init__(self, team_id: _Optional[str] = ..., actor_id: _Optional[str] = ...) -> None: ...

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

class GetMembersRequest(_message.Message):
    __slots__ = ("team_id", "pagination")
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    team_id: str
    pagination: PaginationRequest
    def __init__(self, team_id: _Optional[str] = ..., pagination: _Optional[_Union[PaginationRequest, _Mapping]] = ...) -> None: ...

class SearchMembersRequest(_message.Message):
    __slots__ = ("team_id", "search", "pagination")
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    SEARCH_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    team_id: str
    search: str
    pagination: PaginationRequest
    def __init__(self, team_id: _Optional[str] = ..., search: _Optional[str] = ..., pagination: _Optional[_Union[PaginationRequest, _Mapping]] = ...) -> None: ...

class CheckCapacityRequest(_message.Message):
    __slots__ = ("team_id",)
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    team_id: str
    def __init__(self, team_id: _Optional[str] = ...) -> None: ...

class CheckCapacityResponse(_message.Message):
    __slots__ = ("can_add", "current_members", "max_members")
    CAN_ADD_FIELD_NUMBER: _ClassVar[int]
    CURRENT_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    MAX_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    can_add: bool
    current_members: int
    max_members: int
    def __init__(self, can_add: bool = ..., current_members: _Optional[int] = ..., max_members: _Optional[int] = ...) -> None: ...

class IsMemberRequest(_message.Message):
    __slots__ = ("team_id", "user_id")
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    team_id: str
    user_id: str
    def __init__(self, team_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class IsMemberResponse(_message.Message):
    __slots__ = ("is_member", "role")
    IS_MEMBER_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    is_member: bool
    role: str
    def __init__(self, is_member: bool = ..., role: _Optional[str] = ...) -> None: ...
