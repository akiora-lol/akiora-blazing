from pydantic import BaseModel
from typing import Literal
from uuid import UUID


class Team(BaseModel):
    type: Literal["red", "blue"]
    id: UUID


class Action(BaseModel):
    type: Literal["pick", "ban"]
    champion_id: int


class Command(BaseModel):
    team: Team
    action: Action

    def short(self) -> str:
        return f"{self.team.type.upper()}_{self.action.type.upper()}"

    def from_short(short: str, team_id: UUID) -> "Command":
        team_str, action_str = short.split("_")
        team = Team(type=team_str.lower(), id=team_id)
        action = Action(type=action_str.lower(), champion_id=0)
        return Command(team=team, action=action)


class PrepareDraft(BaseModel):
    game_id: UUID
    forbidden_champions: list[int]
    teams: list[Team]
    seconds_per_action: int
    allow_redo: bool
    team_size: int
