import datetime

from google.api import config_change_pb2 as _config_change_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ManagedService(_message.Message):
    __slots__ = ("service_name", "producer_project_id")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    PRODUCER_PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    producer_project_id: str
    def __init__(self, service_name: _Optional[str] = ..., producer_project_id: _Optional[str] = ...) -> None: ...

class OperationMetadata(_message.Message):
    __slots__ = ("resource_names", "steps", "progress_percentage", "start_time")
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        STATUS_UNSPECIFIED: _ClassVar[OperationMetadata.Status]
        DONE: _ClassVar[OperationMetadata.Status]
        NOT_STARTED: _ClassVar[OperationMetadata.Status]
        IN_PROGRESS: _ClassVar[OperationMetadata.Status]
        FAILED: _ClassVar[OperationMetadata.Status]
        CANCELLED: _ClassVar[OperationMetadata.Status]
    STATUS_UNSPECIFIED: OperationMetadata.Status
    DONE: OperationMetadata.Status
    NOT_STARTED: OperationMetadata.Status
    IN_PROGRESS: OperationMetadata.Status
    FAILED: OperationMetadata.Status
    CANCELLED: OperationMetadata.Status
    class Step(_message.Message):
        __slots__ = ("description", "status")
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        STATUS_FIELD_NUMBER: _ClassVar[int]
        description: str
        status: OperationMetadata.Status
        def __init__(self, description: _Optional[str] = ..., status: _Optional[_Union[OperationMetadata.Status, str]] = ...) -> None: ...
    RESOURCE_NAMES_FIELD_NUMBER: _ClassVar[int]
    STEPS_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    resource_names: _containers.RepeatedScalarFieldContainer[str]
    steps: _containers.RepeatedCompositeFieldContainer[OperationMetadata.Step]
    progress_percentage: int
    start_time: _timestamp_pb2.Timestamp
    def __init__(self, resource_names: _Optional[_Iterable[str]] = ..., steps: _Optional[_Iterable[_Union[OperationMetadata.Step, _Mapping]]] = ..., progress_percentage: _Optional[int] = ..., start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Diagnostic(_message.Message):
    __slots__ = ("location", "kind", "message")
    class Kind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        WARNING: _ClassVar[Diagnostic.Kind]
        ERROR: _ClassVar[Diagnostic.Kind]
    WARNING: Diagnostic.Kind
    ERROR: Diagnostic.Kind
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    location: str
    kind: Diagnostic.Kind
    message: str
    def __init__(self, location: _Optional[str] = ..., kind: _Optional[_Union[Diagnostic.Kind, str]] = ..., message: _Optional[str] = ...) -> None: ...

class ConfigSource(_message.Message):
    __slots__ = ("id", "files")
    ID_FIELD_NUMBER: _ClassVar[int]
    FILES_FIELD_NUMBER: _ClassVar[int]
    id: str
    files: _containers.RepeatedCompositeFieldContainer[ConfigFile]
    def __init__(self, id: _Optional[str] = ..., files: _Optional[_Iterable[_Union[ConfigFile, _Mapping]]] = ...) -> None: ...

class ConfigFile(_message.Message):
    __slots__ = ("file_path", "file_contents", "file_type")
    class FileType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        FILE_TYPE_UNSPECIFIED: _ClassVar[ConfigFile.FileType]
        SERVICE_CONFIG_YAML: _ClassVar[ConfigFile.FileType]
        OPEN_API_JSON: _ClassVar[ConfigFile.FileType]
        OPEN_API_YAML: _ClassVar[ConfigFile.FileType]
        FILE_DESCRIPTOR_SET_PROTO: _ClassVar[ConfigFile.FileType]
        PROTO_FILE: _ClassVar[ConfigFile.FileType]
    FILE_TYPE_UNSPECIFIED: ConfigFile.FileType
    SERVICE_CONFIG_YAML: ConfigFile.FileType
    OPEN_API_JSON: ConfigFile.FileType
    OPEN_API_YAML: ConfigFile.FileType
    FILE_DESCRIPTOR_SET_PROTO: ConfigFile.FileType
    PROTO_FILE: ConfigFile.FileType
    FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    FILE_CONTENTS_FIELD_NUMBER: _ClassVar[int]
    FILE_TYPE_FIELD_NUMBER: _ClassVar[int]
    file_path: str
    file_contents: bytes
    file_type: ConfigFile.FileType
    def __init__(self, file_path: _Optional[str] = ..., file_contents: _Optional[bytes] = ..., file_type: _Optional[_Union[ConfigFile.FileType, str]] = ...) -> None: ...

class ConfigRef(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class ChangeReport(_message.Message):
    __slots__ = ("config_changes",)
    CONFIG_CHANGES_FIELD_NUMBER: _ClassVar[int]
    config_changes: _containers.RepeatedCompositeFieldContainer[_config_change_pb2.ConfigChange]
    def __init__(self, config_changes: _Optional[_Iterable[_Union[_config_change_pb2.ConfigChange, _Mapping]]] = ...) -> None: ...

class Rollout(_message.Message):
    __slots__ = ("rollout_id", "create_time", "created_by", "status", "traffic_percent_strategy", "delete_service_strategy", "service_name")
    class RolloutStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ROLLOUT_STATUS_UNSPECIFIED: _ClassVar[Rollout.RolloutStatus]
        IN_PROGRESS: _ClassVar[Rollout.RolloutStatus]
        SUCCESS: _ClassVar[Rollout.RolloutStatus]
        CANCELLED: _ClassVar[Rollout.RolloutStatus]
        FAILED: _ClassVar[Rollout.RolloutStatus]
        PENDING: _ClassVar[Rollout.RolloutStatus]
        FAILED_ROLLED_BACK: _ClassVar[Rollout.RolloutStatus]
    ROLLOUT_STATUS_UNSPECIFIED: Rollout.RolloutStatus
    IN_PROGRESS: Rollout.RolloutStatus
    SUCCESS: Rollout.RolloutStatus
    CANCELLED: Rollout.RolloutStatus
    FAILED: Rollout.RolloutStatus
    PENDING: Rollout.RolloutStatus
    FAILED_ROLLED_BACK: Rollout.RolloutStatus
    class TrafficPercentStrategy(_message.Message):
        __slots__ = ("percentages",)
        class PercentagesEntry(_message.Message):
            __slots__ = ("key", "value")
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: float
            def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
        PERCENTAGES_FIELD_NUMBER: _ClassVar[int]
        percentages: _containers.ScalarMap[str, float]
        def __init__(self, percentages: _Optional[_Mapping[str, float]] = ...) -> None: ...
    class DeleteServiceStrategy(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    ROLLOUT_ID_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TRAFFIC_PERCENT_STRATEGY_FIELD_NUMBER: _ClassVar[int]
    DELETE_SERVICE_STRATEGY_FIELD_NUMBER: _ClassVar[int]
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    rollout_id: str
    create_time: _timestamp_pb2.Timestamp
    created_by: str
    status: Rollout.RolloutStatus
    traffic_percent_strategy: Rollout.TrafficPercentStrategy
    delete_service_strategy: Rollout.DeleteServiceStrategy
    service_name: str
    def __init__(self, rollout_id: _Optional[str] = ..., create_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., created_by: _Optional[str] = ..., status: _Optional[_Union[Rollout.RolloutStatus, str]] = ..., traffic_percent_strategy: _Optional[_Union[Rollout.TrafficPercentStrategy, _Mapping]] = ..., delete_service_strategy: _Optional[_Union[Rollout.DeleteServiceStrategy, _Mapping]] = ..., service_name: _Optional[str] = ...) -> None: ...
