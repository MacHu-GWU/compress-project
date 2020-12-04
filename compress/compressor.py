# -*- coding: utf-8 -*-

import typing
import base64
import bz2
import gzip
import lzma
from enum import Enum

try:
    import snappy
except:  # pragma: no cover
    pass

try:
    import lz4.frame, lz4.block, lz4.stream
except:  # pragma: no cover
    pass


def gzip_compress(data: bytes, compresslevel=9) -> bytes:
    return gzip.compress(data, compresslevel=compresslevel)


def gzip_decompress(data: bytes) -> bytes:
    return gzip.decompress(data)


def bz2_compress(data: bytes, compresslevel=9) -> bytes:
    return bz2.compress(data, compresslevel=compresslevel)


def bz2_decompress(data: bytes) -> bytes:
    return bz2.decompress(data)


def lzma_compress(data: bytes, mode="") -> bytes:
    return lzma.compress(data)


def lzma_decompress(data: bytes) -> bytes:
    return lzma.decompress(data)


def snappy_compress(data: bytes) -> bytes:
    return snappy.compress(data)


def snappy_decompress(data: bytes) -> bytes:
    return snappy.decompress(data)


def lz4_compress(data: bytes, mode: str="default") -> bytes:
    return lz4.block.compress(data, mode=mode)


def lz4_decompress(data: bytes) -> bytes:
    return lz4.block.decompress(data)


class Algorithm(Enum):
    gzip = "gzip"
    bz2 = "bz2"
    lzma = "lzma"
    snappy = "snappy"
    lz4 = "lz4"


_compress_algo_mapper = {
    Algorithm.gzip: gzip_compress,
    Algorithm.bz2: bz2_compress,
    Algorithm.lzma: lzma_compress,
    Algorithm.snappy: snappy_compress,
    Algorithm.lz4: lz4_compress,
}

_decompress_algo_mapper = {
    Algorithm.gzip: gzip_decompress,
    Algorithm.bz2: bz2_decompress,
    Algorithm.lzma: lzma_decompress,
    Algorithm.snappy: snappy_decompress,
    Algorithm.lz4: lz4_decompress,
}


def compress_bytes_to_bytes(algo: Algorithm, data: bytes, **kwargs):
    return _compress_algo_mapper[algo](data, **kwargs)


def compress_str_to_bytes(algo: Algorithm, data: str, **kwargs):
    return _compress_algo_mapper[algo](data=data.encode("utf-8"), **kwargs)


def compress_bytes_to_b64str(algo: Algorithm, data: bytes, **kwargs):
    return base64.b64encode(_compress_algo_mapper[algo](data=data, **kwargs)) \
        .decode("utf-8")


def compress_str_to_b64str(algo: Algorithm, data: str, **kwargs):
    return base64.b64encode(_compress_algo_mapper[algo](
        data=data.encode("utf-8"), **kwargs
    )).decode("utf-8")


def decompress_bytes_to_bytes(algo: Algorithm, data: bytes, **kwargs):
    return _decompress_algo_mapper[algo](data, **kwargs)


def decompress_bytes_to_str(algo: Algorithm, data: bytes, **kwargs):
    return _decompress_algo_mapper[algo](data=data, **kwargs).decode("utf-8")


def decompress_b64str_to_bytes(algo: Algorithm, data: str, **kwargs):
    return _decompress_algo_mapper[algo](
        data=base64.b64decode(data.encode("utf-8")), **kwargs
    )


def decompress_b64str_to_str(algo: Algorithm, data: str, **kwargs):
    return _decompress_algo_mapper[algo](
        data=base64.b64decode(data.encode("utf-8")), **kwargs
    ).decode("utf-8")


class Compressor:
    """
    Neat api for Lazy people.

    Example::

        >>> binary_data = ("hello world" * 100).encode("utf-8")
        >>> compressor = Compressor()
        >>> compressed_binary_data = compressor.compress(binary_data)
        ...
        >>> compressor.decompress(compressed_binary_data)
        ...
    """

    def __init__(self, algorithm: Algorithm = Algorithm.gzip):
        self.algo = None  # type: Algorithm
        self.use(algorithm)

    def use(self, algo: Algorithm):
        """
        Use specified compression algorithm.
        """
        self.algo = algo

    def use_gzip(self):
        return self.use(Algorithm.gzip)

    def use_bz2(self):
        return self.use(Algorithm.bz2)

    def use_lzma(self):
        return self.use(Algorithm.lzma)

    def use_snappy(self):
        return self.use(Algorithm.snappy)

    def use_lz4(self):
        return self.use(Algorithm.lz4)

    def compress(self, data: typing.Union[str, bytes], **kwargs) -> bytes:
        """
        Compress binary data, returns binary data
        """
        if isinstance(data, bytes):
            return compress_bytes_to_bytes(algo=self.algo, data=data, **kwargs)
        else:
            return compress_str_to_bytes(algo=self.algo, data=data, **kwargs)

    def decompress(self, data: bytes, **kwargs) -> bytes:
        """
        Decompress binary data, returns binary data
        """
        return decompress_bytes_to_bytes(algo=self.algo, data=data, **kwargs)
