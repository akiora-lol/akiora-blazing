from enum import Enum

from pydantic import BaseModel

from uuid import UUID


class Team(BaseModel):
    type: TeamType
    id: UUID


class TeamType(Enum):
    RED = "red"
    BLUE = "blue"


class Action(BaseModel):
    type: ActionType
    champion_id: int


class ActionType(Enum):
    PICK = "pick"
    BAN = "ban"


class Command(BaseModel):
    team: Team
    action: Action


class PrepareDraft(BaseModel):
    game_id: UUID
    forbidden_champions: list[int]
    teams: list[Team]
    seconds_per_action: int
    team_size: int
