from beanie import Document
from uuid import UUID, uuid4
from domain.value_objects.actors import TeamParticipant, Actor
from datetime import datetime, UTC

from domain.value_objects.statuses import GameStatus
from domain.value_objects.settings import LolGameSettings
from shared.contracts.draft.model import Draft


class Game(Document):
    id: UUID
    game_series_id: UUID
    teams: list[TeamParticipant]
    ready_check: list[TeamParticipant]
    results: list[TeamParticipant]
    start: datetime
    end: datetime | None
    status: GameStatus
    settings: LolGameSettings
    draft: Draft | None

    class Settings:
        bson_encoders = {UUID: str}

    @classmethod
    def domain_create(
        cls,
        game_series_id: UUID,
        teams: list[TeamParticipant],
        settings: LolGameSettings,
    ) -> "Game":
        return cls(
            id=uuid4(),
            game_series_id=game_series_id,
            teams=teams,
            ready_check=[],
            results=[],
            start=datetime.now(),
            end=None,
            status=GameStatus.SCHEDULED,
            settings=settings,
            draft=None,
        )

    def toggle_ready(
        self,
        tp: TeamParticipant,
    ) -> "Game":
        if (
            self.status != GameStatus.SCHEDULED
            and self.status != GameStatus.SIDE_CHOSEN
        ):
            raise Exception("Game is not in toggle check state")
        if tp in self.ready_check:
            self.ready_check.remove(tp)
        else:
            self.ready_check.append(tp)
            if len(self.ready_check) == len(self.teams):
                self.status = GameStatus.ACTIVE
        return self

    def chose_side(
        self,
        tp: TeamParticipant,
        side: int,  # 0 for blue, 1 for red
    ) -> "Game":
        if self.status == GameStatus.SIDE_CHOSEN or self.status != GameStatus.SCHEDULED:
            raise Exception("Already chose sides")
        if self.teams.index(tp) != side:
            self.teams[side], self.teams[1 - side] = (
                self.teams[1 - side],
                self.teams[side],
            )
        self.status = GameStatus.SIDE_CHOSEN
        return self

    def set_winner(self, winner_actor: Actor) -> "Game":
        """Mark this game as finished with the given winner.

        Idempotent: re-calling overwrites the previously recorded winner
        (per product spec — host can correct mistakes any time before the
        whole tournament is FINISHED). `results` stores exactly one entry
        for a finished game (the winning team participant).
        """
        winner_tp = next(
            (tp for tp in self.teams if tp.actor == winner_actor),
            None,
        )
        if winner_tp is None:
            raise Exception(
                f"Winner {winner_actor.id} is not a participant of this game"
            )
        self.results = [winner_tp]
        self.status = GameStatus.FINISHED
        self.end = datetime.now(UTC)
        return self
