# -*- coding: utf-8 -*-

"""
Improve the original enum module.
"""

import typing as T
import enum

__version__ = "0.1.1"

class Mixin:
    @classmethod
    def get_by_name(cls, name: str):
        """
        Get the enum member (an enum object) by name.
        """
        return cls[name]

    @classmethod
    def is_valid_name(cls, name: str) -> bool:
        """
        Return a boolean to indicate if the name is valid.
        """
        try:
            _ = cls[name]
            return True
        except KeyError:
            return False

    @classmethod
    def get_names(cls) -> T.List[str]:
        """
        Return a list of names.
        """
        return [i.name for i in cls]


class BetterIntEnum(Mixin, int, enum.Enum):
    """
    Example:

    .. code-block:: python

        >>> class CodeEnum(BetterIntEnum):
        ...     succeeded = 1
        ...     failed = 0
        >>> CodeEnum.get_by_name("succeeded")
        <CodeEnum.succeeded: 1>
        >>> CodeEnum.get_by_value(1)
        <CodeEnum.succeeded: 1>
        >>> CodeEnum.is_valid_name("succeeded")
        True
        >>> CodeEnum.is_valid_name("SUCCEEDED")
        False
        >>> CodeEnum.is_valid_name(1)
        False
        >>> CodeEnum.is_valid_value("succeeded")
        False
        >>> CodeEnum.is_valid_value("SUCCEEDED")
        False
        >>> CodeEnum.is_valid_value(1)
        True
        >>> CodeEnum.ensure_is_valid_value(1)
        >>> CodeEnum.ensure_is_valid_value("succeeded")
        Traceback (most recent call last):
        ...
        ValueError: Invalid CodeEnum: 'succeeded'
        >>> CodeEnum.ensure_int(1)
        1
        >>> CodeEnum.ensure_int(CodeEnum.succeeded)
        1
        >>> isinstance(CodeEnum.ensure_int(1), int)
        True
    """

    @classmethod
    def get_by_value(cls, value: int):
        """
        Get the enum member (an enum object) by value.
        """
        return cls(value)

    @classmethod
    def is_valid_value(cls, value: int) -> bool:
        """
        Return a boolean to indicate if the value is valid.
        """
        try:
            _ = cls(value)
            return True
        except ValueError:
            return False

    @classmethod
    def ensure_is_valid_value(cls, value):
        """
        Ensure the value is valid. Raise ValueError if not.
        """
        if cls.is_valid_value(value) is False:
            raise ValueError(f"Invalid {cls.__name__}: {value!r}")

    @classmethod
    def ensure_int(cls, value: T.Union[int, "BetterIntEnum"]) -> int:
        """
        Ensure the value is an integer. If it is an enum object, return its value.
        """
        if isinstance(value, cls):
            return value.value
        else:
            return cls(value).value

    @classmethod
    def get_values(cls) -> T.List[int]:
        """
        Return a list of values.
        """
        return [i.value for i in cls]


class BetterStrEnum(Mixin, str, enum.Enum):
    """
    Example:

    .. code-block:: python

        >>> class StatusEnum(BetterStrEnum):
        ...     succeeded = "SUCCEEDED"
        ...     failed = "FAILED"
        >>> StatusEnum.get_by_name("succeeded")
        <StatusEnum.succeeded: 'SUCCEEDED'>
        >>> StatusEnum.get_by_value("SUCCEEDED")
        <StatusEnum.succeeded: 'SUCCEEDED'>
        >>> StatusEnum.is_valid_name("succeeded")
        True
        >>> StatusEnum.is_valid_name("SUCCEEDED")
        False
        >>> StatusEnum.is_valid_value("succeeded")
        False
        >>> StatusEnum.is_valid_value("SUCCEEDED")
        True
        >>> StatusEnum.ensure_is_valid_value("SUCCEEDED")
        >>> StatusEnum.ensure_is_valid_value("succeeded")
        Traceback (most recent call last):
        ...
        ValueError: Invalid StatusEnum: 'succeeded'
        >>> StatusEnum.ensure_str("SUCCEEDED")
        'SUCCEEDED'
        >>> StatusEnum.ensure_str(StatusEnum.succeeded)
        'SUCCEEDED'
        >>> isinstance(StatusEnum.ensure_str("SUCCEEDED"), str)
        True
    """

    @classmethod
    def get_by_value(cls, value: str):
        """
        Get the enum member (an enum object) by value.
        """
        return cls(value)

    @classmethod
    def is_valid_value(cls, value: str) -> bool:
        """
        Return a boolean to indicate if the value is valid.
        """
        try:
            _ = cls(value)
            return True
        except ValueError:
            return False

    @classmethod
    def ensure_is_valid_value(cls, value):
        """
        Ensure the value is valid. Raise ValueError if not.
        """
        if cls.is_valid_value(value) is False:
            raise ValueError(f"Invalid {cls.__name__}: {value!r}")

    @classmethod
    def ensure_str(cls, value: T.Union[str, "BetterStrEnum"]) -> str:
        """
        Ensure the value is a string. If it is an enum object, return its value.
        """
        if isinstance(value, cls):
            return value.value
        else:
            return cls(value).value

    @classmethod
    def get_values(cls) -> T.List[str]:
        """
        Return a list of values.
        """
        return [i.value for i in cls]