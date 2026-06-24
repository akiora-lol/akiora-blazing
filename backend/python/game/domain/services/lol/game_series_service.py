from uuid import UUID
from uuid import uuid4
from datetime import datetime, UTC
from domain.value_objects.actors import Actor, TeamParticipant
from domain.entities.lol.game_series import GameSeries
from domain.value_objects.settings import LolGameSeriesSettings, DraftType
from domain.services.lol.game_service import GameService
from domain.entities.lol.game import Game
from domain.value_objects.statuses import GameStatus, GameSeriesStatus
from shared.redis import RedisService


class GameSeriesService:
    def __init__(self, redis_service: RedisService, game_service: GameService):
        self.redis_service = redis_service
        self.game_service = game_service

    async def create(
        self,
        id: UUID,
        participants: list[TeamParticipant],
        settings: LolGameSeriesSettings,
    ) -> GameSeries:
        gs = GameSeries.domain_create(
            id=uuid4(),
            tournament_id=id,
            teams=participants,
            settings=settings,
        )
        await gs.save()
        return gs

    async def get_by_tournament_id(self, id: UUID) -> list[GameSeries]:
        return await GameSeries.find(GameSeries.tournament_id == id).to_list()

    async def games(self, id: UUID) -> list[Game]:
        return await self.game_service.get_by_gs_id(id)

    async def start(self, id: UUID) -> None:
        # pub to redis for start
        gs = await GameSeries.get(id)
        if gs is None:
            raise Exception(f"GameSeries {id} not found")
        gs.begin()
        await gs.save()

    async def next_game(self, id: UUID) -> Game | None:
        games = await self.games(id)
        for g in games:
            if (
                g.status in [GameStatus.SCHEDULED, GameStatus.SIDE_CHOSEN]
                and not g.results
            ):
                return g
        return None

    async def toggle_ready(self, id: UUID, tp: TeamParticipant) -> None:
        next_game = await self.next_game(id)
        if next_game:
            await self.game_service.toggle_ready(next_game.id, tp)
        raise Exception("No next game found")

    async def chose_side(self, id: UUID, tp: TeamParticipant, side: int) -> None:
        games = await self.games(id)
        next_game = await self.next_game(id)

        if next_game:
            idx = games.index(next_game)
            if idx == 0:
                if tp != next_game.teams[0]:
                    raise Exception("First team must chose side")
            else:
                if tp != games[idx - 1].results[-1]:
                    raise Exception("Loser team must chose side")
            await self.game_service.chose_side(next_game.id, tp, side)
        raise Exception("No next game found")

    async def set_game_winner(
        self,
        series_id: UUID,
        game_id: UUID,
        winner_actor: Actor,
    ) -> tuple[GameSeries, Game, Actor | None]:
        """Record the winner of a single game; close the series if best-of clinched.

        Returns (series, game, series_winner_actor_or_None). The series winner
        is non-None only when this submission clinches the series.
        """
        gs = await GameSeries.get(series_id)
        if gs is None:
            raise Exception(f"GameSeries {series_id} not found")
        game = await Game.get(game_id)
        if game is None or game.game_series_id != series_id:
            raise Exception(f"Game {game_id} does not belong to series {series_id}")

        game.set_winner(winner_actor)
        await game.save()

        # Re-tally wins from all games in the series (cheap, and avoids stale
        # in-memory state if the host re-submits).
        games = await self.game_service.get_by_gs_id(series_id)
        wins: dict[UUID, int] = {}
        for g in games:
            if g.status == GameStatus.FINISHED and g.results:
                wid = g.results[0].actor.id
                wins[wid] = wins.get(wid, 0) + 1

        # best_of can be missing on legacy series; default to 1 → first win clinches.
        best_of = max(1, gs.settings.best_of or 1)
        needed = best_of // 2 + 1

        series_winner: Actor | None = None
        for actor_id, count in wins.items():
            if count >= needed:
                tp = next((t for t in gs.teams if t.actor.id == actor_id), None)
                if tp is not None:
                    series_winner = tp.actor
                    break

        if series_winner is not None and gs.status != GameSeriesStatus.FINISHED:
            gs.status = GameSeriesStatus.FINISHED
            gs.end = datetime.now(UTC)
            await gs.save()
        elif series_winner is None and gs.status == GameSeriesStatus.FINISHED:
            # Host overwrote a previously-clinching result; reopen the series.
            gs.status = GameSeriesStatus.ACTIVE
            gs.end = None
            await gs.save()

        return gs, game, series_winner

    async def swap_teams(
        self, id: UUID, t1: TeamParticipant, t2: TeamParticipant
    ) -> None:
        gs = await GameSeries.get(id)
        gs.swap_teams(t1, t2)
        await gs.save()

    async def get_forbidden_champions(self, id: UUID) -> list[int]:
        gs = await GameSeries.get(id)
        games = await self.games(id)
        if gs:
            match gs.settings.draft_type:
                case DraftType.FEARLESS:
                    return self.get_fearless_forbidden(games)
                case DraftType.IRON_MAN:
                    return self.get_iron_man_forbidden(games)
                case DraftType.CLASSIC:
                    return gs.settings.forbidden_champions
                case DraftType.ALL_RANDOM:
                    return gs.settings.forbidden_champions
        raise Exception("No next game found")

    def get_fearless_forbidden(self, games: list[Game]) -> list[int]:
        forbidden = []
        for g in games:
            if g.status == GameStatus.FINISHED and g.draft:
                return g.draft.get_picks()
        return forbidden

    def get_iron_man_forbidden(self, games: list[Game]) -> list[int]:
        forbidden = []
        for g in games:
            if g.status == GameStatus.FINISHED and g.draft:
                return g.draft.get_bans() + g.draft.get_picks()
        return forbidden
