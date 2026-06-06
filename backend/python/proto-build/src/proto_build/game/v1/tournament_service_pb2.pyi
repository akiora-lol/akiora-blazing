from google.api import annotations_pb2 as _annotations_pb2
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

class PaginationRequest(_message.Message):
    __slots__ = ("page", "page_size")
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    page: int
    page_size: int
    def __init__(self, page: _Optional[int] = ..., page_size: _Optional[int] = ...) -> None: ...

class TournamentFilter(_message.Message):
    __slots__ = ("game_type", "status", "host_id", "is_participant", "min_start_time", "max_start_time", "is_open")
    GAME_TYPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    HOST_ID_FIELD_NUMBER: _ClassVar[int]
    IS_PARTICIPANT_FIELD_NUMBER: _ClassVar[int]
    MIN_START_TIME_FIELD_NUMBER: _ClassVar[int]
    MAX_START_TIME_FIELD_NUMBER: _ClassVar[int]
    IS_OPEN_FIELD_NUMBER: _ClassVar[int]
    game_type: _game_settings_pb2.GameType
    status: _types_pb2.Status
    host_id: str
    is_participant: bool
    min_start_time: int
    max_start_time: int
    is_open: bool
    def __init__(self, game_type: _Optional[_Union[_game_settings_pb2.GameType, str]] = ..., status: _Optional[_Union[_types_pb2.Status, str]] = ..., host_id: _Optional[str] = ..., is_participant: bool = ..., min_start_time: _Optional[int] = ..., max_start_time: _Optional[int] = ..., is_open: bool = ...) -> None: ...

class ParticipantInfo(_message.Message):
    __slots__ = ("participant", "user_ids", "joined_at")
    PARTICIPANT_FIELD_NUMBER: _ClassVar[int]
    USER_IDS_FIELD_NUMBER: _ClassVar[int]
    JOINED_AT_FIELD_NUMBER: _ClassVar[int]
    participant: _game_actors_pb2.Actor
    user_ids: _containers.RepeatedScalarFieldContainer[str]
    joined_at: int
    def __init__(self, participant: _Optional[_Union[_game_actors_pb2.Actor, _Mapping]] = ..., user_ids: _Optional[_Iterable[str]] = ..., joined_at: _Optional[int] = ...) -> None: ...

class BracketInfo(_message.Message):
    __slots__ = ("bracket_id", "participant_ids", "round")
    BRACKET_ID_FIELD_NUMBER: _ClassVar[int]
    PARTICIPANT_IDS_FIELD_NUMBER: _ClassVar[int]
    ROUND_FIELD_NUMBER: _ClassVar[int]
    bracket_id: str
    participant_ids: _containers.RepeatedScalarFieldContainer[str]
    round: int
    def __init__(self, bracket_id: _Optional[str] = ..., participant_ids: _Optional[_Iterable[str]] = ..., round: _Optional[int] = ...) -> None: ...

class ListTournamentsRequest(_message.Message):
    __slots__ = ("filter", "pagination")
    FILTER_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    filter: TournamentFilter
    pagination: PaginationRequest
    def __init__(self, filter: _Optional[_Union[TournamentFilter, _Mapping]] = ..., pagination: _Optional[_Union[PaginationRequest, _Mapping]] = ...) -> None: ...

class ListTournamentsResponse(_message.Message):
    __slots__ = ("tournaments", "total_count", "page", "page_size", "has_next")
    TOURNAMENTS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    HAS_NEXT_FIELD_NUMBER: _ClassVar[int]
    tournaments: _containers.RepeatedCompositeFieldContainer[TournamentResponse]
    total_count: int
    page: int
    page_size: int
    has_next: bool
    def __init__(self, tournaments: _Optional[_Iterable[_Union[TournamentResponse, _Mapping]]] = ..., total_count: _Optional[int] = ..., page: _Optional[int] = ..., page_size: _Optional[int] = ..., has_next: bool = ...) -> None: ...

class GetParticipantsRequest(_message.Message):
    __slots__ = ("tournament_id", "pagination")
    TOURNAMENT_ID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    tournament_id: str
    pagination: PaginationRequest
    def __init__(self, tournament_id: _Optional[str] = ..., pagination: _Optional[_Union[PaginationRequest, _Mapping]] = ...) -> None: ...

class GetParticipantsResponse(_message.Message):
    __slots__ = ("participants", "total_count")
    PARTICIPANTS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    participants: _containers.RepeatedCompositeFieldContainer[ParticipantInfo]
    total_count: int
    def __init__(self, participants: _Optional[_Iterable[_Union[ParticipantInfo, _Mapping]]] = ..., total_count: _Optional[int] = ...) -> None: ...

class GetWaitlistRequest(_message.Message):
    __slots__ = ("tournament_id", "pagination")
    TOURNAMENT_ID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    tournament_id: str
    pagination: PaginationRequest
    def __init__(self, tournament_id: _Optional[str] = ..., pagination: _Optional[_Union[PaginationRequest, _Mapping]] = ...) -> None: ...

class GetWaitlistResponse(_message.Message):
    __slots__ = ("participants", "total_count")
    PARTICIPANTS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    participants: _containers.RepeatedCompositeFieldContainer[_game_actors_pb2.Actor]
    total_count: int
    def __init__(self, participants: _Optional[_Iterable[_Union[_game_actors_pb2.Actor, _Mapping]]] = ..., total_count: _Optional[int] = ...) -> None: ...

class GetBracketRequest(_message.Message):
    __slots__ = ("tournament_id",)
    TOURNAMENT_ID_FIELD_NUMBER: _ClassVar[int]
    tournament_id: str
    def __init__(self, tournament_id: _Optional[str] = ...) -> None: ...

class GetBracketResponse(_message.Message):
    __slots__ = ("bracket",)
    BRACKET_FIELD_NUMBER: _ClassVar[int]
    bracket: BracketInfo
    def __init__(self, bracket: _Optional[_Union[BracketInfo, _Mapping]] = ...) -> None: ...

class CreateTournamentRequest(_message.Message):
    __slots__ = ("host", "settings", "start", "prizepool", "is_open", "name", "description", "avatar")
    HOST_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    PRIZEPOOL_FIELD_NUMBER: _ClassVar[int]
    IS_OPEN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    AVATAR_FIELD_NUMBER: _ClassVar[int]
    host: _game_actors_pb2.Actor
    settings: TournamentSettings
    start: int
    prizepool: str
    is_open: bool
    name: str
    description: str
    avatar: str
    def __init__(self, host: _Optional[_Union[_game_actors_pb2.Actor, _Mapping]] = ..., settings: _Optional[_Union[TournamentSettings, _Mapping]] = ..., start: _Optional[int] = ..., prizepool: _Optional[str] = ..., is_open: bool = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., avatar: _Optional[str] = ...) -> None: ...

class GetTournamentRequest(_message.Message):
    __slots__ = ("ids", "game_type")
    IDS_FIELD_NUMBER: _ClassVar[int]
    GAME_TYPE_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    game_type: _game_settings_pb2.GameType
    def __init__(self, ids: _Optional[_Iterable[str]] = ..., game_type: _Optional[_Union[_game_settings_pb2.GameType, str]] = ...) -> None: ...

class UpdateTournamentRequest(_message.Message):
    __slots__ = ("tournament_id", "actor_id", "start", "prizepool", "is_open", "status", "name", "description")
    TOURNAMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ACTOR_ID_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    PRIZEPOOL_FIELD_NUMBER: _ClassVar[int]
    IS_OPEN_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    tournament_id: str
    actor_id: str
    start: int
    prizepool: str
    is_open: bool
    status: _types_pb2.Status
    name: str
    description: str
    def __init__(self, tournament_id: _Optional[str] = ..., actor_id: _Optional[str] = ..., start: _Optional[int] = ..., prizepool: _Optional[str] = ..., is_open: bool = ..., status: _Optional[_Union[_types_pb2.Status, str]] = ..., name: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class DeleteTournamentRequest(_message.Message):
    __slots__ = ("tournament_id", "actor_id")
    TOURNAMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ACTOR_ID_FIELD_NUMBER: _ClassVar[int]
    tournament_id: str
    actor_id: str
    def __init__(self, tournament_id: _Optional[str] = ..., actor_id: _Optional[str] = ...) -> None: ...

class AddParticipantRequest(_message.Message):
    __slots__ = ("tournament_id", "participant", "team_name")
    TOURNAMENT_ID_FIELD_NUMBER: _ClassVar[int]
    PARTICIPANT_FIELD_NUMBER: _ClassVar[int]
    TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
    tournament_id: str
    participant: _game_actors_pb2.Actor
    team_name: str
    def __init__(self, tournament_id: _Optional[str] = ..., participant: _Optional[_Union[_game_actors_pb2.Actor, _Mapping]] = ..., team_name: _Optional[str] = ...) -> None: ...

class AddTeamParticipantRequest(_message.Message):
    __slots__ = ("tournament_id", "team_participant")
    TOURNAMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_PARTICIPANT_FIELD_NUMBER: _ClassVar[int]
    tournament_id: str
    team_participant: _game_actors_pb2.TeamParticipant
    def __init__(self, tournament_id: _Optional[str] = ..., team_participant: _Optional[_Union[_game_actors_pb2.TeamParticipant, _Mapping]] = ...) -> None: ...

class RemoveParticipantRequest(_message.Message):
    __slots__ = ("tournament_id", "participant_id", "actor_id")
    TOURNAMENT_ID_FIELD_NUMBER: _ClassVar[int]
    PARTICIPANT_ID_FIELD_NUMBER: _ClassVar[int]
    ACTOR_ID_FIELD_NUMBER: _ClassVar[int]
    tournament_id: str
    participant_id: str
    actor_id: str
    def __init__(self, tournament_id: _Optional[str] = ..., participant_id: _Optional[str] = ..., actor_id: _Optional[str] = ...) -> None: ...

class UpdateParticipantRequest(_message.Message):
    __slots__ = ("tournament_id", "participant_id", "actor_id", "team_name")
    TOURNAMENT_ID_FIELD_NUMBER: _ClassVar[int]
    PARTICIPANT_ID_FIELD_NUMBER: _ClassVar[int]
    ACTOR_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
    tournament_id: str
    participant_id: str
    actor_id: str
    team_name: str
    def __init__(self, tournament_id: _Optional[str] = ..., participant_id: _Optional[str] = ..., actor_id: _Optional[str] = ..., team_name: _Optional[str] = ...) -> None: ...

class StartTournamentRequest(_message.Message):
    __slots__ = ("tournament_id", "actor_id")
    TOURNAMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ACTOR_ID_FIELD_NUMBER: _ClassVar[int]
    tournament_id: str
    actor_id: str
    def __init__(self, tournament_id: _Optional[str] = ..., actor_id: _Optional[str] = ...) -> None: ...

class FinishTournamentRequest(_message.Message):
    __slots__ = ("tournament_id", "actor_id", "winner_id")
    TOURNAMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ACTOR_ID_FIELD_NUMBER: _ClassVar[int]
    WINNER_ID_FIELD_NUMBER: _ClassVar[int]
    tournament_id: str
    actor_id: str
    winner_id: str
    def __init__(self, tournament_id: _Optional[str] = ..., actor_id: _Optional[str] = ..., winner_id: _Optional[str] = ...) -> None: ...

class PreBuildBracketRequest(_message.Message):
    __slots__ = ("tournament_id", "actor_id")
    TOURNAMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ACTOR_ID_FIELD_NUMBER: _ClassVar[int]
    tournament_id: str
    actor_id: str
    def __init__(self, tournament_id: _Optional[str] = ..., actor_id: _Optional[str] = ...) -> None: ...

class ChangeBracketRequest(_message.Message):
    __slots__ = ("tournament_id", "swap_initiator", "swap_victim")
    TOURNAMENT_ID_FIELD_NUMBER: _ClassVar[int]
    SWAP_INITIATOR_FIELD_NUMBER: _ClassVar[int]
    SWAP_VICTIM_FIELD_NUMBER: _ClassVar[int]
    tournament_id: str
    swap_initiator: _game_actors_pb2.Actor
    swap_victim: _game_actors_pb2.Actor
    def __init__(self, tournament_id: _Optional[str] = ..., swap_initiator: _Optional[_Union[_game_actors_pb2.Actor, _Mapping]] = ..., swap_victim: _Optional[_Union[_game_actors_pb2.Actor, _Mapping]] = ...) -> None: ...

class AddParticipantToWaitListRequest(_message.Message):
    __slots__ = ("tournament_id", "participant")
    TOURNAMENT_ID_FIELD_NUMBER: _ClassVar[int]
    PARTICIPANT_FIELD_NUMBER: _ClassVar[int]
    tournament_id: str
    participant: _game_actors_pb2.Actor
    def __init__(self, tournament_id: _Optional[str] = ..., participant: _Optional[_Union[_game_actors_pb2.Actor, _Mapping]] = ...) -> None: ...

class RemoveFromWaitListRequest(_message.Message):
    __slots__ = ("tournament_id", "participant_id")
    TOURNAMENT_ID_FIELD_NUMBER: _ClassVar[int]
    PARTICIPANT_ID_FIELD_NUMBER: _ClassVar[int]
    tournament_id: str
    participant_id: str
    def __init__(self, tournament_id: _Optional[str] = ..., participant_id: _Optional[str] = ...) -> None: ...

class GetTournamentStatsRequest(_message.Message):
    __slots__ = ("tournament_id",)
    TOURNAMENT_ID_FIELD_NUMBER: _ClassVar[int]
    tournament_id: str
    def __init__(self, tournament_id: _Optional[str] = ...) -> None: ...

class TournamentStatsResponse(_message.Message):
    __slots__ = ("total_participants", "total_teams", "waitlist_count", "status", "time_until_start")
    TOTAL_PARTICIPANTS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_TEAMS_FIELD_NUMBER: _ClassVar[int]
    WAITLIST_COUNT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TIME_UNTIL_START_FIELD_NUMBER: _ClassVar[int]
    total_participants: int
    total_teams: int
    waitlist_count: int
    status: str
    time_until_start: int
    def __init__(self, total_participants: _Optional[int] = ..., total_teams: _Optional[int] = ..., waitlist_count: _Optional[int] = ..., status: _Optional[str] = ..., time_until_start: _Optional[int] = ...) -> None: ...

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

class IsParticipantRequest(_message.Message):
    __slots__ = ("tournament_id", "participant_id")
    TOURNAMENT_ID_FIELD_NUMBER: _ClassVar[int]
    PARTICIPANT_ID_FIELD_NUMBER: _ClassVar[int]
    tournament_id: str
    participant_id: str
    def __init__(self, tournament_id: _Optional[str] = ..., participant_id: _Optional[str] = ...) -> None: ...

class IsParticipantResponse(_message.Message):
    __slots__ = ("is_participant", "role")
    IS_PARTICIPANT_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    is_participant: bool
    role: str
    def __init__(self, is_participant: bool = ..., role: _Optional[str] = ...) -> None: ...
