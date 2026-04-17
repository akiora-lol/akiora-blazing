from common import game_actors_pb2 as _game_actors_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Command(_message.Message):
    __slots__ = ("actor", "action")
    ACTOR_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    actor: _game_actors_pb2.Actor
    action: Action
    def __init__(self, actor: _Optional[_Union[_game_actors_pb2.Actor, _Mapping]] = ..., action: _Optional[_Union[Action, _Mapping]] = ...) -> None: ...

class Action(_message.Message):
    __slots__ = ("pick", "ban")
    PICK_FIELD_NUMBER: _ClassVar[int]
    BAN_FIELD_NUMBER: _ClassVar[int]
    pick: int
    ban: int
    def __init__(self, pick: _Optional[int] = ..., ban: _Optional[int] = ...) -> None: ...

class ChampLock(_message.Message):
    __slots__ = ("champion_id", "player_id")
    CHAMPION_ID_FIELD_NUMBER: _ClassVar[int]
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    champion_id: int
    player_id: str
    def __init__(self, champion_id: _Optional[int] = ..., player_id: _Optional[str] = ...) -> None: ...
