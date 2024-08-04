"""
Part 1 straightforward, just parse the nanobots and sort them according to radius to find the largest one, then
use manhattan distance to count how many other bots are in its range.
Solution to part 2 is basically treating the nanobots as cubes and splits them into smaller and smaller with A* until
down to a single coordinate.
"""
import sys
from pathlib import Path
import re
from dataclasses import dataclass
import math
from heapq import heappop, heappush
from itertools import count, product

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2018/day23.txt')


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    def get_distance(self, other: "Point") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def get_point(self) -> tuple[int, int, int]:
        return self.x, self.y, self.z


@dataclass(frozen=True)
class Rect:
    x: tuple[int, int]
    y: tuple[int, int]
    z: tuple[int, int]

    def get_point(self) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int]]:
        return self.x, self.y, self.z

    def get_zerodistance(self) -> int:
        return min([abs(x) for x in self.x]) + min([abs(y) for y in self.y]) + min([abs(z) for z in self.z])


@dataclass(frozen=True)
class Node:
    rect: Rect
    size: int

    def get_next_nodes(self) -> iter:
        newsize = self.size // 2
        if newsize > 0:
            for steps in product(range(2), repeat=3):
                r = Rect(*[(length + (s * newsize), min(length + (s + 1) * newsize - 1, height))
                           for (length, height), s in zip(self.rect.get_point(), steps)])
                yield Node(r, newsize)


@dataclass(frozen=True)
class Nanobot:
    point: Point
    radius: int

    def intersects_node(self, r: Rect) -> bool:
        distance = 0
        for c, (length, height) in zip(self.point.get_point(), r.get_point()):
            if c < length:
                distance += length - c
            elif c > height:
                distance += c - height
            if distance > self.radius:
                return False
        return True

    def __lt__(self, other: "Nanobot") -> bool:
        return self.radius < other.radius


class Teleport:
    def __init__(self, rawstr: str) -> None:
        self.__bots = sorted([Nanobot(Point(x, y, z), r) for x, y, z, r in
                              [list(map(int, re.findall(r"-?\d+", line)))
                               for line in rawstr.splitlines()]], reverse=True)

    def get_in_range_largest_bot(self) -> int:
        return sum([1 for bot in self.__bots if self.__bots[0].point.get_distance(bot.point) <= self.__bots[0].radius])

    def __get_node_prio(self, n: Node) -> tuple[int, int, int]:
        c = sum([1 for b in self.__bots if not b.intersects_node(n.rect)])
        return c, n.rect.get_zerodistance(), n.size

    def get_best_position_distance(self) -> int:
        minpoints = tuple(map(min, zip(*[b.point.get_point() for b in self.__bots])))
        maxpoints = tuple(map(max, zip(*[b.point.get_point() for b in self.__bots])))
        rect = Rect(*[(min(low, 0), max(high, 0)) for low, high in zip(minpoints, maxpoints)])
        size = 2 ** (int(math.log2(max(maxpoints))) + 1)
        start = Node(rect, size)
        u = count()
        queue = []
        heappush(queue, (*self.__get_node_prio(start), next(u), start))
        while queue:
            _, _, _, _, currentnode = heappop(queue)
            if currentnode.size == 1:
                return currentnode.rect.get_zerodistance()
            for nextnode in currentnode.get_next_nodes():
                heappush(queue, (*self.__get_node_prio(nextnode), next(u), nextnode))
        return -1


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        teleport = Teleport(file.read().strip('\n'))
    print(f"Part 1: {teleport.get_in_range_largest_bot()}")
    print(f"Part 2: {teleport.get_best_position_distance()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
