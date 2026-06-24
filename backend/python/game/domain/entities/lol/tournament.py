from beanie import Document
from pydantic import Field
from uuid import UUID, uuid4
from domain.value_objects.actors import Actor, TeamParticipant
from datetime import datetime, UTC, timedelta

from domain.value_objects.statuses import TournamentStatus
from domain.value_objects.settings import LolTournamentSettings
from domain.value_objects.settings import (
    DraftState,
    TournamentLifecycle,
    TournamentType,
)
from domain.value_objects.bracket import Bracket


class Tournament(Document):
    id: UUID

    host: Actor
    participant_pool: list[TeamParticipant] = Field(default_factory=list)
    prizepool: str
    is_open: bool = True
    wait_list: list[TeamParticipant] = Field(default_factory=list)
    status: TournamentStatus = TournamentStatus.SCHEDULED
    settings: LolTournamentSettings
    lifecycle: TournamentLifecycle = TournamentLifecycle.REGISTRATION_OPEN
    draft_start: datetime | None = None
    registration_locked_at: datetime | None = None
    draft_state: DraftState | None = None
    start: datetime
    end: datetime | None = None
    bracket: Bracket | None = None

    class Settings:
        bson_encoders = {UUID: str}

    @classmethod
    def domain_create(
        cls,
        host: Actor,
        start: int,
        is_open: bool,
        prizepool: str,
        settings: LolTournamentSettings,
        draft_start: int | None = None,
    ) -> "Tournament":
        start_dt = datetime.fromtimestamp(start, UTC)
        draft_start_dt = (
            datetime.fromtimestamp(draft_start, UTC) if draft_start else None
        )
        if settings.tournament_type == TournamentType.DRAFT:
            if not draft_start_dt:
                raise Exception("Draft tournaments require draft start time")
            if start_dt - draft_start_dt < timedelta(days=2):
                raise Exception(
                    "Tournament start must be at least 2 days after draft start"
                )
        return Tournament(
            id=uuid4(),
            host=host,
            prizepool=prizepool,
            is_open=is_open,
            participant_pool=[],
            start=start_dt,
            end=None,
            status=TournamentStatus.SCHEDULED,
            settings=settings,
            lifecycle=TournamentLifecycle.REGISTRATION_OPEN,
            draft_start=draft_start_dt,
            registration_locked_at=None,
            draft_state=None,
            bracket=None,
            wait_list=[],
        )

    def add_to_waitlist(self, p: Actor, team: list[UUID]) -> "Tournament":

        self.wait_list.append(TeamParticipant(actor=p, players=team))
        return self

    def add_participant(
        self, p: Actor, team: list[UUID], draft_roles: list[str] | None = None
    ) -> "Tournament":
        if self.lifecycle != TournamentLifecycle.REGISTRATION_OPEN:
            raise Exception("Registration is locked")
        self.participant_pool.append(
            TeamParticipant(actor=p, players=team, draft_roles=draft_roles or [])
        )
        return self

    def reschedule(self, start: int, draft_start: int | None = None) -> "Tournament":
        new_start = datetime.fromtimestamp(start, UTC)
        new_draft_start = (
            datetime.fromtimestamp(draft_start, UTC)
            if draft_start
            else self.draft_start
        )
        if self.settings.tournament_type == TournamentType.DRAFT:
            if not new_draft_start:
                raise Exception("Draft tournaments require draft start time")
            if new_start - new_draft_start < timedelta(days=2):
                raise Exception(
                    "Tournament start must be at least 2 days after draft start"
                )
            self.draft_start = new_draft_start
        self.start = new_start
        self.status = TournamentStatus.SCHEDULED
        return self

    # How early before `start` the tournament can be kicked off.
    START_EARLY_GRACE: "timedelta" = timedelta(minutes=5)

    def begin(self) -> "Tournament":
        # Renamed from `start` to avoid colliding with the `start: datetime` Pydantic field.
        # The bug manifested as `TypeError: 'datetime.datetime' object is not callable` at
        # TournamentService.start_tournament → t.start().

        self.status = TournamentStatus.ACTIVE
        self.lifecycle = TournamentLifecycle.TOURNAMENT_ACTIVE
        return self
