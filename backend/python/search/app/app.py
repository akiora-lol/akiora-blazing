import asyncio

from grpc import aio
from grpc_reflection.v1alpha import reflection
from loguru import logger

from shared.metrics import PrometheusGrpcInterceptor, start_grpc_metrics_server

from app.search_grpc import PartnerSearchGrpc
from search.v1.partner_search_service_pb2 import DESCRIPTOR as search_descriptor
from search.v1.partner_search_service_pb2_grpc import (
    PartnerSearchServiceServicer,
    add_PartnerSearchServiceServicer_to_server,
)
from settings import settings
from setup import setup


class _PartnerSearchGrpc(PartnerSearchGrpc, PartnerSearchServiceServicer):
    pass


async def serve():
    await setup()

    start_grpc_metrics_server()
    server = aio.server(interceptors=[PrometheusGrpcInterceptor("search")])
    add_PartnerSearchServiceServicer_to_server(_PartnerSearchGrpc(), server)

    service_names = [
        service.full_name
        for service in search_descriptor.services_by_name.values()
    ]
    reflection.enable_server_reflection(
        service_names + [reflection.SERVICE_NAME],
        server,
    )

    listen_addr = f"[::]:{settings.grpc_port}"
    server.add_insecure_port(listen_addr)

    await server.start()
    logger.info("Search gRPC server started on {}", listen_addr)

    try:
        await server.wait_for_termination()
    finally:
        logger.info("Search gRPC server shutting down...")
        await server.stop(grace=5)


if __name__ == "__main__":
    asyncio.run(serve())
