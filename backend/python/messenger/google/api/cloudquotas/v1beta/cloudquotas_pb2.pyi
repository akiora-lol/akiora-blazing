from google.api import annotations_pb2 as _annotations_pb2
from google.api import client_pb2 as _client_pb2
from google.api.cloudquotas.v1beta import resources_pb2 as _resources_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.api import resource_pb2 as _resource_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ListQuotaInfosRequest(_message.Message):
    __slots__ = ("parent", "page_size", "page_token")
    PARENT_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    parent: str
    page_size: int
    page_token: str
    def __init__(self, parent: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListQuotaInfosResponse(_message.Message):
    __slots__ = ("quota_infos", "next_page_token")
    QUOTA_INFOS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    quota_infos: _containers.RepeatedCompositeFieldContainer[_resources_pb2.QuotaInfo]
    next_page_token: str
    def __init__(self, quota_infos: _Optional[_Iterable[_Union[_resources_pb2.QuotaInfo, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class GetQuotaInfoRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class ListQuotaPreferencesRequest(_message.Message):
    __slots__ = ("parent", "page_size", "page_token", "filter", "order_by")
    PARENT_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    ORDER_BY_FIELD_NUMBER: _ClassVar[int]
    parent: str
    page_size: int
    page_token: str
    filter: str
    order_by: str
    def __init__(self, parent: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ..., filter: _Optional[str] = ..., order_by: _Optional[str] = ...) -> None: ...

class ListQuotaPreferencesResponse(_message.Message):
    __slots__ = ("quota_preferences", "next_page_token", "unreachable")
    QUOTA_PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    UNREACHABLE_FIELD_NUMBER: _ClassVar[int]
    quota_preferences: _containers.RepeatedCompositeFieldContainer[_resources_pb2.QuotaPreference]
    next_page_token: str
    unreachable: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, quota_preferences: _Optional[_Iterable[_Union[_resources_pb2.QuotaPreference, _Mapping]]] = ..., next_page_token: _Optional[str] = ..., unreachable: _Optional[_Iterable[str]] = ...) -> None: ...

class GetQuotaPreferenceRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class CreateQuotaPreferenceRequest(_message.Message):
    __slots__ = ("parent", "quota_preference_id", "quota_preference", "ignore_safety_checks")
    PARENT_FIELD_NUMBER: _ClassVar[int]
    QUOTA_PREFERENCE_ID_FIELD_NUMBER: _ClassVar[int]
    QUOTA_PREFERENCE_FIELD_NUMBER: _ClassVar[int]
    IGNORE_SAFETY_CHECKS_FIELD_NUMBER: _ClassVar[int]
    parent: str
    quota_preference_id: str
    quota_preference: _resources_pb2.QuotaPreference
    ignore_safety_checks: _containers.RepeatedScalarFieldContainer[_resources_pb2.QuotaSafetyCheck]
    def __init__(self, parent: _Optional[str] = ..., quota_preference_id: _Optional[str] = ..., quota_preference: _Optional[_Union[_resources_pb2.QuotaPreference, _Mapping]] = ..., ignore_safety_checks: _Optional[_Iterable[_Union[_resources_pb2.QuotaSafetyCheck, str]]] = ...) -> None: ...

class UpdateQuotaPreferenceRequest(_message.Message):
    __slots__ = ("update_mask", "quota_preference", "allow_missing", "validate_only", "ignore_safety_checks")
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    QUOTA_PREFERENCE_FIELD_NUMBER: _ClassVar[int]
    ALLOW_MISSING_FIELD_NUMBER: _ClassVar[int]
    VALIDATE_ONLY_FIELD_NUMBER: _ClassVar[int]
    IGNORE_SAFETY_CHECKS_FIELD_NUMBER: _ClassVar[int]
    update_mask: _field_mask_pb2.FieldMask
    quota_preference: _resources_pb2.QuotaPreference
    allow_missing: bool
    validate_only: bool
    ignore_safety_checks: _containers.RepeatedScalarFieldContainer[_resources_pb2.QuotaSafetyCheck]
    def __init__(self, update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ..., quota_preference: _Optional[_Union[_resources_pb2.QuotaPreference, _Mapping]] = ..., allow_missing: bool = ..., validate_only: bool = ..., ignore_safety_checks: _Optional[_Iterable[_Union[_resources_pb2.QuotaSafetyCheck, str]]] = ...) -> None: ...
