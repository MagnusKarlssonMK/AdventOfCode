"""
"""
import sys
from dataclasses import dataclass
from collections import Counter
from itertools import combinations


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    def get_manhattan(self, other: "Point") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def get_values(self) -> tuple[int, int, int]:
        return self.x, self.y, self.z

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)


class Probe:
    __NBR_OF_BEACONS = 12

    def __init__(self, rawstr: str) -> None:
        self.__scanners = {}
        for i, block in enumerate(rawstr.split('\n\n')):
            self.__scanners[i] = set([Point(*map(int, line.split(','))) for line in block.splitlines()[1:]])
        self.__offsets = []

    def __create_map(self):
        aligned = [0]
        queue = [s for s in self.__scanners if s not in aligned]

        while queue:
            for a in aligned:
                offset_list = []
                rotation = []
                found = -1
                for u in queue:
                    for base_i in range(3):
                        for sign, direction in [(1, 0), (-1, 0), (1, 1), (-1, 1), (1, 2), (-1, 2)]:
                            delta = [b0.get_values()[base_i] - sign * b1.get_values()[direction]
                                     for b1 in self.__scanners[u] for b0 in self.__scanners[a]]
                            offset, matches = Counter(delta).most_common()[0]
                            if matches >= Probe.__NBR_OF_BEACONS:
                                offset_list.append(offset)
                                rotation.append((sign, direction))
                    if len(offset_list) > 0:
                        found = u
                        break
                if found >= 0:
                    queue.remove(found)
                    aligned.append(found)
                    self.__offsets.append(Point(*offset_list))
                    scanner_aligned = [[x, y, z] for x, y, z in [b.get_values() for b in self.__scanners[found]]]
                    scanner_aligned = [[rotation[0][0] * xyz[rotation[0][1]],
                                        rotation[1][0] * xyz[rotation[1][1]],
                                        rotation[2][0] * xyz[rotation[2][1]]] for xyz in scanner_aligned]
                    scanner_aligned = [Point(x + offset_list[0], y + offset_list[1], z + offset_list[2])
                                       for x, y, z in scanner_aligned]
                    self.__scanners[found] = set(scanner_aligned)

    def get_nbr_beacons(self) -> int:
        self.__create_map()
        return len({b for s in self.__scanners for b in self.__scanners[s]})

    def get_biggest_distance(self) -> int:
        return max([self.__offsets[i].get_manhattan(self.__offsets[j])
                    for i, j in combinations(range(len(self.__offsets)), 2)])


def main() -> int:
    with open('../Inputfiles/aoc19.txt', 'r') as file:
        myprobe = Probe(file.read().strip('\n'))
    print(f"Part 1: {myprobe.get_nbr_beacons()}")
    print(f"Part 2: {myprobe.get_biggest_distance()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
