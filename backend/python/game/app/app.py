import asyncio
from grpc import aio

from dishka.integrations.grpcio import DishkaAioInterceptor

from game.v1.gameseries_service_pb2_grpc import (
    add_GameSeriesServiceServicer_to_server,
)
from game.v1.tournament_service_pb2_grpc import (
    add_TournamentServiceServicer_to_server,
)

from app.gameseries_grpc import GameSeriesGrpc
from app.tournament_gprc import TournamentGrpc
from ioc import container
from setup import setup
from settings import settings


async def serve():

    await setup()

    server = aio.server(interceptors=[DishkaAioInterceptor(container)])

    add_GameSeriesServiceServicer_to_server(GameSeriesGrpc(), server)
    add_TournamentServiceServicer_to_server(TournamentGrpc(), server)

    listen_addr = f"[::]:{settings.grpc_port}"
    server.add_insecure_port(listen_addr)

    await server.start()
    print(f"gRPC server started on {listen_addr}")

    try:
        await server.wait_for_termination()
    finally:
        await container.close()
        await server.stop(grace=5)
