import datetime

from google.api.servicecontrol.v1 import http_request_pb2 as _http_request_pb2
from google.logging.type import log_severity_pb2 as _log_severity_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LogEntry(_message.Message):
    __slots__ = ("name", "timestamp", "severity", "http_request", "trace", "insert_id", "labels", "proto_payload", "text_payload", "struct_payload", "operation", "source_location")
    class LabelsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    HTTP_REQUEST_FIELD_NUMBER: _ClassVar[int]
    TRACE_FIELD_NUMBER: _ClassVar[int]
    INSERT_ID_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    PROTO_PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    TEXT_PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    STRUCT_PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    SOURCE_LOCATION_FIELD_NUMBER: _ClassVar[int]
    name: str
    timestamp: _timestamp_pb2.Timestamp
    severity: _log_severity_pb2.LogSeverity
    http_request: _http_request_pb2.HttpRequest
    trace: str
    insert_id: str
    labels: _containers.ScalarMap[str, str]
    proto_payload: _any_pb2.Any
    text_payload: str
    struct_payload: _struct_pb2.Struct
    operation: LogEntryOperation
    source_location: LogEntrySourceLocation
    def __init__(self, name: _Optional[str] = ..., timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., severity: _Optional[_Union[_log_severity_pb2.LogSeverity, str]] = ..., http_request: _Optional[_Union[_http_request_pb2.HttpRequest, _Mapping]] = ..., trace: _Optional[str] = ..., insert_id: _Optional[str] = ..., labels: _Optional[_Mapping[str, str]] = ..., proto_payload: _Optional[_Union[_any_pb2.Any, _Mapping]] = ..., text_payload: _Optional[str] = ..., struct_payload: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., operation: _Optional[_Union[LogEntryOperation, _Mapping]] = ..., source_location: _Optional[_Union[LogEntrySourceLocation, _Mapping]] = ...) -> None: ...

class LogEntryOperation(_message.Message):
    __slots__ = ("id", "producer", "first", "last")
    ID_FIELD_NUMBER: _ClassVar[int]
    PRODUCER_FIELD_NUMBER: _ClassVar[int]
    FIRST_FIELD_NUMBER: _ClassVar[int]
    LAST_FIELD_NUMBER: _ClassVar[int]
    id: str
    producer: str
    first: bool
    last: bool
    def __init__(self, id: _Optional[str] = ..., producer: _Optional[str] = ..., first: bool = ..., last: bool = ...) -> None: ...

class LogEntrySourceLocation(_message.Message):
    __slots__ = ("file", "line", "function")
    FILE_FIELD_NUMBER: _ClassVar[int]
    LINE_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    file: str
    line: int
    function: str
    def __init__(self, file: _Optional[str] = ..., line: _Optional[int] = ..., function: _Optional[str] = ...) -> None: ...
