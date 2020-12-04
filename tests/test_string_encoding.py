# -*- coding: utf-8 -*-

import sys

import pytest
from pytest import raises

from compress.string_encoding import Encoder, EncodingAlgorithms

with open(__file__, "rb") as f:
    data = f.read()


class TestEncoder(object):
    def test_NotImplementError(self):
        encoder = Encoder()
        with raises(NotImplementedError):
            encoder.encode(data)
        with raises(NotImplementedError):
            encoder.decode(data)

    def test_use(self):
        encoder = Encoder()

        encoder.use_hex()
        encoder.use_base32()
        encoder.use_base64()
        encoder.use_base85()

        encoder.use(EncodingAlgorithms.Base64)
        with raises(ValueError):
            encoder.use("Unknown")

    def test_algorithm(self):
        encoder = Encoder()
        for algo in EncodingAlgorithms._algorithm_list:
            encoder.use(algo)
            data_encoded = encoder.encode(data)
            data_decoded = encoder.decode(data_encoded)
            assert sys.getsizeof(data) <= sys.getsizeof(data_encoded)
            assert data == data_decoded


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
