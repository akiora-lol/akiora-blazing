from enum import Enum

from pydantic import BaseModel, Field
from typing import Literal
from uuid import UUID


class LolGameSettings(BaseModel):
    team_size: int
    map: int


class TournamentType(Enum):
    PRESIGNED = "presigned"
    DRAFT = "draft"


class TournamentLifecycle(Enum):
    REGISTRATION_OPEN = "registration_open"
    REGISTRATION_LOCKED = "registration_locked"
    CAPTAIN_SETUP = "captain_setup"
    DRAFT_READY = "draft_ready"
    DRAFT_IN_PROGRESS = "draft_in_progress"
    DRAFT_FINISHED = "draft_finished"
    BRACKET_READY = "bracket_ready"
    TOURNAMENT_ACTIVE = "tournament_active"
    TOURNAMENT_FINISHED = "tournament_finished"
    TOURNAMENT_CANCELLED = "tournament_cancelled"


class DraftPickDirection(Enum):
    LINEAR = "linear"
    SNAKE = "snake"
    MANUAL = "manual"


class DraftType(Enum):
    FEARLESS = "fearless"
    IRON_MAN = "iron_man"
    CLASSIC = "classic"
    ALL_RANDOM = "all_random"


class BracketType(Enum):
    SINGLE_ELIMINATION = "single_elimination"
    SINGLE_ELIMINATION_WITH_THIRD = "single_elimination_with_third"
    DOUBLE_ELIMINATION = "double_elimination"
    SWISS = "swiss"
    ROUND_ROBIN = "round_robin"


class LolGameSeriesSettings(BaseModel):
    game_settings: LolGameSettings
    forbidden_champions: list[int]
    best_of: int | None
    draft_type: DraftType


class LolTournamentSettings(BaseModel):
    tournament_type: TournamentType = TournamentType.PRESIGNED
    game_settings: LolGameSettings
    game_series_settings: LolGameSeriesSettings
    best_of: list[int]  # finals to semifinals etc...
    bracket_type: BracketType
    draft_start: int | None = None


class DraftCaptainInfo(BaseModel):
    captain: UUID
    order: int
    picked_players: list[UUID] = Field(default_factory=list)


class DraftConfig(BaseModel):
    captain_count: int = 0
    captains: list[DraftCaptainInfo] = Field(default_factory=list)
    pick_order_captain_ids: list[UUID] = Field(default_factory=list)
    pick_direction: DraftPickDirection = DraftPickDirection.LINEAR
    max_extra_players_per_team: int = 4


class DraftState(BaseModel):
    config: DraftConfig = Field(default_factory=DraftConfig)
    current_pick_index: int = 0
    current_captain_id: UUID | None = None
    available_player_ids: list[UUID] = Field(default_factory=list)
    finished: bool = False
