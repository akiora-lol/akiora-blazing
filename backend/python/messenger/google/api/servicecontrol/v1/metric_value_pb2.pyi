import datetime

from google.api.servicecontrol.v1 import distribution_pb2 as _distribution_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MetricValue(_message.Message):
    __slots__ = ("labels", "start_time", "end_time", "bool_value", "int64_value", "double_value", "string_value", "distribution_value")
    class LabelsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    LABELS_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    BOOL_VALUE_FIELD_NUMBER: _ClassVar[int]
    INT64_VALUE_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_VALUE_FIELD_NUMBER: _ClassVar[int]
    STRING_VALUE_FIELD_NUMBER: _ClassVar[int]
    DISTRIBUTION_VALUE_FIELD_NUMBER: _ClassVar[int]
    labels: _containers.ScalarMap[str, str]
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    bool_value: bool
    int64_value: int
    double_value: float
    string_value: str
    distribution_value: _distribution_pb2.Distribution
    def __init__(self, labels: _Optional[_Mapping[str, str]] = ..., start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., bool_value: bool = ..., int64_value: _Optional[int] = ..., double_value: _Optional[float] = ..., string_value: _Optional[str] = ..., distribution_value: _Optional[_Union[_distribution_pb2.Distribution, _Mapping]] = ...) -> None: ...

class MetricValueSet(_message.Message):
    __slots__ = ("metric_name", "metric_values")
    METRIC_NAME_FIELD_NUMBER: _ClassVar[int]
    METRIC_VALUES_FIELD_NUMBER: _ClassVar[int]
    metric_name: str
    metric_values: _containers.RepeatedCompositeFieldContainer[MetricValue]
    def __init__(self, metric_name: _Optional[str] = ..., metric_values: _Optional[_Iterable[_Union[MetricValue, _Mapping]]] = ...) -> None: ...
