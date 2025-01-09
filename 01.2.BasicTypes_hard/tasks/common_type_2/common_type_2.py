from typing import Any, List


def convert_to_common_type(data: List[Any]) -> List[Any]:
    """
    Takes a list of multiple types' elements and converts each element to a common type according to given rules.

    :param data: list of multiple types' elements
    :return: list with elements converted to a common type
    """

    def is_no_info(value: Any) -> bool:
        return (
            value is None or value == "" or value == () or value == [] or value is False
        )

    if data == [False] * len(data):
        return data
    types = {type(v) for v in data if not is_no_info(v)}
    if not types:
        return [""] * len(data)
    if bool in types and all(
        isinstance(v, (bool, int, float)) or is_no_info(v) for v in data
    ):
        return [bool(v) if not is_no_info(v) else False for v in data]

    if list in types or tuple in types:
        return [
            list(v)
            if isinstance(v, (list, tuple))
            else [v]
            if not is_no_info(v)
            else []
            for v in data
        ]
    if int in types or float in types:
        if all(
            isinstance(v, int) or isinstance(v, bool) or is_no_info(v) for v in data
        ):
            return [int(v) if not is_no_info(v) else 0 for v in data]
        else:
            return [float(v) if not is_no_info(v) else 0.0 for v in data]
    return [str(v) if not is_no_info(v) else "" for v in data]
