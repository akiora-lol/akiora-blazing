from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ActorType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ACTOR_UNSPECIFIED: _ClassVar[ActorType]
    USER: _ClassVar[ActorType]
    TEAM: _ClassVar[ActorType]
    CLUB: _ClassVar[ActorType]
ACTOR_UNSPECIFIED: ActorType
USER: ActorType
TEAM: ActorType
CLUB: ActorType

class Actor(_message.Message):
    __slots__ = ("id", "actor_type")
    ID_FIELD_NUMBER: _ClassVar[int]
    ACTOR_TYPE_FIELD_NUMBER: _ClassVar[int]
    id: str
    actor_type: ActorType
    def __init__(self, id: _Optional[str] = ..., actor_type: _Optional[_Union[ActorType, str]] = ...) -> None: ...

class TeamParticipant(_message.Message):
    __slots__ = ("participant", "user_ids")
    PARTICIPANT_FIELD_NUMBER: _ClassVar[int]
    USER_IDS_FIELD_NUMBER: _ClassVar[int]
    participant: Actor
    user_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, participant: _Optional[_Union[Actor, _Mapping]] = ..., user_ids: _Optional[_Iterable[str]] = ...) -> None: ...
