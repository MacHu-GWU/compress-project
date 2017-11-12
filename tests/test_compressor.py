#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pytest import raises
import sys
from compress.compressor import Compressor, CompressAlgorithms

with open(__file__, "rb") as f:
    data = f.read()


class TestCompressor(object):
    def test_NotImplementError(self):
        compressor = Compressor()
        with raises(NotImplementedError):
            compressor.compress(data)
        with raises(NotImplementedError):
            compressor.decompress(data)

    def test_use(self):
        compressor = Compressor()
        compressor.use_bz2()
        compressor.use_zlib()
        compressor.use_lzma()
        compressor.use_pylzma()
        compressor.use_snappy()
        compressor.use_lz4()
        with raises(ValueError):
            compressor.use("Unknown")

    def test_algorithm(self):
        compressor = Compressor()
        for algo in CompressAlgorithms._algorithm_list:
            compressor.use(algo)
            data_compressed = compressor.compress(data)
            data_decompressed = compressor.decompress(data_compressed)
            assert sys.getsizeof(data) >= sys.getsizeof(data_compressed)
            assert data == data_decompressed


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
