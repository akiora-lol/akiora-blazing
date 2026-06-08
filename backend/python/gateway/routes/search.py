from typing import Optional
from uuid import UUID

import grpc
from fastapi import APIRouter, HTTPException, Query, status
from loguru import logger

from dependencies import get_search_channel
from shared.contracts.search import (
    ColdDeckRequest,
    ColdDeckResponse,
    ColdFormResponse,
    CreateColdFormRequest,
    CreateHotFormRequest,
    DeleteFormRequest,
    FormStatus,
    GetFormRequest,
    HotFormResponse,
    HotFormSwipeRequest,
    HotFormSwipeResponse,
    ListColdFormsRequest,
    ListColdFormsResponse,
    ListHotFormsRequest,
    ListHotFormsResponse,
    LolRole,
    PaginationRequest,
    PopularColdFormsRequest,
    SearchFormsFilter,
    Server,
    SwipeAction,
    SwipeFormRequest,
    SwipeFormResponse,
)
from stubs.search_stub import SearchStub

router = APIRouter(prefix="/v1/search", tags=["search"])


def _get_stub() -> SearchStub:
    return SearchStub(get_search_channel())


def _grpc_to_http(code: grpc.StatusCode) -> int:
    return {
        grpc.StatusCode.NOT_FOUND: status.HTTP_404_NOT_FOUND,
        grpc.StatusCode.PERMISSION_DENIED: status.HTTP_403_FORBIDDEN,
        grpc.StatusCode.UNAUTHENTICATED: status.HTTP_401_UNAUTHORIZED,
        grpc.StatusCode.INVALID_ARGUMENT: status.HTTP_400_BAD_REQUEST,
        grpc.StatusCode.ALREADY_EXISTS: status.HTTP_409_CONFLICT,
    }.get(code, status.HTTP_500_INTERNAL_SERVER_ERROR)


def _filter(
    roles: Optional[list[LolRole]] = None,
    servers: Optional[list[Server]] = None,
    owner_id: Optional[UUID] = None,
    exclude_owner_id: Optional[UUID] = None,
    exclude_blocked_by: Optional[UUID] = None,
    status_: Optional[FormStatus] = FormStatus.ACTIVE,
    min_likes: Optional[int] = None,
    query: Optional[str] = None,
) -> SearchFormsFilter:
    return SearchFormsFilter(
        looking_for_roles=roles or [],
        servers=servers or [],
        owner_id=owner_id,
        exclude_owner_id=exclude_owner_id,
        exclude_blocked_by=exclude_blocked_by,
        status=status_,
        min_likes=min_likes,
        query=query,
    )


@router.post("/cold-forms", response_model=ColdFormResponse, status_code=status.HTTP_201_CREATED)
async def create_cold_form(request: CreateColdFormRequest):
    try:
        return await _get_stub().create_cold_form(request)
    except grpc.RpcError as e:
        logger.warning("gRPC error in create_cold_form: {} {}", e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.post("/hot-forms", response_model=HotFormResponse, status_code=status.HTTP_201_CREATED)
async def create_hot_form(request: CreateHotFormRequest):
    try:
        return await _get_stub().create_hot_form(request)
    except grpc.RpcError as e:
        logger.warning("gRPC error in create_hot_form: {} {}", e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get("/cold-forms/{form_id}", response_model=ColdFormResponse)
async def get_cold_form(form_id: UUID):
    try:
        return await _get_stub().get_cold_form(GetFormRequest(form_id=form_id))
    except grpc.RpcError as e:
        logger.warning("gRPC error in get_cold_form({}): {} {}", form_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.delete("/cold-forms/{form_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cold_form(form_id: UUID, actor_id: UUID):
    try:
        await _get_stub().delete_cold_form(
            DeleteFormRequest(form_id=form_id, actor_id=actor_id)
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in delete_cold_form({}): {} {}", form_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.post("/cold-forms/deck", response_model=ColdDeckResponse)
async def get_cold_deck(request: ColdDeckRequest):
    try:
        return await _get_stub().get_cold_deck(request)
    except grpc.RpcError as e:
        logger.warning("gRPC error in get_cold_deck: {} {}", e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.post("/cold-forms/search", response_model=ListColdFormsResponse)
async def search_cold_forms(request: ListColdFormsRequest):
    try:
        return await _get_stub().search_cold_forms(request)
    except grpc.RpcError as e:
        logger.warning("gRPC error in search_cold_forms: {} {}", e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get("/cold-forms/popular", response_model=ListColdFormsResponse)
async def get_popular_cold_forms(limit: int = Query(default=10, ge=1, le=100)):
    try:
        return await _get_stub().get_popular_cold_forms(PopularColdFormsRequest(limit=limit))
    except grpc.RpcError as e:
        logger.warning("gRPC error in get_popular_cold_forms: {} {}", e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.post("/cold-forms/{form_id}/swipe", response_model=SwipeFormResponse)
async def swipe_cold_form(form_id: UUID, user_id: UUID, action: SwipeAction):
    try:
        return await _get_stub().swipe_cold_form(
            SwipeFormRequest(form_id=form_id, user_id=user_id, action=action)
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in swipe_cold_form({}): {} {}", form_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get("/hot-forms/{form_id}", response_model=HotFormResponse)
async def get_hot_form(form_id: UUID):
    try:
        return await _get_stub().get_hot_form(GetFormRequest(form_id=form_id))
    except grpc.RpcError as e:
        logger.warning("gRPC error in get_hot_form({}): {} {}", form_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.get("/hot-forms", response_model=ListHotFormsResponse)
async def list_hot_forms(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=100),
    roles: Optional[list[LolRole]] = Query(default=None),
    servers: Optional[list[Server]] = Query(default=None),
    owner_id: Optional[UUID] = None,
    exclude_owner_id: Optional[UUID] = None,
    query: Optional[str] = None,
):
    try:
        return await _get_stub().search_hot_forms(
            ListHotFormsRequest(
                filter=_filter(
                    roles=roles,
                    servers=servers,
                    owner_id=owner_id,
                    exclude_owner_id=exclude_owner_id,
                    status_=None,
                    query=query,
                ),
                pagination=PaginationRequest(page=page, page_size=page_size),
            )
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in list_hot_forms: {} {}", e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.post("/hot-forms/search", response_model=ListHotFormsResponse)
async def search_hot_forms(request: ListHotFormsRequest):
    try:
        return await _get_stub().search_hot_forms(request)
    except grpc.RpcError as e:
        logger.warning("gRPC error in search_hot_forms: {} {}", e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())


@router.post("/hot-forms/{form_id}/swipe", response_model=HotFormSwipeResponse)
async def swipe_hot_form(form_id: UUID, user_id: UUID, action: SwipeAction):
    try:
        return await _get_stub().swipe_hot_form(
            HotFormSwipeRequest(form_id=form_id, user_id=user_id, action=action)
        )
    except grpc.RpcError as e:
        logger.warning("gRPC error in swipe_hot_form({}): {} {}", form_id, e.code(), e.details())
        raise HTTPException(status_code=_grpc_to_http(e.code()), detail=e.details())
