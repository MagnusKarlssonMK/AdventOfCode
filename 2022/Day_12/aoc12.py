import sys

RowCol = tuple[int, int]
Directions = ((0, 1), (1, 0), (0, -1), (-1, 0))


class Grid:
    def __init__(self, inputstring: str):
        self.grid: list[str] = []
        [self.grid.append(line) for line in inputstring.splitlines()]
        self.height = len(self.grid)
        self.width = len(self.grid[0])
        self.startpos: RowCol = 0, 0
        self.endpos: RowCol = 0, 0
        for row in range(self.height):
            if (startcol := self.grid[row].find('S')) >= 0:
                self.startpos = row, startcol
                self.grid[row] = self.grid[row].replace('S', 'a')
            if (endcol := self.grid[row].find('E')) >= 0:
                self.endpos = row, endcol
                self.grid[row] = self.grid[row].replace('E', 'z')

    def getneigbors(self, coord: RowCol, downhill: bool = False) -> iter:
        for d in Directions:
            if 0 <= coord[0] + d[0] < self.height and 0 <= coord[1] + d[1] < self.width:
                current = ord(self.grid[coord[0]][coord[1]])
                candidate = ord(self.grid[coord[0] + d[0]][coord[1] + d[1]])
                if (current + 1 >= candidate and not downhill) or (current <= candidate + 1 and downhill):
                    yield coord[0] + d[0], coord[1] + d[1]


def main() -> int:
    with open('../Inputfiles/aoc12.txt', 'r') as file:
        mygrid = Grid(file.read().strip('\n'))

    # Part 1: Regular BFS search from S to E
    visited: dict[RowCol: (int, RowCol)] = {}
    tilequeue: list[tuple[RowCol, int, RowCol]] = [(mygrid.startpos, 0, None)]
    while len(tilequeue) > 0:
        current = tilequeue.pop(0)
        if current[0] in visited:
            continue
        for neighbor in mygrid.getneigbors(current[0]):
            if neighbor not in visited:
                tilequeue.append((neighbor, current[1] + 1, current[0]))
        visited[current[0]] = current[1], current[2]
        if mygrid.endpos in visited:
            break

    print("Part 1:", visited[mygrid.endpos][0])

    # Part 2: BFS again but starting from E and going downhill until finding the first 'a'
    visited_p2: dict[RowCol: (int, RowCol)] = {}
    tilequeue_p2: list[tuple[RowCol, int, RowCol]] = [(mygrid.endpos, 0, None)]
    beststart = -1, -1
    while len(tilequeue_p2) > 0:
        current = tilequeue_p2.pop(0)
        if current[0] in visited_p2:
            continue
        for neighbor in mygrid.getneigbors(current[0], True):
            if neighbor not in visited_p2:
                tilequeue_p2.append((neighbor, current[1] + 1, current[0]))
        visited_p2[current[0]] = current[1], current[2]
        if mygrid.grid[current[0][0]][current[0][1]] == 'a':
            beststart = current[0]
            break

    print("Part 2:", visited_p2[beststart][0], beststart)
    return 0


if __name__ == "__main__":
    sys.exit(main())
