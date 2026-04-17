from google.api import annotations_pb2 as _annotations_pb2
from google.api import client_pb2 as _client_pb2
from google.rpc.context import attribute_context_pb2 as _attribute_context_pb2
from google.rpc import status_pb2 as _status_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CheckRequest(_message.Message):
    __slots__ = ("service_name", "service_config_id", "attributes", "resources", "flags")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    SERVICE_CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    service_config_id: str
    attributes: _attribute_context_pb2.AttributeContext
    resources: _containers.RepeatedCompositeFieldContainer[ResourceInfo]
    flags: str
    def __init__(self, service_name: _Optional[str] = ..., service_config_id: _Optional[str] = ..., attributes: _Optional[_Union[_attribute_context_pb2.AttributeContext, _Mapping]] = ..., resources: _Optional[_Iterable[_Union[ResourceInfo, _Mapping]]] = ..., flags: _Optional[str] = ...) -> None: ...

class ResourceInfo(_message.Message):
    __slots__ = ("name", "type", "permission", "container", "location")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    PERMISSION_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: str
    permission: str
    container: str
    location: str
    def __init__(self, name: _Optional[str] = ..., type: _Optional[str] = ..., permission: _Optional[str] = ..., container: _Optional[str] = ..., location: _Optional[str] = ...) -> None: ...

class CheckResponse(_message.Message):
    __slots__ = ("status", "headers")
    class HeadersEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    STATUS_FIELD_NUMBER: _ClassVar[int]
    HEADERS_FIELD_NUMBER: _ClassVar[int]
    status: _status_pb2.Status
    headers: _containers.ScalarMap[str, str]
    def __init__(self, status: _Optional[_Union[_status_pb2.Status, _Mapping]] = ..., headers: _Optional[_Mapping[str, str]] = ...) -> None: ...

class ReportRequest(_message.Message):
    __slots__ = ("service_name", "service_config_id", "operations")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    SERVICE_CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    service_config_id: str
    operations: _containers.RepeatedCompositeFieldContainer[_attribute_context_pb2.AttributeContext]
    def __init__(self, service_name: _Optional[str] = ..., service_config_id: _Optional[str] = ..., operations: _Optional[_Iterable[_Union[_attribute_context_pb2.AttributeContext, _Mapping]]] = ...) -> None: ...

class ReportResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ResourceInfoList(_message.Message):
    __slots__ = ("resources",)
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    resources: _containers.RepeatedCompositeFieldContainer[ResourceInfo]
    def __init__(self, resources: _Optional[_Iterable[_Union[ResourceInfo, _Mapping]]] = ...) -> None: ...
