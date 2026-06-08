from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field
from uuid import UUID


class ActorType(str, Enum):
    ACTOR_UNSPECIFIED = "ACTOR_UNSPECIFIED"
    USER = "USER"
    TEAM = "TEAM"
    CLUB = "CLUB"


class GameType(str, Enum):
    GAME_TYPE_UNSPECIFIED = "GAME_TYPE_UNSPECIFIED"
    LOL = "LOL"
    TFT = "TFT"
    VALORANT = "VALORANT"


class LolGameMode(str, Enum):
    GAME_MODE_UNSPECIFIED = "GAME_MODE_UNSPECIFIED"
    CLASSIC = "CLASSIC"
    FEARLESS = "FEARLESS"
    IRON_MAN = "IRON_MAN"
    ALL_RANDOM = "ALL_RANDOM"


class LolBracketMode(str, Enum):
    LOL_BRACKET_MODE_UNSPECIFIED = "LOL_BRACKET_MODE_UNSPECIFIED"
    DOUBLE_ELIM = "DOUBLE_ELIM"
    SINGLE_ELIM_THIRD_PLACE = "SINGLE_ELIM_THIRD_PLACE"
    SINGLE_ELIM_NO_THIRD_PLACE = "SINGLE_ELIM_NO_THIRD_PLACE"
    SWISS = "SWISS"
    ROUND_ROBIN = "ROUND_ROBIN"
    SCRIM = "SCRIM"


class Status(str, Enum):
    STATUS_UNSPECIFIED = "STATUS_UNSPECIFIED"
    SCHEDULED = "SCHEDULED"
    ACTIVE = "ACTIVE"
    FINISHED = "FINISHED"
    CANCELLED = "CANCELLED"


class TournamentType(str, Enum):
    UNSPECIFIED = "UNSPECIFIED"
    PRESIGNED = "PRESIGNED"
    DRAFT = "DRAFT"
    PRESIGN = "PRESIGN"
    PICKEM = "PICKEM"


class TournamentLifecycle(str, Enum):
    TOURNAMENT_LIFECYCLE_UNSPECIFIED = "TOURNAMENT_LIFECYCLE_UNSPECIFIED"
    REGISTRATION_OPEN = "REGISTRATION_OPEN"
    REGISTRATION_LOCKED = "REGISTRATION_LOCKED"
    CAPTAIN_SETUP = "CAPTAIN_SETUP"
    DRAFT_READY = "DRAFT_READY"
    DRAFT_IN_PROGRESS = "DRAFT_IN_PROGRESS"
    DRAFT_FINISHED = "DRAFT_FINISHED"
    BRACKET_READY = "BRACKET_READY"
    TOURNAMENT_ACTIVE = "TOURNAMENT_ACTIVE"
    TOURNAMENT_FINISHED = "TOURNAMENT_FINISHED"
    TOURNAMENT_CANCELLED = "TOURNAMENT_CANCELLED"


class DraftPickDirection(str, Enum):
    DRAFT_PICK_DIRECTION_UNSPECIFIED = "DRAFT_PICK_DIRECTION_UNSPECIFIED"
    LINEAR = "LINEAR"
    SNAKE = "SNAKE"
    MANUAL = "MANUAL"


class Actor(BaseModel):
    id: UUID
    actor_type: ActorType


class TeamParticipant(BaseModel):
    participant: Actor
    user_ids: List[str] = Field(default_factory=list)


class LolGameSettings(BaseModel):
    mode: LolGameMode = LolGameMode.GAME_MODE_UNSPECIFIED
    team_size: int = 5
    map: int = 11
    best_of: int = 1


class TftGameSettings(BaseModel):
    todo: Optional[str] = None


class ValorantGameSettings(BaseModel):
    todo: Optional[str] = None


class GameSettings(BaseModel):
    game_type: GameType = GameType.GAME_TYPE_UNSPECIFIED
    lol: Optional[LolGameSettings] = None
    tft: Optional[TftGameSettings] = None
    valorant: Optional[ValorantGameSettings] = None


class LolTournamentSettings(BaseModel):
    tournament_type: TournamentType = TournamentType.UNSPECIFIED
    bracket_mode: LolBracketMode = LolBracketMode.LOL_BRACKET_MODE_UNSPECIFIED
    draft_mode: List[LolGameMode] = Field(default_factory=list)
    team_size: int = 5
    map: int = 11
    forbidden_champions: List[int] = Field(default_factory=list)
    series_best_of: List[int] = Field(default_factory=list)
    draft_start: Optional[int] = None


class TftTournamentSettings(BaseModel):
    todo: Optional[str] = None


class ValorantTournamentSettings(BaseModel):
    todo: Optional[str] = None


class TournamentSettings(BaseModel):
    game_type: GameType = GameType.GAME_TYPE_UNSPECIFIED
    lol: Optional[LolTournamentSettings] = None
    tft: Optional[TftTournamentSettings] = None
    valorant: Optional[ValorantTournamentSettings] = None


class TournamentResponse(BaseModel):
    id: UUID
    host: Actor
    participants: List[Actor] = Field(default_factory=list)
    settings: TournamentSettings
    game_series_ids: List[str] = Field(default_factory=list)
    start: int
    end: Optional[int] = None
    status: Status = Status.STATUS_UNSPECIFIED
    prizepool: Optional[str] = None
    is_open: bool = False
    lifecycle: TournamentLifecycle = TournamentLifecycle.TOURNAMENT_LIFECYCLE_UNSPECIFIED
    draft_start: Optional[int] = None
    registration_locked_at: Optional[int] = None
    draft_state: Optional["DraftState"] = None
    bracket: Optional["BracketInfo"] = None

    class Config:
        from_attributes = True


class ManyTournamentsResponse(BaseModel):
    tournaments: List[TournamentResponse] = Field(default_factory=list)


class CreateTournamentRequest(BaseModel):
    host: Actor
    settings: TournamentSettings
    start: int
    prizepool: Optional[str] = None
    is_open: bool = False
    name: Optional[str] = None
    description: Optional[str] = None
    avatar: Optional[str] = None
    draft_start: Optional[int] = None


class GetTournamentRequest(BaseModel):
    ids: List[str] = Field(default_factory=list)
    game_type: Optional[GameType] = None


class ChangeBracketRequest(BaseModel):
    tournament_id: UUID
    swap_initiator: Actor
    swap_victim: Actor


class BracketRoundSettings(BaseModel):
    round: int
    label: str = ""
    best_of: int = 1


class BracketMatchInfo(BaseModel):
    game_series_id: str
    team1: Optional[Actor] = None
    team2: Optional[Actor] = None
    winner: Optional[Actor] = None
    round: int = 0
    match_number: int = 0
    next_match_id: Optional[int] = None
    best_of: int = 1


class DraftCaptainInfo(BaseModel):
    captain: Actor
    order: int = 0
    picked_players: List[Actor] = Field(default_factory=list)


class DraftConfig(BaseModel):
    captain_count: int = 0
    captains: List[DraftCaptainInfo] = Field(default_factory=list)
    pick_order_captain_ids: List[str] = Field(default_factory=list)
    pick_direction: DraftPickDirection = DraftPickDirection.LINEAR
    max_extra_players_per_team: int = 4


class DraftState(BaseModel):
    config: DraftConfig = Field(default_factory=DraftConfig)
    current_pick_index: int = 0
    current_captain_id: Optional[str] = None
    available_player_ids: List[str] = Field(default_factory=list)
    finished: bool = False


class AddParticipantRequest(BaseModel):
    tournament_id: UUID
    participant: Actor
    team_name: Optional[str] = None
    draft_roles: List[str] = Field(default_factory=list)


class AddTeamParticipantRequest(BaseModel):
    tournament_id: UUID
    team_participant: TeamParticipant


class RemoveParticipantRequest(BaseModel):
    tournament_id: UUID
    participant_id: str
    actor_id: Optional[UUID] = None


class UpdateTournamentRequest(BaseModel):
    tournament_id: UUID
    actor_id: UUID
    start: Optional[int] = None
    prizepool: Optional[str] = None
    is_open: bool = False
    status: Optional[Status] = None
    name: Optional[str] = None
    description: Optional[str] = None
    draft_start: Optional[int] = None


class DeleteTournamentRequest(BaseModel):
    tournament_id: UUID
    actor_id: UUID


class StartTournamentRequest(BaseModel):
    tournament_id: UUID
    actor_id: Optional[UUID] = None


class FinishTournamentRequest(BaseModel):
    tournament_id: UUID
    actor_id: Optional[UUID] = None
    winner_id: Optional[str] = None


class PreBuildBracketRequest(BaseModel):
    tournament_id: UUID
    actor_id: Optional[UUID] = None
    round_settings: List[BracketRoundSettings] = Field(default_factory=list)


class LockRegistrationRequest(BaseModel):
    tournament_id: UUID
    actor_id: UUID


class RescheduleTournamentRequest(BaseModel):
    tournament_id: UUID
    actor_id: UUID
    start: int
    draft_start: Optional[int] = None


class SetDraftCaptainsRequest(BaseModel):
    tournament_id: UUID
    actor_id: UUID
    captain_count: int
    captain_ids: List[str] = Field(default_factory=list)
    pick_direction: DraftPickDirection = DraftPickDirection.LINEAR
    max_extra_players_per_team: int = 4


class UpdateDraftPickOrderRequest(BaseModel):
    tournament_id: UUID
    actor_id: UUID
    captain_ids: List[str] = Field(default_factory=list)


class DraftPickPlayerRequest(BaseModel):
    tournament_id: UUID
    actor_id: UUID
    captain_id: str
    player_id: str


class UpdateBracketMatchRequest(BaseModel):
    tournament_id: UUID
    actor_id: UUID
    game_series_id: str
    team1: Optional[Actor] = None
    team2: Optional[Actor] = None
    best_of: Optional[int] = None


class UpdateParticipantRequest(BaseModel):
    tournament_id: UUID
    participant_id: str
    actor_id: Optional[UUID] = None
    team_name: Optional[str] = None


class AddParticipantToWaitListRequest(BaseModel):
    tournament_id: UUID
    participant: Actor


class RemoveFromWaitListRequest(BaseModel):
    tournament_id: UUID
    participant_id: str


class PaginationRequest(BaseModel):
    page: int = 1
    page_size: int = 50


class TournamentFilter(BaseModel):
    game_type: Optional[GameType] = None
    status: Optional[Status] = None
    host_id: Optional[UUID] = None
    is_participant: bool = False
    min_start_time: Optional[int] = None
    max_start_time: Optional[int] = None
    is_open: bool = False


class ListTournamentsRequest(BaseModel):
    filter: TournamentFilter = Field(default_factory=TournamentFilter)
    pagination: PaginationRequest = Field(default_factory=PaginationRequest)


class ListTournamentsResponse(BaseModel):
    tournaments: List[TournamentResponse] = Field(default_factory=list)
    total_count: int = 0
    page: int = 1
    page_size: int = 50
    has_next: bool = False


class ParticipantInfo(BaseModel):
    participant: Actor
    user_ids: List[str] = Field(default_factory=list)
    joined_at: int = 0
    draft_roles: List[str] = Field(default_factory=list)
    is_captain: Optional[bool] = None
    captain_order: Optional[int] = None


class BracketInfo(BaseModel):
    bracket_id: str = ""
    participant_ids: List[str] = Field(default_factory=list)
    round: int = 0
    round_settings: List[BracketRoundSettings] = Field(default_factory=list)
    matches: List[BracketMatchInfo] = Field(default_factory=list)


class GetParticipantsRequest(BaseModel):
    tournament_id: UUID
    pagination: PaginationRequest = Field(default_factory=PaginationRequest)


class GetParticipantsResponse(BaseModel):
    participants: List[ParticipantInfo] = Field(default_factory=list)
    total_count: int = 0


class GetWaitlistRequest(BaseModel):
    tournament_id: UUID
    pagination: PaginationRequest = Field(default_factory=PaginationRequest)


class GetWaitlistResponse(BaseModel):
    participants: List[Actor] = Field(default_factory=list)
    total_count: int = 0


class GetBracketRequest(BaseModel):
    tournament_id: UUID


class GetBracketResponse(BaseModel):
    bracket: Optional[BracketInfo] = None


class IsParticipantRequest(BaseModel):
    tournament_id: UUID
    participant_id: str


class IsParticipantResponse(BaseModel):
    is_participant: bool = False
    role: Optional[str] = None


class GetTournamentStatsRequest(BaseModel):
    tournament_id: UUID


class TournamentStatsResponse(BaseModel):
    total_participants: int = 0
    total_teams: int = 0
    waitlist_count: int = 0
    status: str = ""
    time_until_start: int = 0
