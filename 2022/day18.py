import sys
from pathlib import Path
from dataclasses import dataclass

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2022/day18.txt')


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    def get_adjacent(self) -> iter:
        for d in ((0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)):
            yield self + Point(*d)

    def get_additional_air(self) -> iter:
        for d in ((0, 1, 1), (0, 1, -1), (0, -1, 1), (0, -1, -1),
                  (1, 0, 1), (-1, 0, 1), (1, 0, -1), (-1, 0, -1),
                  (1, 1, 0), (-1, 1, 0), (1, -1, 0), (-1, -1, 0)):
            yield self + Point(*d)

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)


class Lavapool:
    def __init__(self, rawstr: str) -> None:
        self.__adj: dict[Point: set[Point]] = {}
        for point in [Point(*list(map(int, line.split(',')))) for line in rawstr.splitlines()]:
            self.__adj[point] = set()
        start = Point(999, 999, 999)
        air: set[Point] = set()
        for point in self.__adj:
            for adj in point.get_adjacent():
                if adj not in self.__adj:
                    self.__adj[point].add(adj)
                    air.add(adj)
                    if adj.x < start.x:
                        start = adj
            for additional_air in point.get_additional_air():
                if additional_air not in self.__adj:
                    air.add(additional_air)
        # Use BFS on the air from the start point which is guaranteed to be exterior, and any unreachable points are
        # interior pockets.
        queue = [start]
        seen = set()
        while queue:
            current = queue.pop(0)
            if current in seen:
                continue
            seen.add(current)
            for adj_air in current.get_adjacent():
                if adj_air in air:
                    queue.append(adj_air)
            air.remove(current)
        # Calculate number of points representing enclosed air
        self.__enclosed_air = 0
        for point in self.__adj:
            for a in air:
                if a in self.__adj[point]:
                    self.__enclosed_air += 1

    def get_surface_area(self, remove_interior: bool = False) -> int:
        result = sum([len(adj) for adj in list(self.__adj.values())])
        if remove_interior:
            result -= self.__enclosed_air
        return result


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        pool = Lavapool(file.read().strip('\n'))
    print(f"Part 1: {pool.get_surface_area()}")
    print(f"Part 2: {pool.get_surface_area(True)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
