from google.rpc import status_pb2 as _status_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CheckError(_message.Message):
    __slots__ = ("code", "subject", "detail", "status")
    class Code(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ERROR_CODE_UNSPECIFIED: _ClassVar[CheckError.Code]
        NOT_FOUND: _ClassVar[CheckError.Code]
        PERMISSION_DENIED: _ClassVar[CheckError.Code]
        RESOURCE_EXHAUSTED: _ClassVar[CheckError.Code]
        SERVICE_NOT_ACTIVATED: _ClassVar[CheckError.Code]
        BILLING_DISABLED: _ClassVar[CheckError.Code]
        PROJECT_DELETED: _ClassVar[CheckError.Code]
        PROJECT_INVALID: _ClassVar[CheckError.Code]
        CONSUMER_INVALID: _ClassVar[CheckError.Code]
        IP_ADDRESS_BLOCKED: _ClassVar[CheckError.Code]
        REFERER_BLOCKED: _ClassVar[CheckError.Code]
        CLIENT_APP_BLOCKED: _ClassVar[CheckError.Code]
        API_TARGET_BLOCKED: _ClassVar[CheckError.Code]
        API_KEY_INVALID: _ClassVar[CheckError.Code]
        API_KEY_EXPIRED: _ClassVar[CheckError.Code]
        API_KEY_NOT_FOUND: _ClassVar[CheckError.Code]
        INVALID_CREDENTIAL: _ClassVar[CheckError.Code]
        NAMESPACE_LOOKUP_UNAVAILABLE: _ClassVar[CheckError.Code]
        SERVICE_STATUS_UNAVAILABLE: _ClassVar[CheckError.Code]
        BILLING_STATUS_UNAVAILABLE: _ClassVar[CheckError.Code]
        CLOUD_RESOURCE_MANAGER_BACKEND_UNAVAILABLE: _ClassVar[CheckError.Code]
    ERROR_CODE_UNSPECIFIED: CheckError.Code
    NOT_FOUND: CheckError.Code
    PERMISSION_DENIED: CheckError.Code
    RESOURCE_EXHAUSTED: CheckError.Code
    SERVICE_NOT_ACTIVATED: CheckError.Code
    BILLING_DISABLED: CheckError.Code
    PROJECT_DELETED: CheckError.Code
    PROJECT_INVALID: CheckError.Code
    CONSUMER_INVALID: CheckError.Code
    IP_ADDRESS_BLOCKED: CheckError.Code
    REFERER_BLOCKED: CheckError.Code
    CLIENT_APP_BLOCKED: CheckError.Code
    API_TARGET_BLOCKED: CheckError.Code
    API_KEY_INVALID: CheckError.Code
    API_KEY_EXPIRED: CheckError.Code
    API_KEY_NOT_FOUND: CheckError.Code
    INVALID_CREDENTIAL: CheckError.Code
    NAMESPACE_LOOKUP_UNAVAILABLE: CheckError.Code
    SERVICE_STATUS_UNAVAILABLE: CheckError.Code
    BILLING_STATUS_UNAVAILABLE: CheckError.Code
    CLOUD_RESOURCE_MANAGER_BACKEND_UNAVAILABLE: CheckError.Code
    CODE_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    DETAIL_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    code: CheckError.Code
    subject: str
    detail: str
    status: _status_pb2.Status
    def __init__(self, code: _Optional[_Union[CheckError.Code, str]] = ..., subject: _Optional[str] = ..., detail: _Optional[str] = ..., status: _Optional[_Union[_status_pb2.Status, _Mapping]] = ...) -> None: ...
