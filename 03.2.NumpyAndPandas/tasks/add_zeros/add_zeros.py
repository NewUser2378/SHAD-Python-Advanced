import numpy as np
import numpy.typing as npt


def add_zeros(x: npt.NDArray[np.int_]) -> npt.NDArray[np.int_]:
    """
    Add zeros between values of given array
    :param x: array,
    :return: array with zeros inserted
    """
    if x.size == 0:
        return np.array([], dtype=np.int_)
    zeros = np.zeros(len(x) - 1, dtype=int)
    result = np.empty(len(zeros) + len(x), dtype=np.int_)
    result[0::2] = x
    result[1::2] = zeros
    return result
