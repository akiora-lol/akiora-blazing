import grpc
from grpc_reflection.v1alpha.proto_reflection_descriptor_database import (
    ProtoReflectionDescriptorDatabase,
)
from google.protobuf import descriptor_pool as descriptor_pool_module
from google.protobuf import json_format
from google.protobuf.message_factory import GetMessageClassesForFiles
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from loguru import logger

from settings import Settings

settings = Settings()

app = FastAPI(title="Akiora Gateway")

_channels: dict[str, grpc.Channel] = {}
_pools: dict[str, descriptor_pool_module.DescriptorPool] = {}


def get_channel(service_key: str) -> grpc.Channel:
    if service_key not in _channels:
        address = settings.grpc_services.get(service_key)
        if address is None:
            raise KeyError(f"Unknown gRPC service: {service_key!r}")
        channel = grpc.insecure_channel(address)
        reflection_db = ProtoReflectionDescriptorDatabase(channel)
        _channels[service_key] = channel
        _pools[service_key] = descriptor_pool_module.DescriptorPool(reflection_db)
        logger.info(f"Connected to gRPC service {service_key!r} at {address}")
    return _channels[service_key]


def get_pool(service_key: str) -> descriptor_pool_module.DescriptorPool:
    get_channel(service_key)
    return _pools[service_key]


@app.post("/{service_key}/{full_path:path}")
async def dynamic_proxy(
    service_key: str,
    full_path: str,
    request: Request,
) -> Response:
    # full_path = "akiora.game.tournament.TournamentService/GetTournament"
    if "/" not in full_path:
        return JSONResponse(
            status_code=400, content={"detail": "Path must be ServiceName/MethodName"}
        )

    grpc_service, method_name = full_path.rsplit("/", 1)

    cookies = dict(request.cookies)
    logger.info(f"[{service_key}/{grpc_service}/{method_name}] cookies: {cookies}")

    try:
        channel = get_channel(service_key)
    except KeyError as e:
        return JSONResponse(status_code=404, content={"detail": str(e)})

    pool = get_pool(service_key)

    grpc_method = f"/{grpc_service}/{method_name}"
    full_method_name = f"{grpc_service}.{method_name}"

    try:
        service_desc = pool.FindServiceByName(grpc_service)
        method_desc = service_desc.FindMethodByName(method_name)
    except KeyError:
        return JSONResponse(
            status_code=404,
            content={
                "detail": f"gRPC method {full_method_name!r} not found via reflection"
            },
        )

    input_desc = method_desc.input_type
    output_desc = method_desc.output_type

    classes = GetMessageClassesForFiles([input_desc.file.name], pool)
    input_class = classes.get(input_desc.full_name)
    output_class = classes.get(output_desc.full_name)

    if input_class is None or output_class is None:
        return JSONResponse(
            status_code=500,
            content={"detail": "Could not resolve protobuf message classes"},
        )

    body = await request.json()
    grpc_request = json_format.ParseDict(body, input_class())

    stub_method = channel.unary_unary(
        grpc_method,
        request_serializer=lambda msg: msg.SerializeToString(),
        response_deserializer=output_class.FromString,
    )

    try:
        grpc_response = stub_method(grpc_request)
    except grpc.RpcError as e:
        code: grpc.StatusCode = e.code()
        return JSONResponse(
            status_code=_grpc_status_to_http(code),
            content={"detail": e.details(), "grpc_code": code.name},
        )

    return JSONResponse(
        content=json_format.MessageToDict(
            grpc_response, preserving_proto_field_name=True
        )
    )


def _grpc_status_to_http(code: grpc.StatusCode) -> int:
    mapping = {
        grpc.StatusCode.OK: 200,
        grpc.StatusCode.NOT_FOUND: 404,
        grpc.StatusCode.ALREADY_EXISTS: 409,
        grpc.StatusCode.PERMISSION_DENIED: 403,
        grpc.StatusCode.UNAUTHENTICATED: 401,
        grpc.StatusCode.INVALID_ARGUMENT: 400,
        grpc.StatusCode.UNAVAILABLE: 503,
        grpc.StatusCode.UNIMPLEMENTED: 501,
        grpc.StatusCode.INTERNAL: 500,
        grpc.StatusCode.RESOURCE_EXHAUSTED: 429,
        grpc.StatusCode.DEADLINE_EXCEEDED: 504,
    }
    return mapping.get(code, 500)


if __name__ == "__main__":
    from granian import Granian

    Granian(
        "main:app",
        address="0.0.0.0",
        port=8000,
        interface="asgi",
    ).serve()
