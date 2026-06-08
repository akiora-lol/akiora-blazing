import grpc.aio as grpc
from uuid import UUID

from shared.contracts.search import (
    ColdDeckRequest,
    ColdDeckResponse,
    ColdFormHistoryResponse,
    ColdFormResponse,
    CreateColdFormRequest,
    CreateHotFormRequest,
    DeleteFormRequest,
    FormStatus,
    GetFormRequest,
    GetOwnerFormsRequest,
    HotFormResponse,
    HotFormSwipeRequest,
    HotFormSwipeResponse,
    LeagueRank,
    ListColdFormsRequest,
    ListColdFormsResponse,
    ListHotFormsRequest,
    ListHotFormsResponse,
    LolRankName,
    LolRole,
    OwnerPreview,
    PaginationRequest,
    PopularColdFormsRequest,
    RankRange,
    SearchFormsFilter,
    Server,
    SetColdFormStatusRequest,
    ShortFormResponse,
    SwipeAction,
    SwipeFormRequest,
    SwipeFormResponse,
    UpdateColdFormRequest,
)

import search.v1.partner_search_service_pb2 as pb2_module
import search.v1.partner_search_service_pb2_grpc as pb2_grpc_module


class SearchMapper:
    SERVER_TO_PROTO = {
        Server.EUW: pb2_module.SERVER_EUW,
        Server.RU: pb2_module.SERVER_RU,
        Server.EUNE: pb2_module.SERVER_EUNE,
        Server.NA: pb2_module.SERVER_NA,
        Server.TR: pb2_module.SERVER_TR,
    }
    SERVER_FROM_PROTO = {v: k for k, v in SERVER_TO_PROTO.items()}

    ROLE_TO_PROTO = {
        LolRole.TOP: pb2_module.LOL_ROLE_TOP,
        LolRole.JG: pb2_module.LOL_ROLE_JG,
        LolRole.MID: pb2_module.LOL_ROLE_MID,
        LolRole.ADC: pb2_module.LOL_ROLE_ADC,
        LolRole.SUP: pb2_module.LOL_ROLE_SUP,
    }
    ROLE_FROM_PROTO = {v: k for k, v in ROLE_TO_PROTO.items()}

    RANK_TO_PROTO = {
        LolRankName.IRON: pb2_module.LOL_RANK_NAME_IRON,
        LolRankName.BRONZE: pb2_module.LOL_RANK_NAME_BRONZE,
        LolRankName.SILVER: pb2_module.LOL_RANK_NAME_SILVER,
        LolRankName.GOLD: pb2_module.LOL_RANK_NAME_GOLD,
        LolRankName.PLATINUM: pb2_module.LOL_RANK_NAME_PLATINUM,
        LolRankName.EMERALD: pb2_module.LOL_RANK_NAME_EMERALD,
        LolRankName.DIAMOND: pb2_module.LOL_RANK_NAME_DIAMOND,
        LolRankName.MASTER: pb2_module.LOL_RANK_NAME_MASTER,
        LolRankName.GRANDMASTER: pb2_module.LOL_RANK_NAME_GRANDMASTER,
        LolRankName.CHALLENGER: pb2_module.LOL_RANK_NAME_CHALLENGER,
    }
    RANK_FROM_PROTO = {v: k for k, v in RANK_TO_PROTO.items()}

    STATUS_TO_PROTO = {
        FormStatus.ACTIVE: pb2_module.FORM_STATUS_ACTIVE,
        FormStatus.FROZEN: pb2_module.FORM_STATUS_FROZEN,
    }
    STATUS_FROM_PROTO = {v: k for k, v in STATUS_TO_PROTO.items()}

    ACTION_TO_PROTO = {
        SwipeAction.LIKE: pb2_module.SWIPE_ACTION_LIKE,
        SwipeAction.DISLIKE: pb2_module.SWIPE_ACTION_DISLIKE,
        SwipeAction.BLOCK: pb2_module.SWIPE_ACTION_BLOCK,
    }
    ACTION_FROM_PROTO = {v: k for k, v in ACTION_TO_PROTO.items()}

    @classmethod
    def to_pydantic_rank(cls, rank) -> LeagueRank:
        return LeagueRank(
            rank=cls.RANK_FROM_PROTO.get(rank.rank, LolRankName.IRON),
            division=rank.division or 1,
            lp=rank.lp if rank.HasField("lp") else None,
        )

    @classmethod
    def to_grpc_rank(cls, rank: LeagueRank):
        grpc_rank = pb2_module.LeagueRank(
            rank=cls.RANK_TO_PROTO.get(rank.rank, pb2_module.LOL_RANK_NAME_UNSPECIFIED),
            division=rank.division,
        )
        if rank.lp is not None:
            grpc_rank.lp = rank.lp
        return grpc_rank

    @classmethod
    def to_pydantic_range(cls, rank_range) -> RankRange:
        return RankRange(
            server=cls.SERVER_FROM_PROTO.get(rank_range.server, Server.EUW),
            min_rank=cls.to_pydantic_rank(rank_range.min_rank),
            max_rank=cls.to_pydantic_rank(rank_range.max_rank),
        )

    @classmethod
    def to_grpc_range(cls, rank_range: RankRange):
        return pb2_module.RankRange(
            server=cls.SERVER_TO_PROTO.get(rank_range.server, pb2_module.SERVER_UNSPECIFIED),
            min_rank=cls.to_grpc_rank(rank_range.min_rank),
            max_rank=cls.to_grpc_rank(rank_range.max_rank),
        )

    @classmethod
    def to_pydantic_owner(cls, owner) -> OwnerPreview | None:
        if not owner or not owner.user_id:
            return None
        return OwnerPreview(
            user_id=UUID(owner.user_id),
            username=owner.username or None,
            avatar_url=owner.avatar_url or None,
            riot_game_name=owner.riot_game_name or None,
            riot_tagline=owner.riot_tagline or None,
            profile_image_url=owner.profile_image_url or None,
            solo_rank=cls.to_pydantic_rank(owner.solo_rank)
            if owner.HasField("solo_rank")
            else None,
            solo_tier_image_url=owner.solo_tier_image_url or None,
        )

    @classmethod
    def to_pydantic_short_form(cls, form) -> ShortFormResponse:
        return ShortFormResponse(
            blocked_by=[UUID(user_id) for user_id in form.blocked_by],
            rank_range=[cls.to_pydantic_range(item) for item in form.rank_range],
            my_roles=[cls.ROLE_FROM_PROTO.get(role, LolRole.TOP) for role in form.my_roles],
            looking_for_roles=[
                cls.ROLE_FROM_PROTO.get(role, LolRole.TOP)
                for role in form.looking_for_roles
            ],
            description=form.description,
        )

    @classmethod
    def to_pydantic_cold(cls, form) -> ColdFormResponse:
        return ColdFormResponse(
            id=UUID(form.id),
            owner_id=UUID(form.owner_id),
            owner=cls.to_pydantic_owner(form.owner) if form.HasField("owner") else None,
            liked_by=[UUID(user_id) for user_id in form.liked_by],
            disliked_by=[UUID(user_id) for user_id in form.disliked_by],
            blocked_by=[UUID(user_id) for user_id in form.blocked_by],
            created_at=form.created_at,
            rank_range=[cls.to_pydantic_range(item) for item in form.rank_range],
            my_roles=[cls.ROLE_FROM_PROTO.get(role, LolRole.TOP) for role in form.my_roles],
            looking_for_roles=[
                cls.ROLE_FROM_PROTO.get(role, LolRole.TOP)
                for role in form.looking_for_roles
            ],
            description=form.description,
            status=cls.STATUS_FROM_PROTO.get(form.status, FormStatus.ACTIVE),
            updated_at=form.updated_at,
            history=[cls.to_pydantic_short_form(item) for item in form.history],
        )

    @classmethod
    def to_pydantic_hot(cls, form) -> HotFormResponse:
        return HotFormResponse(
            id=UUID(form.id),
            owner_id=UUID(form.owner_id),
            owner=cls.to_pydantic_owner(form.owner) if form.HasField("owner") else None,
            liked_by=[UUID(user_id) for user_id in form.liked_by],
            disliked_by=[UUID(user_id) for user_id in form.disliked_by],
            created_at=form.created_at,
            rank_range=[cls.to_pydantic_range(item) for item in form.rank_range],
            my_roles=[cls.ROLE_FROM_PROTO.get(role, LolRole.TOP) for role in form.my_roles],
            looking_for_roles=[
                cls.ROLE_FROM_PROTO.get(role, LolRole.TOP)
                for role in form.looking_for_roles
            ],
            description=form.description,
            expires_at=form.expires_at if form.HasField("expires_at") else None,
        )

    @classmethod
    def to_grpc_pagination(cls, pagination: PaginationRequest):
        request = pb2_module.PaginationRequest(
            page=pagination.page,
            page_size=pagination.page_size,
        )
        if pagination.skip is not None:
            request.skip = pagination.skip
        if pagination.limit is not None:
            request.limit = pagination.limit
        return request

    @classmethod
    def to_grpc_filter(cls, filter_: SearchFormsFilter):
        request = pb2_module.SearchFormsFilter(
            rank_range=[cls.to_grpc_range(item) for item in filter_.rank_range],
            my_roles=[cls.ROLE_TO_PROTO.get(role, 0) for role in filter_.my_roles],
            looking_for_roles=[
                cls.ROLE_TO_PROTO.get(role, 0) for role in filter_.looking_for_roles
            ],
            servers=[cls.SERVER_TO_PROTO.get(server, 0) for server in filter_.servers],
        )
        if filter_.owner_id:
            request.owner_id = str(filter_.owner_id)
        if filter_.exclude_owner_id:
            request.exclude_owner_id = str(filter_.exclude_owner_id)
        if filter_.exclude_blocked_by:
            request.exclude_blocked_by = str(filter_.exclude_blocked_by)
        if filter_.status:
            request.status = cls.STATUS_TO_PROTO.get(filter_.status, 0)
        if filter_.min_likes is not None:
            request.min_likes = filter_.min_likes
        if filter_.query:
            request.query = filter_.query
        return request

    @classmethod
    def to_grpc_create_cold(cls, request: CreateColdFormRequest):
        return pb2_module.CreateColdFormRequest(
            owner_id=str(request.owner_id),
            rank_range=[cls.to_grpc_range(item) for item in request.rank_range],
            my_roles=[cls.ROLE_TO_PROTO.get(role, 0) for role in request.my_roles],
            looking_for_roles=[
                cls.ROLE_TO_PROTO.get(role, 0) for role in request.looking_for_roles
            ],
            description=request.description,
            status=cls.STATUS_TO_PROTO.get(request.status, 0),
        )

    @classmethod
    def to_grpc_update_cold(cls, request: UpdateColdFormRequest):
        grpc_request = pb2_module.UpdateColdFormRequest(
            form_id=str(request.form_id),
            actor_id=str(request.actor_id),
            rank_range=[cls.to_grpc_range(item) for item in request.rank_range],
            my_roles=[cls.ROLE_TO_PROTO.get(role, 0) for role in request.my_roles],
            looking_for_roles=[
                cls.ROLE_TO_PROTO.get(role, 0) for role in request.looking_for_roles
            ],
        )
        if request.description is not None:
            grpc_request.description = request.description
        if request.status is not None:
            grpc_request.status = cls.STATUS_TO_PROTO.get(request.status, 0)
        return grpc_request

    @classmethod
    def to_grpc_create_hot(cls, request: CreateHotFormRequest):
        return pb2_module.CreateHotFormRequest(
            owner_id=str(request.owner_id),
            rank_range=[cls.to_grpc_range(item) for item in request.rank_range],
            my_roles=[cls.ROLE_TO_PROTO.get(role, 0) for role in request.my_roles],
            looking_for_roles=[
                cls.ROLE_TO_PROTO.get(role, 0) for role in request.looking_for_roles
            ],
            description=request.description,
        )


class SearchStub:
    def __init__(self, channel: grpc.Channel):
        self.stub = pb2_grpc_module.PartnerSearchServiceStub(channel)
        self.mapper = SearchMapper()

    async def create_cold_form(self, request: CreateColdFormRequest) -> ColdFormResponse:
        response = await self.stub.CreateColdForm(self.mapper.to_grpc_create_cold(request))
        return self.mapper.to_pydantic_cold(response)

    async def update_cold_form(self, request: UpdateColdFormRequest) -> ColdFormResponse:
        response = await self.stub.UpdateColdForm(self.mapper.to_grpc_update_cold(request))
        return self.mapper.to_pydantic_cold(response)

    async def get_cold_form(self, request: GetFormRequest) -> ColdFormResponse:
        response = await self.stub.GetColdForm(
            pb2_module.GetFormRequest(form_id=str(request.form_id))
        )
        return self.mapper.to_pydantic_cold(response)

    async def delete_cold_form(self, request: DeleteFormRequest):
        return await self.stub.DeleteColdForm(
            pb2_module.DeleteFormRequest(
                form_id=str(request.form_id),
                actor_id=str(request.actor_id),
            )
        )

    async def get_owner_cold_forms(
        self, request: GetOwnerFormsRequest
    ) -> ListColdFormsResponse:
        response = await self.stub.GetOwnerColdForms(
            pb2_module.GetOwnerFormsRequest(
                owner_id=str(request.owner_id),
                pagination=self.mapper.to_grpc_pagination(request.pagination),
            )
        )
        return self.mapper.to_pydantic_cold_list(response)

    async def set_cold_form_status(
        self, request: SetColdFormStatusRequest
    ) -> ColdFormResponse:
        response = await self.stub.SetColdFormStatus(
            pb2_module.SetColdFormStatusRequest(
                form_id=str(request.form_id),
                actor_id=str(request.actor_id),
                status=self.mapper.STATUS_TO_PROTO.get(request.status, 0),
            )
        )
        return self.mapper.to_pydantic_cold(response)

    async def swipe_cold_form(self, request: SwipeFormRequest) -> SwipeFormResponse:
        response = await self.stub.SwipeColdForm(
            pb2_module.SwipeFormRequest(
                form_id=str(request.form_id),
                user_id=str(request.user_id),
                action=self.mapper.ACTION_TO_PROTO.get(request.action, 0),
            )
        )
        return SwipeFormResponse(
            matched=response.matched,
            form=self.mapper.to_pydantic_cold(response.form),
            matched_user_id=UUID(response.matched_user_id)
            if response.HasField("matched_user_id")
            else None,
        )

    async def get_cold_deck(self, request: ColdDeckRequest) -> ColdDeckResponse:
        response = await self.stub.GetColdDeck(
            pb2_module.ColdDeckRequest(
                actor_id=str(request.actor_id),
                filter=self.mapper.to_grpc_filter(request.filter),
                limit=request.limit,
            )
        )
        return ColdDeckResponse(
            forms=[self.mapper.to_pydantic_cold(form) for form in response.forms]
        )

    async def search_cold_forms(
        self, request: ListColdFormsRequest
    ) -> ListColdFormsResponse:
        response = await self.stub.SearchColdForms(
            pb2_module.ListColdFormsRequest(
                filter=self.mapper.to_grpc_filter(request.filter),
                pagination=self.mapper.to_grpc_pagination(request.pagination),
            )
        )
        return self.mapper.to_pydantic_cold_list(response)

    async def get_popular_cold_forms(
        self, request: PopularColdFormsRequest
    ) -> ListColdFormsResponse:
        response = await self.stub.GetPopularColdForms(
            pb2_module.PopularColdFormsRequest(limit=request.limit)
        )
        return self.mapper.to_pydantic_cold_list(response)

    async def get_cold_form_history(
        self, request: GetFormRequest
    ) -> ColdFormHistoryResponse:
        response = await self.stub.GetColdFormHistory(
            pb2_module.GetFormRequest(form_id=str(request.form_id))
        )
        return ColdFormHistoryResponse(
            history=[self.mapper.to_pydantic_short_form(item) for item in response.history]
        )

    async def create_hot_form(self, request: CreateHotFormRequest) -> HotFormResponse:
        response = await self.stub.CreateHotForm(self.mapper.to_grpc_create_hot(request))
        return self.mapper.to_pydantic_hot(response)

    async def get_hot_form(self, request: GetFormRequest) -> HotFormResponse:
        response = await self.stub.GetHotForm(
            pb2_module.GetFormRequest(form_id=str(request.form_id))
        )
        return self.mapper.to_pydantic_hot(response)

    async def search_hot_forms(
        self, request: ListHotFormsRequest
    ) -> ListHotFormsResponse:
        response = await self.stub.SearchHotForms(
            pb2_module.ListHotFormsRequest(
                filter=self.mapper.to_grpc_filter(request.filter),
                pagination=self.mapper.to_grpc_pagination(request.pagination),
            )
        )
        return self.mapper.to_pydantic_hot_list(response)

    async def swipe_hot_form(
        self, request: HotFormSwipeRequest
    ) -> HotFormSwipeResponse:
        response = await self.stub.SwipeHotForm(
            pb2_module.HotFormSwipeRequest(
                form_id=str(request.form_id),
                user_id=str(request.user_id),
                action=self.mapper.ACTION_TO_PROTO.get(request.action, 0),
            )
        )
        return HotFormSwipeResponse(
            matched=response.matched,
            form=self.mapper.to_pydantic_hot(response.form),
            matched_user_id=UUID(response.matched_user_id)
            if response.HasField("matched_user_id")
            else None,
        )


def _to_cold_list(mapper: SearchMapper, response) -> ListColdFormsResponse:
    return ListColdFormsResponse(
        forms=[mapper.to_pydantic_cold(form) for form in response.forms],
        total_count=response.total_count,
        page=response.page,
        page_size=response.page_size,
        has_next=response.has_next,
    )


def _to_hot_list(mapper: SearchMapper, response) -> ListHotFormsResponse:
    return ListHotFormsResponse(
        forms=[mapper.to_pydantic_hot(form) for form in response.forms],
        total_count=response.total_count,
        page=response.page,
        page_size=response.page_size,
        has_next=response.has_next,
    )


SearchMapper.to_pydantic_cold_list = _to_cold_list
SearchMapper.to_pydantic_hot_list = _to_hot_list
