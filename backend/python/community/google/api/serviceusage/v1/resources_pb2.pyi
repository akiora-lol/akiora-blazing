from google.api import auth_pb2 as _auth_pb2
from google.api import documentation_pb2 as _documentation_pb2
from google.api import endpoint_pb2 as _endpoint_pb2
from google.api import monitored_resource_pb2 as _monitored_resource_pb2
from google.api import monitoring_pb2 as _monitoring_pb2
from google.api import quota_pb2 as _quota_pb2
from google.api import resource_pb2 as _resource_pb2
from google.api import usage_pb2 as _usage_pb2
from google.protobuf import api_pb2 as _api_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STATE_UNSPECIFIED: _ClassVar[State]
    DISABLED: _ClassVar[State]
    ENABLED: _ClassVar[State]
STATE_UNSPECIFIED: State
DISABLED: State
ENABLED: State

class Service(_message.Message):
    __slots__ = ("name", "parent", "config", "state")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PARENT_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    name: str
    parent: str
    config: ServiceConfig
    state: State
    def __init__(self, name: _Optional[str] = ..., parent: _Optional[str] = ..., config: _Optional[_Union[ServiceConfig, _Mapping]] = ..., state: _Optional[_Union[State, str]] = ...) -> None: ...

class ServiceConfig(_message.Message):
    __slots__ = ("name", "title", "apis", "documentation", "quota", "authentication", "usage", "endpoints", "monitored_resources", "monitoring")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    APIS_FIELD_NUMBER: _ClassVar[int]
    DOCUMENTATION_FIELD_NUMBER: _ClassVar[int]
    QUOTA_FIELD_NUMBER: _ClassVar[int]
    AUTHENTICATION_FIELD_NUMBER: _ClassVar[int]
    USAGE_FIELD_NUMBER: _ClassVar[int]
    ENDPOINTS_FIELD_NUMBER: _ClassVar[int]
    MONITORED_RESOURCES_FIELD_NUMBER: _ClassVar[int]
    MONITORING_FIELD_NUMBER: _ClassVar[int]
    name: str
    title: str
    apis: _containers.RepeatedCompositeFieldContainer[_api_pb2.Api]
    documentation: _documentation_pb2.Documentation
    quota: _quota_pb2.Quota
    authentication: _auth_pb2.Authentication
    usage: _usage_pb2.Usage
    endpoints: _containers.RepeatedCompositeFieldContainer[_endpoint_pb2.Endpoint]
    monitored_resources: _containers.RepeatedCompositeFieldContainer[_monitored_resource_pb2.MonitoredResourceDescriptor]
    monitoring: _monitoring_pb2.Monitoring
    def __init__(self, name: _Optional[str] = ..., title: _Optional[str] = ..., apis: _Optional[_Iterable[_Union[_api_pb2.Api, _Mapping]]] = ..., documentation: _Optional[_Union[_documentation_pb2.Documentation, _Mapping]] = ..., quota: _Optional[_Union[_quota_pb2.Quota, _Mapping]] = ..., authentication: _Optional[_Union[_auth_pb2.Authentication, _Mapping]] = ..., usage: _Optional[_Union[_usage_pb2.Usage, _Mapping]] = ..., endpoints: _Optional[_Iterable[_Union[_endpoint_pb2.Endpoint, _Mapping]]] = ..., monitored_resources: _Optional[_Iterable[_Union[_monitored_resource_pb2.MonitoredResourceDescriptor, _Mapping]]] = ..., monitoring: _Optional[_Union[_monitoring_pb2.Monitoring, _Mapping]] = ...) -> None: ...

class OperationMetadata(_message.Message):
    __slots__ = ("resource_names",)
    RESOURCE_NAMES_FIELD_NUMBER: _ClassVar[int]
    resource_names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, resource_names: _Optional[_Iterable[str]] = ...) -> None: ...
