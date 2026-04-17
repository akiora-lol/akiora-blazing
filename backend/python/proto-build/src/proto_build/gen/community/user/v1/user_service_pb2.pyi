from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Gender(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    HELICOPTER: _ClassVar[Gender]
    MALE: _ClassVar[Gender]
    FEMALE: _ClassVar[Gender]
HELICOPTER: Gender
MALE: Gender
FEMALE: Gender

class CreateUserRequest(_message.Message):
    __slots__ = ("email", "name")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    email: str
    name: str
    def __init__(self, email: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class Social(_message.Message):
    __slots__ = ("link", "hide")
    LINK_FIELD_NUMBER: _ClassVar[int]
    HIDE_FIELD_NUMBER: _ClassVar[int]
    link: str
    hide: bool
    def __init__(self, link: _Optional[str] = ..., hide: bool = ...) -> None: ...

class PatchUserRequest(_message.Message):
    __slots__ = ("email", "name", "bio", "gender", "birthday", "socials")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    BIO_FIELD_NUMBER: _ClassVar[int]
    GENDER_FIELD_NUMBER: _ClassVar[int]
    BIRTHDAY_FIELD_NUMBER: _ClassVar[int]
    SOCIALS_FIELD_NUMBER: _ClassVar[int]
    email: str
    name: str
    bio: str
    gender: Gender
    birthday: str
    socials: _containers.RepeatedCompositeFieldContainer[Social]
    def __init__(self, email: _Optional[str] = ..., name: _Optional[str] = ..., bio: _Optional[str] = ..., gender: _Optional[_Union[Gender, str]] = ..., birthday: _Optional[str] = ..., socials: _Optional[_Iterable[_Union[Social, _Mapping]]] = ...) -> None: ...

class UserResponse(_message.Message):
    __slots__ = ("email", "name", "bio", "gender", "birthday", "socials", "id")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    BIO_FIELD_NUMBER: _ClassVar[int]
    GENDER_FIELD_NUMBER: _ClassVar[int]
    BIRTHDAY_FIELD_NUMBER: _ClassVar[int]
    SOCIALS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    email: str
    name: str
    bio: str
    gender: Gender
    birthday: str
    socials: _containers.RepeatedCompositeFieldContainer[Social]
    id: str
    def __init__(self, email: _Optional[str] = ..., name: _Optional[str] = ..., bio: _Optional[str] = ..., gender: _Optional[_Union[Gender, str]] = ..., birthday: _Optional[str] = ..., socials: _Optional[_Iterable[_Union[Social, _Mapping]]] = ..., id: _Optional[str] = ...) -> None: ...

class GetUserRequest(_message.Message):
    __slots__ = ("id", "email")
    ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    id: str
    email: str
    def __init__(self, id: _Optional[str] = ..., email: _Optional[str] = ...) -> None: ...
