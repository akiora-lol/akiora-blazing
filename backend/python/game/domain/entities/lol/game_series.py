from beanie import Document
from uuid import UUID, uuid4
from domain.value_objects.actors import Actor, TeamParticipant
from datetime import UTC, datetime

from domain.value_objects.statuses import GameSeriesStatus
from domain.value_objects.settings import LolGameSeriesSettings


class GameSeries(Document):
    id: UUID
    tournament_id: UUID
    teams: list[TeamParticipant]
    start: datetime | None
    end: datetime | None
    status: GameSeriesStatus
    settings: LolGameSeriesSettings

    class Settings:
        bson_encoders = {UUID: str}

    @classmethod
    def domain_create(
        cls,
        id: UUID,
        tournament_id: UUID,
        teams: list[TeamParticipant],
        settings: LolGameSeriesSettings,
    ) -> "GameSeries":
        return GameSeries(
            id=id,
            tournament_id=tournament_id,
            teams=teams,
            results=[],
            start=None,
            end=None,
            status=GameSeriesStatus.SCHEDULED,
            settings=settings,
            draft=None,
        )

    def start(self) -> "GameSeries":
        self.start = datetime.now(UTC)
        return self

    def swap_teams(
        self,
        t1: TeamParticipant,
        t2: TeamParticipant,
    ) -> "GameSeries":
        if self.status != GameSeriesStatus.SCHEDULED:
            raise Exception("Cannot swap teams in active game series")
        if t1 in self.teams and t2 in self.teams:
            idx1 = self.teams.index(t1)
            idx2 = self.teams.index(t2)
            self.teams[idx1], self.teams[idx2] = self.teams[idx2], self.teams[idx1]
            return self

        try:
            idx1 = self.teams.index(t1)
            self.teams[idx1] = t2
        except ValueError:
            pass
        try:
            idx2 = self.teams.index(t2)
            self.teams[idx2] = t1
        except ValueError:
            pass
        return self
