"""
Stores the grid as a graph with the gridpoints connecting to more than two neighbors as vertices. Uses BFS to find
the edges, and then a recursive DFS to calculate all path lengths from start to exit to find the longest path.
An argument can be given when rebuilding the graph to ignore the slopes for part 2. Note that this graph results in
significantly more edges and makes Part 2 take a really long time to complete.
"""
import sys
from pathlib import Path
from dataclasses import dataclass

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2023/day23.txt')


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def get_neighbors(self) -> iter:
        for d in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            yield self + Point(*d)

    def is_opposite_direction(self, d: str) -> bool:
        dirmap = {(1, 0): '<', (-1, 0): '>', (0, 1): '^', (0, -1): 'v'}
        return dirmap[(self.x, self.y)] == d

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)


class Island:
    def __init__(self, rawstr: str) -> None:
        self.__grid = rawstr.splitlines()
        self.__height = len(self.__grid)
        self.__width = len(self.__grid[0])
        self.__start = Point(self.__grid[0].index('.'), 0)
        self.__exit = Point(self.__grid[-1].index('.'), self.__height - 1)
        # Find the nodes that connects to more than two other neighbors.
        self.__connectors: set[Point] = set()
        self.__adj: dict[Point: tuple[set[Point], int]] = {}
        for y in range(self.__height):
            for x in range(self.__width):
                if self.__grid[y][x] == "#":
                    continue
                neighbors = 0
                for n in Point(x, y).get_neighbors():
                    if (0 <= n.y < self.__height and 0 <= n.x < self.__width and
                            self.__grid[n.y][n.x] != "#"):
                        neighbors += 1
                if neighbors > 2:
                    self.__connectors.add(Point(x, y))
        self.__connectors.add(self.__start)
        self.__connectors.add(self.__exit)

    def __load_tree(self, ignore_slopes: bool):
        """Creates the neighbor list between the connectors."""
        self.__adj.clear()
        for vertex in self.__connectors:
            queue: list[tuple[Point, int]] = [(vertex, 0)]
            seen: set[Point] = set()
            if vertex not in self.__adj:
                self.__adj[vertex] = set()
            while queue:
                point, distance = queue.pop(0)
                if point in seen:
                    continue
                seen.add(point)
                for direction in Point(0, 0).get_neighbors():
                    neighbor = point + direction
                    if (0 <= neighbor.y < self.__height and 0 <= neighbor.x < self.__width and
                            (nchar := self.__grid[neighbor.y][neighbor.x]) != "#"):
                        if neighbor in self.__connectors and neighbor != vertex:
                            self.__adj[vertex].add((neighbor, distance + 1))
                        elif ignore_slopes or not direction.is_opposite_direction(nchar):
                            queue.append((neighbor, distance + 1))
        # Optimization - only move 'right' / 'down' when on an outer node, meaning nodes with only 3 neighbors.
        # I.e. make those edges directional so that they don't allow backtracking towards the start, since that would
        # make the path cut itself off from the rest of the map.
        trim_queue = [(self.__start, None)]
        trim_seen = set()
        while trim_queue:
            node, prev = trim_queue.pop(0)
            remove_me = None
            exit_in_neighbors = self.__exit in [x for x, _ in self.__adj[node]]
            for n, s in self.__adj[node]:
                if n == prev:
                    remove_me = n, s
                elif not exit_in_neighbors and len(self.__adj[n]) < 4:
                    trim_queue.append((n, node))
            if remove_me:
                self.__adj[node].remove(remove_me)
            trim_seen.add(node)

    def __dfs(self, from_v: Point, to_v: Point, seen: set) -> list[int]:
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

    def get_maxpathlength(self, ignore_slopes: bool = False) -> int:
        self.__load_tree(ignore_slopes)
        return max(self.__dfs(self.__start, self.__exit, set()))


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        island = Island(file.read().strip('\n'))
    print(f"Part 1: {island.get_maxpathlength()}")
    print(f"Part 2: {island.get_maxpathlength(True)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
