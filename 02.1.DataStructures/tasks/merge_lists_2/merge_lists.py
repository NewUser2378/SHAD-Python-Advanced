import heapq
import typing as tp


def merge(seq: tp.Sequence[tp.Sequence[int]]) -> list[int]:
    """
    :param seq: sequence of sorted sequences
    :return: merged sorted list
    """

    def merge_two_heaps(heap1: list[int], heap2: tp.Sequence[int]) -> list[int]:
        for element in heap2:
            heapq.heappush(heap1, element)
        return heap1

    res_heap: list[int] = []
    for subseq in seq:
        res_heap = merge_two_heaps(res_heap, subseq)

    return [heapq.heappop(res_heap) for _ in range(len(res_heap))]
