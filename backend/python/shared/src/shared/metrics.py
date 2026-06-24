"""Общие утилиты для экспорта Prometheus-метрик.

Для HTTP (FastAPI) — middleware + /metrics endpoint.
Для gRPC — отдельный HTTP-сервер на фиксированном порту + interceptor.
"""

from __future__ import annotations

import os
import time
from typing import Awaitable, Callable

import grpc
from fastapi import FastAPI, Request, Response
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    Counter,
    Histogram,
    generate_latest,
    start_http_server,
)


_DEF_BUCKETS = (0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10)


def _app_name(default: str = "unknown") -> str:
    return os.getenv("APP_NAME", default)


# ---------------------------------------------------------------------------
# HTTP / FastAPI
# ---------------------------------------------------------------------------

def setup_fastapi_metrics(app: FastAPI, service_name: str | None = None) -> None:
    """Регистрирует middleware и /metrics endpoint для FastAPI-приложения."""

    service = service_name or _app_name()
    registry = CollectorRegistry(auto_describe=True)

    requests_total = Counter(
        "http_requests_total",
        "Количество HTTP-запросов",
        labelnames=("service", "method", "path", "status"),
        registry=registry,
    )
    request_duration = Histogram(
        "http_request_duration_seconds",
        "Длительность HTTP-запросов в секундах",
        labelnames=("service", "method", "path"),
        buckets=_DEF_BUCKETS,
        registry=registry,
    )
    in_progress = Counter(
        "http_requests_in_progress",
        "Запросы, выполняющиеся прямо сейчас",
        labelnames=("service", "method"),
        registry=registry,
    )

    @app.middleware("http")
    async def _metrics_middleware(request: Request, call_next):  # type: ignore[no-untyped-def]
        if request.url.path == "/metrics":
            return await call_next(request)

        in_progress.labels(service, request.method).inc()
        start = time.perf_counter()
        status = "500"
        try:
            response: Response = await call_next(request)
            status = str(response.status_code)
            return response
        finally:
            elapsed = time.perf_counter() - start
            route = request.scope.get("route")
            path = getattr(route, "path", request.url.path)
            requests_total.labels(service, request.method, path, status).inc()
            request_duration.labels(service, request.method, path).observe(elapsed)

    @app.get("/metrics", include_in_schema=False)
    def _metrics() -> Response:
        return Response(generate_latest(registry), media_type=CONTENT_TYPE_LATEST)


# ---------------------------------------------------------------------------
# gRPC
# ---------------------------------------------------------------------------

_GRPC_REGISTRY = CollectorRegistry(auto_describe=True)
_grpc_started = False

GRPC_REQUESTS = Counter(
    "grpc_server_handled_total",
    "Количество обработанных gRPC-запросов",
    labelnames=("service", "grpc_service", "grpc_method", "code"),
    registry=_GRPC_REGISTRY,
)
GRPC_LATENCY = Histogram(
    "grpc_server_handling_seconds",
    "Длительность обработки gRPC-запросов",
    labelnames=("service", "grpc_service", "grpc_method"),
    buckets=_DEF_BUCKETS,
    registry=_GRPC_REGISTRY,
)


class PrometheusGrpcInterceptor(grpc.aio.ServerInterceptor):
    """Минимальный async-interceptor: считает запросы и длительность."""

    def __init__(self, service_name: str | None = None) -> None:
        self._service = service_name or _app_name()

    async def intercept_service(self, continuation, handler_call_details):  # type: ignore[override]
        handler = await continuation(handler_call_details)
        if handler is None:
            return handler

        full_method = handler_call_details.method or "/unknown/unknown"
        # /package.Service/Method
        try:
            _, grpc_service, grpc_method = full_method.split("/", 2)
        except ValueError:
            grpc_service, grpc_method = "unknown", full_method

        service = self._service

        # Подменяем unary_unary (самый распространённый случай).
        if handler.unary_unary:
            original = handler.unary_unary

            async def wrapper(request, context):  # type: ignore[no-untyped-def]
                start = time.perf_counter()
                code = "OK"
                try:
                    return await original(request, context)
                except grpc.RpcError as exc:  # type: ignore[attr-defined]
                    code = getattr(exc, "code", lambda: grpc.StatusCode.UNKNOWN)().name
                    raise
                except Exception:
                    code = "UNKNOWN"
                    raise
                finally:
                    GRPC_REQUESTS.labels(service, grpc_service, grpc_method, code).inc()
                    GRPC_LATENCY.labels(service, grpc_service, grpc_method).observe(
                        time.perf_counter() - start
                    )

            return grpc.unary_unary_rpc_method_handler(
                wrapper,
                request_deserializer=handler.request_deserializer,
                response_serializer=handler.response_serializer,
            )

        if handler.unary_stream:
            original = handler.unary_stream

            async def us_wrapper(request, context):  # type: ignore[no-untyped-def]
                start = time.perf_counter()
                code = "OK"
                try:
                    async for resp in original(request, context):
                        yield resp
                except grpc.RpcError as exc:  # type: ignore[attr-defined]
                    code = getattr(exc, "code", lambda: grpc.StatusCode.UNKNOWN)().name
                    raise
                except Exception:
                    code = "UNKNOWN"
                    raise
                finally:
                    GRPC_REQUESTS.labels(service, grpc_service, grpc_method, code).inc()
                    GRPC_LATENCY.labels(service, grpc_service, grpc_method).observe(
                        time.perf_counter() - start
                    )

            return grpc.unary_stream_rpc_method_handler(
                us_wrapper,
                request_deserializer=handler.request_deserializer,
                response_serializer=handler.response_serializer,
            )

        if handler.stream_unary:
            original = handler.stream_unary

            async def su_wrapper(request_iterator, context):  # type: ignore[no-untyped-def]
                start = time.perf_counter()
                code = "OK"
                try:
                    return await original(request_iterator, context)
                except grpc.RpcError as exc:  # type: ignore[attr-defined]
                    code = getattr(exc, "code", lambda: grpc.StatusCode.UNKNOWN)().name
                    raise
                except Exception:
                    code = "UNKNOWN"
                    raise
                finally:
                    GRPC_REQUESTS.labels(service, grpc_service, grpc_method, code).inc()
                    GRPC_LATENCY.labels(service, grpc_service, grpc_method).observe(
                        time.perf_counter() - start
                    )

            return grpc.stream_unary_rpc_method_handler(
                su_wrapper,
                request_deserializer=handler.request_deserializer,
                response_serializer=handler.response_serializer,
            )

        if handler.stream_stream:
            original = handler.stream_stream

            async def ss_wrapper(request_iterator, context):  # type: ignore[no-untyped-def]
                start = time.perf_counter()
                code = "OK"
                try:
                    async for resp in original(request_iterator, context):
                        yield resp
                except grpc.RpcError as exc:  # type: ignore[attr-defined]
                    code = getattr(exc, "code", lambda: grpc.StatusCode.UNKNOWN)().name
                    raise
                except Exception:
                    code = "UNKNOWN"
                    raise
                finally:
                    GRPC_REQUESTS.labels(service, grpc_service, grpc_method, code).inc()
                    GRPC_LATENCY.labels(service, grpc_service, grpc_method).observe(
                        time.perf_counter() - start
                    )

            return grpc.stream_stream_rpc_method_handler(
                ss_wrapper,
                request_deserializer=handler.request_deserializer,
                response_serializer=handler.response_serializer,
            )

        return handler


def start_grpc_metrics_server(port: int | None = None) -> None:
    """Поднимает отдельный HTTP-сервер для отдачи метрик gRPC-сервиса."""

    global _grpc_started
    if _grpc_started:
        return
    port = port or int(os.getenv("METRICS_PORT", "9100"))
    start_http_server(port, registry=_GRPC_REGISTRY)
    _grpc_started = True
