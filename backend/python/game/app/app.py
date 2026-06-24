import asyncio
from grpc import aio
from grpc_reflection.v1alpha import reflection

from dishka.integrations.grpcio import DishkaAioInterceptor
from shared.metrics import PrometheusGrpcInterceptor, start_grpc_metrics_server

from game.v1.gameseries_service_pb2_grpc import (
    add_GameSeriesServiceServicer_to_server,
)
from game.v1.gameseries_service_pb2 import DESCRIPTOR as gameseries_descriptor
from game.v1.tournament_service_pb2_grpc import (
    add_TournamentServiceServicer_to_server,
)
from game.v1.tournament_service_pb2 import DESCRIPTOR as tournament_descriptor

from app.gameseries_grpc import GameSeriesGrpc
from app.tournament_gprc import TournamentGrpc
from ioc import container
from setup import setup
from settings import settings


async def serve():

    await setup()

    start_grpc_metrics_server()
    server = aio.server(
        interceptors=[
            PrometheusGrpcInterceptor("game"),
            DishkaAioInterceptor(container),
        ]
    )

    add_GameSeriesServiceServicer_to_server(GameSeriesGrpc(), server)
    add_TournamentServiceServicer_to_server(TournamentGrpc(), server)

    service_names = [
        s.full_name
        for descriptor in (gameseries_descriptor, tournament_descriptor)
        for s in descriptor.services_by_name.values()
    ]
    reflection.enable_server_reflection(
        service_names + [reflection.SERVICE_NAME], server
    )

    listen_addr = f"[::]:{settings.grpc_port}"
    server.add_insecure_port(listen_addr)

    await server.start()
    print(f"gRPC server started on {listen_addr}")

    try:
        await server.wait_for_termination()
    finally:
        await container.close()
        await server.stop(grace=5)
