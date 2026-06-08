# services/providers.py

from typing import AsyncIterator
from dishka import Provider, Scope, make_async_container, provide

from redis.asyncio import Redis
import grpc

from settings import Settings
from fastapi_sso.sso.yandex import YandexSSO
from fastapi_sso.sso.discord import DiscordSSO
from fastapi_sso import SSOBase


from dishka.integrations.fastapi import (
    FastapiProvider,
)
from shared.mail import MailSender
from shared.redis_manager import RedisManager
from shared.redis import RedisService
from domain.session_repo import SessionRepo
from domain.session_service import SessionService
from domain.auth_service import AuthService

from stubs.user_stub import UserStub
from community.user.v1 import user_service_pb2 as user_pb2
from community.user.v1 import user_service_pb2_grpc as user_pb2_grpc


class SSOProvider(Provider):
    @provide(scope=Scope.APP)
    def get_yandex_sso(self, settings: Settings) -> YandexSSO:
        return YandexSSO(
            client_id=settings.yandex_cid,
            client_secret=settings.yandex_cs,
            redirect_uri="http://localhost:8000/auth/yandex/callback",
            allow_insecure_http=True,
            scope=["login:email"],
        )

    @provide(scope=Scope.APP)
    def get_discord_sso(self, settings: Settings) -> DiscordSSO:
        return DiscordSSO(
            client_id=settings.discord_cid,
            client_secret=settings.discord_cs,
            redirect_uri="http://localhost:8000/auth/discord/callback",
            allow_insecure_http=True,
            scope=["email"],
        )

    @provide(scope=Scope.APP)
    def get_sso_dict(
        self, yandex_sso: YandexSSO, discord_sso: DiscordSSO
    ) -> dict[str, SSOBase]:
        return {"yandex": yandex_sso, "discord": discord_sso}


class ConfigProvider(Provider):
    @provide(scope=Scope.APP)
    def get_settings(self) -> Settings:
        return Settings()


class GrpcProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_community_channel(
        self, settings: Settings
    ) -> AsyncIterator[grpc.aio.Channel]:
        async with grpc.aio.insecure_channel(
            settings.community_grpc_address
        ) as channel:
            yield channel

    @provide(scope=Scope.APP)
    def get_user_stub(self, channel: grpc.aio.Channel) -> UserStub:
        return UserStub(channel)


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
    def get_session_repo(self, redis: RedisService) -> SessionRepo:
        return SessionRepo(redis)

    @provide(scope=Scope.REQUEST)
    def get_session_service(self, repo: SessionRepo) -> SessionService:
        return SessionService(repo)

    @provide(scope=Scope.REQUEST)
    def get_auth_service(
        self,
        session_service: SessionService,
        mail_service: MailSender,
        redis_service: RedisService,
        settings: Settings,
        sso_dict: dict[str, SSOBase],
        user_stub: UserStub,
    ) -> AuthService:
        return AuthService(
            session_service, mail_service, redis_service, settings, sso_dict, user_stub
        )


container = make_async_container(
    ServiceProvider(),
    ConfigProvider(),
    SSOProvider(),
    GrpcProvider(),
    FastapiProvider(),
)
