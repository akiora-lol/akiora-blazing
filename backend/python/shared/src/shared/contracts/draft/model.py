from pydantic import BaseModel
from uuid import UUID
from shared.contracts.draft.schemas import Command, Team, ActionType


class Draft(BaseModel):
    history: list[Command]
    game_id: UUID
    teams: list[Team]
    forbidden_champions: list[int]
    team_size: int

    def get_picks(self) -> list[int]:
        picks = []
        for command in self.history:
            if command.action.type == ActionType.PICK:
                picks.append(command.action.champion_id)
        return picks

    def get_bans(self) -> list[int]:
        bans = []
        for command in self.history:
            if command.action.type == ActionType.BAN:
                bans.append(command.action.champion_id)
        return bans
