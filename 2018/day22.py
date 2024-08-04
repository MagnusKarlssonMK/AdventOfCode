"""
Generates the map dynamically as needed in a dictionary, sort of like a cache.
For part 1 the answer is then simply the sum of the values of the region types of each location in the square defined
by the start and target nodes.
For part 2, find the shortest path with a Dijkstra algorithm, using a combination of point + equipped tool as nodes.
Attempt to limit the state space by keeping track of the 'worst case', i.e. having to swap gears every remaining
square for the manhattan distance from current point to target.
Also using a weighted time for the pq, adding 'best case scenario' to the remaining squares from manhattan distance
to the time used for queue prioritization only, to try to steer the states towards the target node. This basically
turns the algorithm into A*, since the added weight acts as heuristic.
"""
import sys
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
from heapq import heappop, heappush

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2018/day22.txt')


class Tool(Enum):
    TORCH = 0
    GEAR = 1
    NEITHER = 2


class Type(Enum):
    ROCKY = 0
    WET = 1
    NARROW = 2


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def get_adjacent(self) -> iter:
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            if 0 <= self.x + dx and 0 <= self.y + dy:
                yield Point(self.x + dx, self.y + dy)

    def get_distance(self, other: "Point") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __lt__(self, other: "Point") -> bool:
        return self.x < other.x if self.y == other.y else self.y < other.y


@dataclass(frozen=True)
class Node:
    point: Point
    tool: Tool

    def __lt__(self, other: "Node") -> bool:
        return self.point < other.point


class Cave:
    __SWAP_COST = 7
    __STEP_COST = 1

    def __init__(self, rawstr: str) -> None:
        lines = rawstr.splitlines()
        self.__depth = int(lines[0].split(': ')[1])
        self.__target = Point(*list(map(int, lines[1].split(': ')[1].split(','))))
        self.__start = Point(0, 0)
        self.__geoindex: dict[Point: int] = {}

    def __get_geoindex(self, p: Point) -> int:
        if p in self.__geoindex:
            return self.__geoindex[p]
        i = 0
        if p not in (self.__start, self.__target):
            if p.y == 0:
                i = p.x * 16807
            elif p.x == 0:
                i = p.y * 48271
            else:
                i = self.__get_erosionlevel(Point(p.x - 1, p.y)) * self.__get_erosionlevel(Point(p.x, p.y - 1))
        self.__geoindex[p] = i
        return i

    def __get_erosionlevel(self, p: Point) -> int:
        return (self.__depth + self.__get_geoindex(p)) % 20183

    def __get_region_type(self, p: Point) -> Type:
        return Type(self.__get_erosionlevel(p) % 3)

    def get_total_risk_level(self) -> int:
        return sum([self.__get_region_type(Point(x, y)).value
                    for x in range(self.__target.x + 1) for y in range(self.__target.y + 1)])

    def __get_worstcase(self, p: Point) -> int:
        return (self.__target.get_distance(p) * (Cave.__STEP_COST + Cave.__SWAP_COST)) + Cave.__SWAP_COST

    def __get_bestcase(self, p: Point) -> int:
        return self.__target.get_distance(p) * Cave.__STEP_COST

    def get_shortest_path(self) -> int:
        toolnotallowed = {Type.ROCKY: Tool.NEITHER, Type.WET: Tool.TORCH, Type.NARROW: Tool.GEAR}
        pqueue = []
        heappush(pqueue, (self.__get_bestcase(self.__start),
                          0,
                          Node(self.__start, Tool.TORCH),
                          Node(Point(-1, -1), Tool.TORCH)))
        target = Node(self.__target, Tool.TORCH)
        visited: dict[Node: int] = {target: self.__get_worstcase(self.__start)}
        while pqueue:
            _, timespent, current, previous = heappop(pqueue)
            if current == target:
                visited[current] = timespent
                break
            if (worstcase := timespent + self.__get_worstcase(current.point)) < visited[target]:
                visited[target] = worstcase
            if (timespent + self.__get_bestcase(current.point) >= visited[target] or
                    (current in visited and timespent >= visited[current])):
                continue
            visited[current] = timespent
            if current.point != previous.point:  # Add the option to swap tools unless that's what we came from doing
                newtool = [t for t in Tool
                           if t not in (current.tool, toolnotallowed[self.__get_region_type(current.point)])][0]
                heappush(pqueue, (timespent + Cave.__SWAP_COST + self.__get_bestcase(current.point),
                                  timespent + Cave.__SWAP_COST,
                                  Node(current.point, newtool),
                                  Node(current.point, current.tool)))
            for np in current.point.get_adjacent():
                if (np, current.tool) == previous:
                    continue
                if current.tool != toolnotallowed[self.__get_region_type(np)]:
                    heappush(pqueue, (timespent + Cave.__STEP_COST + self.__get_bestcase(np),
                                      timespent + Cave.__STEP_COST,
                                      Node(np, current.tool),
                                      Node(current.point, current.tool)))
        return visited[target]


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        cave = Cave(file.read().strip('\n'))
    print(f"Part 1: {cave.get_total_risk_level()}")
    print(f"Part 2: {cave.get_shortest_path()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
