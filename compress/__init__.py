# -*- coding: utf-8 -*-

"""
Package Description.
"""


from ._version import __version__

__short_description__ = "All in one data compression library."
__license__ = "MIT"
__author__ = "Sanhe Hu"
__author_email__ = "husanhe@gmail.com"
__github_username__ = "MacHu-GWU"

try:
    from .compressor import (
        Algorithm, Compressor,
        compress_bytes_to_bytes, compress_str_to_bytes,
        compress_bytes_to_b64str, compress_str_to_b64str,
        decompress_bytes_to_bytes, decompress_bytes_to_str,
        decompress_b64str_to_bytes, decompress_b64str_to_str,
    )
    from .string_encoding import Encoder, EncodingAlgorithms
except:  # pragma: no cover
    pass