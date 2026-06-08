from pydantic import BaseModel

from uuid import UUID

from shared.contracts.draft.schemas import Team, Action


class Command(BaseModel):
    team: Team
    action: Action


class PrepareDraft(BaseModel):
    game_id: UUID
    forbidden_champions: list[int]
    teams: list[Team]
    seconds_per_action: int
    team_size: int
