from typing import AsyncIterator

from dishka import Provider, Scope, provide, make_async_container

from settings import Settings
from shared.redis import RedisService
from shared.redis_manager import RedisManager
from redis.asyncio import Redis
from domain.services.lol.tournament_serivce import TournamentService
from domain.services.lol.game_series_service import GameSeriesService
from domain.services.lol.game_service import GameService
from domain.services.lol.single_elim_builder import SingleEliminationBuilder


class ConfigProvider(Provider):
    @provide(scope=Scope.APP)
    def get_settings(self) -> Settings:
        return Settings()


class InfraProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_redis_manager(
        self, settings: Settings
    ) -> AsyncIterator[RedisManager]:
        manager = RedisManager(settings.redis_url)
        async with manager.managed() as m:
            yield m

    @provide(scope=Scope.REQUEST)
    async def get_redis_client(self, rm: RedisManager) -> AsyncIterator[Redis]:
        async with rm.get_client_context() as client:
            yield client

    @provide(scope=Scope.REQUEST)
    def get_redis_service(self, redis_client: Redis, st: Settings) -> RedisService:
        return RedisService(redis_client, st.redis_ttl)


class DomainProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_se_bracket(self) -> SingleEliminationBuilder:
        return SingleEliminationBuilder()

    @provide(scope=Scope.REQUEST)
    def get_game_service(self, redis_client: RedisService) -> GameService:
        return GameService(redis_client)

    @provide(scope=Scope.REQUEST)
    def get_game_series_service(
        self, redis_client: RedisService, gs: GameService
    ) -> GameSeriesService:
        return GameSeriesService(redis_client, gs)

    @provide(scope=Scope.REQUEST)
    def get_tournament_service(
        self,
        redis_client: RedisService,
        gss: GameSeriesService,
        se: SingleEliminationBuilder,
    ) -> TournamentService:
        return TournamentService(redis_client, gss, se)


container = make_async_container(ConfigProvider(), InfraProvider(), DomainProvider())
