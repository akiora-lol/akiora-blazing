from dishka import Provider, Scope, provide, make_async_container

from settings import Settings
from domain.services.user_service import UserService
from domain.services.club_service import ClubService
from domain.services.team_service import TeamService


class ConfigProvider(Provider):
    @provide(scope=Scope.APP)
    def get_settings(self) -> Settings:
        return Settings()


class DomainProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_user_service(self) -> UserService:
        return UserService()

    @provide(scope=Scope.REQUEST)
    def get_club_service(self) -> ClubService:
        return ClubService()

    @provide(scope=Scope.REQUEST)
    def get_team_service(self) -> TeamService:
        return TeamService()


container = make_async_container(ConfigProvider(), DomainProvider())
