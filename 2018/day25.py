"""
Arrange the fixed points in a neighbor adjacency list, then:
- traverse with BFS starting from any key in that list, to find all reachable points, which will be one constellation
- remove the points from that constellation from the list
- increase the constellation counter
- repeat until the list is empty
"""
import time
from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class FixedPoint:
    uid: int
    coord: tuple[int, int, int, int]

    def get_distance(self, other: "FixedPoint") -> int:
        return sum([abs(a - b) for a, b in zip(self.coord, other.coord)])


class Spacetime:
    def __init__(self, rawstr: str) -> None:
        self.__fixedpoints = [FixedPoint(i, (a, b, c, d)) for i, (a, b, c, d) in enumerate(
                              [list(map(int, line.split(','))) for line in rawstr.splitlines()])]

    def get_constellations_count(self) -> int:
        adj: dict[int, set[int]] = {f.uid: set() for f in self.__fixedpoints}
        for i in range(len(self.__fixedpoints) - 1):
            for j in range(i + 1, len(self.__fixedpoints)):
                if self.__fixedpoints[i].get_distance(self.__fixedpoints[j]) <= 3:
                    adj[self.__fixedpoints[i].uid].add(self.__fixedpoints[j].uid)
                    adj[self.__fixedpoints[j].uid].add(self.__fixedpoints[i].uid)
        constellations = 0
        while adj:
            seen: set[int] = set()
            queue = [list(adj.keys())[0]]
            while queue:
                currentid = queue.pop(0)
                if currentid in seen:
                    continue
                seen.add(currentid)
                for n in adj[currentid]:
                    queue.append(n)
            constellations += 1
            for s in seen:
                adj.pop(s)
        return constellations


def main(aoc_input: str) -> None:
    spacetime = Spacetime(aoc_input)
    print(f"Part 1: {spacetime.get_constellations_count()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2018/day25.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
