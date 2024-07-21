"""

"""
import sys
from dataclasses import dataclass
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


class DonutMaze:
    def __init__(self, rawstr: str) -> None:
        self.__path: dict[Point: set[Point]] = {}
        self.__portals: dict[set[Point]: str] = {}
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
            name = ''.join(sorted([portpoints[p1], portpoints[p2]]))
            self.__portals[entrance] = name
        # [print(k, v) for k, v in self.__portals.items()]

    def get_steps_aa_to_zz(self) -> int:
        portalmap: dict[str: tuple[str, int]] = {n: set() for n in self.__portals.values()}
        for p, pname in self.__portals.items():
            # portalmap[pname] = set()
            seen = set()
            targetsfound = {}
            queue = [(p, Point(-1, -1), 0)]
            while queue:
                current, previous, steps = queue.pop(0)
                if current in self.__portals and self.__portals[current] != pname:
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
                for portal, s in portalmap[pname]:
                    if portal == k and s <= v:
                        break
                else:
                    portalmap[pname].add((k, v))

        visited = {}
        pqueue = []
        heappush(pqueue, (0, 'AA', ''))
        while pqueue:
            steps, current, previous = heappop(pqueue)
            if current == 'ZZ':
                return steps
            if current != 'AA':
                steps = steps + 1  # portal cost
            if current in visited and visited[current] <= steps:
                continue
            visited[current] = steps
            for n, n_steps in portalmap[current]:
                if n != previous:
                    heappush(pqueue, (steps + n_steps, n, current))
        return -1


def main() -> int:
    with open('../Inputfiles/aoc20.txt', 'r') as file:
        maze = DonutMaze(file.read().strip('\n'))
    print(f"Part 1: {maze.get_steps_aa_to_zz()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
