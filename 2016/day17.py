"""
Once again, a point class which also generates neighbor points, this time with a hash function to see which directions
are unlocked, meaning we also need to store the path taken to reach the point.
This is used in a simple BFS loop which runs until all paths either get locked in somewhere or reach the target,
and from the found paths the answer to part 1 is the first entry (the actual path), and the answer to part 2 is the
length of the last entry.
"""
import sys
from dataclasses import dataclass
import hashlib


GRID_SIZE = 4


@dataclass(frozen=True)
class Point:
    row: int
    col: int
    path: str = ''

    def get_neighbors(self, passcode: str) -> iter:
        h = hashlib.md5((passcode + self.path).encode()).hexdigest()
        for i, (d, (r, c)) in enumerate({'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}.items()):
            new_row, new_col = self.row + r, self.col + c
            if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE and h[i] in ('b', 'c', 'd', 'e', 'f'):
                yield Point(new_row, new_col, self.path + d)


class Vault:
    def __init__(self, rawstr: str) -> None:
        self.__passcode = rawstr

    def get_shortestpath(self) -> tuple[str, int]:
        p = Point(0, 0)
        found_paths = []
        queue = [p]
        while queue:
            p = queue.pop(0)
            if p.col == GRID_SIZE - 1 and p.row == GRID_SIZE - 1:
                found_paths.append(p.path)
                continue
            for new_p in p.get_neighbors(self.__passcode):
                queue.append(new_p)
        return found_paths[0], len(found_paths[-1])


def main() -> int:
    with open('../Inputfiles/aoc17.txt', 'r') as file:
        vault = Vault(file.read().strip('\n'))
    p1, p2 = vault.get_shortestpath()
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
