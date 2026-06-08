from uuid import UUID

import grpc

from domain.services.cold_form_service import ColdFormService
from domain.services.hot_form_service import HotFormService
from domain.values import LeagueRank, LolRankName, LolRole, RankRange, Server


def _pagination(pagination):
    page = pagination.page or 1
    page_size = pagination.page_size or 50
    skip = pagination.skip if pagination.HasField("skip") else (page - 1) * page_size
    limit = pagination.limit if pagination.HasField("limit") else page_size
    return page, page_size, skip, limit


def _rank_from_proto(rank, pb2) -> LeagueRank:
    rank_map = {
        pb2.LOL_RANK_NAME_IRON: LolRankName.IRON,
        pb2.LOL_RANK_NAME_BRONZE: LolRankName.BRONZE,
        pb2.LOL_RANK_NAME_SILVER: LolRankName.SILVER,
        pb2.LOL_RANK_NAME_GOLD: LolRankName.GOLD,
        pb2.LOL_RANK_NAME_PLATINUM: LolRankName.PLATINUM,
        pb2.LOL_RANK_NAME_EMERALD: LolRankName.EMERALD,
        pb2.LOL_RANK_NAME_DIAMOND: LolRankName.DIAMOND,
        pb2.LOL_RANK_NAME_MASTER: LolRankName.MASTER,
        pb2.LOL_RANK_NAME_GRANDMASTER: LolRankName.GRANDMASTER,
        pb2.LOL_RANK_NAME_CHALLENGER: LolRankName.CHALLENGER,
    }
    return LeagueRank(
        rank=rank_map.get(rank.rank, LolRankName.IRON),
        division=rank.division or 1,
        lp=rank.lp if rank.HasField("lp") else None,
    )


def _rank_to_proto(rank: LeagueRank, pb2):
    rank_map = {
        LolRankName.IRON: pb2.LOL_RANK_NAME_IRON,
        LolRankName.BRONZE: pb2.LOL_RANK_NAME_BRONZE,
        LolRankName.SILVER: pb2.LOL_RANK_NAME_SILVER,
        LolRankName.GOLD: pb2.LOL_RANK_NAME_GOLD,
        LolRankName.PLATINUM: pb2.LOL_RANK_NAME_PLATINUM,
        LolRankName.EMERALD: pb2.LOL_RANK_NAME_EMERALD,
        LolRankName.DIAMOND: pb2.LOL_RANK_NAME_DIAMOND,
        LolRankName.MASTER: pb2.LOL_RANK_NAME_MASTER,
        LolRankName.GRANDMASTER: pb2.LOL_RANK_NAME_GRANDMASTER,
        LolRankName.CHALLENGER: pb2.LOL_RANK_NAME_CHALLENGER,
    }
    message = pb2.LeagueRank(
        rank=rank_map.get(rank.rank, pb2.LOL_RANK_NAME_UNSPECIFIED),
        division=rank.division,
    )
    if rank.lp is not None:
        message.lp = rank.lp
    return message


def _range_from_proto(rank_range, pb2) -> RankRange:
    server_map = {
        pb2.SERVER_EUW: Server.EUW,
        pb2.SERVER_RU: Server.RU,
        pb2.SERVER_EUNE: Server.EUNE,
        pb2.SERVER_NA: Server.NA,
        pb2.SERVER_TR: Server.TR,
    }
    return RankRange(
        server=server_map.get(rank_range.server, Server.EUW),
        min_rank=_rank_from_proto(rank_range.min_rank, pb2),
        max_rank=_rank_from_proto(rank_range.max_rank, pb2),
    )


def _range_to_proto(rank_range: RankRange, pb2):
    server_map = {
        Server.EUW: pb2.SERVER_EUW,
        Server.RU: pb2.SERVER_RU,
        Server.EUNE: pb2.SERVER_EUNE,
        Server.NA: pb2.SERVER_NA,
        Server.TR: pb2.SERVER_TR,
    }
    return pb2.RankRange(
        server=server_map.get(rank_range.server, pb2.SERVER_UNSPECIFIED),
        min_rank=_rank_to_proto(rank_range.min_rank, pb2),
        max_rank=_rank_to_proto(rank_range.max_rank, pb2),
    )


def _roles_from_proto(roles, pb2) -> list[LolRole]:
    role_map = {
        pb2.LOL_ROLE_TOP: LolRole.TOP,
        pb2.LOL_ROLE_JG: LolRole.JG,
        pb2.LOL_ROLE_MID: LolRole.MID,
        pb2.LOL_ROLE_ADC: LolRole.ADC,
        pb2.LOL_ROLE_SUP: LolRole.SUP,
    }
    return [role_map[role] for role in roles if role in role_map]


def _roles_to_proto(roles: list[LolRole], pb2) -> list[int]:
    role_map = {
        LolRole.TOP: pb2.LOL_ROLE_TOP,
        LolRole.JG: pb2.LOL_ROLE_JG,
        LolRole.MID: pb2.LOL_ROLE_MID,
        LolRole.ADC: pb2.LOL_ROLE_ADC,
        LolRole.SUP: pb2.LOL_ROLE_SUP,
    }
    return [role_map[role] for role in roles if role in role_map]


def _status_from_proto(status, pb2):
    if status == pb2.FORM_STATUS_FROZEN:
        return "frozen"
    return "active"


def _status_to_proto(status: str, pb2):
    return pb2.FORM_STATUS_FROZEN if status == "frozen" else pb2.FORM_STATUS_ACTIVE


def _short_to_proto(short, pb2):
    return pb2.ShortFormResponse(
        blocked_by=[str(user_id) for user_id in short.blocked_by],
        rank_range=[_range_to_proto(item, pb2) for item in short.rank_range],
        my_roles=_roles_to_proto(short.my_roles, pb2),
        looking_for_roles=_roles_to_proto(short.looking_for_roles, pb2),
        description=short.description,
    )


def _cold_to_proto(form, pb2):
    return pb2.ColdFormResponse(
        id=str(form.id),
        owner_id=str(form.owner_id),
        liked_by=[str(user_id) for user_id in form.liked_by],
        disliked_by=[str(user_id) for user_id in form.disliked_by],
        blocked_by=[str(user_id) for user_id in form.blocked_by],
        created_at=form.created_at.isoformat(),
        rank_range=[_range_to_proto(item, pb2) for item in form.rank_range],
        my_roles=_roles_to_proto(form.my_roles, pb2),
        looking_for_roles=_roles_to_proto(form.looking_for_roles, pb2),
        description=form.description,
        status=_status_to_proto(form.status, pb2),
        updated_at=form.updated_at.isoformat(),
        history=[_short_to_proto(item, pb2) for item in form.history],
    )


def _hot_to_proto(form, pb2):
    return pb2.HotFormResponse(
        id=str(form.id),
        owner_id=str(form.owner_id),
        liked_by=[str(user_id) for user_id in form.liked_by],
        disliked_by=[str(user_id) for user_id in form.disliked_by],
        created_at=form.created_at.isoformat(),
        rank_range=[_range_to_proto(item, pb2) for item in form.rank_range],
        my_roles=_roles_to_proto(form.my_roles, pb2),
        looking_for_roles=_roles_to_proto(form.looking_for_roles, pb2),
        description=form.description,
        expires_at=HotFormService.expires_at(form).isoformat(),
    )


def _filter_kwargs(filter_, pb2):
    kwargs = {
        "rank_range": [_range_from_proto(item, pb2) for item in filter_.rank_range]
        or None,
        "my_roles": _roles_from_proto(filter_.my_roles, pb2) or None,
        "looking_for_roles": _roles_from_proto(filter_.looking_for_roles, pb2) or None,
    }
    if filter_.HasField("owner_id"):
        kwargs["owner_id"] = UUID(filter_.owner_id)
    if filter_.HasField("exclude_owner_id"):
        kwargs["exclude_owner_id"] = UUID(filter_.exclude_owner_id)
    return kwargs


def _apply_local_filters(forms, filter_, pb2):
    if not filter_:
        return forms

    if filter_.servers:
        server_map = {
            pb2.SERVER_EUW: Server.EUW,
            pb2.SERVER_RU: Server.RU,
            pb2.SERVER_EUNE: Server.EUNE,
            pb2.SERVER_NA: Server.NA,
            pb2.SERVER_TR: Server.TR,
        }
        servers = {server_map[item] for item in filter_.servers if item in server_map}
        if servers:
            forms = [
                form
                for form in forms
                if any(rank_range.server in servers for rank_range in form.rank_range)
            ]

    if filter_.HasField("query"):
        query = filter_.query.strip().lower()
        if query:
            forms = [form for form in forms if query in form.description.lower()]

    return forms


class PartnerSearchGrpc:
    async def CreateColdForm(self, request, context: grpc.aio.ServicerContext):
        from search.v1 import partner_search_service_pb2 as pb2

        form = await ColdFormService.create(
            owner_id=UUID(request.owner_id),
            rank_range=[_range_from_proto(item, pb2) for item in request.rank_range],
            my_roles=_roles_from_proto(request.my_roles, pb2),
            looking_for_roles=_roles_from_proto(request.looking_for_roles, pb2),
            description=request.description,
            status=_status_from_proto(request.status, pb2),
        )
        return _cold_to_proto(form, pb2)

    async def UpdateColdForm(self, request, context: grpc.aio.ServicerContext):
        from search.v1 import partner_search_service_pb2 as pb2

        existing = await ColdFormService.get_by_id(UUID(request.form_id))
        if not existing:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Cold form not found")
        if request.actor_id and UUID(request.actor_id) != existing.owner_id:
            await context.abort(grpc.StatusCode.PERMISSION_DENIED, "Only owner can update form")

        form = await ColdFormService.update(
            form_id=UUID(request.form_id),
            rank_range=[_range_from_proto(item, pb2) for item in request.rank_range]
            if request.rank_range
            else None,
            my_roles=_roles_from_proto(request.my_roles, pb2)
            if request.my_roles
            else None,
            looking_for_roles=_roles_from_proto(request.looking_for_roles, pb2)
            if request.looking_for_roles
            else None,
            description=request.description if request.HasField("description") else None,
            status=_status_from_proto(request.status, pb2)
            if request.HasField("status")
            else None,
        )
        return _cold_to_proto(form, pb2)

    async def GetColdForm(self, request, context: grpc.aio.ServicerContext):
        from search.v1 import partner_search_service_pb2 as pb2

        form = await ColdFormService.get_by_id(UUID(request.form_id))
        if not form:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Cold form not found")
        return _cold_to_proto(form, pb2)

    async def DeleteColdForm(self, request, context: grpc.aio.ServicerContext):
        from common.types_pb2 import Empty

        existing = await ColdFormService.get_by_id(UUID(request.form_id))
        if not existing:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Cold form not found")
        if request.actor_id and UUID(request.actor_id) != existing.owner_id:
            await context.abort(grpc.StatusCode.PERMISSION_DENIED, "Only owner can delete form")
        await ColdFormService.delete(UUID(request.form_id))
        return Empty()

    async def GetOwnerColdForms(self, request, context: grpc.aio.ServicerContext):
        from search.v1 import partner_search_service_pb2 as pb2

        forms = await ColdFormService.get_by_owner(UUID(request.owner_id))
        page, page_size, skip, limit = _pagination(request.pagination)
        chunk = forms[skip : skip + limit]
        return pb2.ListColdFormsResponse(
            forms=[_cold_to_proto(form, pb2) for form in chunk],
            total_count=len(forms),
            page=page,
            page_size=page_size,
            has_next=skip + limit < len(forms),
        )

    async def SetColdFormStatus(self, request, context: grpc.aio.ServicerContext):
        from search.v1 import partner_search_service_pb2 as pb2

        existing = await ColdFormService.get_by_id(UUID(request.form_id))
        if not existing:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Cold form not found")
        if request.actor_id and UUID(request.actor_id) != existing.owner_id:
            await context.abort(grpc.StatusCode.PERMISSION_DENIED, "Only owner can update form")
        form = await ColdFormService.update(
            UUID(request.form_id),
            status=_status_from_proto(request.status, pb2),
        )
        return _cold_to_proto(form, pb2)

    async def SwipeColdForm(self, request, context: grpc.aio.ServicerContext):
        from search.v1 import partner_search_service_pb2 as pb2

        action = request.action
        if action == pb2.SWIPE_ACTION_LIKE:
            form = await ColdFormService.like(UUID(request.form_id), UUID(request.user_id))
        elif action == pb2.SWIPE_ACTION_BLOCK:
            form = await ColdFormService.block(UUID(request.form_id), UUID(request.user_id))
        else:
            form = await ColdFormService.dislike(UUID(request.form_id), UUID(request.user_id))
        if not form:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Cold form not found")
        return pb2.SwipeFormResponse(matched=False, form=_cold_to_proto(form, pb2))

    async def GetColdDeck(self, request, context: grpc.aio.ServicerContext):
        from search.v1 import partner_search_service_pb2 as pb2

        kwargs = _filter_kwargs(request.filter, pb2) if request.HasField("filter") else {}
        actor_id = UUID(request.actor_id)
        kwargs["exclude_owner_id"] = actor_id
        kwargs["exclude_blocked_by"] = actor_id
        kwargs["status"] = "active"
        forms = await ColdFormService.search(limit=request.limit or 20, **kwargs)
        forms = _apply_local_filters(forms, request.filter if request.HasField("filter") else None, pb2)
        forms = [
            form
            for form in forms
            if actor_id not in form.liked_by
            and actor_id not in form.disliked_by
            and actor_id not in form.blocked_by
        ]
        return pb2.ColdDeckResponse(forms=[_cold_to_proto(form, pb2) for form in forms])

    async def SearchColdForms(self, request, context: grpc.aio.ServicerContext):
        from search.v1 import partner_search_service_pb2 as pb2

        page, page_size, skip, limit = _pagination(request.pagination)
        kwargs = _filter_kwargs(request.filter, pb2) if request.HasField("filter") else {}
        if request.HasField("filter"):
            if request.filter.HasField("exclude_blocked_by"):
                kwargs["exclude_blocked_by"] = UUID(request.filter.exclude_blocked_by)
            if request.filter.HasField("status"):
                kwargs["status"] = _status_from_proto(request.filter.status, pb2)
            if request.filter.HasField("min_likes"):
                kwargs["min_likes"] = request.filter.min_likes
        forms = await ColdFormService.search(limit=limit + 1, skip=skip, **kwargs)
        forms = _apply_local_filters(forms, request.filter if request.HasField("filter") else None, pb2)
        return pb2.ListColdFormsResponse(
            forms=[_cold_to_proto(form, pb2) for form in forms[:limit]],
            total_count=skip + len(forms[:limit]),
            page=page,
            page_size=page_size,
            has_next=len(forms) > limit,
        )

    async def GetPopularColdForms(self, request, context: grpc.aio.ServicerContext):
        from search.v1 import partner_search_service_pb2 as pb2

        limit = request.limit if request.HasField("limit") else 10
        forms = await ColdFormService.get_popular(limit=limit)
        return pb2.ListColdFormsResponse(
            forms=[_cold_to_proto(form, pb2) for form in forms],
            total_count=len(forms),
            page=1,
            page_size=limit,
            has_next=False,
        )

    async def GetColdFormHistory(self, request, context: grpc.aio.ServicerContext):
        from search.v1 import partner_search_service_pb2 as pb2

        history = await ColdFormService.get_history(UUID(request.form_id))
        return pb2.ColdFormHistoryResponse(
            history=[_short_to_proto(item, pb2) for item in history]
        )

    async def CreateHotForm(self, request, context: grpc.aio.ServicerContext):
        from search.v1 import partner_search_service_pb2 as pb2

        form = await HotFormService.create(
            owner_id=UUID(request.owner_id),
            rank_range=[_range_from_proto(item, pb2) for item in request.rank_range],
            my_roles=_roles_from_proto(request.my_roles, pb2),
            looking_for_roles=_roles_from_proto(request.looking_for_roles, pb2),
            description=request.description,
        )
        return _hot_to_proto(form, pb2)

    async def GetHotForm(self, request, context: grpc.aio.ServicerContext):
        from search.v1 import partner_search_service_pb2 as pb2

        form = await HotFormService.get_by_id(UUID(request.form_id))
        if not form:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Hot form not found")
        return _hot_to_proto(form, pb2)

    async def SearchHotForms(self, request, context: grpc.aio.ServicerContext):
        from search.v1 import partner_search_service_pb2 as pb2

        page, page_size, skip, limit = _pagination(request.pagination)
        kwargs = _filter_kwargs(request.filter, pb2) if request.HasField("filter") else {}
        forms = await HotFormService.search(limit=limit + 1, skip=skip, **kwargs)
        forms = _apply_local_filters(forms, request.filter if request.HasField("filter") else None, pb2)
        return pb2.ListHotFormsResponse(
            forms=[_hot_to_proto(form, pb2) for form in forms[:limit]],
            total_count=skip + len(forms[:limit]),
            page=page,
            page_size=page_size,
            has_next=len(forms) > limit,
        )

    async def SwipeHotForm(self, request, context: grpc.aio.ServicerContext):
        from search.v1 import partner_search_service_pb2 as pb2

        if request.action == pb2.SWIPE_ACTION_LIKE:
            form = await HotFormService.like(UUID(request.form_id), UUID(request.user_id))
        else:
            form = await HotFormService.dislike(UUID(request.form_id), UUID(request.user_id))
        if not form:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Hot form not found")
        return pb2.HotFormSwipeResponse(matched=False, form=_hot_to_proto(form, pb2))
