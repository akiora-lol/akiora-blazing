from common import game_actors_pb2 as _game_actors_pb2
from common import game_settings_pb2 as _game_settings_pb2
from common import types_pb2 as _types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TournamentType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNSPECIFIED: _ClassVar[TournamentType]
    PRESIGN: _ClassVar[TournamentType]
    PICKEM: _ClassVar[TournamentType]
UNSPECIFIED: TournamentType
PRESIGN: TournamentType
PICKEM: TournamentType

class LolTournamentSettings(_message.Message):
    __slots__ = ("tournament_type", "bracket_mode", "draft_mode", "team_size", "map", "forbidden_champions", "series_best_of")
    TOURNAMENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    BRACKET_MODE_FIELD_NUMBER: _ClassVar[int]
    DRAFT_MODE_FIELD_NUMBER: _ClassVar[int]
    TEAM_SIZE_FIELD_NUMBER: _ClassVar[int]
    MAP_FIELD_NUMBER: _ClassVar[int]
    FORBIDDEN_CHAMPIONS_FIELD_NUMBER: _ClassVar[int]
    SERIES_BEST_OF_FIELD_NUMBER: _ClassVar[int]
    tournament_type: TournamentType
    bracket_mode: _game_settings_pb2.LolBracketMode
    draft_mode: _containers.RepeatedScalarFieldContainer[_game_settings_pb2.LolGameMode]
    team_size: int
    map: int
    forbidden_champions: _containers.RepeatedScalarFieldContainer[int]
    series_best_of: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, tournament_type: _Optional[_Union[TournamentType, str]] = ..., bracket_mode: _Optional[_Union[_game_settings_pb2.LolBracketMode, str]] = ..., draft_mode: _Optional[_Iterable[_Union[_game_settings_pb2.LolGameMode, str]]] = ..., team_size: _Optional[int] = ..., map: _Optional[int] = ..., forbidden_champions: _Optional[_Iterable[int]] = ..., series_best_of: _Optional[_Iterable[int]] = ...) -> None: ...

class TftTournamentSettings(_message.Message):
    __slots__ = ("todo",)
    TODO_FIELD_NUMBER: _ClassVar[int]
    todo: str
    def __init__(self, todo: _Optional[str] = ...) -> None: ...

class ValorantTournamentSettings(_message.Message):
    __slots__ = ("todo",)
    TODO_FIELD_NUMBER: _ClassVar[int]
    todo: str
    def __init__(self, todo: _Optional[str] = ...) -> None: ...

class TournamentSettings(_message.Message):
    __slots__ = ("game_type", "lol", "tft", "valorant")
    GAME_TYPE_FIELD_NUMBER: _ClassVar[int]
    LOL_FIELD_NUMBER: _ClassVar[int]
    TFT_FIELD_NUMBER: _ClassVar[int]
    VALORANT_FIELD_NUMBER: _ClassVar[int]
    game_type: _game_settings_pb2.GameType
    lol: LolTournamentSettings
    tft: TftTournamentSettings
    valorant: ValorantTournamentSettings
    def __init__(self, game_type: _Optional[_Union[_game_settings_pb2.GameType, str]] = ..., lol: _Optional[_Union[LolTournamentSettings, _Mapping]] = ..., tft: _Optional[_Union[TftTournamentSettings, _Mapping]] = ..., valorant: _Optional[_Union[ValorantTournamentSettings, _Mapping]] = ...) -> None: ...

class CreateTournamentRequest(_message.Message):
    __slots__ = ("host", "settings", "start", "prizepool", "is_open")
    HOST_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    PRIZEPOOL_FIELD_NUMBER: _ClassVar[int]
    IS_OPEN_FIELD_NUMBER: _ClassVar[int]
    host: _game_actors_pb2.Actor
    settings: TournamentSettings
    start: int
    prizepool: str
    is_open: bool
    def __init__(self, host: _Optional[_Union[_game_actors_pb2.Actor, _Mapping]] = ..., settings: _Optional[_Union[TournamentSettings, _Mapping]] = ..., start: _Optional[int] = ..., prizepool: _Optional[str] = ..., is_open: bool = ...) -> None: ...

class GetTournamentRequest(_message.Message):
    __slots__ = ("ids", "game_type")
    IDS_FIELD_NUMBER: _ClassVar[int]
    GAME_TYPE_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    game_type: _game_settings_pb2.GameType
    def __init__(self, ids: _Optional[_Iterable[str]] = ..., game_type: _Optional[_Union[_game_settings_pb2.GameType, str]] = ...) -> None: ...

class TournamentResponse(_message.Message):
    __slots__ = ("id", "host", "participants", "settings", "game_series_ids", "start", "end", "status", "prizepool")
    ID_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    PARTICIPANTS_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    GAME_SERIES_IDS_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PRIZEPOOL_FIELD_NUMBER: _ClassVar[int]
    id: str
    host: _game_actors_pb2.Actor
    participants: _containers.RepeatedCompositeFieldContainer[_game_actors_pb2.Actor]
    settings: TournamentSettings
    game_series_ids: _containers.RepeatedScalarFieldContainer[str]
    start: int
    end: int
    status: _types_pb2.Status
    prizepool: str
    def __init__(self, id: _Optional[str] = ..., host: _Optional[_Union[_game_actors_pb2.Actor, _Mapping]] = ..., participants: _Optional[_Iterable[_Union[_game_actors_pb2.Actor, _Mapping]]] = ..., settings: _Optional[_Union[TournamentSettings, _Mapping]] = ..., game_series_ids: _Optional[_Iterable[str]] = ..., start: _Optional[int] = ..., end: _Optional[int] = ..., status: _Optional[_Union[_types_pb2.Status, str]] = ..., prizepool: _Optional[str] = ...) -> None: ...

class ManyTournamentsResponse(_message.Message):
    __slots__ = ("tournaments",)
    TOURNAMENTS_FIELD_NUMBER: _ClassVar[int]
    tournaments: _containers.RepeatedCompositeFieldContainer[TournamentResponse]
    def __init__(self, tournaments: _Optional[_Iterable[_Union[TournamentResponse, _Mapping]]] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ChangeBracketRequest(_message.Message):
    __slots__ = ("tournament_id", "swap_initiator", "swap_victim")
    TOURNAMENT_ID_FIELD_NUMBER: _ClassVar[int]
    SWAP_INITIATOR_FIELD_NUMBER: _ClassVar[int]
    SWAP_VICTIM_FIELD_NUMBER: _ClassVar[int]
    tournament_id: str
    swap_initiator: _game_actors_pb2.Actor
    swap_victim: _game_actors_pb2.Actor
    def __init__(self, tournament_id: _Optional[str] = ..., swap_initiator: _Optional[_Union[_game_actors_pb2.Actor, _Mapping]] = ..., swap_victim: _Optional[_Union[_game_actors_pb2.Actor, _Mapping]] = ...) -> None: ...

class AddParticipantRequest(_message.Message):
    __slots__ = ("tournament_id", "participant")
    TOURNAMENT_ID_FIELD_NUMBER: _ClassVar[int]
    PARTICIPANT_FIELD_NUMBER: _ClassVar[int]
    tournament_id: str
    participant: _game_actors_pb2.Actor
    def __init__(self, tournament_id: _Optional[str] = ..., participant: _Optional[_Union[_game_actors_pb2.Actor, _Mapping]] = ...) -> None: ...

class AddTeamParticipantRequest(_message.Message):
    __slots__ = ("tournament_id", "team_participant")
    TOURNAMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_PARTICIPANT_FIELD_NUMBER: _ClassVar[int]
    tournament_id: str
    team_participant: _game_actors_pb2.TeamParticipant
    def __init__(self, tournament_id: _Optional[str] = ..., team_participant: _Optional[_Union[_game_actors_pb2.TeamParticipant, _Mapping]] = ...) -> None: ...

class RemoveParticipantRequest(_message.Message):
    __slots__ = ("tournament_id", "participant_id")
    TOURNAMENT_ID_FIELD_NUMBER: _ClassVar[int]
    PARTICIPANT_ID_FIELD_NUMBER: _ClassVar[int]
    tournament_id: str
    participant_id: str
    def __init__(self, tournament_id: _Optional[str] = ..., participant_id: _Optional[str] = ...) -> None: ...
