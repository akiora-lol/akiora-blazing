import datetime

from google.api import annotations_pb2 as _annotations_pb2
from google.api import client_pb2 as _client_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.api import field_info_pb2 as _field_info_pb2
from google.api import resource_pb2 as _resource_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MaintenanceCategory(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MAINTENANCE_CATEGORY_UNSPECIFIED: _ClassVar[MaintenanceCategory]
    INFRASTRUCTURE: _ClassVar[MaintenanceCategory]
    SERVICE_UPDATE: _ClassVar[MaintenanceCategory]
MAINTENANCE_CATEGORY_UNSPECIFIED: MaintenanceCategory
INFRASTRUCTURE: MaintenanceCategory
SERVICE_UPDATE: MaintenanceCategory

class SummarizeMaintenancesRequest(_message.Message):
    __slots__ = ("parent", "page_size", "page_token", "filter", "order_by")
    PARENT_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    ORDER_BY_FIELD_NUMBER: _ClassVar[int]
    parent: str
    page_size: int
    page_token: str
    filter: str
    order_by: str
    def __init__(self, parent: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ..., filter: _Optional[str] = ..., order_by: _Optional[str] = ...) -> None: ...

class SummarizeMaintenancesResponse(_message.Message):
    __slots__ = ("maintenances", "next_page_token", "unreachable")
    MAINTENANCES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    UNREACHABLE_FIELD_NUMBER: _ClassVar[int]
    maintenances: _containers.RepeatedCompositeFieldContainer[MaintenanceSummary]
    next_page_token: str
    unreachable: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, maintenances: _Optional[_Iterable[_Union[MaintenanceSummary, _Mapping]]] = ..., next_page_token: _Optional[str] = ..., unreachable: _Optional[_Iterable[str]] = ...) -> None: ...

class MaintenanceSummary(_message.Message):
    __slots__ = ("maintenance_name", "title", "description", "category", "maintenance_scheduled_start_time", "maintenance_scheduled_end_time", "maintenance_start_time", "maintenance_end_time", "user_controllable", "controls", "stats")
    class Stats(_message.Message):
        __slots__ = ("group_by", "aggregates")
        GROUP_BY_FIELD_NUMBER: _ClassVar[int]
        AGGREGATES_FIELD_NUMBER: _ClassVar[int]
        group_by: str
        aggregates: _containers.RepeatedCompositeFieldContainer[MaintenanceSummary.Aggregate]
        def __init__(self, group_by: _Optional[str] = ..., aggregates: _Optional[_Iterable[_Union[MaintenanceSummary.Aggregate, _Mapping]]] = ...) -> None: ...
    class Aggregate(_message.Message):
        __slots__ = ("group", "count")
        GROUP_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        group: str
        count: int
        def __init__(self, group: _Optional[str] = ..., count: _Optional[int] = ...) -> None: ...
    MAINTENANCE_NAME_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    MAINTENANCE_SCHEDULED_START_TIME_FIELD_NUMBER: _ClassVar[int]
    MAINTENANCE_SCHEDULED_END_TIME_FIELD_NUMBER: _ClassVar[int]
    MAINTENANCE_START_TIME_FIELD_NUMBER: _ClassVar[int]
    MAINTENANCE_END_TIME_FIELD_NUMBER: _ClassVar[int]
    USER_CONTROLLABLE_FIELD_NUMBER: _ClassVar[int]
    CONTROLS_FIELD_NUMBER: _ClassVar[int]
    STATS_FIELD_NUMBER: _ClassVar[int]
    maintenance_name: str
    title: str
    description: str
    category: MaintenanceCategory
    maintenance_scheduled_start_time: _timestamp_pb2.Timestamp
    maintenance_scheduled_end_time: _timestamp_pb2.Timestamp
    maintenance_start_time: _timestamp_pb2.Timestamp
    maintenance_end_time: _timestamp_pb2.Timestamp
    user_controllable: bool
    controls: _containers.RepeatedCompositeFieldContainer[MaintenanceControl]
    stats: _containers.RepeatedCompositeFieldContainer[MaintenanceSummary.Stats]
    def __init__(self, maintenance_name: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., category: _Optional[_Union[MaintenanceCategory, str]] = ..., maintenance_scheduled_start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., maintenance_scheduled_end_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., maintenance_start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., maintenance_end_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., user_controllable: bool = ..., controls: _Optional[_Iterable[_Union[MaintenanceControl, _Mapping]]] = ..., stats: _Optional[_Iterable[_Union[MaintenanceSummary.Stats, _Mapping]]] = ...) -> None: ...

class ResourceMaintenance(_message.Message):
    __slots__ = ("name", "resource", "maintenance", "state", "create_time", "update_time", "maintenance_start_time", "maintenance_end_time", "maintenance_cancel_time", "maintenance_scheduled_start_time", "maintenance_scheduled_end_time", "user_controllable", "controls", "labels", "annotations", "uid", "etag")
    class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        STATE_UNSPECIFIED: _ClassVar[ResourceMaintenance.State]
        SCHEDULED: _ClassVar[ResourceMaintenance.State]
        RUNNING: _ClassVar[ResourceMaintenance.State]
        CANCELLED: _ClassVar[ResourceMaintenance.State]
        SUCCEEDED: _ClassVar[ResourceMaintenance.State]
    STATE_UNSPECIFIED: ResourceMaintenance.State
    SCHEDULED: ResourceMaintenance.State
    RUNNING: ResourceMaintenance.State
    CANCELLED: ResourceMaintenance.State
    SUCCEEDED: ResourceMaintenance.State
    class Resource(_message.Message):
        __slots__ = ("resource_name", "location", "type")
        RESOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
        LOCATION_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        resource_name: str
        location: str
        type: str
        def __init__(self, resource_name: _Optional[str] = ..., location: _Optional[str] = ..., type: _Optional[str] = ...) -> None: ...
    class Maintenance(_message.Message):
        __slots__ = ("maintenance_name", "title", "description", "category")
        MAINTENANCE_NAME_FIELD_NUMBER: _ClassVar[int]
        TITLE_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        CATEGORY_FIELD_NUMBER: _ClassVar[int]
        maintenance_name: str
        title: str
        description: str
        category: MaintenanceCategory
        def __init__(self, maintenance_name: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., category: _Optional[_Union[MaintenanceCategory, str]] = ...) -> None: ...
    class LabelsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class AnnotationsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    MAINTENANCE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    MAINTENANCE_START_TIME_FIELD_NUMBER: _ClassVar[int]
    MAINTENANCE_END_TIME_FIELD_NUMBER: _ClassVar[int]
    MAINTENANCE_CANCEL_TIME_FIELD_NUMBER: _ClassVar[int]
    MAINTENANCE_SCHEDULED_START_TIME_FIELD_NUMBER: _ClassVar[int]
    MAINTENANCE_SCHEDULED_END_TIME_FIELD_NUMBER: _ClassVar[int]
    USER_CONTROLLABLE_FIELD_NUMBER: _ClassVar[int]
    CONTROLS_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    ANNOTATIONS_FIELD_NUMBER: _ClassVar[int]
    UID_FIELD_NUMBER: _ClassVar[int]
    ETAG_FIELD_NUMBER: _ClassVar[int]
    name: str
    resource: ResourceMaintenance.Resource
    maintenance: ResourceMaintenance.Maintenance
    state: ResourceMaintenance.State
    create_time: _timestamp_pb2.Timestamp
    update_time: _timestamp_pb2.Timestamp
    maintenance_start_time: _timestamp_pb2.Timestamp
    maintenance_end_time: _timestamp_pb2.Timestamp
    maintenance_cancel_time: _timestamp_pb2.Timestamp
    maintenance_scheduled_start_time: _timestamp_pb2.Timestamp
    maintenance_scheduled_end_time: _timestamp_pb2.Timestamp
    user_controllable: bool
    controls: _containers.RepeatedCompositeFieldContainer[MaintenanceControl]
    labels: _containers.ScalarMap[str, str]
    annotations: _containers.ScalarMap[str, str]
    uid: str
    etag: str
    def __init__(self, name: _Optional[str] = ..., resource: _Optional[_Union[ResourceMaintenance.Resource, _Mapping]] = ..., maintenance: _Optional[_Union[ResourceMaintenance.Maintenance, _Mapping]] = ..., state: _Optional[_Union[ResourceMaintenance.State, str]] = ..., create_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., update_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., maintenance_start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., maintenance_end_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., maintenance_cancel_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., maintenance_scheduled_start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., maintenance_scheduled_end_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., user_controllable: bool = ..., controls: _Optional[_Iterable[_Union[MaintenanceControl, _Mapping]]] = ..., labels: _Optional[_Mapping[str, str]] = ..., annotations: _Optional[_Mapping[str, str]] = ..., uid: _Optional[str] = ..., etag: _Optional[str] = ...) -> None: ...

class MaintenanceControl(_message.Message):
    __slots__ = ("control", "is_custom", "documentation")
    class Control(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CONTROL_UNSPECIFIED: _ClassVar[MaintenanceControl.Control]
        APPLY: _ClassVar[MaintenanceControl.Control]
        MANAGE_POLICY: _ClassVar[MaintenanceControl.Control]
        RESCHEDULE: _ClassVar[MaintenanceControl.Control]
    CONTROL_UNSPECIFIED: MaintenanceControl.Control
    APPLY: MaintenanceControl.Control
    MANAGE_POLICY: MaintenanceControl.Control
    RESCHEDULE: MaintenanceControl.Control
    CONTROL_FIELD_NUMBER: _ClassVar[int]
    IS_CUSTOM_FIELD_NUMBER: _ClassVar[int]
    DOCUMENTATION_FIELD_NUMBER: _ClassVar[int]
    control: MaintenanceControl.Control
    is_custom: bool
    documentation: str
    def __init__(self, control: _Optional[_Union[MaintenanceControl.Control, str]] = ..., is_custom: bool = ..., documentation: _Optional[str] = ...) -> None: ...

class ListResourceMaintenancesRequest(_message.Message):
    __slots__ = ("parent", "page_size", "page_token", "filter", "order_by")
    PARENT_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    ORDER_BY_FIELD_NUMBER: _ClassVar[int]
    parent: str
    page_size: int
    page_token: str
    filter: str
    order_by: str
    def __init__(self, parent: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ..., filter: _Optional[str] = ..., order_by: _Optional[str] = ...) -> None: ...

class ListResourceMaintenancesResponse(_message.Message):
    __slots__ = ("resource_maintenances", "next_page_token", "unreachable")
    RESOURCE_MAINTENANCES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    UNREACHABLE_FIELD_NUMBER: _ClassVar[int]
    resource_maintenances: _containers.RepeatedCompositeFieldContainer[ResourceMaintenance]
    next_page_token: str
    unreachable: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, resource_maintenances: _Optional[_Iterable[_Union[ResourceMaintenance, _Mapping]]] = ..., next_page_token: _Optional[str] = ..., unreachable: _Optional[_Iterable[str]] = ...) -> None: ...

class GetResourceMaintenanceRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...
