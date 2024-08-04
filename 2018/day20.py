"""
Build a dictionary of distances while expanding the map through reading the regex and treating the input like a stack.
From that we can get the answer to part1 just by finding the maximum distance value in the dict, and the answer to
part 2 by counting the number of keys with a distance value of at least 1000.
"""
import sys
from pathlib import Path
from dataclasses import dataclass

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2018/day20.txt')


DIRMAP = {'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)}


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def get_neighbor(self, direction: str) -> "Point":
        return self + Point(*DIRMAP[direction])

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)


class Building:
    def __init__(self, rawstr: str) -> None:
        self.__path = rawstr[1: -1]

    def get_fewest_doors(self) -> tuple[int, int]:
        positions: list[Point] = []
        distances = {}
        current_pos = Point(0, 0)
        previous_pos = Point(0, 0)
        for c in self.__path:
            if c == '(':
                positions.append(current_pos)
            elif c == ')':
                current_pos = positions.pop()
            elif c == '|':
                current_pos = Point(positions[-1].x, positions[-1].y)
            else:
                current_pos = current_pos.get_neighbor(c)
                previous_distance = 0 if previous_pos not in distances else distances[previous_pos]
                if current_pos in distances:
                    distances[current_pos] = min(distances[current_pos], previous_distance + 1)
                else:
                    distances[current_pos] = previous_distance + 1
            previous_pos = Point(current_pos.x, current_pos.y)
        p1 = max(distances.values())
        p2 = sum([1 for d in distances if distances[d] >= 1000])
        return p1, p2


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        building = Building(file.read().strip('\n'))
    p1, p2 = building.get_fewest_doors()
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
