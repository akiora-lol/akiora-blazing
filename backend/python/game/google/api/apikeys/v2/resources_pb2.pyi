import datetime

from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.api import resource_pb2 as _resource_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Key(_message.Message):
    __slots__ = ("name", "uid", "display_name", "key_string", "create_time", "update_time", "delete_time", "annotations", "restrictions", "etag")
    class AnnotationsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    UID_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    KEY_STRING_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    DELETE_TIME_FIELD_NUMBER: _ClassVar[int]
    ANNOTATIONS_FIELD_NUMBER: _ClassVar[int]
    RESTRICTIONS_FIELD_NUMBER: _ClassVar[int]
    ETAG_FIELD_NUMBER: _ClassVar[int]
    name: str
    uid: str
    display_name: str
    key_string: str
    create_time: _timestamp_pb2.Timestamp
    update_time: _timestamp_pb2.Timestamp
    delete_time: _timestamp_pb2.Timestamp
    annotations: _containers.ScalarMap[str, str]
    restrictions: Restrictions
    etag: str
    def __init__(self, name: _Optional[str] = ..., uid: _Optional[str] = ..., display_name: _Optional[str] = ..., key_string: _Optional[str] = ..., create_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., update_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., delete_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., annotations: _Optional[_Mapping[str, str]] = ..., restrictions: _Optional[_Union[Restrictions, _Mapping]] = ..., etag: _Optional[str] = ...) -> None: ...

class Restrictions(_message.Message):
    __slots__ = ("browser_key_restrictions", "server_key_restrictions", "android_key_restrictions", "ios_key_restrictions", "api_targets")
    BROWSER_KEY_RESTRICTIONS_FIELD_NUMBER: _ClassVar[int]
    SERVER_KEY_RESTRICTIONS_FIELD_NUMBER: _ClassVar[int]
    ANDROID_KEY_RESTRICTIONS_FIELD_NUMBER: _ClassVar[int]
    IOS_KEY_RESTRICTIONS_FIELD_NUMBER: _ClassVar[int]
    API_TARGETS_FIELD_NUMBER: _ClassVar[int]
    browser_key_restrictions: BrowserKeyRestrictions
    server_key_restrictions: ServerKeyRestrictions
    android_key_restrictions: AndroidKeyRestrictions
    ios_key_restrictions: IosKeyRestrictions
    api_targets: _containers.RepeatedCompositeFieldContainer[ApiTarget]
    def __init__(self, browser_key_restrictions: _Optional[_Union[BrowserKeyRestrictions, _Mapping]] = ..., server_key_restrictions: _Optional[_Union[ServerKeyRestrictions, _Mapping]] = ..., android_key_restrictions: _Optional[_Union[AndroidKeyRestrictions, _Mapping]] = ..., ios_key_restrictions: _Optional[_Union[IosKeyRestrictions, _Mapping]] = ..., api_targets: _Optional[_Iterable[_Union[ApiTarget, _Mapping]]] = ...) -> None: ...

class BrowserKeyRestrictions(_message.Message):
    __slots__ = ("allowed_referrers",)
    ALLOWED_REFERRERS_FIELD_NUMBER: _ClassVar[int]
    allowed_referrers: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, allowed_referrers: _Optional[_Iterable[str]] = ...) -> None: ...

class ServerKeyRestrictions(_message.Message):
    __slots__ = ("allowed_ips",)
    ALLOWED_IPS_FIELD_NUMBER: _ClassVar[int]
    allowed_ips: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, allowed_ips: _Optional[_Iterable[str]] = ...) -> None: ...

class AndroidKeyRestrictions(_message.Message):
    __slots__ = ("allowed_applications",)
    ALLOWED_APPLICATIONS_FIELD_NUMBER: _ClassVar[int]
    allowed_applications: _containers.RepeatedCompositeFieldContainer[AndroidApplication]
    def __init__(self, allowed_applications: _Optional[_Iterable[_Union[AndroidApplication, _Mapping]]] = ...) -> None: ...

class AndroidApplication(_message.Message):
    __slots__ = ("sha1_fingerprint", "package_name")
    SHA1_FINGERPRINT_FIELD_NUMBER: _ClassVar[int]
    PACKAGE_NAME_FIELD_NUMBER: _ClassVar[int]
    sha1_fingerprint: str
    package_name: str
    def __init__(self, sha1_fingerprint: _Optional[str] = ..., package_name: _Optional[str] = ...) -> None: ...

class IosKeyRestrictions(_message.Message):
    __slots__ = ("allowed_bundle_ids",)
    ALLOWED_BUNDLE_IDS_FIELD_NUMBER: _ClassVar[int]
    allowed_bundle_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, allowed_bundle_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class ApiTarget(_message.Message):
    __slots__ = ("service", "methods")
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    METHODS_FIELD_NUMBER: _ClassVar[int]
    service: str
    methods: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, service: _Optional[str] = ..., methods: _Optional[_Iterable[str]] = ...) -> None: ...
