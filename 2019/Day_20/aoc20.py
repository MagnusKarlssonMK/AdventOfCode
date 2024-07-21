"""

"""
import sys
from dataclasses import dataclass
from enum import Enum
from heapq import heappop, heappush


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def get_neighbors(self) -> iter:
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            yield Point(self.x + dx, self.y + dy)

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __lt__(self, other: "Point") -> bool:
        return self.x < other.x if self.x != other.x else self.y < other.y


class PortalType(Enum):
    INNER = 0
    OUTER = 1

    def get_opposite(self) -> "PortalType":
        return PortalType.INNER if self == PortalType.OUTER else PortalType.OUTER


@dataclass(frozen=True)
class Portal:
    name: str
    ptype: PortalType

    def __lt__(self, other: "Portal") -> bool:  # return whatever in case of tie-breaker in pq
        return self.name < other.name


class DonutMaze:
    def __init__(self, rawstr: str) -> None:
        self.__path: dict[Point: set[Point]] = {}
        self.__portals: dict[set[Point]: tuple[str, PortalType]] = {}
        portpoints: dict[Point, str] = {}
        for y, line in enumerate(rawstr.splitlines()):
            for x, c in enumerate(line):
                if c == '.':
                    self.__path[Point(x, y)] = set()
                elif c.isupper():
                    portpoints[Point(x, y)] = c
        for p in self.__path:
            for n in p.get_neighbors():
                if n in self.__path:
                    self.__path[p].add(n)
        x_outer = min([p.x for p in self.__path]), max([p.x for p in self.__path])
        y_outer = min([p.y for p in self.__path]), max([p.y for p in self.__path])
        pp: list[Point] = list(portpoints.keys())
        while pp:
            p1 = pp.pop()
            p2 = None
            entrance = None
            for n in p1.get_neighbors():
                if n in pp:
                    p2 = n
                    pp.remove(p2)
                elif n in self.__path:
                    entrance = n
            if not entrance:
                for n in p2.get_neighbors():
                    if n in self.__path:
                        entrance = n
                        break
            name = ''.join(portpoints[i] for i in sorted([p1, p2]))
            portaltype = PortalType.OUTER if entrance.x in x_outer or entrance.y in y_outer else PortalType.INNER
            self.__portals[entrance] = Portal(name, portaltype)
        self.__portalmap: dict[str: PortalType] = {pt: set() for pt in self.__portals.values()}
        self.__build_portalmap()

    def __build_portalmap(self) -> None:
        for point, portal in self.__portals.items():
            seen = set()
            targetsfound = {}
            queue = [(point, Point(-1, -1), 0)]
            while queue:
                current, previous, steps = queue.pop(0)
                if current in self.__portals and self.__portals[current] != portal:
                    if self.__portals[current] not in targetsfound or steps < targetsfound[self.__portals[current]]:
                        targetsfound[self.__portals[current]] = steps
                    continue
                if current in seen:
                    continue
                seen.add(current)
                for n in self.__path[current]:
                    if n != previous:
                        queue.append((n, current, steps + 1))
            for k, v in targetsfound.items():
                for p, s in self.__portalmap[portal]:
                    if portal == k and s <= v:
                        break
                else:
                    self.__portalmap[portal].add((k, v))
        for portal in self.__portalmap:
            if (mirror := Portal(portal.name, portal.ptype.get_opposite())) in self.__portalmap:
                self.__portalmap[portal].add((mirror, 1))

    def get_steps_aa_to_zz(self) -> int:
        visited = {}
        pqueue = []
        start = Portal('AA', PortalType.OUTER)
        target = Portal('ZZ', PortalType.OUTER)
        heappush(pqueue, (0, start, start))
        while pqueue:
            steps, current, previous = heappop(pqueue)
            if current == target:
                return steps
            if current in visited and visited[current] <= steps:
                continue
            visited[current] = steps
            for n, n_steps in self.__portalmap[current]:
                if n != previous:
                    heappush(pqueue, (steps + n_steps, n, current))
        return -1

    def get_recursion_steps_aa_to_zz(self) -> int:
        return -1


def main() -> int:
    with open('../Inputfiles/aoc20.txt', 'r') as file:
        maze = DonutMaze(file.read().strip('\n'))
    print(f"Part 1: {maze.get_steps_aa_to_zz()}")
    print(f"Part 2: {maze.get_recursion_steps_aa_to_zz()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
