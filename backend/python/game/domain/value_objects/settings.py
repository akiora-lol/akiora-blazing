from enum import Enum

from pydantic import BaseModel
from typing import Literal
from uuid import UUID


class LolGameSettings(BaseModel):
    team_size: int
    map: int


class LolGameSeriesSettings(BaseModel):
    game_settings: LolGameSettings
    forbidden_champions: list[int]
    best_of: int | None
    draft_type: DraftType


class LolTournamentSettings(BaseModel):
    game_settings: LolGameSettings
    game_series_settings: LolGameSeriesSettings
    best_of: list[int]  # finals to semifinals etc...
    bracket_type: BracketType


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
