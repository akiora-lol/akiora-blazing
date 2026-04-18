import asyncio
from grpc import aio
from grpc_reflection.v1alpha import reflection

from dishka.integrations.grpcio import DishkaAioInterceptor

from messenger.v1.messenger_service_pb2_grpc import (
    add_ChatServiceServicer_to_server,
    add_MessageServiceServicer_to_server,
)
from messenger.v1.messenger_service_pb2 import DESCRIPTOR as messenger_descriptor

from app.chat_grpc import ChatGrpc
from app.message_grpc import MessageGrpc
from ioc import container
from setup import setup
from settings import settings


async def serve():
    await setup()

    server = aio.server(interceptors=[DishkaAioInterceptor(container)])

    add_ChatServiceServicer_to_server(ChatGrpc(), server)
    add_MessageServiceServicer_to_server(MessageGrpc(), server)

    service_names = [
        s.full_name
        for s in messenger_descriptor.services_by_name.values()
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
