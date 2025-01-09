from typing import Any, Generator, List


def transpose(matrix: list[list[Any]]) -> list[list[Any]]:
    """
    :param matrix: rectangular matrix
    :return: transposed matrix
    """
    return [[row[i] for row in matrix] for i in range(len(matrix[0]))]


def uniq(sequence: List[Any]) -> Generator[Any, None, None]:
    """
    :param sequence: arbitrary sequence of comparable elements
    :return: generator of elements of `sequence` in
             the same order without duplicates
    """
    seen = set()
    for x in sequence:
        if x not in seen:
            seen.add(x)
            yield x


def dict_merge(*dicts: dict[Any, Any]) -> dict[Any, Any]:
    """
    :param *dicts: flat dictionaries to be merged
    :return: merged dictionary
    """
    res = {}
    for d in dicts:
        for key, item in d.items():
            res[key] = item
    return res


def product(lhs: list[int], rhs: list[int]) -> int:
    """
    :param rhs: first factor
    :param lhs: second factor
    :return: scalar product
    """
    return sum(x * y for x, y in zip(lhs, rhs))
