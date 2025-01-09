def find_value(nums: list[int] | range, value: int) -> bool:
    """
    Find value in sorted sequence
    :param nums: sequence of integers. Could be empty
    :param value: integer to find
    :return: True if value exists, False otherwise
    """
    left = 0
    right = len(nums)
    if (left > right):
        return False
    while (left < right):
        mid = (left + right) // 2
        if (nums[mid] > value):
            right = mid
        elif (nums[mid] < value):
            var = mid + 1
            left = var
        else:
            return True
    return False
