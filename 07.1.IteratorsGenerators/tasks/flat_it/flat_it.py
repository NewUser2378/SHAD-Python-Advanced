from collections.abc import Iterable
from typing import Any, Iterator


def flat_it(sequence: Iterable[Any]) -> Iterator[Any]:
    """
    :param sequence: iterable with arbitrary level of nested iterables
    :return: generator producing flatten sequence
    """
    for x in sequence:
        pred = isinstance(x, str)
        if isinstance(x, Iterable) and not pred:
            yield from flat_it(x)
        elif pred:
            yield from x
        else:
            yield x
