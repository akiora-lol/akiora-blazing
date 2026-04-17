from pydantic import BaseModel
from uuid import UUID
from draft_schemas import Command, PrepareDraft, Team
from rules import CLASSIC_5_DRAFT
from datetime import datetime, timedelta, UTC


class Draft(BaseModel):
    history: list[Command]
    deadline: int
    game_id: UUID
    teams: list[Team]
    forbidden_champions: list[int]
    stage: int = 0
    team_size: int

    seconds_per_action: int

    @classmethod
    def prepare(cls, prepare_draft: PrepareDraft) -> "Draft":
        return cls(
            history=[],
            deadline=int(datetime.now(UTC).timestamp())
            + int(timedelta(hours=5).total_seconds()),
            game_id=prepare_draft.game_id,
            teams=prepare_draft.teams,
            forbidden_champions=prepare_draft.forbidden_champions,
            stage=0,
            team_size=prepare_draft.team_size,
            seconds_per_action=prepare_draft.seconds_per_action,
        )

    def next_command(self) -> str | None:
        try:
            return CLASSIC_5_DRAFT[self.stage]
        except IndexError:
            return None

    def perform_command(self, command: Command) -> Command | None:
        if command.short() != CLASSIC_5_DRAFT[self.stage]:
            raise Exception("Invalid command for this stage of the draft")
        self.forbidden_champions.append(command.action.champion_id)
        self.history.append(command)
        self.stage += 1
        other_team = (
            self.teams[0] if self.teams[1].id == command.team.id else self.teams[1]
        )
        nc = self.next_command()
        if not nc:
            return None
        return command.from_short(nc, other_team.id)
