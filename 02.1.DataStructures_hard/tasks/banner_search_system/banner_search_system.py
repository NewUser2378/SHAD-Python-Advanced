import heapq
import string
from collections import defaultdict
from typing import List, Dict


def normalize(
        text: str
) -> str:
    """
    Removes punctuation and digits and convert to lower case
    :param text: text to normalize
    :return: normalized query
    """
    return ''.join([ch for ch in text if ch not in string.digits and ch not in string.punctuation]).lower()


def get_words(
        query: str
) -> List[str]:
    """
    Split by words and leave only words with letters greater than 3
    :param query: query to split
    :return: filtered and split query by words
    """
    return [normalize(word) for word in query.split() if len(normalize(word)) > 3]


def build_index(
        banners: List[str]
) -> Dict[str, List[int]]:
    """
    Create index from words to banners ids with preserving order and without repetitions
    :param banners: list of banners for indexation
    :return: mapping from word to banners ids
    """
    index: Dict[str, List[int]] = defaultdict(list)

    for i in range(len(banners)):
        words = banners[i].split()
        unique_words = set(get_words(' '.join(words)))
        for word in unique_words:
            if word:
                index[word].append(i)

    return index


def merge_two_heaps(heap1: List[int], heap2: List[int]) -> List[int]:
    res: List[int] = []
    while heap1 and heap2:
        top1 = heapq.heappop(heap1)
        top2 = heapq.heappop(heap2)
        if top1 == top2:
            heapq.heappush(res, top1)
        elif top1 < top2:
            heapq.heappush(heap2, top2)  # добавляем обратно не минимальный элемент
        elif top1 > top2:
            heapq.heappush(heap1, top1)
    return res


def get_banner_indices_by_query(query: str, index: Dict[str, List[int]]) -> List[int]:
    """
    Extract banner indices from index if all words from the query are contained in the indexed banners.
    Uses heaps (heapq) to find common indices.
    :param query: query to find banners
    :param index: index to search banners
    :return: list of indices of suitable banners
    """
    words = get_words(query)
    if not words:
        return []

    res = index.get(words[0], []).copy()  # Начинаем с кучи для первого слова
    heapq.heapify(res)

    for word in words[1:]:
        if word in index:
            word_heap = index[word].copy()  # Копируем список индексов для текущего слова
            heapq.heapify(word_heap)
            res = merge_two_heaps(res, word_heap)  # Объединяем кучи, оставляя общие элементы
        else:
            return []

    return res


#########################
# Don't change this code
#########################

def get_banners(
        query: str,
        index: Dict[str, List[int]],
        banners: List[str]
) -> List[str]:
    """
    Extract banners matched to queries
    :param query: query to match
    :param index: word-banner_ids index
    :param banners: list of banners
    :return: list of matched banners
    """
    indices = get_banner_indices_by_query(query, index)
    return [banners[i] for i in indices]
