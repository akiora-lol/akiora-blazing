from uuid import UUID, uuid4
from domain.value_objects.actors import Actor, TeamParticipant
from domain.entities.lol.tournament import Tournament
from domain.value_objects.settings import (
    BracketType,
    LolGameSeriesSettings,
    LolTournamentSettings,
    DraftType,
)
from domain.services.lol.game_series_service import GameSeriesService
from domain.entities.lol.game import Game
from domain.value_objects.statuses import GameStatus, TournamentStatus
from domain.services.lol.single_elim_builder import SingleEliminationBuilder
from domain.entities.lol.game_series import GameSeries
from shared.redis import RedisService
from beanie.operators import In


class TournamentService:
    def __init__(
        self,
        redis_service: RedisService,
        game_series_service: GameSeriesService,
        se_bracket: SingleEliminationBuilder,
    ):
        self.redis_service = redis_service
        self.game_series_service = game_series_service
        self.se_bracket = se_bracket

    async def create(
        self,
        host: Actor,
        is_open: bool,
        prize_pool: str,
        start: int,
        settings: LolTournamentSettings,
    ) -> Tournament:
        t = Tournament.domain_create(
            host=host,
            is_open=is_open,
            prizepool=prize_pool,
            start=start,
            settings=settings,
        )
        await t.save()
        return t

    async def get(
        self,
        id: UUID | list[UUID],
    ) -> Tournament:
        if isinstance(id, list):
            trs = await Tournament.find_many(In(Tournament.id, id)).to_list()
            return trs
        t = await Tournament.get(id)

        return t

    async def add_to_waitlist(self, id: UUID, p: Actor, team: list[UUID]) -> None:
        t = await Tournament.get(id)
        t.add_to_waitlist(p, team)
        await t.save()

    async def add_participant(self, id: UUID, p: Actor, team: list[UUID]) -> None:
        t = await Tournament.get(id)
        t.add_participant(p, team)
        await t.save()

    async def start_tournament(self, id: UUID) -> None:
        t = await Tournament.get(id)
        gss = await self.game_series_service.get_by_tournament_id(id)
        for gs in gss:
            await self.game_series_service.start(gs.id)
        t.start()
        await t.save()

    async def swap_teams(self, id: UUID, t1: Actor, t2: Actor) -> None:
        t = await Tournament.get(id)
        if t.status != TournamentStatus.SCHEDULED:
            raise Exception("Cannot swap teams in active tournament")
        if not t.bracket:
            raise Exception("Bracket not built yet")
        gs_id1, gs_id2 = t.bracket.swap_teams(t1, t2)
        tp1, tp2 = (
            TeamParticipant(
                actor=t1,
                team=next((x.players for x in t.participant_pool if x.actor == t1), []),
            ),
            TeamParticipant(
                actor=t2,
                team=next((x.players for x in t.participant_pool if x.actor == t2), []),
            ),
        )
        await self.game_series_service.swap_teams(gs_id1, tp1, tp2)
        await self.game_series_service.swap_teams(gs_id2, tp2, tp1)
        await t.save()

    async def prebuild_bracket(self, id: UUID) -> None:
        t = await Tournament.get(id)
        if t.settings.bracket_type == BracketType.SINGLE_ELIMINATION:
            actors = list(map(lambda x: x.actor, t.participant_pool))
            bracket = self.se_bracket.build_bracket(actors)
            for round in bracket.rounds:
                for match in round:
                    await self.game_series_service.create(
                        id=t.id,
                        participants=[
                            TeamParticipant(
                                actor=match.team1,
                                team=next(
                                    (
                                        x.players
                                        for x in t.participant_pool
                                        if x.actor == match.team1
                                    ),
                                    [],
                                ),
                            ),
                            TeamParticipant(
                                actor=match.team2,
                                team=next(
                                    (
                                        x.players
                                        for x in t.participant_pool
                                        if x.actor == match.team2
                                    ),
                                    [],
                                ),
                            ),
                        ],
                        settings=t.settings.game_series_settings,
                    )
        else:
            raise Exception("not implemented yet")
        t.bracket = bracket
        await t.save()
