from uuid import UUID
from domain.value_objects.actors import TeamParticipant
from domain.entities.lol.game import Game
from domain.value_objects.settings import LolGameSettings
from shared.redis import RedisService


class GameService:
    def __init__(self, rs: RedisService):
        self.rs = rs

    async def create(
        self,
        game_series_id: UUID,
        teams: list[TeamParticipant],
        settings: LolGameSettings,
    ) -> Game:
        g = Game.domain_create(
            game_series_id=game_series_id,
            teams=teams,
            settings=settings,
        )
        await g.save()
        return g

    async def toggle_ready(self, id: UUID, tp: TeamParticipant) -> Game:
        g = await Game.get(id)
        g.toggle_ready(tp)
        await g.save()
        return g

    async def chose_side(self, id: UUID, tp: TeamParticipant, side: int) -> Game:
        g = await Game.get(id)
        g.chose_side(tp, side)
        await g.save()
        return g

    async def get_by_gs_id(self, gs_id: UUID) -> list[Game]:
        return await Game.find(Game.game_series_id == gs_id).to_list()
