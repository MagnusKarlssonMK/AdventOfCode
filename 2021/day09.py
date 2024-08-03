"""
Rather straighforward grid problem.
Create a Grid class to store the input, and add methods to find the low point coordinates and basin coordinates.
The latter uses a stripped down BFS to find any adjacent neighbor until value '9' is found. This assumes (as also
stated in the problem description) that all low points will be surrounded by 9:s and not connected to any other
low point.
"""
import sys

Point = tuple[int, int]


class Grid:
    def __init__(self, inputlines: list[str]):
        self.__grid = [[int(c) for c in line] for line in inputlines]
        self.__height = len(self.__grid)
        self.__width = len(self.__grid[0])
        self.__lowpoints = [p for p in self.__findlowpoints()]

    def __getneighborpoints(self, p: Point) -> iter:
        row, col = p
        if row > 0:  # up
            yield row - 1, col
        if row < self.__height - 1:  # down
            yield row + 1, col
        if col > 0:  # left
            yield row, col - 1
        if col < self.__width - 1:  # right
            yield row, col + 1

    def __findlowpoints(self) -> iter:
        for row in range(self.__height):
            for col in range(self.__width):
                for n_r, n_c in self.__getneighborpoints((row, col)):
                    if self.__grid[row][col] >= self.__grid[n_r][n_c]:
                        break
                else:
                    yield row, col

    def __findbasinpoints(self, lowpoint: Point) -> list[Point]:
        visited = []
        searchqueue = [lowpoint]
        while searchqueue:
            current = searchqueue.pop(0)
            if current not in visited:
                for n_r, n_c in self.__getneighborpoints(current):
                    if (n_r, n_c) not in visited and self.__grid[n_r][n_c] < 9:
                        searchqueue.append((n_r, n_c))
                visited.append(current)
        return visited

    def getlowpointscore(self) -> int:
        """Gives the answer to Part 1."""
        return sum([self.__grid[row][col] + 1 for row, col in self.__findlowpoints()])

    def getbasinscore(self) -> int:
        """Gives the answer to Part 1."""
        basinsizelist = sorted([len(self.__findbasinpoints(lp)) for lp in self.__lowpoints], reverse=True)
        return basinsizelist[0] * basinsizelist[1] * basinsizelist[2]


def main() -> int:
    with open('../Inputfiles/aoc9.txt', 'r') as file:
        mygrid = Grid(file.read().strip('\n').splitlines())
    print(f"Part 1: {mygrid.getlowpointscore()}")
    print(f"Part 2: {mygrid.getbasinscore()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
