# services/providers.py

from typing import AsyncIterator
from dishka import Provider, Scope, make_async_container, provide

from redis.asyncio import Redis


from settings import Settings


from dishka.integrations.fastapi import (
    FastapiProvider,
)
from shared.mail import MailSender
from shared.redis_manager import RedisManager
from shared.redis import RedisService
from redis_invalidator import RedisInvalidator


class ConfigProvider(Provider):
    @provide(scope=Scope.APP)
    def get_settings(self) -> Settings:
        return Settings()


class ServiceProvider(Provider):
    scope = Scope.APP

    @provide(scope=Scope.APP)
    def get_mail_service(self, settings: Settings) -> MailSender:
        return MailSender(
            settings.smtp_server,
            settings.smtp_port,
            settings.email_address,
            settings.email_password,
        )

    @provide(scope=Scope.APP)
    def get_redis_manager(self, settings: Settings) -> RedisManager:
        return RedisManager(settings.redis_url)

    @provide(scope=Scope.REQUEST)
    async def get_redis_client(self, rm: RedisManager) -> AsyncIterator[Redis]:
        async with rm.get_client_context() as client:
            yield client

    @provide(scope=Scope.REQUEST)
    def get_redis_service(self, redis_client: Redis) -> RedisService:
        return RedisService(redis_client)

    @provide(scope=Scope.REQUEST)
    def get_redis_invalidator(self, redis_service: RedisService) -> RedisInvalidator:
        return RedisInvalidator(redis_service)


container = make_async_container(
    ServiceProvider(),
    ConfigProvider(),
    FastapiProvider(),
)
