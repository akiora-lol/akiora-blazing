from google.api import annotations_pb2 as _annotations_pb2
from google.api import http_pb2 as _http_pb2
from common import types_pb2 as _types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
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
