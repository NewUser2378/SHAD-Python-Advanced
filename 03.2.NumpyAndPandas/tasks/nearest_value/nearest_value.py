import numpy as np
import numpy.typing as npt


def nearest_value(matrix: npt.NDArray[np.float64], value: float) -> float | None:
    """
    Find nearest value in matrix.
    If matrix is empty return None
    :param matrix: input matrix
    :param value: value to find
    :return: nearest value in matrix or None
    """
    if matrix.size <= 0:
        return None
    abs_matr = np.vectorize(abs)(matrix - value)
    min_el_row, min_el_col = np.unravel_index(np.argmin(abs_matr), matrix.shape)
    return matrix[min_el_row, min_el_col]
