from google.api import annotations_pb2 as _annotations_pb2
from google.api import http_pb2 as _http_pb2
from common import types_pb2 as _types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Gender(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GENDER_UNSPECIFIED: _ClassVar[Gender]
    MALE: _ClassVar[Gender]
    FEMALE: _ClassVar[Gender]

class UserType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    USER_TYPE_UNSPECIFIED: _ClassVar[UserType]
    DEFAULT: _ClassVar[UserType]
    STAFF: _ClassVar[UserType]
    STREAMER: _ClassVar[UserType]
    PRO: _ClassVar[UserType]
    MODERATOR: _ClassVar[UserType]
GENDER_UNSPECIFIED: Gender
MALE: Gender
FEMALE: Gender
USER_TYPE_UNSPECIFIED: UserType
DEFAULT: UserType
STAFF: UserType
STREAMER: UserType
PRO: UserType
MODERATOR: UserType

class Social(_message.Message):
    __slots__ = ("link", "hidden")
    LINK_FIELD_NUMBER: _ClassVar[int]
    HIDDEN_FIELD_NUMBER: _ClassVar[int]
    link: str
    hidden: bool
    def __init__(self, link: _Optional[str] = ..., hidden: bool = ...) -> None: ...

class Birthday(_message.Message):
    __slots__ = ("day", "hidden")
    DAY_FIELD_NUMBER: _ClassVar[int]
    HIDDEN_FIELD_NUMBER: _ClassVar[int]
    day: str
    hidden: bool
    def __init__(self, day: _Optional[str] = ..., hidden: bool = ...) -> None: ...

class UserResponse(_message.Message):
    __slots__ = ("id", "email", "nickname", "user_type", "avatar", "bio", "gender", "birth_date", "socials", "created_at", "last_updated")
    class SocialsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Social
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Social, _Mapping]] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    USER_TYPE_FIELD_NUMBER: _ClassVar[int]
    AVATAR_FIELD_NUMBER: _ClassVar[int]
    BIO_FIELD_NUMBER: _ClassVar[int]
    GENDER_FIELD_NUMBER: _ClassVar[int]
    BIRTH_DATE_FIELD_NUMBER: _ClassVar[int]
    SOCIALS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATED_FIELD_NUMBER: _ClassVar[int]
    id: str
    email: str
    nickname: str
    user_type: UserType
    avatar: str
    bio: str
    gender: Gender
    birth_date: Birthday
    socials: _containers.MessageMap[str, Social]
    created_at: int
    last_updated: int
    def __init__(self, id: _Optional[str] = ..., email: _Optional[str] = ..., nickname: _Optional[str] = ..., user_type: _Optional[_Union[UserType, str]] = ..., avatar: _Optional[str] = ..., bio: _Optional[str] = ..., gender: _Optional[_Union[Gender, str]] = ..., birth_date: _Optional[_Union[Birthday, _Mapping]] = ..., socials: _Optional[_Mapping[str, Social]] = ..., created_at: _Optional[int] = ..., last_updated: _Optional[int] = ...) -> None: ...

class PaginationRequest(_message.Message):
    __slots__ = ("page", "page_size", "before_timestamp")
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    BEFORE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    page: int
    page_size: int
    before_timestamp: int
    def __init__(self, page: _Optional[int] = ..., page_size: _Optional[int] = ..., before_timestamp: _Optional[int] = ...) -> None: ...

class UserFilter(_message.Message):
    __slots__ = ("search", "user_type", "gender", "has_avatar", "min_created_at", "max_created_at")
    SEARCH_FIELD_NUMBER: _ClassVar[int]
    USER_TYPE_FIELD_NUMBER: _ClassVar[int]
    GENDER_FIELD_NUMBER: _ClassVar[int]
    HAS_AVATAR_FIELD_NUMBER: _ClassVar[int]
    MIN_CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    MAX_CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    search: str
    user_type: UserType
    gender: Gender
    has_avatar: bool
    min_created_at: int
    max_created_at: int
    def __init__(self, search: _Optional[str] = ..., user_type: _Optional[_Union[UserType, str]] = ..., gender: _Optional[_Union[Gender, str]] = ..., has_avatar: bool = ..., min_created_at: _Optional[int] = ..., max_created_at: _Optional[int] = ...) -> None: ...

class ListUsersRequest(_message.Message):
    __slots__ = ("filter", "pagination")
    FILTER_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    filter: UserFilter
    pagination: PaginationRequest
    def __init__(self, filter: _Optional[_Union[UserFilter, _Mapping]] = ..., pagination: _Optional[_Union[PaginationRequest, _Mapping]] = ...) -> None: ...

class ListUsersResponse(_message.Message):
    __slots__ = ("users", "total_count", "page", "page_size", "has_next")
    USERS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    HAS_NEXT_FIELD_NUMBER: _ClassVar[int]
    users: _containers.RepeatedCompositeFieldContainer[UserResponse]
    total_count: int
    page: int
    page_size: int
    has_next: bool
    def __init__(self, users: _Optional[_Iterable[_Union[UserResponse, _Mapping]]] = ..., total_count: _Optional[int] = ..., page: _Optional[int] = ..., page_size: _Optional[int] = ..., has_next: bool = ...) -> None: ...

class FriendRequest(_message.Message):
    __slots__ = ("sender_id", "receiver_id")
    SENDER_ID_FIELD_NUMBER: _ClassVar[int]
    RECEIVER_ID_FIELD_NUMBER: _ClassVar[int]
    sender_id: str
    receiver_id: str
    def __init__(self, sender_id: _Optional[str] = ..., receiver_id: _Optional[str] = ...) -> None: ...

class RespondFriendRequest(_message.Message):
    __slots__ = ("request_id", "responder_id", "accept")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONDER_ID_FIELD_NUMBER: _ClassVar[int]
    ACCEPT_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    responder_id: str
    accept: bool
    def __init__(self, request_id: _Optional[str] = ..., responder_id: _Optional[str] = ..., accept: bool = ...) -> None: ...

class FriendResponse(_message.Message):
    __slots__ = ("id", "user_id_1", "user_id_2", "status", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_1_FIELD_NUMBER: _ClassVar[int]
    USER_ID_2_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    user_id_1: str
    user_id_2: str
    status: str
    created_at: int
    updated_at: int
    def __init__(self, id: _Optional[str] = ..., user_id_1: _Optional[str] = ..., user_id_2: _Optional[str] = ..., status: _Optional[str] = ..., created_at: _Optional[int] = ..., updated_at: _Optional[int] = ...) -> None: ...

class ListFriendsRequest(_message.Message):
    __slots__ = ("user_id", "pagination", "status")
    class FriendStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        FRIEND_STATUS_UNSPECIFIED: _ClassVar[ListFriendsRequest.FriendStatus]
        ACCEPTED: _ClassVar[ListFriendsRequest.FriendStatus]
        PENDING: _ClassVar[ListFriendsRequest.FriendStatus]
        BLOCKED: _ClassVar[ListFriendsRequest.FriendStatus]
    FRIEND_STATUS_UNSPECIFIED: ListFriendsRequest.FriendStatus
    ACCEPTED: ListFriendsRequest.FriendStatus
    PENDING: ListFriendsRequest.FriendStatus
    BLOCKED: ListFriendsRequest.FriendStatus
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    pagination: PaginationRequest
    status: ListFriendsRequest.FriendStatus
    def __init__(self, user_id: _Optional[str] = ..., pagination: _Optional[_Union[PaginationRequest, _Mapping]] = ..., status: _Optional[_Union[ListFriendsRequest.FriendStatus, str]] = ...) -> None: ...

class ListFriendsResponse(_message.Message):
    __slots__ = ("friends", "total_count")
    FRIENDS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    friends: _containers.RepeatedCompositeFieldContainer[FriendResponse]
    total_count: int
    def __init__(self, friends: _Optional[_Iterable[_Union[FriendResponse, _Mapping]]] = ..., total_count: _Optional[int] = ...) -> None: ...

class CreateUserRequest(_message.Message):
    __slots__ = ("email", "nickname")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    email: str
    nickname: str
    def __init__(self, email: _Optional[str] = ..., nickname: _Optional[str] = ...) -> None: ...

class GetUserRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetUserByEmailRequest(_message.Message):
    __slots__ = ("email",)
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    email: str
    def __init__(self, email: _Optional[str] = ...) -> None: ...

class UpdateUserRequest(_message.Message):
    __slots__ = ("user_id", "nickname", "bio", "avatar", "gender", "user_type", "birth_date", "socials")
    class SocialsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Social
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Social, _Mapping]] = ...) -> None: ...
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    BIO_FIELD_NUMBER: _ClassVar[int]
    AVATAR_FIELD_NUMBER: _ClassVar[int]
    GENDER_FIELD_NUMBER: _ClassVar[int]
    USER_TYPE_FIELD_NUMBER: _ClassVar[int]
    BIRTH_DATE_FIELD_NUMBER: _ClassVar[int]
    SOCIALS_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    nickname: str
    bio: str
    avatar: str
    gender: Gender
    user_type: UserType
    birth_date: Birthday
    socials: _containers.MessageMap[str, Social]
    def __init__(self, user_id: _Optional[str] = ..., nickname: _Optional[str] = ..., bio: _Optional[str] = ..., avatar: _Optional[str] = ..., gender: _Optional[_Union[Gender, str]] = ..., user_type: _Optional[_Union[UserType, str]] = ..., birth_date: _Optional[_Union[Birthday, _Mapping]] = ..., socials: _Optional[_Mapping[str, Social]] = ...) -> None: ...

class DeleteUserRequest(_message.Message):
    __slots__ = ("user_id", "actor_id")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ACTOR_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    actor_id: str
    def __init__(self, user_id: _Optional[str] = ..., actor_id: _Optional[str] = ...) -> None: ...

class SendFriendRequestRequest(_message.Message):
    __slots__ = ("request",)
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    request: FriendRequest
    def __init__(self, request: _Optional[_Union[FriendRequest, _Mapping]] = ...) -> None: ...

class RespondFriendRequestRequest(_message.Message):
    __slots__ = ("response",)
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: RespondFriendRequest
    def __init__(self, response: _Optional[_Union[RespondFriendRequest, _Mapping]] = ...) -> None: ...

class RemoveFriendRequest(_message.Message):
    __slots__ = ("user_id_1", "user_id_2", "actor_id")
    USER_ID_1_FIELD_NUMBER: _ClassVar[int]
    USER_ID_2_FIELD_NUMBER: _ClassVar[int]
    ACTOR_ID_FIELD_NUMBER: _ClassVar[int]
    user_id_1: str
    user_id_2: str
    actor_id: str
    def __init__(self, user_id_1: _Optional[str] = ..., user_id_2: _Optional[str] = ..., actor_id: _Optional[str] = ...) -> None: ...

class BlockUserRequest(_message.Message):
    __slots__ = ("blocker_id", "blocked_id")
    BLOCKER_ID_FIELD_NUMBER: _ClassVar[int]
    BLOCKED_ID_FIELD_NUMBER: _ClassVar[int]
    blocker_id: str
    blocked_id: str
    def __init__(self, blocker_id: _Optional[str] = ..., blocked_id: _Optional[str] = ...) -> None: ...

class UnblockUserRequest(_message.Message):
    __slots__ = ("blocker_id", "blocked_id")
    BLOCKER_ID_FIELD_NUMBER: _ClassVar[int]
    BLOCKED_ID_FIELD_NUMBER: _ClassVar[int]
    blocker_id: str
    blocked_id: str
    def __init__(self, blocker_id: _Optional[str] = ..., blocked_id: _Optional[str] = ...) -> None: ...

class GetFriendStatusRequest(_message.Message):
    __slots__ = ("user_id_1", "user_id_2")
    USER_ID_1_FIELD_NUMBER: _ClassVar[int]
    USER_ID_2_FIELD_NUMBER: _ClassVar[int]
    user_id_1: str
    user_id_2: str
    def __init__(self, user_id_1: _Optional[str] = ..., user_id_2: _Optional[str] = ...) -> None: ...

class GetFriendStatusResponse(_message.Message):
    __slots__ = ("status", "request_id")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    status: str
    request_id: str
    def __init__(self, status: _Optional[str] = ..., request_id: _Optional[str] = ...) -> None: ...
