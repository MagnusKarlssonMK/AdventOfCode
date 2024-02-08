import sys
from heapq import heappop, heappush

RowCol = tuple[int, int]
Directions = {'u': (-1, 0), 'd': (1, 0), 'l': (0, -1), 'r': (0, 1)}


class CityBoard:
    def __init__(self, rawstr: str):
        self.grid = [[int(c) for c in line] for line in rawstr.splitlines()]
        self.width = len(self.grid[0])
        self.height = len(self.grid)
        self.minsteps = 0
        self.maxsteps = 3

    def findshortestpath(self) -> int:
        start: RowCol = (0, 0)
        target: RowCol = (self.height - 1, self.width - 1)
        visited = {}
        queue = []
        heappush(queue, (0, start, (0, 1), 0))
        while queue:
            heat, pos, drn, stepcount = heappop(queue)
            if pos == target and stepcount >= self.minsteps:
                return heat
            neighbors = []
            if stepcount >= self.minsteps:
                neighbors.append(((pos[0] - drn[1], pos[1] + drn[0]), (-drn[1], drn[0]), 1))
                neighbors.append(((pos[0] + drn[1], pos[1] - drn[0]), (drn[1], -drn[0]), 1))
            if stepcount < self.maxsteps:
                neighbors.append(((pos[0] + drn[0], pos[1] + drn[1]), drn, stepcount + 1))
            for n in neighbors:
                if 0 <= n[0][0] < self.height and 0 <= n[0][1] < self.width:
                    new_heat = heat + self.grid[n[0][0]][n[0][1]]
                    if n not in visited or new_heat < visited[n]:
                        visited[n] = new_heat
                        heappush(queue, (new_heat, *n))
        return -1


def main() -> int:
    with open('../Inputfiles/aoc17.txt') as file:
        mygrid = CityBoard(file.read().strip('\n'))
    print("Part 1:", mygrid.findshortestpath())
    mygrid.minsteps = 4
    mygrid.maxsteps = 10
    print("Part 2:", mygrid.findshortestpath())
    return 0


if __name__ == "__main__":
    sys.exit(main())
