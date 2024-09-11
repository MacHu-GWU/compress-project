# -*- coding: utf-8 -*-

import typing as T
import bz2
import gzip
from .vendor.better_enum import BetterStrEnum

try:
    import lzma

    has_lzma = True
except ImportError:  # pragma: no cover
    has_lzma = False

try:
    import snappy

    has_snappy = True
except ImportError:  # pragma: no cover
    has_snappy = False

try:
    import lz4.block

    has_lz4 = True
except ImportError:  # pragma: no cover
    has_lz4 = False

try:
    import pyzstd

    has_pyzstd = True
except ImportError:  # pragma: no cover
    has_pyzstd = False


class Algorithm(BetterStrEnum):
    uncompressed = "uncompressed"
    gzip = "gzip"
    bz2 = "bz2"
    snappy = "snappy"
    lzma = "lzma"
    lz4 = "lz4"
    zstd = "zstd"


T_KWARGS = T.Dict[str, T.Any]


def no_compress(data: bytes, kwargs: T_KWARGS) -> bytes:
    return data


def no_decompress(data: bytes, kwargs: T_KWARGS) -> bytes:
    return data


def gzip_compress(data: bytes, kwargs: T_KWARGS) -> bytes:
    return gzip.compress(data, **kwargs)


def gzip_decompress(data: bytes, kwargs: T_KWARGS) -> bytes:
    return gzip.decompress(data)


def bz2_compress(data: bytes, kwargs: T_KWARGS) -> bytes:
    return bz2.compress(data, **kwargs)


def bz2_decompress(data: bytes, kwargs: T_KWARGS) -> bytes:
    return bz2.decompress(data)


def lzma_compress(data: bytes, kwargs: T_KWARGS) -> bytes:
    return lzma.compress(data, **kwargs)


def lzma_decompress(data: bytes, kwargs: T_KWARGS) -> bytes:
    return lzma.decompress(data, **kwargs)


def snappy_compress(data: bytes, kwargs: T_KWARGS) -> bytes:
    return snappy.compress(data, **kwargs)


def snappy_decompress(data: bytes, kwargs: T_KWARGS) -> bytes:
    return snappy.decompress(data, **kwargs)


def lz4_compress(data: bytes, kwargs: T_KWARGS) -> bytes:
    return lz4.block.compress(data, **kwargs)


def lz4_decompress(data: bytes, kwargs: T_KWARGS) -> bytes:
    return lz4.block.decompress(data, **kwargs)


def zstd_compress(data: bytes, kwargs: T_KWARGS) -> bytes:
    return pyzstd.compress(data, **kwargs)


def zstd_decompress(data: bytes, kwargs: T_KWARGS) -> bytes:
    return pyzstd.decompress(data, **kwargs)


_compress_algo_mapper = {
    Algorithm.uncompressed.value: no_compress,
    Algorithm.gzip.value: gzip_compress,
    Algorithm.bz2.value: bz2_compress,
    Algorithm.lzma.value: lzma_compress,
    Algorithm.snappy.value: snappy_compress,
    Algorithm.lz4.value: lz4_compress,
    Algorithm.zstd.value: zstd_compress,
}

_decompress_algo_mapper = {
    Algorithm.uncompressed.value: no_decompress,
    Algorithm.gzip.value: gzip_decompress,
    Algorithm.bz2.value: bz2_decompress,
    Algorithm.lzma.value: lzma_decompress,
    Algorithm.snappy.value: snappy_decompress,
    Algorithm.lz4.value: lz4_decompress,
    Algorithm.zstd.value: zstd_decompress,
}


def compress(
    algo: T.Union[Algorithm, str],
    data: bytes,
    kwargs: T.Optional[T_KWARGS] = None,
) -> bytes:
    algo = Algorithm.ensure_str(algo)
    if kwargs is None:
        kwargs = {}
    method = _compress_algo_mapper[algo]
    return method(data, kwargs)


def decompress(
    algo: T.Union[Algorithm, str],
    data: bytes,
    kwargs: T.Optional[T_KWARGS] = None,
):
    algo = Algorithm.ensure_str(algo)
    if kwargs is None:
        kwargs = {}
    method = _decompress_algo_mapper[algo]
    return method(data, kwargs)
