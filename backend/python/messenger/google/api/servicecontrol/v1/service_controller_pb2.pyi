from google.api import annotations_pb2 as _annotations_pb2
from google.api import client_pb2 as _client_pb2
from google.api.servicecontrol.v1 import check_error_pb2 as _check_error_pb2
from google.api.servicecontrol.v1 import operation_pb2 as _operation_pb2
from google.rpc import status_pb2 as _status_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CheckRequest(_message.Message):
    __slots__ = ("service_name", "operation", "service_config_id")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    SERVICE_CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    operation: _operation_pb2.Operation
    service_config_id: str
    def __init__(self, service_name: _Optional[str] = ..., operation: _Optional[_Union[_operation_pb2.Operation, _Mapping]] = ..., service_config_id: _Optional[str] = ...) -> None: ...

class CheckResponse(_message.Message):
    __slots__ = ("operation_id", "check_errors", "service_config_id", "service_rollout_id", "check_info")
    class CheckInfo(_message.Message):
        __slots__ = ("unused_arguments", "consumer_info", "api_key_uid")
        UNUSED_ARGUMENTS_FIELD_NUMBER: _ClassVar[int]
        CONSUMER_INFO_FIELD_NUMBER: _ClassVar[int]
        API_KEY_UID_FIELD_NUMBER: _ClassVar[int]
        unused_arguments: _containers.RepeatedScalarFieldContainer[str]
        consumer_info: CheckResponse.ConsumerInfo
        api_key_uid: str
        def __init__(self, unused_arguments: _Optional[_Iterable[str]] = ..., consumer_info: _Optional[_Union[CheckResponse.ConsumerInfo, _Mapping]] = ..., api_key_uid: _Optional[str] = ...) -> None: ...
    class ConsumerInfo(_message.Message):
        __slots__ = ("project_number", "type", "consumer_number")
        class ConsumerType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            CONSUMER_TYPE_UNSPECIFIED: _ClassVar[CheckResponse.ConsumerInfo.ConsumerType]
            PROJECT: _ClassVar[CheckResponse.ConsumerInfo.ConsumerType]
            FOLDER: _ClassVar[CheckResponse.ConsumerInfo.ConsumerType]
            ORGANIZATION: _ClassVar[CheckResponse.ConsumerInfo.ConsumerType]
            SERVICE_SPECIFIC: _ClassVar[CheckResponse.ConsumerInfo.ConsumerType]
        CONSUMER_TYPE_UNSPECIFIED: CheckResponse.ConsumerInfo.ConsumerType
        PROJECT: CheckResponse.ConsumerInfo.ConsumerType
        FOLDER: CheckResponse.ConsumerInfo.ConsumerType
        ORGANIZATION: CheckResponse.ConsumerInfo.ConsumerType
        SERVICE_SPECIFIC: CheckResponse.ConsumerInfo.ConsumerType
        PROJECT_NUMBER_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        CONSUMER_NUMBER_FIELD_NUMBER: _ClassVar[int]
        project_number: int
        type: CheckResponse.ConsumerInfo.ConsumerType
        consumer_number: int
        def __init__(self, project_number: _Optional[int] = ..., type: _Optional[_Union[CheckResponse.ConsumerInfo.ConsumerType, str]] = ..., consumer_number: _Optional[int] = ...) -> None: ...
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    CHECK_ERRORS_FIELD_NUMBER: _ClassVar[int]
    SERVICE_CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ROLLOUT_ID_FIELD_NUMBER: _ClassVar[int]
    CHECK_INFO_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    check_errors: _containers.RepeatedCompositeFieldContainer[_check_error_pb2.CheckError]
    service_config_id: str
    service_rollout_id: str
    check_info: CheckResponse.CheckInfo
    def __init__(self, operation_id: _Optional[str] = ..., check_errors: _Optional[_Iterable[_Union[_check_error_pb2.CheckError, _Mapping]]] = ..., service_config_id: _Optional[str] = ..., service_rollout_id: _Optional[str] = ..., check_info: _Optional[_Union[CheckResponse.CheckInfo, _Mapping]] = ...) -> None: ...

class ReportRequest(_message.Message):
    __slots__ = ("service_name", "operations", "service_config_id")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    SERVICE_CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    operations: _containers.RepeatedCompositeFieldContainer[_operation_pb2.Operation]
    service_config_id: str
    def __init__(self, service_name: _Optional[str] = ..., operations: _Optional[_Iterable[_Union[_operation_pb2.Operation, _Mapping]]] = ..., service_config_id: _Optional[str] = ...) -> None: ...

class ReportResponse(_message.Message):
    __slots__ = ("report_errors", "service_config_id", "service_rollout_id")
    class ReportError(_message.Message):
        __slots__ = ("operation_id", "status")
        OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
        STATUS_FIELD_NUMBER: _ClassVar[int]
        operation_id: str
        status: _status_pb2.Status
        def __init__(self, operation_id: _Optional[str] = ..., status: _Optional[_Union[_status_pb2.Status, _Mapping]] = ...) -> None: ...
    REPORT_ERRORS_FIELD_NUMBER: _ClassVar[int]
    SERVICE_CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ROLLOUT_ID_FIELD_NUMBER: _ClassVar[int]
    report_errors: _containers.RepeatedCompositeFieldContainer[ReportResponse.ReportError]
    service_config_id: str
    service_rollout_id: str
    def __init__(self, report_errors: _Optional[_Iterable[_Union[ReportResponse.ReportError, _Mapping]]] = ..., service_config_id: _Optional[str] = ..., service_rollout_id: _Optional[str] = ...) -> None: ...
