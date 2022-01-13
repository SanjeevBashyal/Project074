import numpy as np
import math as m


class Grid:
    def __init__(self, matrix):
        self.map = np.array(matrix)
        self.check = 1
        self.h = len(matrix)
        self.w = len(matrix[0])
        self.manhattan_boundry = None
        self.curr_boundry = None

    def _in_bounds(self, ij):
        x, y = ij
        return 0 <= x < self.h and 0 <= y < self.w

    def _passable(self, ij):
        x, y = ij
        return self.map[x][y] is not None

    def is_valid(self, ij):
        return self._in_bounds(ij) and self._passable(ij)

    def neighbors(self, ij):
        x, y = ij
        results = [
            (x + 1, y),
            (x, y - 1),
            (x - 1, y),
            (x, y + 1),
            (x + 1, y - 1),
            (x + 1, y + 1),
            (x - 1, y - 1),
            (x - 1, y + 1),
        ]
        results = list(filter(self.is_valid, results))
        return np.array(results)

    def neighbors_ext(self, ij):
        x, y = ij
        results = [
            (x + 1, y),
            (x, y - 1),
            (x - 1, y),
            (x, y + 1),
            (x + 1, y - 1),
            (x + 1, y + 1),
            (x - 1, y - 1),
            (x - 1, y + 1),
            (x + 2, y + 1),
            (x + 1, y + 2),
            (x - 1, y + 2),
            (x - 2, y + 1),
            (x - 2, y - 1),
            (x - 1, y - 2),
            (x + 1, y - 2),
            (x + 2, y - 1),
        ]
        results = list(filter(self.is_valid, results))
        return np.array(results)

    def values(self, ij):
        return self.map[ij[:, 0], ij[:, 1]]

    def value(self, ij):
        return self.map[ij[0], ij[1]]

    def insert(self, value, ij):
        self.map[ij[0], ij[1]] = value

    def update_less_than(self, values, ijs):
        vals = self.values(ijs)
        ijs = ijs[np.where(values < vals)]
        list(map(lambda n, m: self.insert(m, n), values[ijs], ijs))
