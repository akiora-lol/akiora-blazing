import datetime

from google.api.servicecontrol.v1 import log_entry_pb2 as _log_entry_pb2
from google.api.servicecontrol.v1 import metric_value_pb2 as _metric_value_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Operation(_message.Message):
    __slots__ = ("operation_id", "operation_name", "consumer_id", "start_time", "end_time", "labels", "metric_value_sets", "log_entries", "importance", "extensions")
    class Importance(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LOW: _ClassVar[Operation.Importance]
        HIGH: _ClassVar[Operation.Importance]
    LOW: Operation.Importance
    HIGH: Operation.Importance
    class LabelsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    OPERATION_NAME_FIELD_NUMBER: _ClassVar[int]
    CONSUMER_ID_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    METRIC_VALUE_SETS_FIELD_NUMBER: _ClassVar[int]
    LOG_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    IMPORTANCE_FIELD_NUMBER: _ClassVar[int]
    EXTENSIONS_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    operation_name: str
    consumer_id: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    labels: _containers.ScalarMap[str, str]
    metric_value_sets: _containers.RepeatedCompositeFieldContainer[_metric_value_pb2.MetricValueSet]
    log_entries: _containers.RepeatedCompositeFieldContainer[_log_entry_pb2.LogEntry]
    importance: Operation.Importance
    extensions: _containers.RepeatedCompositeFieldContainer[_any_pb2.Any]
    def __init__(self, operation_id: _Optional[str] = ..., operation_name: _Optional[str] = ..., consumer_id: _Optional[str] = ..., start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., labels: _Optional[_Mapping[str, str]] = ..., metric_value_sets: _Optional[_Iterable[_Union[_metric_value_pb2.MetricValueSet, _Mapping]]] = ..., log_entries: _Optional[_Iterable[_Union[_log_entry_pb2.LogEntry, _Mapping]]] = ..., importance: _Optional[_Union[Operation.Importance, str]] = ..., extensions: _Optional[_Iterable[_Union[_any_pb2.Any, _Mapping]]] = ...) -> None: ...
