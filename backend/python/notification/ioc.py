from typing import AsyncIterator

from dishka import Provider, Scope, make_async_container, provide
from redis.asyncio import Redis
from shared.redis import RedisService
from shared.redis_manager import RedisManager

from notification_service import NotificationService
from settings import Settings


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
        async with manager.managed() as redis_manager:
            yield redis_manager

    @provide(scope=Scope.REQUEST)
    async def get_redis_client(self, manager: RedisManager) -> AsyncIterator[Redis]:
        async with manager.get_client_context() as client:
            yield client

    @provide(scope=Scope.REQUEST)
    def get_redis_service(self, redis_client: Redis, settings: Settings) -> RedisService:
        return RedisService(redis_client, settings.redis_ttl)


class DomainProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_notification_service(
        self, redis_service: RedisService, settings: Settings
    ) -> NotificationService:
        return NotificationService(redis_service, settings)


container = make_async_container(ConfigProvider(), InfraProvider(), DomainProvider())
