from google.api import annotations_pb2 as _annotations_pb2
from google.api import http_pb2 as _http_pb2
from common import types_pb2 as _types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Server(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SERVER_UNSPECIFIED: _ClassVar[Server]
    SERVER_EUW: _ClassVar[Server]
    SERVER_RU: _ClassVar[Server]
    SERVER_EUNE: _ClassVar[Server]
    SERVER_NA: _ClassVar[Server]
    SERVER_TR: _ClassVar[Server]

class LolRole(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LOL_ROLE_UNSPECIFIED: _ClassVar[LolRole]
    LOL_ROLE_TOP: _ClassVar[LolRole]
    LOL_ROLE_JG: _ClassVar[LolRole]
    LOL_ROLE_MID: _ClassVar[LolRole]
    LOL_ROLE_ADC: _ClassVar[LolRole]
    LOL_ROLE_SUP: _ClassVar[LolRole]

class LolRankName(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LOL_RANK_NAME_UNSPECIFIED: _ClassVar[LolRankName]
    LOL_RANK_NAME_IRON: _ClassVar[LolRankName]
    LOL_RANK_NAME_BRONZE: _ClassVar[LolRankName]
    LOL_RANK_NAME_SILVER: _ClassVar[LolRankName]
    LOL_RANK_NAME_GOLD: _ClassVar[LolRankName]
    LOL_RANK_NAME_PLATINUM: _ClassVar[LolRankName]
    LOL_RANK_NAME_EMERALD: _ClassVar[LolRankName]
    LOL_RANK_NAME_DIAMOND: _ClassVar[LolRankName]
    LOL_RANK_NAME_MASTER: _ClassVar[LolRankName]
    LOL_RANK_NAME_GRANDMASTER: _ClassVar[LolRankName]
    LOL_RANK_NAME_CHALLENGER: _ClassVar[LolRankName]

class FormStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FORM_STATUS_UNSPECIFIED: _ClassVar[FormStatus]
    FORM_STATUS_ACTIVE: _ClassVar[FormStatus]
    FORM_STATUS_FROZEN: _ClassVar[FormStatus]

class SwipeAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SWIPE_ACTION_UNSPECIFIED: _ClassVar[SwipeAction]
    SWIPE_ACTION_LIKE: _ClassVar[SwipeAction]
    SWIPE_ACTION_DISLIKE: _ClassVar[SwipeAction]
    SWIPE_ACTION_BLOCK: _ClassVar[SwipeAction]
SERVER_UNSPECIFIED: Server
SERVER_EUW: Server
SERVER_RU: Server
SERVER_EUNE: Server
SERVER_NA: Server
SERVER_TR: Server
LOL_ROLE_UNSPECIFIED: LolRole
LOL_ROLE_TOP: LolRole
LOL_ROLE_JG: LolRole
LOL_ROLE_MID: LolRole
LOL_ROLE_ADC: LolRole
LOL_ROLE_SUP: LolRole
LOL_RANK_NAME_UNSPECIFIED: LolRankName
LOL_RANK_NAME_IRON: LolRankName
LOL_RANK_NAME_BRONZE: LolRankName
LOL_RANK_NAME_SILVER: LolRankName
LOL_RANK_NAME_GOLD: LolRankName
LOL_RANK_NAME_PLATINUM: LolRankName
LOL_RANK_NAME_EMERALD: LolRankName
LOL_RANK_NAME_DIAMOND: LolRankName
LOL_RANK_NAME_MASTER: LolRankName
LOL_RANK_NAME_GRANDMASTER: LolRankName
LOL_RANK_NAME_CHALLENGER: LolRankName
FORM_STATUS_UNSPECIFIED: FormStatus
FORM_STATUS_ACTIVE: FormStatus
FORM_STATUS_FROZEN: FormStatus
SWIPE_ACTION_UNSPECIFIED: SwipeAction
SWIPE_ACTION_LIKE: SwipeAction
SWIPE_ACTION_DISLIKE: SwipeAction
SWIPE_ACTION_BLOCK: SwipeAction

class LeagueRank(_message.Message):
    __slots__ = ("rank", "division", "lp")
    RANK_FIELD_NUMBER: _ClassVar[int]
    DIVISION_FIELD_NUMBER: _ClassVar[int]
    LP_FIELD_NUMBER: _ClassVar[int]
    rank: LolRankName
    division: int
    lp: int
    def __init__(self, rank: _Optional[_Union[LolRankName, str]] = ..., division: _Optional[int] = ..., lp: _Optional[int] = ...) -> None: ...

class RankRange(_message.Message):
    __slots__ = ("server", "min_rank", "max_rank")
    SERVER_FIELD_NUMBER: _ClassVar[int]
    MIN_RANK_FIELD_NUMBER: _ClassVar[int]
    MAX_RANK_FIELD_NUMBER: _ClassVar[int]
    server: Server
    min_rank: LeagueRank
    max_rank: LeagueRank
    def __init__(self, server: _Optional[_Union[Server, str]] = ..., min_rank: _Optional[_Union[LeagueRank, _Mapping]] = ..., max_rank: _Optional[_Union[LeagueRank, _Mapping]] = ...) -> None: ...

class OwnerPreview(_message.Message):
    __slots__ = ("user_id", "username", "avatar_url", "riot_game_name", "riot_tagline", "profile_image_url", "solo_rank", "solo_tier_image_url")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    AVATAR_URL_FIELD_NUMBER: _ClassVar[int]
    RIOT_GAME_NAME_FIELD_NUMBER: _ClassVar[int]
    RIOT_TAGLINE_FIELD_NUMBER: _ClassVar[int]
    PROFILE_IMAGE_URL_FIELD_NUMBER: _ClassVar[int]
    SOLO_RANK_FIELD_NUMBER: _ClassVar[int]
    SOLO_TIER_IMAGE_URL_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    username: str
    avatar_url: str
    riot_game_name: str
    riot_tagline: str
    profile_image_url: str
    solo_rank: LeagueRank
    solo_tier_image_url: str
    def __init__(self, user_id: _Optional[str] = ..., username: _Optional[str] = ..., avatar_url: _Optional[str] = ..., riot_game_name: _Optional[str] = ..., riot_tagline: _Optional[str] = ..., profile_image_url: _Optional[str] = ..., solo_rank: _Optional[_Union[LeagueRank, _Mapping]] = ..., solo_tier_image_url: _Optional[str] = ...) -> None: ...

class ShortFormResponse(_message.Message):
    __slots__ = ("blocked_by", "rank_range", "my_roles", "looking_for_roles", "description")
    BLOCKED_BY_FIELD_NUMBER: _ClassVar[int]
    RANK_RANGE_FIELD_NUMBER: _ClassVar[int]
    MY_ROLES_FIELD_NUMBER: _ClassVar[int]
    LOOKING_FOR_ROLES_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    blocked_by: _containers.RepeatedScalarFieldContainer[str]
    rank_range: _containers.RepeatedCompositeFieldContainer[RankRange]
    my_roles: _containers.RepeatedScalarFieldContainer[LolRole]
    looking_for_roles: _containers.RepeatedScalarFieldContainer[LolRole]
    description: str
    def __init__(self, blocked_by: _Optional[_Iterable[str]] = ..., rank_range: _Optional[_Iterable[_Union[RankRange, _Mapping]]] = ..., my_roles: _Optional[_Iterable[_Union[LolRole, str]]] = ..., looking_for_roles: _Optional[_Iterable[_Union[LolRole, str]]] = ..., description: _Optional[str] = ...) -> None: ...

class ColdFormResponse(_message.Message):
    __slots__ = ("id", "owner_id", "owner", "liked_by", "disliked_by", "blocked_by", "created_at", "rank_range", "my_roles", "looking_for_roles", "description", "status", "updated_at", "history")
    ID_FIELD_NUMBER: _ClassVar[int]
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    LIKED_BY_FIELD_NUMBER: _ClassVar[int]
    DISLIKED_BY_FIELD_NUMBER: _ClassVar[int]
    BLOCKED_BY_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    RANK_RANGE_FIELD_NUMBER: _ClassVar[int]
    MY_ROLES_FIELD_NUMBER: _ClassVar[int]
    LOOKING_FOR_ROLES_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    HISTORY_FIELD_NUMBER: _ClassVar[int]
    id: str
    owner_id: str
    owner: OwnerPreview
    liked_by: _containers.RepeatedScalarFieldContainer[str]
    disliked_by: _containers.RepeatedScalarFieldContainer[str]
    blocked_by: _containers.RepeatedScalarFieldContainer[str]
    created_at: str
    rank_range: _containers.RepeatedCompositeFieldContainer[RankRange]
    my_roles: _containers.RepeatedScalarFieldContainer[LolRole]
    looking_for_roles: _containers.RepeatedScalarFieldContainer[LolRole]
    description: str
    status: FormStatus
    updated_at: str
    history: _containers.RepeatedCompositeFieldContainer[ShortFormResponse]
    def __init__(self, id: _Optional[str] = ..., owner_id: _Optional[str] = ..., owner: _Optional[_Union[OwnerPreview, _Mapping]] = ..., liked_by: _Optional[_Iterable[str]] = ..., disliked_by: _Optional[_Iterable[str]] = ..., blocked_by: _Optional[_Iterable[str]] = ..., created_at: _Optional[str] = ..., rank_range: _Optional[_Iterable[_Union[RankRange, _Mapping]]] = ..., my_roles: _Optional[_Iterable[_Union[LolRole, str]]] = ..., looking_for_roles: _Optional[_Iterable[_Union[LolRole, str]]] = ..., description: _Optional[str] = ..., status: _Optional[_Union[FormStatus, str]] = ..., updated_at: _Optional[str] = ..., history: _Optional[_Iterable[_Union[ShortFormResponse, _Mapping]]] = ...) -> None: ...

class HotFormResponse(_message.Message):
    __slots__ = ("id", "owner_id", "owner", "liked_by", "disliked_by", "created_at", "rank_range", "my_roles", "looking_for_roles", "description", "expires_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    LIKED_BY_FIELD_NUMBER: _ClassVar[int]
    DISLIKED_BY_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    RANK_RANGE_FIELD_NUMBER: _ClassVar[int]
    MY_ROLES_FIELD_NUMBER: _ClassVar[int]
    LOOKING_FOR_ROLES_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    owner_id: str
    owner: OwnerPreview
    liked_by: _containers.RepeatedScalarFieldContainer[str]
    disliked_by: _containers.RepeatedScalarFieldContainer[str]
    created_at: str
    rank_range: _containers.RepeatedCompositeFieldContainer[RankRange]
    my_roles: _containers.RepeatedScalarFieldContainer[LolRole]
    looking_for_roles: _containers.RepeatedScalarFieldContainer[LolRole]
    description: str
    expires_at: str
    def __init__(self, id: _Optional[str] = ..., owner_id: _Optional[str] = ..., owner: _Optional[_Union[OwnerPreview, _Mapping]] = ..., liked_by: _Optional[_Iterable[str]] = ..., disliked_by: _Optional[_Iterable[str]] = ..., created_at: _Optional[str] = ..., rank_range: _Optional[_Iterable[_Union[RankRange, _Mapping]]] = ..., my_roles: _Optional[_Iterable[_Union[LolRole, str]]] = ..., looking_for_roles: _Optional[_Iterable[_Union[LolRole, str]]] = ..., description: _Optional[str] = ..., expires_at: _Optional[str] = ...) -> None: ...

class PaginationRequest(_message.Message):
    __slots__ = ("page", "page_size", "skip", "limit")
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    SKIP_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    page: int
    page_size: int
    skip: int
    limit: int
    def __init__(self, page: _Optional[int] = ..., page_size: _Optional[int] = ..., skip: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class SearchFormsFilter(_message.Message):
    __slots__ = ("rank_range", "my_roles", "looking_for_roles", "servers", "owner_id", "exclude_owner_id", "exclude_blocked_by", "status", "min_likes", "query")
    RANK_RANGE_FIELD_NUMBER: _ClassVar[int]
    MY_ROLES_FIELD_NUMBER: _ClassVar[int]
    LOOKING_FOR_ROLES_FIELD_NUMBER: _ClassVar[int]
    SERVERS_FIELD_NUMBER: _ClassVar[int]
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_BLOCKED_BY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MIN_LIKES_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    rank_range: _containers.RepeatedCompositeFieldContainer[RankRange]
    my_roles: _containers.RepeatedScalarFieldContainer[LolRole]
    looking_for_roles: _containers.RepeatedScalarFieldContainer[LolRole]
    servers: _containers.RepeatedScalarFieldContainer[Server]
    owner_id: str
    exclude_owner_id: str
    exclude_blocked_by: str
    status: FormStatus
    min_likes: int
    query: str
    def __init__(self, rank_range: _Optional[_Iterable[_Union[RankRange, _Mapping]]] = ..., my_roles: _Optional[_Iterable[_Union[LolRole, str]]] = ..., looking_for_roles: _Optional[_Iterable[_Union[LolRole, str]]] = ..., servers: _Optional[_Iterable[_Union[Server, str]]] = ..., owner_id: _Optional[str] = ..., exclude_owner_id: _Optional[str] = ..., exclude_blocked_by: _Optional[str] = ..., status: _Optional[_Union[FormStatus, str]] = ..., min_likes: _Optional[int] = ..., query: _Optional[str] = ...) -> None: ...

class CreateColdFormRequest(_message.Message):
    __slots__ = ("owner_id", "rank_range", "my_roles", "looking_for_roles", "description", "status")
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    RANK_RANGE_FIELD_NUMBER: _ClassVar[int]
    MY_ROLES_FIELD_NUMBER: _ClassVar[int]
    LOOKING_FOR_ROLES_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    owner_id: str
    rank_range: _containers.RepeatedCompositeFieldContainer[RankRange]
    my_roles: _containers.RepeatedScalarFieldContainer[LolRole]
    looking_for_roles: _containers.RepeatedScalarFieldContainer[LolRole]
    description: str
    status: FormStatus
    def __init__(self, owner_id: _Optional[str] = ..., rank_range: _Optional[_Iterable[_Union[RankRange, _Mapping]]] = ..., my_roles: _Optional[_Iterable[_Union[LolRole, str]]] = ..., looking_for_roles: _Optional[_Iterable[_Union[LolRole, str]]] = ..., description: _Optional[str] = ..., status: _Optional[_Union[FormStatus, str]] = ...) -> None: ...

class UpdateColdFormRequest(_message.Message):
    __slots__ = ("form_id", "actor_id", "rank_range", "my_roles", "looking_for_roles", "description", "status")
    FORM_ID_FIELD_NUMBER: _ClassVar[int]
    ACTOR_ID_FIELD_NUMBER: _ClassVar[int]
    RANK_RANGE_FIELD_NUMBER: _ClassVar[int]
    MY_ROLES_FIELD_NUMBER: _ClassVar[int]
    LOOKING_FOR_ROLES_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    form_id: str
    actor_id: str
    rank_range: _containers.RepeatedCompositeFieldContainer[RankRange]
    my_roles: _containers.RepeatedScalarFieldContainer[LolRole]
    looking_for_roles: _containers.RepeatedScalarFieldContainer[LolRole]
    description: str
    status: FormStatus
    def __init__(self, form_id: _Optional[str] = ..., actor_id: _Optional[str] = ..., rank_range: _Optional[_Iterable[_Union[RankRange, _Mapping]]] = ..., my_roles: _Optional[_Iterable[_Union[LolRole, str]]] = ..., looking_for_roles: _Optional[_Iterable[_Union[LolRole, str]]] = ..., description: _Optional[str] = ..., status: _Optional[_Union[FormStatus, str]] = ...) -> None: ...

class GetFormRequest(_message.Message):
    __slots__ = ("form_id",)
    FORM_ID_FIELD_NUMBER: _ClassVar[int]
    form_id: str
    def __init__(self, form_id: _Optional[str] = ...) -> None: ...

class DeleteFormRequest(_message.Message):
    __slots__ = ("form_id", "actor_id")
    FORM_ID_FIELD_NUMBER: _ClassVar[int]
    ACTOR_ID_FIELD_NUMBER: _ClassVar[int]
    form_id: str
    actor_id: str
    def __init__(self, form_id: _Optional[str] = ..., actor_id: _Optional[str] = ...) -> None: ...

class GetOwnerFormsRequest(_message.Message):
    __slots__ = ("owner_id", "pagination")
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    owner_id: str
    pagination: PaginationRequest
    def __init__(self, owner_id: _Optional[str] = ..., pagination: _Optional[_Union[PaginationRequest, _Mapping]] = ...) -> None: ...

class SetColdFormStatusRequest(_message.Message):
    __slots__ = ("form_id", "actor_id", "status")
    FORM_ID_FIELD_NUMBER: _ClassVar[int]
    ACTOR_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    form_id: str
    actor_id: str
    status: FormStatus
    def __init__(self, form_id: _Optional[str] = ..., actor_id: _Optional[str] = ..., status: _Optional[_Union[FormStatus, str]] = ...) -> None: ...

class SwipeFormRequest(_message.Message):
    __slots__ = ("form_id", "user_id", "action")
    FORM_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    form_id: str
    user_id: str
    action: SwipeAction
    def __init__(self, form_id: _Optional[str] = ..., user_id: _Optional[str] = ..., action: _Optional[_Union[SwipeAction, str]] = ...) -> None: ...

class SwipeFormResponse(_message.Message):
    __slots__ = ("matched", "form", "matched_user_id")
    MATCHED_FIELD_NUMBER: _ClassVar[int]
    FORM_FIELD_NUMBER: _ClassVar[int]
    MATCHED_USER_ID_FIELD_NUMBER: _ClassVar[int]
    matched: bool
    form: ColdFormResponse
    matched_user_id: str
    def __init__(self, matched: bool = ..., form: _Optional[_Union[ColdFormResponse, _Mapping]] = ..., matched_user_id: _Optional[str] = ...) -> None: ...

class ColdDeckRequest(_message.Message):
    __slots__ = ("actor_id", "filter", "limit")
    ACTOR_ID_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    actor_id: str
    filter: SearchFormsFilter
    limit: int
    def __init__(self, actor_id: _Optional[str] = ..., filter: _Optional[_Union[SearchFormsFilter, _Mapping]] = ..., limit: _Optional[int] = ...) -> None: ...

class ColdDeckResponse(_message.Message):
    __slots__ = ("forms",)
    FORMS_FIELD_NUMBER: _ClassVar[int]
    forms: _containers.RepeatedCompositeFieldContainer[ColdFormResponse]
    def __init__(self, forms: _Optional[_Iterable[_Union[ColdFormResponse, _Mapping]]] = ...) -> None: ...

class ListColdFormsRequest(_message.Message):
    __slots__ = ("filter", "pagination")
    FILTER_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    filter: SearchFormsFilter
    pagination: PaginationRequest
    def __init__(self, filter: _Optional[_Union[SearchFormsFilter, _Mapping]] = ..., pagination: _Optional[_Union[PaginationRequest, _Mapping]] = ...) -> None: ...

class ListColdFormsResponse(_message.Message):
    __slots__ = ("forms", "total_count", "page", "page_size", "has_next")
    FORMS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    HAS_NEXT_FIELD_NUMBER: _ClassVar[int]
    forms: _containers.RepeatedCompositeFieldContainer[ColdFormResponse]
    total_count: int
    page: int
    page_size: int
    has_next: bool
    def __init__(self, forms: _Optional[_Iterable[_Union[ColdFormResponse, _Mapping]]] = ..., total_count: _Optional[int] = ..., page: _Optional[int] = ..., page_size: _Optional[int] = ..., has_next: bool = ...) -> None: ...

class ColdFormHistoryResponse(_message.Message):
    __slots__ = ("history",)
    HISTORY_FIELD_NUMBER: _ClassVar[int]
    history: _containers.RepeatedCompositeFieldContainer[ShortFormResponse]
    def __init__(self, history: _Optional[_Iterable[_Union[ShortFormResponse, _Mapping]]] = ...) -> None: ...

class CreateHotFormRequest(_message.Message):
    __slots__ = ("owner_id", "rank_range", "my_roles", "looking_for_roles", "description")
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    RANK_RANGE_FIELD_NUMBER: _ClassVar[int]
    MY_ROLES_FIELD_NUMBER: _ClassVar[int]
    LOOKING_FOR_ROLES_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    owner_id: str
    rank_range: _containers.RepeatedCompositeFieldContainer[RankRange]
    my_roles: _containers.RepeatedScalarFieldContainer[LolRole]
    looking_for_roles: _containers.RepeatedScalarFieldContainer[LolRole]
    description: str
    def __init__(self, owner_id: _Optional[str] = ..., rank_range: _Optional[_Iterable[_Union[RankRange, _Mapping]]] = ..., my_roles: _Optional[_Iterable[_Union[LolRole, str]]] = ..., looking_for_roles: _Optional[_Iterable[_Union[LolRole, str]]] = ..., description: _Optional[str] = ...) -> None: ...

class ListHotFormsRequest(_message.Message):
    __slots__ = ("filter", "pagination")
    FILTER_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    filter: SearchFormsFilter
    pagination: PaginationRequest
    def __init__(self, filter: _Optional[_Union[SearchFormsFilter, _Mapping]] = ..., pagination: _Optional[_Union[PaginationRequest, _Mapping]] = ...) -> None: ...

class ListHotFormsResponse(_message.Message):
    __slots__ = ("forms", "total_count", "page", "page_size", "has_next")
    FORMS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    HAS_NEXT_FIELD_NUMBER: _ClassVar[int]
    forms: _containers.RepeatedCompositeFieldContainer[HotFormResponse]
    total_count: int
    page: int
    page_size: int
    has_next: bool
    def __init__(self, forms: _Optional[_Iterable[_Union[HotFormResponse, _Mapping]]] = ..., total_count: _Optional[int] = ..., page: _Optional[int] = ..., page_size: _Optional[int] = ..., has_next: bool = ...) -> None: ...

class HotFormSwipeRequest(_message.Message):
    __slots__ = ("form_id", "user_id", "action")
    FORM_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    form_id: str
    user_id: str
    action: SwipeAction
    def __init__(self, form_id: _Optional[str] = ..., user_id: _Optional[str] = ..., action: _Optional[_Union[SwipeAction, str]] = ...) -> None: ...

class HotFormSwipeResponse(_message.Message):
    __slots__ = ("matched", "form", "matched_user_id")
    MATCHED_FIELD_NUMBER: _ClassVar[int]
    FORM_FIELD_NUMBER: _ClassVar[int]
    MATCHED_USER_ID_FIELD_NUMBER: _ClassVar[int]
    matched: bool
    form: HotFormResponse
    matched_user_id: str
    def __init__(self, matched: bool = ..., form: _Optional[_Union[HotFormResponse, _Mapping]] = ..., matched_user_id: _Optional[str] = ...) -> None: ...

class PopularColdFormsRequest(_message.Message):
    __slots__ = ("limit",)
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    limit: int
    def __init__(self, limit: _Optional[int] = ...) -> None: ...
