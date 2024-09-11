# -*- coding: utf-8 -*-

import typing as T

from compress.impl import (
    Algorithm,
    compress,
    decompress,
    T_KWARGS,
)

TEST_CASE_DATA_STR = "hello world! " * 100
TEST_CASE_DATA_BYTES = TEST_CASE_DATA_STR.encode("utf-8")


def run_case(
    b: bytes,
    algo: Algorithm,
    compress_kwargs: T.Optional[T_KWARGS] = None,
    uncompress_kwargs: T.Optional[T_KWARGS] = None,
):
    b_compressed = compress(algo=algo, data=b, kwargs=compress_kwargs)
    b_uncompressed = decompress(algo=algo, data=b_compressed, kwargs=uncompress_kwargs)
    assert b == b_uncompressed


cases = [
    (TEST_CASE_DATA_BYTES, Algorithm.uncompressed, None, None),
    (TEST_CASE_DATA_BYTES, Algorithm.gzip.value, None, None),
    (TEST_CASE_DATA_BYTES, Algorithm.bz2.value, None, None),
    (TEST_CASE_DATA_BYTES, Algorithm.lzma.value, None, None),
    (TEST_CASE_DATA_BYTES, Algorithm.snappy, None, None),
    (TEST_CASE_DATA_BYTES, Algorithm.lz4, None, None),
    (TEST_CASE_DATA_BYTES, Algorithm.zstd, None, None),
]


def test():
    for case in cases:
        run_case(*case)


if __name__ == "__main__":
    from compress.tests import run_cov_test

    run_cov_test(__file__, "compress.impl", preview=False)
