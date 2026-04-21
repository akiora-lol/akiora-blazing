from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GameType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GAME_TYPE_UNSPECIFIED: _ClassVar[GameType]
    LOL: _ClassVar[GameType]
    TFT: _ClassVar[GameType]
    VALORANT: _ClassVar[GameType]

class LolGameMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GAME_MODE_UNSPECIFIED: _ClassVar[LolGameMode]
    CLASSIC: _ClassVar[LolGameMode]
    FEARLESS: _ClassVar[LolGameMode]
    IRON_MAN: _ClassVar[LolGameMode]
    ALL_RANDOM: _ClassVar[LolGameMode]

class LolBracketMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LOL_BRACKET_MODE_UNSPECIFIED: _ClassVar[LolBracketMode]
    DOUBLE_ELIM: _ClassVar[LolBracketMode]
    SINGLE_ELIM_THIRD_PLACE: _ClassVar[LolBracketMode]
    SINGLE_ELIM_NO_THIRD_PLACE: _ClassVar[LolBracketMode]
    SWISS: _ClassVar[LolBracketMode]
    ROUND_ROBIN: _ClassVar[LolBracketMode]
    SCRIM: _ClassVar[LolBracketMode]
GAME_TYPE_UNSPECIFIED: GameType
LOL: GameType
TFT: GameType
VALORANT: GameType
GAME_MODE_UNSPECIFIED: LolGameMode
CLASSIC: LolGameMode
FEARLESS: LolGameMode
IRON_MAN: LolGameMode
ALL_RANDOM: LolGameMode
LOL_BRACKET_MODE_UNSPECIFIED: LolBracketMode
DOUBLE_ELIM: LolBracketMode
SINGLE_ELIM_THIRD_PLACE: LolBracketMode
SINGLE_ELIM_NO_THIRD_PLACE: LolBracketMode
SWISS: LolBracketMode
ROUND_ROBIN: LolBracketMode
SCRIM: LolBracketMode

class LolGameSettings(_message.Message):
    __slots__ = ("mode", "team_size", "map", "best_of")
    MODE_FIELD_NUMBER: _ClassVar[int]
    TEAM_SIZE_FIELD_NUMBER: _ClassVar[int]
    MAP_FIELD_NUMBER: _ClassVar[int]
    BEST_OF_FIELD_NUMBER: _ClassVar[int]
    mode: LolGameMode
    team_size: int
    map: int
    best_of: int
    def __init__(self, mode: _Optional[_Union[LolGameMode, str]] = ..., team_size: _Optional[int] = ..., map: _Optional[int] = ..., best_of: _Optional[int] = ...) -> None: ...

class TftGameSettings(_message.Message):
    __slots__ = ("todo",)
    TODO_FIELD_NUMBER: _ClassVar[int]
    todo: str
    def __init__(self, todo: _Optional[str] = ...) -> None: ...

class ValorantGameSettings(_message.Message):
    __slots__ = ("todo",)
    TODO_FIELD_NUMBER: _ClassVar[int]
    todo: str
    def __init__(self, todo: _Optional[str] = ...) -> None: ...

class GameSettings(_message.Message):
    __slots__ = ("game_type", "lol", "tft", "valorant")
    GAME_TYPE_FIELD_NUMBER: _ClassVar[int]
    LOL_FIELD_NUMBER: _ClassVar[int]
    TFT_FIELD_NUMBER: _ClassVar[int]
    VALORANT_FIELD_NUMBER: _ClassVar[int]
    game_type: GameType
    lol: LolGameSettings
    tft: TftGameSettings
    valorant: ValorantGameSettings
    def __init__(self, game_type: _Optional[_Union[GameType, str]] = ..., lol: _Optional[_Union[LolGameSettings, _Mapping]] = ..., tft: _Optional[_Union[TftGameSettings, _Mapping]] = ..., valorant: _Optional[_Union[ValorantGameSettings, _Mapping]] = ...) -> None: ...
