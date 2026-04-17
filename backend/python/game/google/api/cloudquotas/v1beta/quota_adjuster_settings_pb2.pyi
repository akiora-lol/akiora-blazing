import datetime

from google.api import annotations_pb2 as _annotations_pb2
from google.api import client_pb2 as _client_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.api import resource_pb2 as _resource_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetQuotaAdjusterSettingsRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class UpdateQuotaAdjusterSettingsRequest(_message.Message):
    __slots__ = ("quota_adjuster_settings", "update_mask", "validate_only")
    QUOTA_ADJUSTER_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    VALIDATE_ONLY_FIELD_NUMBER: _ClassVar[int]
    quota_adjuster_settings: QuotaAdjusterSettings
    update_mask: _field_mask_pb2.FieldMask
    validate_only: bool
    def __init__(self, quota_adjuster_settings: _Optional[_Union[QuotaAdjusterSettings, _Mapping]] = ..., update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ..., validate_only: bool = ...) -> None: ...

class QuotaAdjusterSettings(_message.Message):
    __slots__ = ("name", "enablement", "update_time", "etag", "inherited", "inherited_from")
    class Enablement(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ENABLEMENT_UNSPECIFIED: _ClassVar[QuotaAdjusterSettings.Enablement]
        ENABLED: _ClassVar[QuotaAdjusterSettings.Enablement]
        DISABLED: _ClassVar[QuotaAdjusterSettings.Enablement]
    ENABLEMENT_UNSPECIFIED: QuotaAdjusterSettings.Enablement
    ENABLED: QuotaAdjusterSettings.Enablement
    DISABLED: QuotaAdjusterSettings.Enablement
    NAME_FIELD_NUMBER: _ClassVar[int]
    ENABLEMENT_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    ETAG_FIELD_NUMBER: _ClassVar[int]
    INHERITED_FIELD_NUMBER: _ClassVar[int]
    INHERITED_FROM_FIELD_NUMBER: _ClassVar[int]
    name: str
    enablement: QuotaAdjusterSettings.Enablement
    update_time: _timestamp_pb2.Timestamp
    etag: str
    inherited: bool
    inherited_from: str
    def __init__(self, name: _Optional[str] = ..., enablement: _Optional[_Union[QuotaAdjusterSettings.Enablement, str]] = ..., update_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., etag: _Optional[str] = ..., inherited: bool = ..., inherited_from: _Optional[str] = ...) -> None: ...
