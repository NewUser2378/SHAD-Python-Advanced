import numpy as np
import numpy.typing as npt


def max_element(array: npt.NDArray[np.int_]) -> int | None:
    """
    Return the maximum element that comes right after a zero in the input array.
    If no such element exists, return None.
    :param array: The input array
    :return: The maximum element or None
    """
    zero_indices = np.where(array == 0)[0]
    if zero_indices.size > 0:
        valid_ind = zero_indices[zero_indices + 1 < array.size]
        prev_zero = array[valid_ind + 1]
        if prev_zero.size > 0:
            return np.max(prev_zero)
    return None
