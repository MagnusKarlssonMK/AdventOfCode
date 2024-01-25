import sys

RowCol = tuple[int, int]


def getstardistance(star1: RowCol, star2: RowCol):
    return abs(star1[0] - star2[0]) + abs(star1[1] - star2[1])


class Grid:
    def __init__(self, rawstr: str, expansionrate: int = 2):
        self.grid: list[list[str]] = []
        self.starlist: list[RowCol] = []
        self.expansionrate = expansionrate
        count = 0
        for line in rawstr.splitlines():
            count += 1
            if len(line) > 1:
                if line.find("#") >= 0:
                    charlist = []
                    for idx, c in enumerate(line):
                        charlist.append(c)
                        if c == "#":
                            self.starlist.append((len(self.grid), idx))
                    self.grid.append([c for c in line])
                else:
                    self.grid.append(['X'] * len(line))
        # Replace every empty column with 'X'
        for col in range(0, len(self.grid[0])):
            if not any(row[col] == "#" for row in self.grid):
                for row in self.grid:
                    row[col] = 'X'

    def setexpansionrate(self, newrate) -> None:
        self.expansionrate = newrate

    def getdistancesum(self) -> int:
        retval = 0
        starqueue = self.starlist.copy()
        while len(starqueue) > 0:
            nextstar = starqueue.pop(0)
            for neighborstar in starqueue:
                for row in range(nextstar[0], neighborstar[0]):
                    if self.grid[row][nextstar[1]] == 'X':
                        retval += self.expansionrate
                    else:
                        retval += 1
                for col in range(min(nextstar[1], neighborstar[1]), max(nextstar[1], neighborstar[1])):
                    if self.grid[neighborstar[0]][col] == 'X':
                        retval += self.expansionrate
                    else:
                        retval += 1
        return retval


def main() -> int:
    with open("aoc11.txt", "r") as file:
        mygrid = Grid(file.read())

    result_p1 = mygrid.getdistancesum()
    print("Part1: ", result_p1)
    mygrid.setexpansionrate(1000000)
    result_p2 = mygrid.getdistancesum()
    print("Part2: ", result_p2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
