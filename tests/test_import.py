# -*- coding: utf-8 -*-

import pytest


def test():
    import compress

    _ = compress.Algorithm
    _ = compress.Compressor
    _ = compress.compress_bytes_to_bytes
    _ = compress.compress_str_to_bytes
    _ = compress.compress_bytes_to_b64str
    _ = compress.compress_str_to_b64str
    _ = compress.decompress_bytes_to_bytes
    _ = compress.decompress_bytes_to_str
    _ = compress.decompress_b64str_to_bytes
    _ = compress.decompress_b64str_to_str
    _ = compress.Encoder
    _ = compress.EncodingAlgorithms
    pass


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
