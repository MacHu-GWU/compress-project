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
    from .compressor import Compressor, CompressAlgorithms
    from .string_encoding import Encoder, EncodingAlgorithms
except:  # pragma: no cover
    pass