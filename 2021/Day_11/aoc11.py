"""
Creates a cavern class containing the octopus grid. Also adds a class internal adjacency list to avoid having to
generate the adjacent nodes every single time. When taking a step, go through all nodes and increment them (unless
they already flashed this step), and if a node flashes, increment all adjacent nodes, i.e. incrementation is done
recursively.
"""
import sys


class Cavern:
    def __init__(self, indata: list[str]):
        self.grid = [[int(c) for c in line] for line in indata]
        self.__height = len(self.grid)
        self.__width = len(self.grid[0])
        self.flashcount = 0
        self.__flashed: set[tuple[int, int]] = set()
        self.__adj: dict[tuple[int, int]: list[tuple[int, int]]] = {}
        for row in range(self.__height):
            for col in range(self.__width):
                self.__adj[row, col] = [n for n in self.__getadjacent(row, col)]

    def __getadjacent(self, row: int, col: int) -> iter:
        rowlimits = max(0, row - 1), min(row + 1, self.__height - 1)
        collimits = max(0, col - 1), min(col + 1, self.__width - 1)
        for r in range(rowlimits[0], rowlimits[1] + 1):
            for c in range(collimits[0], collimits[1] + 1):
                if (r, c) != (row, col):
                    yield r, c

    def takestep(self) -> bool:
        for key in list(self.__adj.keys()):
            if key not in self.__flashed:
                self.__increment(*key)
        flashed = len(self.__flashed)
        self.flashcount += flashed
        self.__flashed = set()
        if flashed == self.__height * self.__width:
            return True
        return False

    def __increment(self, row: int, col: int):
        if (row, col) not in self.__flashed:
            if self.grid[row][col] < 9:
                self.grid[row][col] += 1
            else:
                self.grid[row][col] = 0
                self.__flashed.add((row, col))
                [self.__increment(r, c) for r, c in self.__adj[(row, col)]]

    def __str__(self):
        return f"{''.join([''.join([str(n) for n in row]) + '\n' for row in self.grid])}"


def main() -> int:
    with open('../Inputfiles/aoc11.txt', 'r') as file:
        cavern = Cavern(file.read().strip('\n').splitlines())
    count = 0
    p1 = -1
    while not cavern.takestep():
        count += 1
        if count == 100:
            p1 = cavern.flashcount
    print("Part 1:", p1)
    print("Part 2:", count + 1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
