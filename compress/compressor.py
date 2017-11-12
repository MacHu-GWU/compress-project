#!/usr/bin/env python
# -*- coding: utf-8 -*-

import inspect

import zlib

import bz2

try:
    import lzma
except ImportError:  # pragma: no cover
    from backports import lzma
except:  # pragma: no cover
    pass

try:
    import pylzma
except:  # pragma: no cover
    pass

try:
    import snappy
except:  # pragma: no cover
    pass

try:
    import lz4.block
except:  # pragma: no cover
    pass

try:
    from . import sixmini
except:  # pragma: no cover
    from compress import sixmini

_example_data = ("Hello World" * 1000).encode("utf-8")


class CompressAlgorithm(object):
    name = None
    all_params = None

    @classmethod
    def validate_implement(cls):
        for com_params, decom_params in cls.all_params:
            compressed_data = cls.compress(_example_data, **com_params)
            decompressed_data = cls.decompress(compressed_data, **decom_params)
            assert _example_data == decompressed_data


class CompressAlgorithmsMeta(type):
    def __new__(cls, name, bases, attrs):
        klass = super(CompressAlgorithmsMeta, cls).__new__(
            cls, name, bases, attrs)

        _mapper = dict()
        _algorithm_list = list()
        _algorithm_class_list = list()
        for key, value in attrs.items():
            if inspect.isclass(value):
                if issubclass(value, CompressAlgorithm):
                    algo_name = key
                    algo_class = value
                    algo_class.validate_implement()
                    algo_class.name = algo_class.__name__
                    _mapper[key] = {
                        "_compress": algo_class.compress,
                        "_decompress": algo_class.decompress,
                    }
                    _algorithm_list.append(algo_name)
                    _algorithm_class_list.append(algo_class)
                _algorithm_list.sort()

        klass._mapper = _mapper
        klass._algorithm_list = _algorithm_list
        klass._algorithm_set = set(_algorithm_list)
        klass._algorithm_class_list = _algorithm_class_list
        return klass


@sixmini.add_metaclass(CompressAlgorithmsMeta)
class CompressAlgorithms(object):
    """
    Collection of string encoding algorithms. API in different API are
    normalized.

    Each algorithm's python implementation is tested, and their performance are
    listed in class doc string. There are five level for speed and compress
    ratio.

    Speed:

    5. very fast
    4. fast
    3. normal
    2. slow
    1. very slow

    Compress Ratio:

    5. very high
    4. high
    3. normal
    2. low
    1. very low

    Reference: `Benchmark for all algorithm <https://quixdb.github.io/squash-benchmark/>`_
    """
    _algorithm_list = list()
    """All available algorithm name list.
    """

    _algorithm_set = set()
    """All available algorithm name set.
    """

    _algorithm_class_list = list()
    """All available algorithm class list.
    """

    class Zlib(CompressAlgorithm):
        """
        Speed: 3

        Ratio: 3

        API:

        - https://docs.python.org/2/library/zlib.html

        or

        - https://docs.python.org/3/library/zlib.html
        """
        all_params = [
            (
                {"zlib_level": zlib_level},
                {},
            ) for zlib_level in range(0, 9 + 1)
        ]

        @staticmethod
        def compress(data, zlib_level, **kwargs):
            return zlib.compress(data, zlib_level)

        @staticmethod
        def decompress(data, **kwargs):
            return zlib.decompress(data)

    class Bz2(CompressAlgorithm):
        """
        Compress Speed: 2

        Decompress Speed: 1

        Compress Ratio: 5

        API:

        - https://docs.python.org/2/library/bz2.html

        or

        - https://docs.python.org/3/library/bz2.html
        """
        all_params = [
            (
                {"bz2_level": bz2_level},
                {},
            ) for bz2_level in range(1, 9 + 1)
        ]

        @staticmethod
        def compress(data, bz2_level, **kwargs):
            return bz2.compress(data, compresslevel=bz2_level)

        @staticmethod
        def decompress(data, **kwargs):
            return bz2.decompress(data)

    class LZMA(CompressAlgorithm):
        """
        Speed: 1

        Compress Ratio: 5

        API:

        - https://docs.python.org/3/library/lzma.html

        or

        - https://pypi.python.org/pypi/backports.lzma
        """
        all_params = [
            ({}, {}),
        ]

        @staticmethod
        def compress(data, **kwargs):
            return lzma.compress(data)

        @staticmethod
        def decompress(data, **kwargs):
            return lzma.decompress(data)

    class PyLZMA(CompressAlgorithm):
        all_params = [
            ({}, {}),
        ]

        @staticmethod
        def compress(data, **kwargs):
            return pylzma.compress(data)

        @staticmethod
        def decompress(data, **kwargs):
            return pylzma.decompress(data)

    class Snappy(CompressAlgorithm):
        """
        Speed: 5

        Compress Ratio: 2

        API:

        - https://pypi.python.org/pypi/python-snappy
        """
        all_params = [
            ({}, {}),
        ]

        @staticmethod
        def compress(data, **kwargs):
            return snappy.compress(data)

        @staticmethod
        def decompress(data, **kwargs):
            return snappy.uncompress(data)

    class Lz4(CompressAlgorithm):
        """
        Speed: 5

        Compress Ratio: 2

        API:

        - https://pypi.python.org/pypi/lz4

        """
        all_params = [
            ({"lz4_mode": "default"}, {}),
            ({"lz4_mode": "fast"}, {}),
            ({"lz4_mode": "high_compression"}, {}),
        ]

        @staticmethod
        def compress(data, lz4_mode, **kwargs):
            return lz4.block.compress(data, mode=lz4_mode)

        @staticmethod
        def decompress(data, **kwargs):
            return lz4.block.decompress(data)


class Compressor(object):
    """
    String encoder utility class.

    Example::

        >>> compressor = Compressor().use_zlib()
        >>> compressor.compress(binary_data)
        ...
        >>> compressor.decompress(binary_data)
        ...
    """

    def __init__(self,
                 algorithm=None,
                 **kwargs):
        self.use(algorithm)

    def use(self, algo=None):
        """
        Use specified compression algorithm.

        :param algo: str or :class:`CompressAlgorithm`
        """
        if algo is None:
            return self

        try:
            algo_name = algo.__name__  # if it is a class
        except:
            algo_name = algo  # if it is a string

        if algo_name in CompressAlgorithms._algorithm_set:
            self._compress = CompressAlgorithms._mapper[algo_name]["_compress"]
            self._decompress = CompressAlgorithms._mapper[algo_name]["_decompress"]
            return self
        else:
            raise ValueError(
                "algorithm has to be one of "
                "%r" % CompressAlgorithms._algorithm_list
            )

    def use_zlib(self):
        """
        Use zlib algorithm.
        """
        return self.use(CompressAlgorithms.Zlib)

    def use_bz2(self):
        """
        Use bz2 algorithm.
        """
        return self.use(CompressAlgorithms.Bz2)

    def use_lzma(self):
        """
        Use lzma algorithm.
        """
        return self.use(CompressAlgorithms.LZMA)

    def use_pylzma(self):
        """
        Use pylzma algorithm.
        """
        return self.use(CompressAlgorithms.PyLZMA)

    def use_snappy(self):
        """
        Use snappy algorithm.
        """
        return self.use(CompressAlgorithms.Snappy)

    def use_lz4(self):
        """
        Use lz4 algorithm.
        """
        return self.use(CompressAlgorithms.Lz4)

    def _compress(self, data, **kwargs):
        raise NotImplementedError

    def _decompress(self, data, **kwargs):
        raise NotImplementedError

    def compress(self,
                 data,
                 zlib_level=6,
                 bz2_level=9,
                 lz4_mode="default",
                 **kwargs):
        """
        Compress binary data.

        :return: binary data.
        """
        kwargs["zlib_level"] = zlib_level
        kwargs["bz2_level"] = bz2_level
        kwargs["lz4_mode"] = lz4_mode
        return self._compress(data, **kwargs)

    def decompress(self, data, **kwargs):
        """
        Decompress binary data.

        :return: binary data.
        """
        return self._decompress(data, **kwargs)
