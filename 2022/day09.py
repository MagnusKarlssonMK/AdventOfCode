import sys
from pathlib import Path
from dataclasses import dataclass


ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2022/day09.txt')


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def catchup(self, other: "Point") -> "Point":
        def sign(nbr: int) -> int:
            if nbr == 0:
                return 0
            return 1 if nbr > 0 else -1
        return Point(self.x + sign(other.x), self.y + sign(other.y))

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y)


class Rope:
    def __init__(self, rawstr: str) -> None:
        dirmap = {'U': Point(-1, 0), 'D': Point(1, 0), 'L': Point(0, -1), 'R': Point(0, 1)}
        self.__motions = [(dirmap[left], int(right)) for left, right in [line.split() for line in rawstr.splitlines()]]

    def get_nbr_tail_positions(self, nbr_knots: int = 2) -> int:
        knotpos = [Point(0, 0) for _ in range(nbr_knots)]
        tail_seen: set[Point] = {Point(0, 0)}
        for direction, steps in self.__motions:
            for _ in range(steps):
                knotpos[0] += direction
                for i in range(1, nbr_knots):
                    diff = knotpos[i - 1] - knotpos[i]
                    if abs(diff.x) > 1 or abs(diff.y) > 1:
                        # Tail out of range and needs to catch up
                        knotpos[i] = knotpos[i].catchup(diff)
                tail_seen.add(knotpos[-1])
        return len(tail_seen)


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        rope = Rope(file.read().strip('\n'))
    print(f"Part 1: {rope.get_nbr_tail_positions()}")
    print(f"Part 2: {rope.get_nbr_tail_positions(10)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
