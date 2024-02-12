"""
Part 1: Pretty much a basic Djikstra exercise.
Part 2: Expand the graph according to the updated rules and re-run the shortest-path calculation.
"""
import sys
from heapq import heappop, heappush


class Cavegrid:
    def __init__(self, griddata: list[str], expanded: bool = False):
        grid = griddata
        self.__height = len(grid)
        self.__width = len(grid[0])
        if expanded:
            self.__height *= 5
            self.__width *= 5
        self.__adj: dict[tuple[int, int]: list[tuple[int, int, int]]] = {}
        for row in range(self.__height):
            for col in range(self.__width):
                self.__adj[(row, col)] = []
                for direction in {(1, 0), (-1, 0), (0, 1), (0, -1)}:
                    if 0 <= row + direction[0] < self.__height and 0 <= col + direction[1] < self.__width:
                        row_div = (row + direction[0]) // len(grid)
                        row_mod = (row + direction[0]) % len(grid)
                        col_div = (col + direction[1]) // len(grid[0])
                        col_mod = (col + direction[1]) % len(grid[0])
                        value = int(grid[row_mod][col_mod]) + row_div + col_div
                        if value > 9:  # Note - wrap around to 1, not 0
                            value -= 9
                        self.__adj[(row, col)].append((row + direction[0], col + direction[1], value))

    def getminimumrisk(self) -> int:
        start = 0, 0
        end = self.__height - 1, self.__width - 1
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
        indata = file.read().strip('\n').splitlines()
        cave = Cavegrid(indata)
        largecave = Cavegrid(indata, True)
    print("Part 1:", cave.getminimumrisk())
    print("Part 2:", largecave.getminimumrisk())
    return 0


if __name__ == "__main__":
    sys.exit(main())
