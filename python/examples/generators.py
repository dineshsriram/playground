# Any function is a generator function if it cotains "yield" keyword.


def generator_function():
    yield 1
    yield 2
    yield 3


import re

RE_WORD = re.compile(r"\w+")


class Sentence:
    def __init__(self, text: str):
        self.text = text

    def __iter__(self):
        for match in RE_WORD.finditer(self.text):
            yield match.group()

        # The above can also be written via Generator expression as -
        # (match.group() for match in RE_WORD.finditer(self.text))
