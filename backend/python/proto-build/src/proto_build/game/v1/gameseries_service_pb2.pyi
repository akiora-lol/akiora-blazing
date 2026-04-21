from google.api import annotations_pb2 as _annotations_pb2
from google.api import http_pb2 as _http_pb2
from common import game_actors_pb2 as _game_actors_pb2
from common import game_settings_pb2 as _game_settings_pb2
from common import game_draft_pb2 as _game_draft_pb2
from common import types_pb2 as _types_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ToggleReadyRequest(_message.Message):
    __slots__ = ("series_id", "actor")
    SERIES_ID_FIELD_NUMBER: _ClassVar[int]
    ACTOR_FIELD_NUMBER: _ClassVar[int]
    series_id: str
    actor: _game_actors_pb2.Actor
    def __init__(self, series_id: _Optional[str] = ..., actor: _Optional[_Union[_game_actors_pb2.Actor, _Mapping]] = ...) -> None: ...

class DraftActionRequest(_message.Message):
    __slots__ = ("series_id", "command")
    SERIES_ID_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    series_id: str
    command: _game_draft_pb2.Command
    def __init__(self, series_id: _Optional[str] = ..., command: _Optional[_Union[_game_draft_pb2.Command, _Mapping]] = ...) -> None: ...

class ChampLockRequest(_message.Message):
    __slots__ = ("series_id", "champ_lock")
    SERIES_ID_FIELD_NUMBER: _ClassVar[int]
    CHAMP_LOCK_FIELD_NUMBER: _ClassVar[int]
    series_id: str
    champ_lock: _game_draft_pb2.ChampLock
    def __init__(self, series_id: _Optional[str] = ..., champ_lock: _Optional[_Union[_game_draft_pb2.ChampLock, _Mapping]] = ...) -> None: ...
