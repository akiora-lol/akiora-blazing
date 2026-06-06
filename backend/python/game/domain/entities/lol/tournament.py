from beanie import Document
from uuid import UUID, uuid4
from domain.value_objects.actors import Actor, TeamParticipant
from datetime import datetime, UTC, timedelta

from domain.value_objects.statuses import TournamentStatus
from domain.value_objects.settings import LolTournamentSettings
from domain.value_objects.bracket import Bracket


class Tournament(Document):
    id: UUID

    host: Actor
    participant_pool: list[TeamParticipant]
    prizepool: str
    is_open: bool
    wait_list: list[TeamParticipant]
    status: TournamentStatus
    settings: LolTournamentSettings
    start: datetime
    end: datetime | None
    bracket: Bracket | None

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
    ) -> "Tournament":
        return Tournament(
            id=uuid4(),
            host=host,
            prizepool=prizepool,
            is_open=is_open,
            participant_pool=[],
            start=datetime.fromtimestamp(start, UTC),
            end=None,
            status=TournamentStatus.SCHEDULED,
            settings=settings,
            bracket=None,
            wait_list=[],
        )

    def add_to_waitlist(self, p: Actor, team: list[UUID]) -> "Tournament":

        self.wait_list.append(TeamParticipant(actor=p, players=team))
        return self

    def add_participant(self, p: Actor, team: list[UUID]) -> "Tournament":
        self.participant_pool.append(TeamParticipant(actor=p, players=team))
        return self

    def reschedule(self, start: int) -> "Tournament":
        new_start = datetime.fromtimestamp(start, UTC)
        if self.start >= new_start:
            raise Exception("Tournament cannot reschedule to earlier time")
        self.start = new_start
        self.status = TournamentStatus.SCHEDULED
        return self

    def start(self) -> "Tournament":
        if self.start > datetime.now(UTC):
            raise Exception("Tournament cannot be started before start time")

        if datetime.now(UTC) - self.start > timedelta(hours=2):
            raise Exception("Tournament cannot be started after 2 hrs past start time")
        self.status = TournamentStatus.ACTIVE
        return self
