#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "0.0.2"
__short_description__ = "All in one data compression library."
__license__ = "MIT"
__author__ = "Sanhe Hu"
__author_email__ = "husanhe@gmail.com"
__maintainer__ = "Sanhe Hu"
__maintainer_email__ = "husanhe@gmail.com"
__github_username__ = "MacHu-GWU"

try:
    from .compressor import Compressor, CompressAlgorithms
    from .string_encoding import Encoder, EncodingAlgorithms
except ImportError:  # pragma: no cover
    pass
