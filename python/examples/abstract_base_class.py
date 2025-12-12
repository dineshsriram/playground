import abc
import random


# Create Abstract Base Classes from "abc" module.
class Tombola(abc.ABC):
    @abc.abstractmethod
    def pick(self):
        """Remove item at random, returning it"""

    @abc.abstractmethod
    def load(self, iterable):
        """Add items from iterable"""

    def loaded(self):
        """Check if there is at-least one item"""
        return bool(self.inspect())

    def inspect(self) -> tuple:
        """Return a tuple of items, original ordering is not preserved"""
        items: list = []
        while True:
            try:
                item = self.pick()
            except LookupError:
                break
            items.append(item)
        self.load(items)
        return tuple(items)


# Concrete sub-class
class BingoCage(Tombola):

    def __init__(self, items):
        self._items = []
        self._randomizer = random.SystemRandom()
        self.load(items)

    def load(self, items):
        self._items.extend(items)
        self._randomizer.shuffle(self._items)

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError("pick from Empty BingoCage")

    def __call__(self):
        self.pick()


# Another concrete sub-class but this overrides concrete methods of Tombola, loaded() and inspect() as they're too expensive.


class LottoBlower(Tombola):
    def __init__(self, iterable):
        self._balls = list(iterable)

    def load(self, iterable):
        self._balls.extend(iterable)

    def pick(self):
        try:
            position = random.randrange(len(self._balls))
        except ValueError:

            raise LookupError("pick from empty LottoBlower")
        return self._balls.pop(position)

    def loaded(self):
        return bool(self._balls)

    def inspect(self):
        return tuple(self._balls)


# Virtual Sub-class.


@Tombola.register
class TombolaList(list):
    """I can choose to not implement any abstract methods as this is a virtual sub-class"""
