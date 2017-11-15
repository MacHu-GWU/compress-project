#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
string encoding is a technique to convert arbitrary binary data to string
based encoding binary, which is easily to represent string.
"""

import sys
import inspect
import base64
import binascii
import warnings

if sys.version_info.major >= 3 and sys.version_info.minor >= 4:  # pragma: no cover
    flag_base85 = True
else:  # pragma: no cover
    flag_base85 = False

try:
    from . import sixmini
except:  # pragma: no cover
    from compress import sixmini

_example_data = ("Hello World" * 1000).encode("utf-8")


class EncodingAlgorithm(object):
    """
    Base encoding algorithm class.
    """
    name = None

    @classmethod
    def validate_implement(cls):
        encoded_data = cls.encode(_example_data)
        decoded_data = cls.decode(encoded_data)
        assert _example_data == decoded_data

    @staticmethod
    def encode(data, **kwargs):  # pragma: no cover
        raise NotImplementedError

    @staticmethod
    def decode(data, **kwargs):  # pragma: no cover
        raise NotImplementedError


class EncodingAlgorithmsMeta(type):
    def __new__(cls, name, bases, attrs):
        klass = super(EncodingAlgorithmsMeta, cls) \
            .__new__(cls, name, bases, attrs)

        _mapper = dict()
        _algorithm_list = list()
        _algorithm_class_list = list()

        for key, value in attrs.items():
            if inspect.isclass(value):
                if issubclass(value, EncodingAlgorithm):
                    algo_name = key
                    algo_class = value

                    try:
                        algo_class.validate_implement()
                    except:  # pragma: no cover
                        continue

                    algo_class.name = algo_class.__name__
                    _mapper[key] = {
                        "_encode": algo_class.encode,
                        "_decode": algo_class.decode,
                    }
                    _algorithm_list.append(algo_name)
                    _algorithm_class_list.append(algo_class)
                _algorithm_list.sort()

        klass._mapper = _mapper
        klass._algorithm_list = _algorithm_list
        klass._algorithm_set = set(_algorithm_list)
        klass._algorithm_class_list = _algorithm_class_list
        return klass


@sixmini.add_metaclass(EncodingAlgorithmsMeta)
class EncodingAlgorithms(object):
    """
    Collection of string encoding algorithms.

    Example::

        EncodingAlgorithms.Base64

    `Comparison of encoding schemes
 <http://www.tenminutetutor.com/data-formats/binary-encoding/comparison-of-encoding-schemes/>`_
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

    class HexString(EncodingAlgorithm):
        """
        Data increase 100%.

        Doc: https://docs.python.org/2/library/binascii.html#binascii.hexlify
        """

        @staticmethod
        def encode(data, **kwargs):
            return binascii.hexlify(data)

        @staticmethod
        def decode(data, **kwargs):
            return binascii.unhexlify(data)

    class Base32(EncodingAlgorithm):
        """
        Data increase 60%.
        """

        @staticmethod
        def encode(data, **kwargs):
            return base64.b32encode(data)

        @staticmethod
        def decode(data, **kwargs):
            return base64.b32decode(data)

    class Base64(EncodingAlgorithm):
        """
        Data increase 33%.
        """

        @staticmethod
        def encode(data, **kwargs):
            return base64.b64encode(data)

        @staticmethod
        def decode(data, **kwargs):
            return base64.b64decode(data)

    class Base85(EncodingAlgorithm):  # pragma: no cover
        """
        Data increase 20%.
        """

        @staticmethod
        def encode(data, **kwargs):
            return base64.b85encode(data)

        @staticmethod
        def decode(data, **kwargs):
            return base64.b85decode(data)


class Encoder(object):
    """
    String encoder utility class.

    Example::

        >>> encoder = Encoder().use_base64()
        >>> encoder.encode(binary_data)
        ...
        >>> encoder.decode(binary_data)
        ...
    """

    def __init__(self,
                 algorithm=None,
                 **kwargs):
        self.use(algorithm)

    def use(self, algo=None):
        """
        Use specified string encoding algorithm.

        :param algo: str or :class:`EncodingAlgorithm`.
        """
        if algo is None:
            return self

        try:
            algo_name = algo.__name__  # if it is a class
        except AttributeError:
            algo_name = algo  # if it is a string

        if algo_name in EncodingAlgorithms._algorithm_set:
            self._encode = EncodingAlgorithms._mapper[algo_name]["_encode"]
            self._decode = EncodingAlgorithms._mapper[algo_name]["_decode"]
            return self
        else:
            raise ValueError(
                "algorithm has to be one of "
                "%r" % EncodingAlgorithms._algorithm_list
            )

    def use_hex(self):
        """
        Use hex string algorithm.
        """
        return self.use(EncodingAlgorithms.HexString)

    def use_base32(self):
        """
        Use base32 algorithm.
        """
        return self.use(EncodingAlgorithms.Base32)

    def use_base64(self):
        """
        Use base64 algorithm.
        """
        return self.use(EncodingAlgorithms.Base64)

    def use_base85(self):  # pragma: no cover
        """
        Use base85 algorithm.
        """
        if flag_base85:
            return self.use(EncodingAlgorithms.Base85)
        else:
            warnings.warn("base85 is NOT available until Python3.4!")

    def _encode(self, data, **kwargs):
        """
        The real encode method will be called.
        """
        raise NotImplementedError

    def _decode(self, data, **kwargs):
        """
        The real decode method will be called.
        """
        raise NotImplementedError

    def encode(self, data, **kwargs):
        """
        Encode binary data to string based binary binary.

        :return: string encoded binary data.
        """
        return self._encode(data, **kwargs)

    def decode(self, data, **kwargs):
        """
        Decode string encoded binary data.

        :return: original binary data.
        """
        return self._decode(data, **kwargs)
