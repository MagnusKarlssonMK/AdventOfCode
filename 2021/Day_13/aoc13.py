"""
Solution: store the parsed coordinates in a Paper class, in a set rather than a list to easier handle overlapping
points when folding the paper later.
"""
import sys


class Paper:
    def __init__(self, coordlist: list[tuple[int, int]]):
        self.coordinates = set()
        [self.coordinates.add(c) for c in coordlist]
        self.height = -1
        self.width = -1

    def fold(self, axis: str, value: int):
        if axis == 'x':  # Col
            coords = [c for c in self.coordinates]
            for row, col in coords:
                if col > value:
                    self.coordinates.remove((row, col))
                    self.coordinates.add((row, 2 * value - col))
            self.width = value
        elif axis == 'y':  # Row
            coords = [c for c in self.coordinates]
            for row, col in coords:
                if row > value:
                    self.coordinates.remove((row, col))
                    self.coordinates.add((2 * value - row, col))
            self.height = value

    def __str__(self):
        grid = [['.' for _ in range(self.width)] for _ in range(self.height)]
        for r, c in self.coordinates:
            grid[r][c] = "#"
        return f"{''.join([line + '\n' for line in [''.join(s) for s in grid]])}"


def main() -> int:
    with open('../Inputfiles/aoc13.txt', 'r') as file:
        c, f = file.read().strip('\n').split('\n\n')
    # Flip the coordinates so x,y -> row, col
    coordinates = [(int(b), int(a)) for a, b in [coord.split(',') for coord in c.splitlines()]]
    folding = [(j, int(k)) for j, k in [i.strip('fold along ').split('=') for i in f.splitlines()]]
    mypaper = Paper(coordinates)
    for idx, fold in enumerate(folding):
        mypaper.fold(*fold)
        if idx == 0:
            print("Part 1:", len(mypaper.coordinates))
    print("Part 2:")
    print(mypaper)
    return 0


if __name__ == "__main__":
    sys.exit(main())
