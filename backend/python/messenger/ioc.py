from typing import AsyncIterator

from dishka import Provider, Scope, provide, make_async_container

from settings import Settings
from shared.redis import RedisService
from shared.redis_manager import RedisManager
from redis.asyncio import Redis
from domain.services.chat import ChatService
from domain.services.message import MessageService


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
    def get_chat_service(self) -> ChatService:
        return ChatService()

    @provide(scope=Scope.REQUEST)
    def get_message_service(self) -> MessageService:
        return MessageService()


container = make_async_container(ConfigProvider(), InfraProvider(), DomainProvider())
