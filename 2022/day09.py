import sys
from pathlib import Path

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2022/day09.txt')


RowCol = tuple[int, int]
DirMap = {'U': (1, 0), 'D': (-1, 0), 'L': (0, -1), 'R': (0, 1)}


def sign(nbr: int) -> int:
    if nbr == 0:
        return 0
    return 1 if nbr > 0 else -1


class Rope:
    def __init__(self, nbrknots: int):
        self.nbrknots = nbrknots
        self.knotpos: list[RowCol] = [(0, 0) for _ in range(self.nbrknots)]
        self.tailvisited: set[RowCol] = {self.knotpos[-1]}

    def movehead(self, direction: DirMap, steps: int) -> None:
        for _ in range(steps):
            self.knotpos[0] = self.knotpos[0][0] + direction[0], self.knotpos[0][1] + direction[1]
            for idx in range(1, self.nbrknots):
                rowdiff = self.knotpos[idx - 1][0] - self.knotpos[idx][0]
                coldiff = self.knotpos[idx - 1][1] - self.knotpos[idx][1]
                if abs(rowdiff) > 1 or abs(coldiff) > 1:
                    # Tail out of range and needs to catch up
                    self.knotpos[idx] = self.knotpos[idx][0] + sign(rowdiff), self.knotpos[idx][1] + sign(coldiff)
            self.tailvisited.add(self.knotpos[-1])


def main() -> int:
    myfirstrope = Rope(2)
    mysecondrope = Rope(10)
    with open(INPUT_FILE, 'r') as file:
        for line in file.read().strip('\n').splitlines():
            direction, length = line.strip('\n').split()
            myfirstrope.movehead(DirMap[direction], int(length))
            mysecondrope.movehead(DirMap[direction], int(length))
    print(f"Part1: {len(myfirstrope.tailvisited)}")
    print(f"Part2: {len(mysecondrope.tailvisited)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
