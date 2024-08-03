"""
Part 1: Stores the grid in a new class, and finds reachable tiles within the step count limit using BFS, then count
only the ones that have odd/even number of steps (depending on whether the count limit is odd/even).
Part 2: Solves it with three-point-formula to determine the coefficients in a quadratic formula, and calculate the
answer from that.
"""
import sys


RowCol = tuple[int, int]


class Grid:
    def __init__(self, rawstr: str):
        self.grid = rawstr.splitlines()
        self.__height = len(self.grid)
        self.__width = len(self.grid[0])
        self.start = -1, -1
        for row in range(self.__height):
            if (col := self.grid[row].find('S')) >= 0:
                self.start = row, col

    def __get_neighbors(self, coord: RowCol, expand: bool) -> iter:
        for direction in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            row, col = tuple(map(sum, zip(coord, direction)))
            if expand:
                if self.grid[row % self.__height][col % self.__width] != "#":
                    yield row, col
            else:
                if 0 <= row < self.__height and 0 <= col < self.__width and self.grid[row][col] != "#":
                    yield row, col

    def get_reachablecount(self, steps: int, expand: bool = False) -> int:
        seen: set[RowCol] = set()
        reachable: set[RowCol] = set()
        bfs_queue = [(self.start, 0)]
        while bfs_queue:
            u, count = bfs_queue.pop(0)
            if count <= steps:
                if count % 2 == steps % 2:
                    reachable.add(u)
                for v in self.__get_neighbors(u, expand):
                    if v not in seen:
                        bfs_queue.append((v, count + 1))
                        seen.add(v)
        return len(reachable)

    def get_reachablecount_infinite(self, maxstep: int) -> int:
        n = (self.__height - 1) // 2
        three_vec = [n + (self.__height * i) for i in range(3)]
        # y = a*x^2 + b*x + c
        y = [self.get_reachablecount(i, True) for i in three_vec]
        c = y[0]
        b = ((4 * y[1]) - (3 * y[0]) - y[2]) // 2
        a = y[1] - y[0] - b
        x = (maxstep - n) // self.__height
        return (a * x ** 2) + (b * x) + c


def main() -> int:
    with open('../Inputfiles/aoc21.txt', 'r') as file:
        mygrid = Grid(file.read().strip('\n'))
    print("Part 1:", mygrid.get_reachablecount(64))
    print("Part 2:", mygrid.get_reachablecount_infinite(26501365))
    return 0


if __name__ == "__main__":
    sys.exit(main())
