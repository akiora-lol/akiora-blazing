from google.api import annotations_pb2 as _annotations_pb2
from google.api.servicecontrol.v1 import metric_value_pb2 as _metric_value_pb2
from google.rpc import status_pb2 as _status_pb2
from google.api import client_pb2 as _client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AllocateQuotaRequest(_message.Message):
    __slots__ = ("service_name", "allocate_operation", "service_config_id")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    ALLOCATE_OPERATION_FIELD_NUMBER: _ClassVar[int]
    SERVICE_CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    allocate_operation: QuotaOperation
    service_config_id: str
    def __init__(self, service_name: _Optional[str] = ..., allocate_operation: _Optional[_Union[QuotaOperation, _Mapping]] = ..., service_config_id: _Optional[str] = ...) -> None: ...

class QuotaOperation(_message.Message):
    __slots__ = ("operation_id", "method_name", "consumer_id", "labels", "quota_metrics", "quota_mode")
    class QuotaMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNSPECIFIED: _ClassVar[QuotaOperation.QuotaMode]
        NORMAL: _ClassVar[QuotaOperation.QuotaMode]
        BEST_EFFORT: _ClassVar[QuotaOperation.QuotaMode]
        CHECK_ONLY: _ClassVar[QuotaOperation.QuotaMode]
        QUERY_ONLY: _ClassVar[QuotaOperation.QuotaMode]
        ADJUST_ONLY: _ClassVar[QuotaOperation.QuotaMode]
    UNSPECIFIED: QuotaOperation.QuotaMode
    NORMAL: QuotaOperation.QuotaMode
    BEST_EFFORT: QuotaOperation.QuotaMode
    CHECK_ONLY: QuotaOperation.QuotaMode
    QUERY_ONLY: QuotaOperation.QuotaMode
    ADJUST_ONLY: QuotaOperation.QuotaMode
    class LabelsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    METHOD_NAME_FIELD_NUMBER: _ClassVar[int]
    CONSUMER_ID_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    QUOTA_METRICS_FIELD_NUMBER: _ClassVar[int]
    QUOTA_MODE_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    method_name: str
    consumer_id: str
    labels: _containers.ScalarMap[str, str]
    quota_metrics: _containers.RepeatedCompositeFieldContainer[_metric_value_pb2.MetricValueSet]
    quota_mode: QuotaOperation.QuotaMode
    def __init__(self, operation_id: _Optional[str] = ..., method_name: _Optional[str] = ..., consumer_id: _Optional[str] = ..., labels: _Optional[_Mapping[str, str]] = ..., quota_metrics: _Optional[_Iterable[_Union[_metric_value_pb2.MetricValueSet, _Mapping]]] = ..., quota_mode: _Optional[_Union[QuotaOperation.QuotaMode, str]] = ...) -> None: ...

class AllocateQuotaResponse(_message.Message):
    __slots__ = ("operation_id", "allocate_errors", "quota_metrics", "service_config_id")
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    ALLOCATE_ERRORS_FIELD_NUMBER: _ClassVar[int]
    QUOTA_METRICS_FIELD_NUMBER: _ClassVar[int]
    SERVICE_CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    allocate_errors: _containers.RepeatedCompositeFieldContainer[QuotaError]
    quota_metrics: _containers.RepeatedCompositeFieldContainer[_metric_value_pb2.MetricValueSet]
    service_config_id: str
    def __init__(self, operation_id: _Optional[str] = ..., allocate_errors: _Optional[_Iterable[_Union[QuotaError, _Mapping]]] = ..., quota_metrics: _Optional[_Iterable[_Union[_metric_value_pb2.MetricValueSet, _Mapping]]] = ..., service_config_id: _Optional[str] = ...) -> None: ...

class QuotaError(_message.Message):
    __slots__ = ("code", "subject", "description", "status")
    class Code(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNSPECIFIED: _ClassVar[QuotaError.Code]
        RESOURCE_EXHAUSTED: _ClassVar[QuotaError.Code]
        BILLING_NOT_ACTIVE: _ClassVar[QuotaError.Code]
        PROJECT_DELETED: _ClassVar[QuotaError.Code]
        API_KEY_INVALID: _ClassVar[QuotaError.Code]
        API_KEY_EXPIRED: _ClassVar[QuotaError.Code]
    UNSPECIFIED: QuotaError.Code
    RESOURCE_EXHAUSTED: QuotaError.Code
    BILLING_NOT_ACTIVE: QuotaError.Code
    PROJECT_DELETED: QuotaError.Code
    API_KEY_INVALID: QuotaError.Code
    API_KEY_EXPIRED: QuotaError.Code
    CODE_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    code: QuotaError.Code
    subject: str
    description: str
    status: _status_pb2.Status
    def __init__(self, code: _Optional[_Union[QuotaError.Code, str]] = ..., subject: _Optional[str] = ..., description: _Optional[str] = ..., status: _Optional[_Union[_status_pb2.Status, _Mapping]] = ...) -> None: ...
