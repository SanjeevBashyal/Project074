import numpy as np

class Grid:
        def __init__(self, matrix):
            self.map = np.array(matrix)
            self.check=1
            self.h = len(matrix)
            self.w = len(matrix[0])
            self.manhattan_boundry = None
            self.curr_boundry = None

        def _in_bounds(self, id):
            x, y = id
            return 0 <= x < self.h and 0 <= y < self.w

        def _passable(self, id):
            x, y = id
            return self.map[x][y] is not None

        def is_valid(self, id):
            return self._in_bounds(id) and self._passable(id)

        def neighbors(self, id):
            x, y = id
            results = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1),
                       (x + 1, y - 1), (x + 1, y + 1), (x - 1, y - 1), (x - 1, y + 1)]
            results = list(filter(self.is_valid, results))
            return np.array(results)
            
        def neighbors_ext(self, id):
            x, y = id
            results = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1),
                       (x + 1, y - 1), (x + 1, y + 1), (x - 1, y - 1), (x - 1, y + 1),
                       (x+2,y+1),(x+1,y+2),(x-1,y+2),(x-2,y+1),(x-2,y-1),(x-1,y-2),(x+1,y-2),(x+2,y-1)]
            results = list(filter(self.is_valid, results))
            return np.array(results)
            
        def values(self, id):
            return self.map[id[:,0],id[:,1]]
            
        def value(self, id):
            return self.map[id[0],id[1]]

        @staticmethod
        def manhattan_distance(id1, id2):
            x1, y1 = id1
            x2, y2 = id2
            return abs(x1 - x2) + abs(y1 - y2)

        @staticmethod
        def min_manhattan(curr_node, end_nodes):
            return min(map(lambda node: Grid.manhattan_distance(curr_node, node), end_nodes))

        @staticmethod
        def max_manhattan(curr_node, end_nodes):
            return max(map(lambda node: Grid.manhattan_distance(curr_node, node), end_nodes))

        @staticmethod
        def all_manhattan(curr_node, end_nodes):
            return {end_node: Grid.manhattan_distance(curr_node, end_node) for end_node in end_nodes}

        def simple_cost(self, cur, nex):
            cx, cy = cur
            nx, ny = nex
            currV = self.map[cx][cy]
            offsetV = self.map[nx][ny]
            if cx == nx or cy == ny:
                return (currV + offsetV) / 2
            else:
                return sqrt2 * (currV + offsetV) / 2