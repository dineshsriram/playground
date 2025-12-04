from random import shuffle
from typing import Any, Iterable, Protocol, Sequence, TypeVar

T = TypeVar("T")


def my_shuffle(arr: Sequence[T]) -> list[T]:
    shuffle(list(arr))
    return list[T](arr)


print(my_shuffle([5, 6, 7]))
print(my_shuffle([8.9, 3, 5, 7.8]))
print(my_shuffle(["dinesh", "sriram", "apple"]))

###

I = TypeVar("I", int, float, str)


def my_test(a: I, b: I) -> I:
    return a + b


print(my_test("dinesh", "sriram"))

###


class SupportsLessThan(Protocol):
    def __lt__(self, other: Any): ...


LT = TypeVar("LT", bound=SupportsLessThan)


def reverse_sort_obj(objs: Iterable[LT]) -> list[LT]:
    return sorted(objs, reverse=True)
