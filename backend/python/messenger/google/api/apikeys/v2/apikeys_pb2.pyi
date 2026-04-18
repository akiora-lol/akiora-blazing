from google.api import annotations_pb2 as _annotations_pb2
from google.api.apikeys.v2 import resources_pb2 as _resources_pb2
from google.api import client_pb2 as _client_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.api import resource_pb2 as _resource_pb2
from google.longrunning import operations_pb2 as _operations_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateKeyRequest(_message.Message):
    __slots__ = ("parent", "key", "key_id")
    PARENT_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    KEY_ID_FIELD_NUMBER: _ClassVar[int]
    parent: str
    key: _resources_pb2.Key
    key_id: str
    def __init__(self, parent: _Optional[str] = ..., key: _Optional[_Union[_resources_pb2.Key, _Mapping]] = ..., key_id: _Optional[str] = ...) -> None: ...

class ListKeysRequest(_message.Message):
    __slots__ = ("parent", "page_size", "page_token", "show_deleted")
    PARENT_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    SHOW_DELETED_FIELD_NUMBER: _ClassVar[int]
    parent: str
    page_size: int
    page_token: str
    show_deleted: bool
    def __init__(self, parent: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ..., show_deleted: bool = ...) -> None: ...

class ListKeysResponse(_message.Message):
    __slots__ = ("keys", "next_page_token")
    KEYS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    keys: _containers.RepeatedCompositeFieldContainer[_resources_pb2.Key]
    next_page_token: str
    def __init__(self, keys: _Optional[_Iterable[_Union[_resources_pb2.Key, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class GetKeyRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class GetKeyStringRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class GetKeyStringResponse(_message.Message):
    __slots__ = ("key_string",)
    KEY_STRING_FIELD_NUMBER: _ClassVar[int]
    key_string: str
    def __init__(self, key_string: _Optional[str] = ...) -> None: ...

class UpdateKeyRequest(_message.Message):
    __slots__ = ("key", "update_mask")
    KEY_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    key: _resources_pb2.Key
    update_mask: _field_mask_pb2.FieldMask
    def __init__(self, key: _Optional[_Union[_resources_pb2.Key, _Mapping]] = ..., update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...) -> None: ...

class DeleteKeyRequest(_message.Message):
    __slots__ = ("name", "etag")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ETAG_FIELD_NUMBER: _ClassVar[int]
    name: str
    etag: str
    def __init__(self, name: _Optional[str] = ..., etag: _Optional[str] = ...) -> None: ...

class UndeleteKeyRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class LookupKeyRequest(_message.Message):
    __slots__ = ("key_string",)
    KEY_STRING_FIELD_NUMBER: _ClassVar[int]
    key_string: str
    def __init__(self, key_string: _Optional[str] = ...) -> None: ...

class LookupKeyResponse(_message.Message):
    __slots__ = ("parent", "name")
    PARENT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    parent: str
    name: str
    def __init__(self, parent: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...
