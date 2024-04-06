"""
Part 1 - loads the grid into a grid class, and then finding the path is pretty much just a basic BFS, with some extra
condition checks when looking up the neighbors.
Part 2 - similar to Part 1, but this instead does the BFS 'backwards' starting from the end point and also reverses
the condition in the neighbor check.
Possible improvement: the grid class methods for part 1 and 2 can probably be merged, since most of the code is the
same.
"""
import sys

RowCol = tuple[int, int]


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
        row, col = coord
        for dr, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            if 0 <= row + dr < self.height and 0 <= col + dc < self.width:
                current = ord(self.grid[row][col])
                candidate = ord(self.grid[row + dr][col + dc])
                if (current + 1 >= candidate and not downhill) or (current <= candidate + 1 and downhill):
                    yield row + dr, col + dc

    def get_minsteps_fromstart(self) -> int:
        # Part 1: Regular BFS search from S to E
        visited: dict[RowCol: (int, RowCol)] = {}
        tilequeue: list[tuple[RowCol, int, RowCol]] = [(self.startpos, 0, None)]
        while len(tilequeue) > 0:
            current_pos, current_steps, previous = tilequeue.pop(0)
            if current_pos in visited:
                continue
            for neighbor in self.getneigbors(current_pos):
                if neighbor not in visited:
                    tilequeue.append((neighbor, current_steps + 1, current_pos))
            visited[current_pos] = current_steps, previous
            if self.endpos in visited:
                break
        return visited[self.endpos][0]

    def get_minsteps_fromany(self) -> int:
        # Part 2: BFS again but starting from E and going downhill until finding the first 'a'
        visited: dict[RowCol: (int, RowCol)] = {}
        tilequeue: list[tuple[RowCol, int, RowCol]] = [(self.endpos, 0, None)]
        beststart = -1, -1
        while len(tilequeue) > 0:
            current_pos, current_steps, previous = tilequeue.pop(0)
            if current_pos in visited:
                continue
            for neighbor in self.getneigbors(current_pos, True):
                if neighbor not in visited:
                    tilequeue.append((neighbor, current_steps + 1, current_pos))
            visited[current_pos] = current_steps, previous
            if self.grid[current_pos[0]][current_pos[1]] == 'a':
                beststart = current_pos
                break
        return visited[beststart][0]


def main() -> int:
    with open('../Inputfiles/aoc12.txt', 'r') as file:
        mygrid = Grid(file.read().strip('\n'))

    print("Part 1:", mygrid.get_minsteps_fromstart())
    print("Part 2:", mygrid.get_minsteps_fromany())
    return 0


if __name__ == "__main__":
    sys.exit(main())
