from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STATUS_UNSPECIFIED: _ClassVar[Status]
    SCHEDULED: _ClassVar[Status]
    ACTIVE: _ClassVar[Status]
    FINISHED: _ClassVar[Status]
    CANCELLED: _ClassVar[Status]
STATUS_UNSPECIFIED: Status
SCHEDULED: Status
ACTIVE: Status
FINISHED: Status
CANCELLED: Status

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
