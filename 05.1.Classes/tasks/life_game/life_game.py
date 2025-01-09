from typing import List, Any, Dict


class LifeGame(object):
    """
    Class for Game life
    """

    def __init__(self, table: List[List[Any]]) -> None:
        self.map = table
        self.rows = len(table)
        self.cols = len(table[0])

    def _get_neighbors_types(self, row: int, col: int) -> List[Any]:
        neighbors = []
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for d in directions:
            new_row, new_col = row + d[0], col + d[1]
            if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                neighbors.append(self.map[new_row][new_col])
        return neighbors

    def _count_types(self, neighbors: List[Any]) -> Dict[int, int]:
        counts = {
            0: 0,  # пустая ячейка
            1: 0,  # скала
            2: 0,  # рыба
            3: 0  # креветка
        }
        for val in neighbors:
            counts[val] += 1
        return counts

    def _iteration_for_cell(self, cell_val: int, counts: Dict[int, int]) -> int:
        if cell_val == 1:
            return 1  # Скала не меняется
        elif cell_val == 2:  # Рыба
            if counts[2] < 2 or counts[2] >= 4:  # Умирает если слишком мало или много рыб-соседей
                return 0
            else:
                return 2  # Живет, если 2 или 3 рыбы-соседа
        elif cell_val == 3:  # Креветка
            if counts[3] < 2 or counts[3] >= 4:  # Умирает если слишком мало или много креветок-соседей
                return 0
            else:
                return 3  # Живет, если 2 или 3 креветки-соседа
        elif cell_val == 0:
            if counts[2] == 3:  # Рождается рыба, если 3 рыбы-соседа
                return 2
            elif counts[3] == 3:  # Рождается креветка, если 3 креветки-соседа
                return 3
        return 0  # Остается пустой

    def get_next_generation(self) -> List[List[Any]]:
        next_generation = [[0] * self.cols for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                neighbors = self._get_neighbors_types(i, j)
                count_for_neigh = self._count_types(neighbors)
                next_generation[i][j] = self._iteration_for_cell(self.map[i][j], count_for_neigh)
        self.map = next_generation
        return self.map
