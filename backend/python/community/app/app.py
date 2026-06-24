import asyncio
from grpc import aio
from grpc_reflection.v1alpha import reflection
from loguru import logger

from dishka.integrations.grpcio import DishkaAioInterceptor
from shared.metrics import PrometheusGrpcInterceptor, start_grpc_metrics_server

from community.user.v1.user_service_pb2_grpc import (
    add_UserServiceServicer_to_server,
    UserServiceServicer,
)
from community.user.v1.user_service_pb2 import DESCRIPTOR as user_descriptor
from community.club.v1.club_service_pb2_grpc import (
    add_ClubServiceServicer_to_server,
    ClubServiceServicer,
)
from community.club.v1.club_service_pb2 import DESCRIPTOR as club_descriptor
from community.team.v1.team_service_pb2_grpc import (
    add_TeamServiceServicer_to_server,
    TeamServiceServicer,
)
from community.team.v1.team_service_pb2 import DESCRIPTOR as team_descriptor

from app.user_grpc import UserGrpc
from app.club_grpc import ClubGrpc
from app.team_grpc import TeamGrpc
from domain.services.lol_refresher import LolRefresher
from ioc import container
from setup import setup
from settings import settings


class _UserGrpc(UserGrpc, UserServiceServicer):
    pass


class _ClubGrpc(ClubGrpc, ClubServiceServicer):
    pass


class _TeamGrpc(TeamGrpc, TeamServiceServicer):
    pass


async def serve():
    await setup()

    start_grpc_metrics_server()
    server = aio.server(
        interceptors=[
            PrometheusGrpcInterceptor("community"),
            DishkaAioInterceptor(container),
        ]
    )

    add_UserServiceServicer_to_server(_UserGrpc(), server)
    add_ClubServiceServicer_to_server(_ClubGrpc(), server)
    add_TeamServiceServicer_to_server(_TeamGrpc(), server)

    service_names = [
        s.full_name
        for descriptor in (user_descriptor, club_descriptor, team_descriptor)
        for s in descriptor.services_by_name.values()
    ]
    reflection.enable_server_reflection(
        service_names + [reflection.SERVICE_NAME], server
    )

    listen_addr = f"[::]:{settings.grpc_port}"
    server.add_insecure_port(listen_addr)

    await server.start()
    logger.info("Community gRPC server started on {}", listen_addr)

    refresher = LolRefresher(interval_seconds=settings.lol_refresh_interval_seconds)
    refresher.start()

    try:
        await server.wait_for_termination()
    finally:
        logger.info("Community gRPC server shutting down...")
        await refresher.stop()
        await container.close()
        await server.stop(grace=5)
