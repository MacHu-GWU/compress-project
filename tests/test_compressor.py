#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from compress.compressor import (
    Algorithm,
    compress_bytes_to_bytes, compress_str_to_bytes,
    compress_bytes_to_b64str, compress_str_to_b64str,
    decompress_bytes_to_bytes, decompress_bytes_to_str,
    decompress_b64str_to_bytes, decompress_b64str_to_str,
    Compressor,
)

TEST_CASE_DATA_STR = "hello world! " * 100
TEST_CASE_DATA_BYTES = TEST_CASE_DATA_STR.encode("utf-8")


class TestLowLevelAPI:
    def test(self):
        for algo in Algorithm:
            res = compress_bytes_to_bytes(algo, TEST_CASE_DATA_BYTES)
            assert decompress_bytes_to_bytes(algo, res) == TEST_CASE_DATA_BYTES

            res = compress_str_to_bytes(algo, TEST_CASE_DATA_STR)
            assert decompress_bytes_to_str(algo, res) == TEST_CASE_DATA_STR

            res = compress_bytes_to_b64str(algo, TEST_CASE_DATA_BYTES)
            assert decompress_b64str_to_bytes(algo, res) == TEST_CASE_DATA_BYTES

            res = compress_str_to_b64str(algo, TEST_CASE_DATA_STR)
            assert decompress_b64str_to_str(algo, res) == TEST_CASE_DATA_STR


class TestCompressor:
    def test(self):
        compressor = Compressor()

        for algo in Algorithm:
            getattr(compressor, f"use_{algo.value}")()
            res = compressor.compress(TEST_CASE_DATA_BYTES)
            assert compressor.decompress(res) == TEST_CASE_DATA_BYTES
            assert len(TEST_CASE_DATA_BYTES) > len(res)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
