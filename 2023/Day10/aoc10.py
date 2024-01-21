import sys

RowCol = tuple[int, int]
Directions: dict[str: RowCol] = {'u': (-1, 0), 'r': (0, 1), 'd': (1, 0), 'l': (0, -1)}
Pipes: dict[str: tuple[str]] = {'|': ('u', 'd'), '-': ('l', 'r'), 'L': ('u', 'r'), 'J': ('u', 'l'),
                                '7': ('d', 'l'), 'F': ('d', 'r'), 'S': {'u', 'r', 'd', 'l'}, '.': ()}


def getreversedirection(indir: str) -> RowCol:
    return Directions[indir][0] * -1, Directions[indir][1] * -1


class Grid:
    def __init__(self):
        self.grid = []
        self.width = 0
        self.height = 0

    def addrow(self, newrow: str) -> None:
        self.grid.append(newrow)
        self.height += 1
        self.width = max(self.width, len(newrow))

    def getvalue(self, coord: RowCol) -> str:
        return self.grid[coord[0]][coord[1]]

    def findneighbors(self, coord: RowCol) -> list[RowCol]:
        retlist = []
        for outdir in Pipes[self.getvalue(coord)]:
            nextpos = coord[0] + Directions[outdir][0], coord[1] + Directions[outdir][1]
            if 0 <= nextpos[0] < self.height and 0 <= nextpos[1] < self.width:
                nextdirections = Pipes[self.getvalue(nextpos)]
                if any(getreversedirection(nd) == Directions[outdir] for nd in nextdirections):
                    retlist.append(nextpos)
        return retlist


def shoelace_area(seq: list[RowCol]) -> int:
    retval = 0
    for idx in range(len(seq) - 1):
        retval += (seq[idx][0] + seq[idx + 1][0]) * (seq[idx][1] - seq[idx + 1][1])
    return abs(retval) // 2


def picks(a: int, b: int) -> int:
    return a + 1 - (b // 2)


def main() -> int:
    mygrid = Grid()
    startpoint: RowCol = -1, -1

    with open("aoc10.txt", "r") as file:
        [mygrid.addrow(line.strip("\n")) for line in file.readlines() if len(line) > 1]

    for rowidx, row in enumerate(mygrid.grid):
        if (idx := row.find("S")) >= 0:
            startpoint = rowidx, idx
            break

    pipepath: list[RowCol] = []
    nexttile = [(startpoint, (-1, -1))]  # current tile, previous tile

    while len(nexttile) > 0:
        current, previous = nexttile.pop(0)
        pipepath.append(current)
        neighbors = mygrid.findneighbors(current)
        if previous in neighbors:
            neighbors.remove(previous)
        if len(neighbors) > 0:
            if startpoint in neighbors:  # Stop if we have completed the loop
                break
            # Note: neighbor list should only contain one element after removing the previous node
            nexttile.append((neighbors[0], current))

    print("Part1: ", len(pipepath) // 2)
    print("Part2: ", picks(shoelace_area(pipepath), len(pipepath)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
