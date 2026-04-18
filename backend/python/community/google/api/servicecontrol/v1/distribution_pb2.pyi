from google.api import distribution_pb2 as _distribution_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Distribution(_message.Message):
    __slots__ = ("count", "mean", "minimum", "maximum", "sum_of_squared_deviation", "bucket_counts", "linear_buckets", "exponential_buckets", "explicit_buckets", "exemplars")
    class LinearBuckets(_message.Message):
        __slots__ = ("num_finite_buckets", "width", "offset")
        NUM_FINITE_BUCKETS_FIELD_NUMBER: _ClassVar[int]
        WIDTH_FIELD_NUMBER: _ClassVar[int]
        OFFSET_FIELD_NUMBER: _ClassVar[int]
        num_finite_buckets: int
        width: float
        offset: float
        def __init__(self, num_finite_buckets: _Optional[int] = ..., width: _Optional[float] = ..., offset: _Optional[float] = ...) -> None: ...
    class ExponentialBuckets(_message.Message):
        __slots__ = ("num_finite_buckets", "growth_factor", "scale")
        NUM_FINITE_BUCKETS_FIELD_NUMBER: _ClassVar[int]
        GROWTH_FACTOR_FIELD_NUMBER: _ClassVar[int]
        SCALE_FIELD_NUMBER: _ClassVar[int]
        num_finite_buckets: int
        growth_factor: float
        scale: float
        def __init__(self, num_finite_buckets: _Optional[int] = ..., growth_factor: _Optional[float] = ..., scale: _Optional[float] = ...) -> None: ...
    class ExplicitBuckets(_message.Message):
        __slots__ = ("bounds",)
        BOUNDS_FIELD_NUMBER: _ClassVar[int]
        bounds: _containers.RepeatedScalarFieldContainer[float]
        def __init__(self, bounds: _Optional[_Iterable[float]] = ...) -> None: ...
    COUNT_FIELD_NUMBER: _ClassVar[int]
    MEAN_FIELD_NUMBER: _ClassVar[int]
    MINIMUM_FIELD_NUMBER: _ClassVar[int]
    MAXIMUM_FIELD_NUMBER: _ClassVar[int]
    SUM_OF_SQUARED_DEVIATION_FIELD_NUMBER: _ClassVar[int]
    BUCKET_COUNTS_FIELD_NUMBER: _ClassVar[int]
    LINEAR_BUCKETS_FIELD_NUMBER: _ClassVar[int]
    EXPONENTIAL_BUCKETS_FIELD_NUMBER: _ClassVar[int]
    EXPLICIT_BUCKETS_FIELD_NUMBER: _ClassVar[int]
    EXEMPLARS_FIELD_NUMBER: _ClassVar[int]
    count: int
    mean: float
    minimum: float
    maximum: float
    sum_of_squared_deviation: float
    bucket_counts: _containers.RepeatedScalarFieldContainer[int]
    linear_buckets: Distribution.LinearBuckets
    exponential_buckets: Distribution.ExponentialBuckets
    explicit_buckets: Distribution.ExplicitBuckets
    exemplars: _containers.RepeatedCompositeFieldContainer[_distribution_pb2.Distribution.Exemplar]
    def __init__(self, count: _Optional[int] = ..., mean: _Optional[float] = ..., minimum: _Optional[float] = ..., maximum: _Optional[float] = ..., sum_of_squared_deviation: _Optional[float] = ..., bucket_counts: _Optional[_Iterable[int]] = ..., linear_buckets: _Optional[_Union[Distribution.LinearBuckets, _Mapping]] = ..., exponential_buckets: _Optional[_Union[Distribution.ExponentialBuckets, _Mapping]] = ..., explicit_buckets: _Optional[_Union[Distribution.ExplicitBuckets, _Mapping]] = ..., exemplars: _Optional[_Iterable[_Union[_distribution_pb2.Distribution.Exemplar, _Mapping]]] = ...) -> None: ...
