from collections.abc import Sequence


def find_median(nums1: Sequence[int], nums2: Sequence[int]) -> float:
    """
    Find median of two sorted sequences. At least one of sequences should be not empty.
    :param nums1: sorted sequence of integers
    :param nums2: sorted sequence of integers
    :return: middle value if sum of sequences' lengths is odd
             average of two middle values if sum of sequences' lengths is even
    """
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    n = len(nums1)
    m = len(nums2)
    left = 0
    right = n
    mid = (n + m + 1) // 2

    # Ищем такой индекс в первом массиве, чтобы он был средним или сразу после среднего
    while left <= right:
        i = (left + right) // 2 # хотим чтобы ни втом ни в другом массиве не было элементов, которые могли бы встать в часть ДО нахих крайних элемпентов тк иначе у нас бы была не середина
        j = mid - i
        if i < n and nums2[j - 1] > nums1[i]:
            left = i + 1
        elif i > 0 and nums1[i - 1] > nums2[j]:
            right = i - 1
        else:
            if i == 0:
                res = nums2[j - 1]  # все элементы с левой стороны из nums2
            elif j == 0:
                res = nums1[i - 1]  # все элементы с левой стороны из nums1
            else:
                res = max(nums1[i - 1], nums2[j - 1])  # Первый средний элемент
            if (n + m) % 2 == 1:
                return float(res)
            if i == n:
                el2 = nums2[j]  # все элементы с правой стороны из nums2
            elif j == m:
                el2 = nums1[i]  # все элементы с правой стороны из nums1
            else:
                el2 = min(nums1[i], nums2[j])
            return (res + el2) / 2.0
    assert False, "Not reachable"
