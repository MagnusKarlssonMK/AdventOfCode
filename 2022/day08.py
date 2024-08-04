import sys
from pathlib import Path
import math

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2022/day08.txt')


RowCol = tuple[int, int]
Directions = {'Up': 0, 'Right': 1, 'Down': 2, 'Left': 3}
DirToRC = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}


class Forest:
    def __init__(self, rawdata: str) -> None:
        self.grid = [[int(c) for c in line] for line in rawdata.split('\n')]
        self.gridscores = [[[-1, -1, -1, -1] for _ in range(len(self.grid[0]))] for _ in range(len(self.grid))]

    def getvisibletreecount(self) -> int:
        visible: set[RowCol] = set()
        for r in range(len(self.grid)):
            # From left:
            [visible.add(tree) for tree in self.generatevisibletrees(r, -1, range(len(self.grid[0])))]
            # From right:
            [visible.add(tree) for tree in self.generatevisibletrees(r, -1, reversed(range(len(self.grid[0]))))]
        for c in range(len(self.grid[0])):
            # From above
            [visible.add(tree) for tree in self.generatevisibletrees(-1, c, range(len(self.grid)))]
            # From below
            [visible.add(tree) for tree in self.generatevisibletrees(-1, c, reversed(range(len(self.grid))))]
        return len(visible)

    def generatevisibletrees(self, row, col, iterable) -> iter:
        tallest = -1
        for i in iterable:
            if row == -1:
                r = i
                c = col
            else:
                r = row
                c = i
            if self.grid[r][c] > tallest:
                tallest = self.grid[r][c]
                yield r, c
                if tallest == 9:
                    break

    def setdirectionscores(self, row, col, direction: Directions, iterable) -> None:
        scorelist = [0 for _ in range(10)]
        for i in iterable:
            if row == -1:
                r = i
                c = col
            else:
                r = row
                c = i
            self.gridscores[r][c][direction] = scorelist[self.grid[r][c]]
            for j in range(10):
                scorelist[j] = (scorelist[j] + 1) if j > self.grid[r][c] else 1

    def getmaxscore(self) -> int:
        currentmax = 0
        for r in range(len(self.grid)):
            # Left direction
            self.setdirectionscores(r, -1, Directions["Left"], range(len(self.grid[0])))
            # Right direction
            self.setdirectionscores(r, -1, Directions["Right"], reversed(range(len(self.grid[0]))))
        for c in range(len(self.grid[0])):
            # Up direction
            self.setdirectionscores(-1, c, Directions["Up"], range(len(self.grid)))
            # Down direction
            self.setdirectionscores(-1, c, Directions["Down"], reversed(range(len(self.grid))))
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                score = math.prod(self.gridscores[r][c])
                currentmax = max(score, currentmax)
        return currentmax


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        myforest = Forest(file.read().strip('\n'))
    print(f"Part1: {myforest.getvisibletreecount()}")
    print(f"Part2: {myforest.getmaxscore()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
