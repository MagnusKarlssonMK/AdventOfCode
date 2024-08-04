"""
Not very efficient solution since it stores and interates over every single coordinate, but still runs in about a
second or so. It might be possible to create a solution just based on corners, but it would be MUCH more complicated.

Simply stores the claimed squares as coordinates in a counter dict, and gets the answer to Part 1 by counting how many
squares have been counted more than once.
While doing that, mark up the claims that don't have overlap just to prune what we need to check for Part 2. Then
go over those once more and find which one still doesn't have overlap after the entire dict has been built.
"""
import sys
from pathlib import Path
import re
from dataclasses import dataclass

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2018/day03.txt')


@dataclass(frozen=True)
class Claim:
    id: int
    x: int
    y: int
    x_len: int
    y_len: int


class Fabric:
    def __init__(self, rawstr: str) -> None:
        self.__claims = [Claim(*list(map(int, re.findall(r"\d+", line)))) for line in rawstr.splitlines()]

    def get_overlap_and_id(self) -> tuple[int, int]:
        seen = {}
        possible = []
        for i, c in enumerate(self.__claims):
            overlap = False
            for x in range(c.x, c.x + c.x_len):
                for y in range(c.y, c.y + c.y_len):
                    if (x, y) not in seen:
                        seen[(x, y)] = 1
                    else:
                        seen[(x, y)] += 1
                        overlap = True
            if not overlap:
                possible.append(i)
        overlap_count = sum([1 for s in seen if seen[s] > 1])

        while possible:
            i = possible.pop(0)
            for x in range(self.__claims[i].x, self.__claims[i].x + self.__claims[i].x_len):
                for y in range(self.__claims[i].y, self.__claims[i].y + self.__claims[i].y_len):
                    if seen[(x, y)] > 1:
                        break
                else:
                    continue
                break
            else:
                return overlap_count, self.__claims[i].id
        return overlap_count, -1


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        fabric = Fabric(file.read().strip('\n'))
    p1, p2 = fabric.get_overlap_and_id()
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
