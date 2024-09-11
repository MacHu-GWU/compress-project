# -*- coding: utf-8 -*-

"""
Lazy time profiling tools.

**中文文档**

- time.perf_counter() 返回的是 **该进程从运行起** 的 CPU 时钟.
- time.time() 返回的是 从 EPOCH 开始起的秒数, 不同系统上的精确度不同.
- datetime.datetime.utcnow() 返回的是从 EPOCH 开始起的时间对象
"""

import typing as T
import time
from datetime import datetime

__version__ = "0.1.1"

class BaseTimer:
    """
    Abstract timer class.
    """

    _base_log_msg_tpl = "from {start_time} to {end_time} elapsed {elapsed:.6f} second."

    __slots__ = ["title", "start_time", "end_time", "elapsed", "display", "log_msg_tpl"]

    def __init__(self, title: str = None, display: bool = True, start: bool = True):
        self.title = title
        self.start_time = None
        self.end_time = None
        self.elapsed = None
        self.display = display

        if title is not None:
            self.log_msg_tpl = title + ": " + self._base_log_msg_tpl
        else:
            self.log_msg_tpl = self._base_log_msg_tpl

        if start is True:
            self.start()

    def __str__(self):
        return self.log_msg_tpl.format(
            start_time=self.start_time,
            end_time=self.end_time,
            elapsed=self.elapsed,
        )

    def __repr__(self):
        if self.elapsed is not None:
            return "Timer(title=%s, elapsed=%.6f)" % (self.title, self.elapsed)
        else:
            return "Timer(title=%s)" % self.title

    def _get_current_time(self):
        raise NotImplementedError

    def _get_delta_in_sec(self, start, end) -> float:
        raise NotImplementedError

    def start(self):
        self.start_time = self._get_current_time()

    def end(self):
        self.end_time = self._get_current_time()
        self.elapsed = self._get_delta_in_sec(self.start_time, self.end_time)
        if self.display:
            print(self)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.end()


class DateTimeTimer(BaseTimer):
    """
    Usage::

        # usage 1
        >>> timer = DateTimeTimer(title="first measure") # start measuring immediately, title is optional
        >>> # .. do something
        >>> timer.end()

        # usage 2
        >>> with DateTimeTimer(title="second measure") as timer:
        ...     # do something
        >>> timer.end()

        # usage 3
        >>> timer = DateTimeTimer(start=False) # not start immediately
        >>> # do something
        >>> timer.start()
        >>> # do someting
        >>> timer.end()

        # usage 4
        >>> timer = DateTimeTimer(display=False) # disable auto display information

    .. warning::

        DateTimeTimer takes around 0.003 seconds to get the time.
    """

    def _get_current_time(self):
        return datetime.utcnow()

    def _get_delta_in_sec(self, start, end):
        return (end - start).total_seconds()


class TimeTimer(BaseTimer):
    """
    Similar to :class:`DateTimeTimer`.
    """

    def _get_current_time(self):
        return time.process_time()

    def _get_delta_in_sec(self, start, end):
        return end - start


class SerialTimer(object):
    def __init__(self, timer_klass: T.Type[BaseTimer] = TimeTimer):
        self.timer_klass = timer_klass
        self.current_timer: T.Optional[BaseTimer] = None
        self.last_stopped_timer: T.Optional[BaseTimer] = None
        self.history_stopped_timer: T.List[BaseTimer] = list()

    def start(self, title: str = None, display: bool = True):
        self.current_timer = self.timer_klass(title, display)
        self.current_timer.start()

    def _measure(self):
        if self.current_timer is None:
            raise RuntimeError("please call SerialTimer.start() first!")
        self.current_timer.end()
        self.last_stopped_timer = self.current_timer
        self.history_stopped_timer.append(self.last_stopped_timer)

    def end(self):
        self._measure()
        self.current_timer = None

    def click(self, title=None, display=True):
        self._measure()
        self.current_timer = self.timer_klass(title, display)

    @property
    def last(self):
        return self.last_stopped_timer

    @property
    def history(self):
        return self.history_stopped_timer


def timeit_wrapper(func: T.Callable, *args, **kwargs):
    """
    Wrapper function makes ``timeit.timeit`` easier to use.

    Usage::

        >>> import timeit
        >>> def func(*args, **kwargs): # a function you want to measure
        ...     pass
        >>> timeit.timeit(timeit_wrapper(func, *args, **kwargs), number=10)
        0.000153
    """

    def wrapper():
        return func(*args, **kwargs)

    return wrapper
