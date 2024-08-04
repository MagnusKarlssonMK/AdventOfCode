"""
Stores the grid as a graph with the gridpoints connecting to more than two neighbors as vertices. Uses BFS to find
the edges, and then a recursive DFS to calculate all path lengths from start to exit to find the longest path.
An argument can be given when building the graph to ignore the slopes for part 2. Note that this results in
significantly more edges and makes Part 2 take well over 10 seconds to complete.
"""
import sys
from pathlib import Path

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2023/day23.txt')


class Island:
    def __init__(self, rawstr: str) -> None:
        self.__grid = rawstr.splitlines()
        self.__height = len(self.__grid)
        self.__width = len(self.__grid[0])
        self.start: tuple[int, int] = 0, self.__grid[0].index('.')
        self.exit: tuple[int, int] = self.__height - 1, self.__grid[-1].index('.')
        # Find vertices
        self.__vertices = set()
        self.__adj: dict[tuple[int, int]: set[tuple[int, int]]] = {}
        for row in range(self.__height):
            for col in range(self.__width):
                if self.__grid[row][col] == "#":
                    continue
                neighbors = 0
                for drow, dcol in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    if (0 <= row + drow < self.__height and 0 <= col + dcol < self.__width and
                            self.__grid[row + drow][col + dcol] != "#"):
                        neighbors += 1
                if neighbors > 2:
                    self.__vertices.add((row, col))
        self.__vertices.add(self.start)
        self.__vertices.add(self.exit)

    def load_tree(self, ignore_slopes: bool = False):
        self.__adj.clear()
        for vertex in self.__vertices:
            queue: list[tuple[tuple[int, int], int]] = [(vertex, 0)]
            visited: set[tuple[int, int]] = set()
            if vertex not in list(self.__adj.keys()):
                self.__adj[vertex] = set()
            while queue:
                (row, col), distance = queue.pop(0)
                if (row, col) not in visited:
                    visited.add((row, col))
                    for drow, dcol in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        neighbor = row + drow, col + dcol
                        if (0 <= neighbor[0] < self.__height and 0 <= neighbor[1] < self.__width and
                                (nchar := self.__grid[neighbor[0]][neighbor[1]]) != "#"):
                            if neighbor in self.__vertices and neighbor != vertex:
                                self.__adj[vertex].add((neighbor, distance + 1))
                            else:
                                if not ignore_slopes:
                                    opposite_direction = {(0, 1): '<', (0, -1): '>', (1, 0): '^', (-1, 0): 'v'}
                                    if nchar == opposite_direction[drow, dcol]:
                                        continue
                                queue.append((neighbor, distance + 1))

    def __dfs(self, from_v: tuple[int, int], to_v: tuple[int, int], seen: set) -> list[int]:
        if from_v == to_v:
            return [0]
        seen.add(from_v)
        lengthlist = []
        for next_v, distance in self.__adj[from_v]:
            if next_v not in seen:
                for length in self.__dfs(next_v, to_v, seen):
                    lengthlist.append(length + distance)
        seen.remove(from_v)
        return lengthlist

    def get_maxpathlength(self) -> int:
        return max(self.__dfs(self.start, self.exit, set()))


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        island = Island(file.read().strip('\n'))
    island.load_tree()
    print(f"Part 1: {island.get_maxpathlength()}")
    island.load_tree(True)
    print(f"Part 2: {island.get_maxpathlength()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
