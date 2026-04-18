from google.api import annotations_pb2 as _annotations_pb2
from google.api import client_pb2 as _client_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.api import service_pb2 as _service_pb2
from google.api.servicemanagement.v1 import resources_pb2 as _resources_pb2
from google.longrunning import operations_pb2 as _operations_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ListServicesRequest(_message.Message):
    __slots__ = ("producer_project_id", "page_size", "page_token", "consumer_id")
    PRODUCER_PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CONSUMER_ID_FIELD_NUMBER: _ClassVar[int]
    producer_project_id: str
    page_size: int
    page_token: str
    consumer_id: str
    def __init__(self, producer_project_id: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ..., consumer_id: _Optional[str] = ...) -> None: ...

class ListServicesResponse(_message.Message):
    __slots__ = ("services", "next_page_token")
    SERVICES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    services: _containers.RepeatedCompositeFieldContainer[_resources_pb2.ManagedService]
    next_page_token: str
    def __init__(self, services: _Optional[_Iterable[_Union[_resources_pb2.ManagedService, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class GetServiceRequest(_message.Message):
    __slots__ = ("service_name",)
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    def __init__(self, service_name: _Optional[str] = ...) -> None: ...

class CreateServiceRequest(_message.Message):
    __slots__ = ("service",)
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    service: _resources_pb2.ManagedService
    def __init__(self, service: _Optional[_Union[_resources_pb2.ManagedService, _Mapping]] = ...) -> None: ...

class DeleteServiceRequest(_message.Message):
    __slots__ = ("service_name",)
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    def __init__(self, service_name: _Optional[str] = ...) -> None: ...

class UndeleteServiceRequest(_message.Message):
    __slots__ = ("service_name",)
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    def __init__(self, service_name: _Optional[str] = ...) -> None: ...

class UndeleteServiceResponse(_message.Message):
    __slots__ = ("service",)
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    service: _resources_pb2.ManagedService
    def __init__(self, service: _Optional[_Union[_resources_pb2.ManagedService, _Mapping]] = ...) -> None: ...

class GetServiceConfigRequest(_message.Message):
    __slots__ = ("service_name", "config_id", "view")
    class ConfigView(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        BASIC: _ClassVar[GetServiceConfigRequest.ConfigView]
        FULL: _ClassVar[GetServiceConfigRequest.ConfigView]
    BASIC: GetServiceConfigRequest.ConfigView
    FULL: GetServiceConfigRequest.ConfigView
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    VIEW_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    config_id: str
    view: GetServiceConfigRequest.ConfigView
    def __init__(self, service_name: _Optional[str] = ..., config_id: _Optional[str] = ..., view: _Optional[_Union[GetServiceConfigRequest.ConfigView, str]] = ...) -> None: ...

class ListServiceConfigsRequest(_message.Message):
    __slots__ = ("service_name", "page_token", "page_size")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    page_token: str
    page_size: int
    def __init__(self, service_name: _Optional[str] = ..., page_token: _Optional[str] = ..., page_size: _Optional[int] = ...) -> None: ...

class ListServiceConfigsResponse(_message.Message):
    __slots__ = ("service_configs", "next_page_token")
    SERVICE_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    service_configs: _containers.RepeatedCompositeFieldContainer[_service_pb2.Service]
    next_page_token: str
    def __init__(self, service_configs: _Optional[_Iterable[_Union[_service_pb2.Service, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class CreateServiceConfigRequest(_message.Message):
    __slots__ = ("service_name", "service_config")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    SERVICE_CONFIG_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    service_config: _service_pb2.Service
    def __init__(self, service_name: _Optional[str] = ..., service_config: _Optional[_Union[_service_pb2.Service, _Mapping]] = ...) -> None: ...

class SubmitConfigSourceRequest(_message.Message):
    __slots__ = ("service_name", "config_source", "validate_only")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    CONFIG_SOURCE_FIELD_NUMBER: _ClassVar[int]
    VALIDATE_ONLY_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    config_source: _resources_pb2.ConfigSource
    validate_only: bool
    def __init__(self, service_name: _Optional[str] = ..., config_source: _Optional[_Union[_resources_pb2.ConfigSource, _Mapping]] = ..., validate_only: bool = ...) -> None: ...

class SubmitConfigSourceResponse(_message.Message):
    __slots__ = ("service_config",)
    SERVICE_CONFIG_FIELD_NUMBER: _ClassVar[int]
    service_config: _service_pb2.Service
    def __init__(self, service_config: _Optional[_Union[_service_pb2.Service, _Mapping]] = ...) -> None: ...

class CreateServiceRolloutRequest(_message.Message):
    __slots__ = ("service_name", "rollout")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    ROLLOUT_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    rollout: _resources_pb2.Rollout
    def __init__(self, service_name: _Optional[str] = ..., rollout: _Optional[_Union[_resources_pb2.Rollout, _Mapping]] = ...) -> None: ...

class ListServiceRolloutsRequest(_message.Message):
    __slots__ = ("service_name", "page_token", "page_size", "filter")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    page_token: str
    page_size: int
    filter: str
    def __init__(self, service_name: _Optional[str] = ..., page_token: _Optional[str] = ..., page_size: _Optional[int] = ..., filter: _Optional[str] = ...) -> None: ...

class ListServiceRolloutsResponse(_message.Message):
    __slots__ = ("rollouts", "next_page_token")
    ROLLOUTS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    rollouts: _containers.RepeatedCompositeFieldContainer[_resources_pb2.Rollout]
    next_page_token: str
    def __init__(self, rollouts: _Optional[_Iterable[_Union[_resources_pb2.Rollout, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class GetServiceRolloutRequest(_message.Message):
    __slots__ = ("service_name", "rollout_id")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    ROLLOUT_ID_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    rollout_id: str
    def __init__(self, service_name: _Optional[str] = ..., rollout_id: _Optional[str] = ...) -> None: ...

class EnableServiceResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GenerateConfigReportRequest(_message.Message):
    __slots__ = ("new_config", "old_config")
    NEW_CONFIG_FIELD_NUMBER: _ClassVar[int]
    OLD_CONFIG_FIELD_NUMBER: _ClassVar[int]
    new_config: _any_pb2.Any
    old_config: _any_pb2.Any
    def __init__(self, new_config: _Optional[_Union[_any_pb2.Any, _Mapping]] = ..., old_config: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...

class GenerateConfigReportResponse(_message.Message):
    __slots__ = ("service_name", "id", "change_reports", "diagnostics")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    CHANGE_REPORTS_FIELD_NUMBER: _ClassVar[int]
    DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    id: str
    change_reports: _containers.RepeatedCompositeFieldContainer[_resources_pb2.ChangeReport]
    diagnostics: _containers.RepeatedCompositeFieldContainer[_resources_pb2.Diagnostic]
    def __init__(self, service_name: _Optional[str] = ..., id: _Optional[str] = ..., change_reports: _Optional[_Iterable[_Union[_resources_pb2.ChangeReport, _Mapping]]] = ..., diagnostics: _Optional[_Iterable[_Union[_resources_pb2.Diagnostic, _Mapping]]] = ...) -> None: ...
