"""

"""
import sys
from heapq import heappop, heappush


class Cavegrid:
    def __init__(self, griddata: list[str]):
        self.grid = griddata
        self.height = len(self.grid)
        self.width = len(self.grid[0])
        self.__adj: dict[tuple[int, int]: list[tuple[int, int, int]]] = {}
        for row in range(self.height):
            for col in range(self.width):
                self.__adj[(row, col)] = []
                for direction in {(1, 0), (-1, 0), (0, 1), (0, -1)}:
                    if 0 <= row + direction[0] < self.height and 0 <= col + direction[1] < self.width:
                        self.__adj[(row, col)].append((row + direction[0], col + direction[1],
                                                       int(self.grid[row + direction[0]][col + direction[1]])))

    def getminimumrisk(self) -> int:
        start = 0, 0
        end = self.height - 1, self.width - 1
        costs = {start: 0}
        visited = set()
        queue = []
        heappush(queue, (0, start))
        while queue:
            c, node = heappop(queue)
            visited.add(node)
            if node == end:
                return c
            for n_row, n_col, n_cost in self.__adj[node]:
                if (n_row, n_col) not in visited:
                    newcost = costs[node] + n_cost
                    if (n_row, n_col) not in costs or costs[(n_row, n_col)] > newcost:
                        costs[(n_row, n_col)] = newcost
                        heappush(queue, (newcost, (n_row, n_col)))
        return -1


def main() -> int:
    with open('../Inputfiles/aoc15.txt', 'r') as file:
        cave = Cavegrid(file.read().strip('\n').splitlines())
    print("Part 1:", cave.getminimumrisk())
    return 0


if __name__ == "__main__":
    sys.exit(main())
