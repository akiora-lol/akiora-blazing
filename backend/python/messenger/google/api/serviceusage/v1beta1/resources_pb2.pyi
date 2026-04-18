from google.api import auth_pb2 as _auth_pb2
from google.api import documentation_pb2 as _documentation_pb2
from google.api import endpoint_pb2 as _endpoint_pb2
from google.api import monitored_resource_pb2 as _monitored_resource_pb2
from google.api import monitoring_pb2 as _monitoring_pb2
from google.api import quota_pb2 as _quota_pb2
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

class QuotaView(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    QUOTA_VIEW_UNSPECIFIED: _ClassVar[QuotaView]
    BASIC: _ClassVar[QuotaView]
    FULL: _ClassVar[QuotaView]

class QuotaSafetyCheck(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    QUOTA_SAFETY_CHECK_UNSPECIFIED: _ClassVar[QuotaSafetyCheck]
    LIMIT_DECREASE_BELOW_USAGE: _ClassVar[QuotaSafetyCheck]
    LIMIT_DECREASE_PERCENTAGE_TOO_HIGH: _ClassVar[QuotaSafetyCheck]
STATE_UNSPECIFIED: State
DISABLED: State
ENABLED: State
QUOTA_VIEW_UNSPECIFIED: QuotaView
BASIC: QuotaView
FULL: QuotaView
QUOTA_SAFETY_CHECK_UNSPECIFIED: QuotaSafetyCheck
LIMIT_DECREASE_BELOW_USAGE: QuotaSafetyCheck
LIMIT_DECREASE_PERCENTAGE_TOO_HIGH: QuotaSafetyCheck

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

class ConsumerQuotaMetric(_message.Message):
    __slots__ = ("name", "metric", "display_name", "consumer_quota_limits", "descendant_consumer_quota_limits", "unit")
    NAME_FIELD_NUMBER: _ClassVar[int]
    METRIC_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    CONSUMER_QUOTA_LIMITS_FIELD_NUMBER: _ClassVar[int]
    DESCENDANT_CONSUMER_QUOTA_LIMITS_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    name: str
    metric: str
    display_name: str
    consumer_quota_limits: _containers.RepeatedCompositeFieldContainer[ConsumerQuotaLimit]
    descendant_consumer_quota_limits: _containers.RepeatedCompositeFieldContainer[ConsumerQuotaLimit]
    unit: str
    def __init__(self, name: _Optional[str] = ..., metric: _Optional[str] = ..., display_name: _Optional[str] = ..., consumer_quota_limits: _Optional[_Iterable[_Union[ConsumerQuotaLimit, _Mapping]]] = ..., descendant_consumer_quota_limits: _Optional[_Iterable[_Union[ConsumerQuotaLimit, _Mapping]]] = ..., unit: _Optional[str] = ...) -> None: ...

class ConsumerQuotaLimit(_message.Message):
    __slots__ = ("name", "metric", "unit", "is_precise", "allows_admin_overrides", "quota_buckets", "supported_locations")
    NAME_FIELD_NUMBER: _ClassVar[int]
    METRIC_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    IS_PRECISE_FIELD_NUMBER: _ClassVar[int]
    ALLOWS_ADMIN_OVERRIDES_FIELD_NUMBER: _ClassVar[int]
    QUOTA_BUCKETS_FIELD_NUMBER: _ClassVar[int]
    SUPPORTED_LOCATIONS_FIELD_NUMBER: _ClassVar[int]
    name: str
    metric: str
    unit: str
    is_precise: bool
    allows_admin_overrides: bool
    quota_buckets: _containers.RepeatedCompositeFieldContainer[QuotaBucket]
    supported_locations: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., metric: _Optional[str] = ..., unit: _Optional[str] = ..., is_precise: bool = ..., allows_admin_overrides: bool = ..., quota_buckets: _Optional[_Iterable[_Union[QuotaBucket, _Mapping]]] = ..., supported_locations: _Optional[_Iterable[str]] = ...) -> None: ...

class QuotaBucket(_message.Message):
    __slots__ = ("effective_limit", "default_limit", "producer_override", "consumer_override", "admin_override", "producer_quota_policy", "dimensions")
    class DimensionsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    EFFECTIVE_LIMIT_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_LIMIT_FIELD_NUMBER: _ClassVar[int]
    PRODUCER_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    CONSUMER_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    ADMIN_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    PRODUCER_QUOTA_POLICY_FIELD_NUMBER: _ClassVar[int]
    DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
    effective_limit: int
    default_limit: int
    producer_override: QuotaOverride
    consumer_override: QuotaOverride
    admin_override: QuotaOverride
    producer_quota_policy: ProducerQuotaPolicy
    dimensions: _containers.ScalarMap[str, str]
    def __init__(self, effective_limit: _Optional[int] = ..., default_limit: _Optional[int] = ..., producer_override: _Optional[_Union[QuotaOverride, _Mapping]] = ..., consumer_override: _Optional[_Union[QuotaOverride, _Mapping]] = ..., admin_override: _Optional[_Union[QuotaOverride, _Mapping]] = ..., producer_quota_policy: _Optional[_Union[ProducerQuotaPolicy, _Mapping]] = ..., dimensions: _Optional[_Mapping[str, str]] = ...) -> None: ...

class QuotaOverride(_message.Message):
    __slots__ = ("name", "override_value", "dimensions", "metric", "unit", "admin_override_ancestor")
    class DimensionsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_VALUE_FIELD_NUMBER: _ClassVar[int]
    DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
    METRIC_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    ADMIN_OVERRIDE_ANCESTOR_FIELD_NUMBER: _ClassVar[int]
    name: str
    override_value: int
    dimensions: _containers.ScalarMap[str, str]
    metric: str
    unit: str
    admin_override_ancestor: str
    def __init__(self, name: _Optional[str] = ..., override_value: _Optional[int] = ..., dimensions: _Optional[_Mapping[str, str]] = ..., metric: _Optional[str] = ..., unit: _Optional[str] = ..., admin_override_ancestor: _Optional[str] = ...) -> None: ...

class OverrideInlineSource(_message.Message):
    __slots__ = ("overrides",)
    OVERRIDES_FIELD_NUMBER: _ClassVar[int]
    overrides: _containers.RepeatedCompositeFieldContainer[QuotaOverride]
    def __init__(self, overrides: _Optional[_Iterable[_Union[QuotaOverride, _Mapping]]] = ...) -> None: ...

class ProducerQuotaPolicy(_message.Message):
    __slots__ = ("name", "policy_value", "dimensions", "metric", "unit", "container")
    class DimensionsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    POLICY_VALUE_FIELD_NUMBER: _ClassVar[int]
    DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
    METRIC_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_FIELD_NUMBER: _ClassVar[int]
    name: str
    policy_value: int
    dimensions: _containers.ScalarMap[str, str]
    metric: str
    unit: str
    container: str
    def __init__(self, name: _Optional[str] = ..., policy_value: _Optional[int] = ..., dimensions: _Optional[_Mapping[str, str]] = ..., metric: _Optional[str] = ..., unit: _Optional[str] = ..., container: _Optional[str] = ...) -> None: ...

class AdminQuotaPolicy(_message.Message):
    __slots__ = ("name", "policy_value", "dimensions", "metric", "unit", "container")
    class DimensionsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    POLICY_VALUE_FIELD_NUMBER: _ClassVar[int]
    DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
    METRIC_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_FIELD_NUMBER: _ClassVar[int]
    name: str
    policy_value: int
    dimensions: _containers.ScalarMap[str, str]
    metric: str
    unit: str
    container: str
    def __init__(self, name: _Optional[str] = ..., policy_value: _Optional[int] = ..., dimensions: _Optional[_Mapping[str, str]] = ..., metric: _Optional[str] = ..., unit: _Optional[str] = ..., container: _Optional[str] = ...) -> None: ...

class ServiceIdentity(_message.Message):
    __slots__ = ("email", "unique_id")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    email: str
    unique_id: str
    def __init__(self, email: _Optional[str] = ..., unique_id: _Optional[str] = ...) -> None: ...
