from fastapi import APIRouter, HTTPException, status
from uuid import UUID
import grpc
from loguru import logger

from shared.contracts.group import (
    CreateGroupRequest,
    GetGroupRequest,
    PatchGroupRequest,
    GroupResponse,
)
from stubs.group_stub import GroupStub
from dependencies import get_community_channel

router = APIRouter(prefix="/v1/groups", tags=["groups"])


def _get_stub() -> GroupStub:
    return GroupStub(get_community_channel())


@router.post(
    path="",
    response_model=GroupResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_group(request: CreateGroupRequest):
    try:
        return await _get_stub().create_group(request)
    except grpc.RpcError as e:
        logger.warning("gRPC error in create_group: {} {}", e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get(path="/{group_id}", response_model=GroupResponse)
async def get_group(group_id: UUID):
    try:
        return await _get_stub().get_group(GetGroupRequest(id=group_id))
    except grpc.RpcError as e:
        logger.warning("gRPC error in get_group({}): {} {}", group_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.patch(path="/{group_id}", response_model=GroupResponse)
async def patch_group(group_id: UUID, request: PatchGroupRequest):
    try:
        return await _get_stub().patch_group(request)
    except grpc.RpcError as e:
        logger.warning("gRPC error in patch_group({}): {} {}", group_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


def _grpc_to_http(code: grpc.StatusCode) -> int:
    mapping = {
        grpc.StatusCode.OK: 200,
        grpc.StatusCode.NOT_FOUND: 404,
        grpc.StatusCode.ALREADY_EXISTS: 409,
        grpc.StatusCode.PERMISSION_DENIED: 403,
        grpc.StatusCode.UNAUTHENTICATED: 401,
        grpc.StatusCode.INVALID_ARGUMENT: 400,
        grpc.StatusCode.UNAVAILABLE: 503,
    }
    return mapping.get(code, 500)
