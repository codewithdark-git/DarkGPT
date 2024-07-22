"""
    readtime.result
    ~~~~~~~~~~~~~~~

    For returning read time results.

    :copyright: (c) 2016 Alan Hamlett.
    :license: BSD, see LICENSE for more details.
"""


import math
import operator
from datetime import timedelta


class Result:
    delta = None

    def __init__(self, seconds=None, wpm=None):
        self.wpm = wpm
        self.delta = timedelta(seconds=seconds)
        self._add_operator_methods()

    def __repr__(self):
        return self.text + ' read'

    def __str__(self):
        return self.__repr__()

    @property
    def seconds(self):
        return int(self.delta.total_seconds())

    @property
    def minutes(self):
        minutes = math.ceil(self.seconds / 60)
        minutes = max(1, minutes)  # Medium's formula has a minimum of 1 min read time
        return minutes

    @property
    def text(self):
        return f'{self.minutes} min'

    def _add_operator_methods(self):
        for op in dir(operator):
            can_set = (getattr(self.__class__, op, None) is None and
                       getattr(self.delta, op, None) is not None and
                       op.startswith('__') and
                       op.endswith('__'))
            if can_set:
                try:
                    setattr(self.__class__, op, self._create_method(op))
                except (AttributeError, TypeError):
                    pass

    def _create_method(self, op):
        fn = getattr(self.delta, op)

        def method(cls, other, *args, **kwargs):
            delta = fn(other.delta)
            return Result(seconds=delta.total_seconds(), wpm=self.wpm)

        return method
