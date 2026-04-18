from google.api import annotations_pb2 as _annotations_pb2
from google.api import client_pb2 as _client_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.api.serviceusage.v1beta1 import resources_pb2 as _resources_pb2
from google.longrunning import operations_pb2 as _operations_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EnableServiceRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class DisableServiceRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class GetServiceRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class ListServicesRequest(_message.Message):
    __slots__ = ("parent", "page_size", "page_token", "filter")
    PARENT_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    parent: str
    page_size: int
    page_token: str
    filter: str
    def __init__(self, parent: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ..., filter: _Optional[str] = ...) -> None: ...

class ListServicesResponse(_message.Message):
    __slots__ = ("services", "next_page_token")
    SERVICES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    services: _containers.RepeatedCompositeFieldContainer[_resources_pb2.Service]
    next_page_token: str
    def __init__(self, services: _Optional[_Iterable[_Union[_resources_pb2.Service, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class BatchEnableServicesRequest(_message.Message):
    __slots__ = ("parent", "service_ids")
    PARENT_FIELD_NUMBER: _ClassVar[int]
    SERVICE_IDS_FIELD_NUMBER: _ClassVar[int]
    parent: str
    service_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, parent: _Optional[str] = ..., service_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class ListConsumerQuotaMetricsRequest(_message.Message):
    __slots__ = ("parent", "page_size", "page_token", "view")
    PARENT_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    VIEW_FIELD_NUMBER: _ClassVar[int]
    parent: str
    page_size: int
    page_token: str
    view: _resources_pb2.QuotaView
    def __init__(self, parent: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ..., view: _Optional[_Union[_resources_pb2.QuotaView, str]] = ...) -> None: ...

class ListConsumerQuotaMetricsResponse(_message.Message):
    __slots__ = ("metrics", "next_page_token")
    METRICS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    metrics: _containers.RepeatedCompositeFieldContainer[_resources_pb2.ConsumerQuotaMetric]
    next_page_token: str
    def __init__(self, metrics: _Optional[_Iterable[_Union[_resources_pb2.ConsumerQuotaMetric, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class GetConsumerQuotaMetricRequest(_message.Message):
    __slots__ = ("name", "view")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VIEW_FIELD_NUMBER: _ClassVar[int]
    name: str
    view: _resources_pb2.QuotaView
    def __init__(self, name: _Optional[str] = ..., view: _Optional[_Union[_resources_pb2.QuotaView, str]] = ...) -> None: ...

class GetConsumerQuotaLimitRequest(_message.Message):
    __slots__ = ("name", "view")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VIEW_FIELD_NUMBER: _ClassVar[int]
    name: str
    view: _resources_pb2.QuotaView
    def __init__(self, name: _Optional[str] = ..., view: _Optional[_Union[_resources_pb2.QuotaView, str]] = ...) -> None: ...

class CreateAdminOverrideRequest(_message.Message):
    __slots__ = ("parent", "override", "force", "force_only")
    PARENT_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    FORCE_FIELD_NUMBER: _ClassVar[int]
    FORCE_ONLY_FIELD_NUMBER: _ClassVar[int]
    parent: str
    override: _resources_pb2.QuotaOverride
    force: bool
    force_only: _containers.RepeatedScalarFieldContainer[_resources_pb2.QuotaSafetyCheck]
    def __init__(self, parent: _Optional[str] = ..., override: _Optional[_Union[_resources_pb2.QuotaOverride, _Mapping]] = ..., force: bool = ..., force_only: _Optional[_Iterable[_Union[_resources_pb2.QuotaSafetyCheck, str]]] = ...) -> None: ...

class UpdateAdminOverrideRequest(_message.Message):
    __slots__ = ("name", "override", "force", "update_mask", "force_only")
    NAME_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    FORCE_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    FORCE_ONLY_FIELD_NUMBER: _ClassVar[int]
    name: str
    override: _resources_pb2.QuotaOverride
    force: bool
    update_mask: _field_mask_pb2.FieldMask
    force_only: _containers.RepeatedScalarFieldContainer[_resources_pb2.QuotaSafetyCheck]
    def __init__(self, name: _Optional[str] = ..., override: _Optional[_Union[_resources_pb2.QuotaOverride, _Mapping]] = ..., force: bool = ..., update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ..., force_only: _Optional[_Iterable[_Union[_resources_pb2.QuotaSafetyCheck, str]]] = ...) -> None: ...

class DeleteAdminOverrideRequest(_message.Message):
    __slots__ = ("name", "force", "force_only")
    NAME_FIELD_NUMBER: _ClassVar[int]
    FORCE_FIELD_NUMBER: _ClassVar[int]
    FORCE_ONLY_FIELD_NUMBER: _ClassVar[int]
    name: str
    force: bool
    force_only: _containers.RepeatedScalarFieldContainer[_resources_pb2.QuotaSafetyCheck]
    def __init__(self, name: _Optional[str] = ..., force: bool = ..., force_only: _Optional[_Iterable[_Union[_resources_pb2.QuotaSafetyCheck, str]]] = ...) -> None: ...

class ListAdminOverridesRequest(_message.Message):
    __slots__ = ("parent", "page_size", "page_token")
    PARENT_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    parent: str
    page_size: int
    page_token: str
    def __init__(self, parent: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListAdminOverridesResponse(_message.Message):
    __slots__ = ("overrides", "next_page_token")
    OVERRIDES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    overrides: _containers.RepeatedCompositeFieldContainer[_resources_pb2.QuotaOverride]
    next_page_token: str
    def __init__(self, overrides: _Optional[_Iterable[_Union[_resources_pb2.QuotaOverride, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class BatchCreateAdminOverridesResponse(_message.Message):
    __slots__ = ("overrides",)
    OVERRIDES_FIELD_NUMBER: _ClassVar[int]
    overrides: _containers.RepeatedCompositeFieldContainer[_resources_pb2.QuotaOverride]
    def __init__(self, overrides: _Optional[_Iterable[_Union[_resources_pb2.QuotaOverride, _Mapping]]] = ...) -> None: ...

class ImportAdminOverridesRequest(_message.Message):
    __slots__ = ("parent", "inline_source", "force", "force_only")
    PARENT_FIELD_NUMBER: _ClassVar[int]
    INLINE_SOURCE_FIELD_NUMBER: _ClassVar[int]
    FORCE_FIELD_NUMBER: _ClassVar[int]
    FORCE_ONLY_FIELD_NUMBER: _ClassVar[int]
    parent: str
    inline_source: _resources_pb2.OverrideInlineSource
    force: bool
    force_only: _containers.RepeatedScalarFieldContainer[_resources_pb2.QuotaSafetyCheck]
    def __init__(self, parent: _Optional[str] = ..., inline_source: _Optional[_Union[_resources_pb2.OverrideInlineSource, _Mapping]] = ..., force: bool = ..., force_only: _Optional[_Iterable[_Union[_resources_pb2.QuotaSafetyCheck, str]]] = ...) -> None: ...

class ImportAdminOverridesResponse(_message.Message):
    __slots__ = ("overrides",)
    OVERRIDES_FIELD_NUMBER: _ClassVar[int]
    overrides: _containers.RepeatedCompositeFieldContainer[_resources_pb2.QuotaOverride]
    def __init__(self, overrides: _Optional[_Iterable[_Union[_resources_pb2.QuotaOverride, _Mapping]]] = ...) -> None: ...

class ImportAdminOverridesMetadata(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CreateConsumerOverrideRequest(_message.Message):
    __slots__ = ("parent", "override", "force", "force_only")
    PARENT_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    FORCE_FIELD_NUMBER: _ClassVar[int]
    FORCE_ONLY_FIELD_NUMBER: _ClassVar[int]
    parent: str
    override: _resources_pb2.QuotaOverride
    force: bool
    force_only: _containers.RepeatedScalarFieldContainer[_resources_pb2.QuotaSafetyCheck]
    def __init__(self, parent: _Optional[str] = ..., override: _Optional[_Union[_resources_pb2.QuotaOverride, _Mapping]] = ..., force: bool = ..., force_only: _Optional[_Iterable[_Union[_resources_pb2.QuotaSafetyCheck, str]]] = ...) -> None: ...

class UpdateConsumerOverrideRequest(_message.Message):
    __slots__ = ("name", "override", "force", "update_mask", "force_only")
    NAME_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    FORCE_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    FORCE_ONLY_FIELD_NUMBER: _ClassVar[int]
    name: str
    override: _resources_pb2.QuotaOverride
    force: bool
    update_mask: _field_mask_pb2.FieldMask
    force_only: _containers.RepeatedScalarFieldContainer[_resources_pb2.QuotaSafetyCheck]
    def __init__(self, name: _Optional[str] = ..., override: _Optional[_Union[_resources_pb2.QuotaOverride, _Mapping]] = ..., force: bool = ..., update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ..., force_only: _Optional[_Iterable[_Union[_resources_pb2.QuotaSafetyCheck, str]]] = ...) -> None: ...

class DeleteConsumerOverrideRequest(_message.Message):
    __slots__ = ("name", "force", "force_only")
    NAME_FIELD_NUMBER: _ClassVar[int]
    FORCE_FIELD_NUMBER: _ClassVar[int]
    FORCE_ONLY_FIELD_NUMBER: _ClassVar[int]
    name: str
    force: bool
    force_only: _containers.RepeatedScalarFieldContainer[_resources_pb2.QuotaSafetyCheck]
    def __init__(self, name: _Optional[str] = ..., force: bool = ..., force_only: _Optional[_Iterable[_Union[_resources_pb2.QuotaSafetyCheck, str]]] = ...) -> None: ...

class ListConsumerOverridesRequest(_message.Message):
    __slots__ = ("parent", "page_size", "page_token")
    PARENT_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    parent: str
    page_size: int
    page_token: str
    def __init__(self, parent: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListConsumerOverridesResponse(_message.Message):
    __slots__ = ("overrides", "next_page_token")
    OVERRIDES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    overrides: _containers.RepeatedCompositeFieldContainer[_resources_pb2.QuotaOverride]
    next_page_token: str
    def __init__(self, overrides: _Optional[_Iterable[_Union[_resources_pb2.QuotaOverride, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class BatchCreateConsumerOverridesResponse(_message.Message):
    __slots__ = ("overrides",)
    OVERRIDES_FIELD_NUMBER: _ClassVar[int]
    overrides: _containers.RepeatedCompositeFieldContainer[_resources_pb2.QuotaOverride]
    def __init__(self, overrides: _Optional[_Iterable[_Union[_resources_pb2.QuotaOverride, _Mapping]]] = ...) -> None: ...

class ImportConsumerOverridesRequest(_message.Message):
    __slots__ = ("parent", "inline_source", "force", "force_only")
    PARENT_FIELD_NUMBER: _ClassVar[int]
    INLINE_SOURCE_FIELD_NUMBER: _ClassVar[int]
    FORCE_FIELD_NUMBER: _ClassVar[int]
    FORCE_ONLY_FIELD_NUMBER: _ClassVar[int]
    parent: str
    inline_source: _resources_pb2.OverrideInlineSource
    force: bool
    force_only: _containers.RepeatedScalarFieldContainer[_resources_pb2.QuotaSafetyCheck]
    def __init__(self, parent: _Optional[str] = ..., inline_source: _Optional[_Union[_resources_pb2.OverrideInlineSource, _Mapping]] = ..., force: bool = ..., force_only: _Optional[_Iterable[_Union[_resources_pb2.QuotaSafetyCheck, str]]] = ...) -> None: ...

class ImportConsumerOverridesResponse(_message.Message):
    __slots__ = ("overrides",)
    OVERRIDES_FIELD_NUMBER: _ClassVar[int]
    overrides: _containers.RepeatedCompositeFieldContainer[_resources_pb2.QuotaOverride]
    def __init__(self, overrides: _Optional[_Iterable[_Union[_resources_pb2.QuotaOverride, _Mapping]]] = ...) -> None: ...

class ImportConsumerOverridesMetadata(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ImportAdminQuotaPoliciesResponse(_message.Message):
    __slots__ = ("policies",)
    POLICIES_FIELD_NUMBER: _ClassVar[int]
    policies: _containers.RepeatedCompositeFieldContainer[_resources_pb2.AdminQuotaPolicy]
    def __init__(self, policies: _Optional[_Iterable[_Union[_resources_pb2.AdminQuotaPolicy, _Mapping]]] = ...) -> None: ...

class ImportAdminQuotaPoliciesMetadata(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CreateAdminQuotaPolicyMetadata(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UpdateAdminQuotaPolicyMetadata(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DeleteAdminQuotaPolicyMetadata(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GenerateServiceIdentityRequest(_message.Message):
    __slots__ = ("parent",)
    PARENT_FIELD_NUMBER: _ClassVar[int]
    parent: str
    def __init__(self, parent: _Optional[str] = ...) -> None: ...

class GetServiceIdentityResponse(_message.Message):
    __slots__ = ("identity", "state")
    class IdentityState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        IDENTITY_STATE_UNSPECIFIED: _ClassVar[GetServiceIdentityResponse.IdentityState]
        ACTIVE: _ClassVar[GetServiceIdentityResponse.IdentityState]
    IDENTITY_STATE_UNSPECIFIED: GetServiceIdentityResponse.IdentityState
    ACTIVE: GetServiceIdentityResponse.IdentityState
    IDENTITY_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    identity: _resources_pb2.ServiceIdentity
    state: GetServiceIdentityResponse.IdentityState
    def __init__(self, identity: _Optional[_Union[_resources_pb2.ServiceIdentity, _Mapping]] = ..., state: _Optional[_Union[GetServiceIdentityResponse.IdentityState, str]] = ...) -> None: ...

class GetServiceIdentityMetadata(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
