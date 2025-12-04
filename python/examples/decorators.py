import functools
from typing import Any, Callable


def decorate(fn: Callable[Any, Any]):
    def inner():
        print("inner")

    return inner


@decorate
def target():
    print("target")


target()

##


class Averager:
    def __init__(self):
        self.total = 0
        self.count = 0

    def __call__(self, n: float):
        self.total += n
        self.count += 1
        avg = self.total / self.count
        print(avg)
        return avg


avg = Averager()
avg(5)
avg(11)


def make_averager():
    series = []

    # "averager" is the closure which uses "series" variable beyond it's scope.
    def averager(n: float):
        series.append(n)  # series is a "free variable"
        avg = sum(series) / len(series)
        print(avg)
        return avg

    return averager


avg = make_averager()
avg(5)
avg(11)

##

import time
import functools


def clock(fn: Callable[...]):
    @functools.wraps(fn)
    # This is needed so the decorated function's attributes, __name__ and __doc__ are preserved.
    def time_wrapper(*args: tuple[Any], **kwargs: dict[Any, Any]):
        start_time = time.perf_counter()
        result = fn(*args, **kwargs)
        name = fn.__name__
        print(f"Elapsed time for {name} is ", time.perf_counter() - start_time)
        return result

    return time_wrapper


@clock
def sleep_fn():
    time.sleep(2)


sleep_fn()
