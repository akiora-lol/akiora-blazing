from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class Server(str, Enum):
    EUW = "euw"
    RU = "ru"
    EUNE = "eune"
    NA = "na"
    TR = "tr"


class LolRole(str, Enum):
    TOP = "top"
    JG = "jg"
    MID = "mid"
    ADC = "adc"
    SUP = "sup"


class LolRankName(str, Enum):
    IRON = "iron"
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"
    EMERALD = "emerald"
    DIAMOND = "diamond"
    MASTER = "master"
    GRANDMASTER = "grandmaster"
    CHALLENGER = "challenger"


class FormStatus(str, Enum):
    ACTIVE = "active"
    FROZEN = "frozen"


class SwipeAction(str, Enum):
    LIKE = "like"
    DISLIKE = "dislike"
    BLOCK = "block"


class LeagueRank(BaseModel):
    rank: LolRankName
    division: int = Field(default=1, ge=1, le=4)
    lp: Optional[int] = Field(default=None, ge=0)


class RankRange(BaseModel):
    server: Server
    min_rank: LeagueRank
    max_rank: LeagueRank


class OwnerPreview(BaseModel):
    user_id: UUID
    username: Optional[str] = None
    avatar_url: Optional[str] = None
    riot_game_name: Optional[str] = None
    riot_tagline: Optional[str] = None
    profile_image_url: Optional[str] = None
    solo_rank: Optional[LeagueRank] = None
    solo_tier_image_url: Optional[str] = None


class ShortFormResponse(BaseModel):
    blocked_by: list[UUID] = Field(default_factory=list)
    rank_range: list[RankRange] = Field(default_factory=list)
    my_roles: list[LolRole] = Field(default_factory=list)
    looking_for_roles: list[LolRole] = Field(default_factory=list)
    description: str = ""


class ColdFormResponse(BaseModel):
    id: UUID
    owner_id: UUID
    owner: Optional[OwnerPreview] = None
    liked_by: list[UUID] = Field(default_factory=list)
    disliked_by: list[UUID] = Field(default_factory=list)
    blocked_by: list[UUID] = Field(default_factory=list)
    created_at: datetime
    rank_range: list[RankRange] = Field(default_factory=list)
    my_roles: list[LolRole] = Field(default_factory=list)
    looking_for_roles: list[LolRole] = Field(default_factory=list)
    description: str
    status: FormStatus = FormStatus.ACTIVE
    updated_at: datetime
    history: list[ShortFormResponse] = Field(default_factory=list)


class HotFormResponse(BaseModel):
    id: UUID
    owner_id: UUID
    owner: Optional[OwnerPreview] = None
    liked_by: list[UUID] = Field(default_factory=list)
    disliked_by: list[UUID] = Field(default_factory=list)
    created_at: datetime
    rank_range: list[RankRange] = Field(default_factory=list)
    my_roles: list[LolRole] = Field(default_factory=list)
    looking_for_roles: list[LolRole] = Field(default_factory=list)
    description: str
    expires_at: Optional[datetime] = None


class PaginationRequest(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=50, ge=1, le=100)
    skip: Optional[int] = Field(default=None, ge=0)
    limit: Optional[int] = Field(default=None, ge=1, le=100)


class SearchFormsFilter(BaseModel):
    rank_range: list[RankRange] = Field(default_factory=list)
    my_roles: list[LolRole] = Field(default_factory=list)
    looking_for_roles: list[LolRole] = Field(default_factory=list)
    servers: list[Server] = Field(default_factory=list)
    owner_id: Optional[UUID] = None
    exclude_owner_id: Optional[UUID] = None
    exclude_blocked_by: Optional[UUID] = None
    status: Optional[FormStatus] = FormStatus.ACTIVE
    min_likes: Optional[int] = Field(default=None, ge=0)
    query: Optional[str] = None


class CreateColdFormRequest(BaseModel):
    owner_id: UUID
    rank_range: list[RankRange]
    my_roles: list[LolRole] = Field(default_factory=list)
    looking_for_roles: list[LolRole] = Field(default_factory=list)
    description: str = Field(min_length=1, max_length=1000)
    status: FormStatus = FormStatus.ACTIVE


class UpdateColdFormRequest(BaseModel):
    form_id: UUID
    actor_id: UUID
    rank_range: list[RankRange] = Field(default_factory=list)
    my_roles: list[LolRole] = Field(default_factory=list)
    looking_for_roles: list[LolRole] = Field(default_factory=list)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: Optional[FormStatus] = None


class GetFormRequest(BaseModel):
    form_id: UUID


class DeleteFormRequest(BaseModel):
    form_id: UUID
    actor_id: UUID


class GetOwnerFormsRequest(BaseModel):
    owner_id: UUID
    pagination: PaginationRequest = Field(default_factory=PaginationRequest)


class SetColdFormStatusRequest(BaseModel):
    form_id: UUID
    actor_id: UUID
    status: FormStatus


class SwipeFormRequest(BaseModel):
    form_id: UUID
    user_id: UUID
    action: SwipeAction


class SwipeFormResponse(BaseModel):
    matched: bool = False
    form: ColdFormResponse
    matched_user_id: Optional[UUID] = None


class ColdDeckRequest(BaseModel):
    actor_id: UUID
    filter: SearchFormsFilter = Field(default_factory=SearchFormsFilter)
    limit: int = Field(default=20, ge=1, le=100)


class ColdDeckResponse(BaseModel):
    forms: list[ColdFormResponse] = Field(default_factory=list)


class ListColdFormsRequest(BaseModel):
    filter: SearchFormsFilter = Field(default_factory=SearchFormsFilter)
    pagination: PaginationRequest = Field(default_factory=PaginationRequest)


class ListColdFormsResponse(BaseModel):
    forms: list[ColdFormResponse] = Field(default_factory=list)
    total_count: int = 0
    page: int = 1
    page_size: int = 50
    has_next: bool = False


class ColdFormHistoryResponse(BaseModel):
    history: list[ShortFormResponse] = Field(default_factory=list)


class CreateHotFormRequest(BaseModel):
    owner_id: UUID
    rank_range: list[RankRange]
    my_roles: list[LolRole] = Field(default_factory=list)
    looking_for_roles: list[LolRole] = Field(default_factory=list)
    description: str = Field(min_length=1, max_length=1000)


class ListHotFormsRequest(BaseModel):
    filter: SearchFormsFilter = Field(default_factory=SearchFormsFilter)
    pagination: PaginationRequest = Field(default_factory=PaginationRequest)


class ListHotFormsResponse(BaseModel):
    forms: list[HotFormResponse] = Field(default_factory=list)
    total_count: int = 0
    page: int = 1
    page_size: int = 50
    has_next: bool = False


class HotFormSwipeRequest(BaseModel):
    form_id: UUID
    user_id: UUID
    action: SwipeAction


class HotFormSwipeResponse(BaseModel):
    matched: bool = False
    form: HotFormResponse
    matched_user_id: Optional[UUID] = None


class PopularColdFormsRequest(BaseModel):
    limit: int = Field(default=10, ge=1, le=100)
