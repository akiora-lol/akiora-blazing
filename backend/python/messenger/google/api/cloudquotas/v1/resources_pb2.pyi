import datetime

from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.api import resource_pb2 as _resource_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QuotaSafetyCheck(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    QUOTA_SAFETY_CHECK_UNSPECIFIED: _ClassVar[QuotaSafetyCheck]
    QUOTA_DECREASE_BELOW_USAGE: _ClassVar[QuotaSafetyCheck]
    QUOTA_DECREASE_PERCENTAGE_TOO_HIGH: _ClassVar[QuotaSafetyCheck]
QUOTA_SAFETY_CHECK_UNSPECIFIED: QuotaSafetyCheck
QUOTA_DECREASE_BELOW_USAGE: QuotaSafetyCheck
QUOTA_DECREASE_PERCENTAGE_TOO_HIGH: QuotaSafetyCheck

class QuotaInfo(_message.Message):
    __slots__ = ("name", "quota_id", "metric", "service", "is_precise", "refresh_interval", "container_type", "dimensions", "metric_display_name", "quota_display_name", "metric_unit", "quota_increase_eligibility", "is_fixed", "dimensions_infos", "is_concurrent", "service_request_quota_uri")
    class ContainerType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CONTAINER_TYPE_UNSPECIFIED: _ClassVar[QuotaInfo.ContainerType]
        PROJECT: _ClassVar[QuotaInfo.ContainerType]
        FOLDER: _ClassVar[QuotaInfo.ContainerType]
        ORGANIZATION: _ClassVar[QuotaInfo.ContainerType]
    CONTAINER_TYPE_UNSPECIFIED: QuotaInfo.ContainerType
    PROJECT: QuotaInfo.ContainerType
    FOLDER: QuotaInfo.ContainerType
    ORGANIZATION: QuotaInfo.ContainerType
    NAME_FIELD_NUMBER: _ClassVar[int]
    QUOTA_ID_FIELD_NUMBER: _ClassVar[int]
    METRIC_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    IS_PRECISE_FIELD_NUMBER: _ClassVar[int]
    REFRESH_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_TYPE_FIELD_NUMBER: _ClassVar[int]
    DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
    METRIC_DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    QUOTA_DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    METRIC_UNIT_FIELD_NUMBER: _ClassVar[int]
    QUOTA_INCREASE_ELIGIBILITY_FIELD_NUMBER: _ClassVar[int]
    IS_FIXED_FIELD_NUMBER: _ClassVar[int]
    DIMENSIONS_INFOS_FIELD_NUMBER: _ClassVar[int]
    IS_CONCURRENT_FIELD_NUMBER: _ClassVar[int]
    SERVICE_REQUEST_QUOTA_URI_FIELD_NUMBER: _ClassVar[int]
    name: str
    quota_id: str
    metric: str
    service: str
    is_precise: bool
    refresh_interval: str
    container_type: QuotaInfo.ContainerType
    dimensions: _containers.RepeatedScalarFieldContainer[str]
    metric_display_name: str
    quota_display_name: str
    metric_unit: str
    quota_increase_eligibility: QuotaIncreaseEligibility
    is_fixed: bool
    dimensions_infos: _containers.RepeatedCompositeFieldContainer[DimensionsInfo]
    is_concurrent: bool
    service_request_quota_uri: str
    def __init__(self, name: _Optional[str] = ..., quota_id: _Optional[str] = ..., metric: _Optional[str] = ..., service: _Optional[str] = ..., is_precise: bool = ..., refresh_interval: _Optional[str] = ..., container_type: _Optional[_Union[QuotaInfo.ContainerType, str]] = ..., dimensions: _Optional[_Iterable[str]] = ..., metric_display_name: _Optional[str] = ..., quota_display_name: _Optional[str] = ..., metric_unit: _Optional[str] = ..., quota_increase_eligibility: _Optional[_Union[QuotaIncreaseEligibility, _Mapping]] = ..., is_fixed: bool = ..., dimensions_infos: _Optional[_Iterable[_Union[DimensionsInfo, _Mapping]]] = ..., is_concurrent: bool = ..., service_request_quota_uri: _Optional[str] = ...) -> None: ...

class QuotaIncreaseEligibility(_message.Message):
    __slots__ = ("is_eligible", "ineligibility_reason")
    class IneligibilityReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        INELIGIBILITY_REASON_UNSPECIFIED: _ClassVar[QuotaIncreaseEligibility.IneligibilityReason]
        NO_VALID_BILLING_ACCOUNT: _ClassVar[QuotaIncreaseEligibility.IneligibilityReason]
        NOT_SUPPORTED: _ClassVar[QuotaIncreaseEligibility.IneligibilityReason]
        NOT_ENOUGH_USAGE_HISTORY: _ClassVar[QuotaIncreaseEligibility.IneligibilityReason]
        OTHER: _ClassVar[QuotaIncreaseEligibility.IneligibilityReason]
    INELIGIBILITY_REASON_UNSPECIFIED: QuotaIncreaseEligibility.IneligibilityReason
    NO_VALID_BILLING_ACCOUNT: QuotaIncreaseEligibility.IneligibilityReason
    NOT_SUPPORTED: QuotaIncreaseEligibility.IneligibilityReason
    NOT_ENOUGH_USAGE_HISTORY: QuotaIncreaseEligibility.IneligibilityReason
    OTHER: QuotaIncreaseEligibility.IneligibilityReason
    IS_ELIGIBLE_FIELD_NUMBER: _ClassVar[int]
    INELIGIBILITY_REASON_FIELD_NUMBER: _ClassVar[int]
    is_eligible: bool
    ineligibility_reason: QuotaIncreaseEligibility.IneligibilityReason
    def __init__(self, is_eligible: bool = ..., ineligibility_reason: _Optional[_Union[QuotaIncreaseEligibility.IneligibilityReason, str]] = ...) -> None: ...

class QuotaPreference(_message.Message):
    __slots__ = ("name", "dimensions", "quota_config", "etag", "create_time", "update_time", "service", "quota_id", "reconciling", "justification", "contact_email")
    class DimensionsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
    QUOTA_CONFIG_FIELD_NUMBER: _ClassVar[int]
    ETAG_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    QUOTA_ID_FIELD_NUMBER: _ClassVar[int]
    RECONCILING_FIELD_NUMBER: _ClassVar[int]
    JUSTIFICATION_FIELD_NUMBER: _ClassVar[int]
    CONTACT_EMAIL_FIELD_NUMBER: _ClassVar[int]
    name: str
    dimensions: _containers.ScalarMap[str, str]
    quota_config: QuotaConfig
    etag: str
    create_time: _timestamp_pb2.Timestamp
    update_time: _timestamp_pb2.Timestamp
    service: str
    quota_id: str
    reconciling: bool
    justification: str
    contact_email: str
    def __init__(self, name: _Optional[str] = ..., dimensions: _Optional[_Mapping[str, str]] = ..., quota_config: _Optional[_Union[QuotaConfig, _Mapping]] = ..., etag: _Optional[str] = ..., create_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., update_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., service: _Optional[str] = ..., quota_id: _Optional[str] = ..., reconciling: bool = ..., justification: _Optional[str] = ..., contact_email: _Optional[str] = ...) -> None: ...

class QuotaConfig(_message.Message):
    __slots__ = ("preferred_value", "state_detail", "granted_value", "trace_id", "annotations", "request_origin")
    class Origin(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ORIGIN_UNSPECIFIED: _ClassVar[QuotaConfig.Origin]
        CLOUD_CONSOLE: _ClassVar[QuotaConfig.Origin]
        AUTO_ADJUSTER: _ClassVar[QuotaConfig.Origin]
    ORIGIN_UNSPECIFIED: QuotaConfig.Origin
    CLOUD_CONSOLE: QuotaConfig.Origin
    AUTO_ADJUSTER: QuotaConfig.Origin
    class AnnotationsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    PREFERRED_VALUE_FIELD_NUMBER: _ClassVar[int]
    STATE_DETAIL_FIELD_NUMBER: _ClassVar[int]
    GRANTED_VALUE_FIELD_NUMBER: _ClassVar[int]
    TRACE_ID_FIELD_NUMBER: _ClassVar[int]
    ANNOTATIONS_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ORIGIN_FIELD_NUMBER: _ClassVar[int]
    preferred_value: int
    state_detail: str
    granted_value: _wrappers_pb2.Int64Value
    trace_id: str
    annotations: _containers.ScalarMap[str, str]
    request_origin: QuotaConfig.Origin
    def __init__(self, preferred_value: _Optional[int] = ..., state_detail: _Optional[str] = ..., granted_value: _Optional[_Union[_wrappers_pb2.Int64Value, _Mapping]] = ..., trace_id: _Optional[str] = ..., annotations: _Optional[_Mapping[str, str]] = ..., request_origin: _Optional[_Union[QuotaConfig.Origin, str]] = ...) -> None: ...

class DimensionsInfo(_message.Message):
    __slots__ = ("dimensions", "details", "applicable_locations")
    class DimensionsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    APPLICABLE_LOCATIONS_FIELD_NUMBER: _ClassVar[int]
    dimensions: _containers.ScalarMap[str, str]
    details: QuotaDetails
    applicable_locations: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, dimensions: _Optional[_Mapping[str, str]] = ..., details: _Optional[_Union[QuotaDetails, _Mapping]] = ..., applicable_locations: _Optional[_Iterable[str]] = ...) -> None: ...

class QuotaDetails(_message.Message):
    __slots__ = ("value", "rollout_info")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    ROLLOUT_INFO_FIELD_NUMBER: _ClassVar[int]
    value: int
    rollout_info: RolloutInfo
    def __init__(self, value: _Optional[int] = ..., rollout_info: _Optional[_Union[RolloutInfo, _Mapping]] = ...) -> None: ...

class RolloutInfo(_message.Message):
    __slots__ = ("ongoing_rollout",)
    ONGOING_ROLLOUT_FIELD_NUMBER: _ClassVar[int]
    ongoing_rollout: bool
    def __init__(self, ongoing_rollout: bool = ...) -> None: ...
