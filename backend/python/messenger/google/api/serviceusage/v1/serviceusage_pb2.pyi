from google.api import annotations_pb2 as _annotations_pb2
from google.api import client_pb2 as _client_pb2
from google.api.serviceusage.v1 import resources_pb2 as _resources_pb2
from google.longrunning import operations_pb2 as _operations_pb2
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

class EnableServiceResponse(_message.Message):
    __slots__ = ("service",)
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    service: _resources_pb2.Service
    def __init__(self, service: _Optional[_Union[_resources_pb2.Service, _Mapping]] = ...) -> None: ...

class DisableServiceRequest(_message.Message):
    __slots__ = ("name", "disable_dependent_services", "check_if_service_has_usage")
    class CheckIfServiceHasUsage(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CHECK_IF_SERVICE_HAS_USAGE_UNSPECIFIED: _ClassVar[DisableServiceRequest.CheckIfServiceHasUsage]
        SKIP: _ClassVar[DisableServiceRequest.CheckIfServiceHasUsage]
        CHECK: _ClassVar[DisableServiceRequest.CheckIfServiceHasUsage]
    CHECK_IF_SERVICE_HAS_USAGE_UNSPECIFIED: DisableServiceRequest.CheckIfServiceHasUsage
    SKIP: DisableServiceRequest.CheckIfServiceHasUsage
    CHECK: DisableServiceRequest.CheckIfServiceHasUsage
    NAME_FIELD_NUMBER: _ClassVar[int]
    DISABLE_DEPENDENT_SERVICES_FIELD_NUMBER: _ClassVar[int]
    CHECK_IF_SERVICE_HAS_USAGE_FIELD_NUMBER: _ClassVar[int]
    name: str
    disable_dependent_services: bool
    check_if_service_has_usage: DisableServiceRequest.CheckIfServiceHasUsage
    def __init__(self, name: _Optional[str] = ..., disable_dependent_services: bool = ..., check_if_service_has_usage: _Optional[_Union[DisableServiceRequest.CheckIfServiceHasUsage, str]] = ...) -> None: ...

class DisableServiceResponse(_message.Message):
    __slots__ = ("service",)
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    service: _resources_pb2.Service
    def __init__(self, service: _Optional[_Union[_resources_pb2.Service, _Mapping]] = ...) -> None: ...

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

class BatchEnableServicesResponse(_message.Message):
    __slots__ = ("services", "failures")
    class EnableFailure(_message.Message):
        __slots__ = ("service_id", "error_message")
        SERVICE_ID_FIELD_NUMBER: _ClassVar[int]
        ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
        service_id: str
        error_message: str
        def __init__(self, service_id: _Optional[str] = ..., error_message: _Optional[str] = ...) -> None: ...
    SERVICES_FIELD_NUMBER: _ClassVar[int]
    FAILURES_FIELD_NUMBER: _ClassVar[int]
    services: _containers.RepeatedCompositeFieldContainer[_resources_pb2.Service]
    failures: _containers.RepeatedCompositeFieldContainer[BatchEnableServicesResponse.EnableFailure]
    def __init__(self, services: _Optional[_Iterable[_Union[_resources_pb2.Service, _Mapping]]] = ..., failures: _Optional[_Iterable[_Union[BatchEnableServicesResponse.EnableFailure, _Mapping]]] = ...) -> None: ...

class BatchGetServicesRequest(_message.Message):
    __slots__ = ("parent", "names")
    PARENT_FIELD_NUMBER: _ClassVar[int]
    NAMES_FIELD_NUMBER: _ClassVar[int]
    parent: str
    names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, parent: _Optional[str] = ..., names: _Optional[_Iterable[str]] = ...) -> None: ...

class BatchGetServicesResponse(_message.Message):
    __slots__ = ("services",)
    SERVICES_FIELD_NUMBER: _ClassVar[int]
    services: _containers.RepeatedCompositeFieldContainer[_resources_pb2.Service]
    def __init__(self, services: _Optional[_Iterable[_Union[_resources_pb2.Service, _Mapping]]] = ...) -> None: ...
