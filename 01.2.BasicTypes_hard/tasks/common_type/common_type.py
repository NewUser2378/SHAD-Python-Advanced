def get_common_type(type1: type, type2: type) -> type:
    """
    Calculate common type according to the rule that it must have the most adequate interpretation after conversion.
    Look in tests for adequacy calibration.
    :param type1: one of [bool, int, float, complex, list, range, tuple, str] types
    :param type2: one of [bool, int, float, complex, list, range, tuple, str] types
    :return: the most concrete common type, which can be used to convert both input values
    """
    if type1 == type2:
        if type1 == range:
            return tuple
        return type1

    numeric_types = [bool, int, float, complex]
    collection_types = [list, range, tuple]

    if type1 in numeric_types and type2 in numeric_types:
        type_hierarchy = {bool: 0, int: 1, float: 2, complex: 3}
        return max(type1, type2, key=lambda t: type_hierarchy[t])

    if type1 == str or type2 == str:
        return str
    if (type1 in collection_types and type2 in numeric_types) or (
        type2 in collection_types and type1 in numeric_types
    ):
        return str
    if type1 in collection_types and type2 in collection_types:

        if list in [type1, type2]:
            return list
        elif range in [type1, type2]:
            return tuple
    return str
