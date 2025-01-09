import enum
from typing import Dict, List, Set


class Status(enum.Enum):
    NEW = 0
    EXTRACTED = 1
    FINISHED = 2


def extract_alphabet(
        graph: Dict[str, Set[str]]
) -> List[str]:
    """
    Extract alphabet from graph
    :param graph: graph with partial order
    :return: alphabet
    """
    used: Dict[str, Status] = {}
    res: List[str] = []

    for key in graph.keys():
        used[key] = Status.NEW

    for vert in graph.keys():
        if used[vert] == Status.NEW:
            dfs(graph, used, vert, res)

    return res


def dfs(
        graph: Dict[str, Set[str]],
        used: Dict[str, Status],
        v: str,
        res: List[str]
) -> None:
    used[v] = Status.EXTRACTED
    for u in graph[v]:
        if used[u] != Status.FINISHED:
            dfs(graph, used, u, res)
    used[v] = Status.FINISHED
    res.insert(0, v)


def build_graph(
        words: List[str]
) -> Dict[str, Set[str]]:
    """
    Build graph from ordered words. Graph should contain all letters from words
    :param words: ordered words
    :return: graph
    """
    graph: Dict[str, Set[str]] = {}

    for word in words:
        for let in word:
            if let not in graph:
                graph[let] = set()

    for i in range(1, len(words)):
        word1 = words[i - 1]
        word2 = words[i]
        for j in range(min(len(word1), len(word2))):
            if word1[j] != word2[j]:
                graph[word1[j]].add(word2[j])
                break

    return graph


#########################
# Don't change this code
#########################

def get_alphabet(
        words: List[str]
) -> List[str]:
    """
    Extract alphabet from sorted words
    :param words: sorted words
    :return: alphabet
    """
    graph = build_graph(words)
    return extract_alphabet(graph)
