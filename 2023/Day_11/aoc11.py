"""
Stores the coordinates of galaxies in a Space class, and also generates lists of empty rows and columns. For Part 1,
the distance is then calculated with the manhattan distance between each pair of galaxies, and for each pair also
checking the number of empty rows/columns between them. Since the grid input doesn't change between Part 1 & 2 other
than the scaling of empty space, we can store the result from Part 1 as [manhattan distance, nbr of empty spaces] and
re-use that for a lightning fast Part 2.
"""
import sys
import re


class Space:
    def __init__(self, spaceinput: list[str], e_rate: int = 2):
        self.galaxies: list[tuple[int, int]] = []  # Row, Col
        self.__expansionrate = e_rate
        for idx, line in enumerate(spaceinput):
            [self.galaxies.append((idx, g.start())) for g in re.finditer(r"#", line)]
        rows = set([c[0] for c in self.galaxies])
        cols = set([c[1] for c in self.galaxies])
        self.__emptyrows = [r for r in range(max(rows)) if r not in rows]
        self.__emptycols = [c for c in range(max(rows)) if c not in cols]
        self.__distancecache = [-1, -1]

    def set_expansionrate(self, newrate: int) -> None:
        self.__expansionrate = newrate

    def get_distancesum(self) -> int:
        retval = 0
        emptyspace = 0
        if self.__distancecache[0] < 0:
            for i in range(len(self.galaxies) - 1):
                for j in range(i + 1, len(self.galaxies)):
                    rowrange = (min(self.galaxies[i][0], self.galaxies[j][0]),
                                max(self.galaxies[i][0], self.galaxies[j][0]))
                    colrange = (min(self.galaxies[i][1], self.galaxies[j][1]),
                                max(self.galaxies[i][1], self.galaxies[j][1]))
                    emptyspace += (sum([1 for r in self.__emptyrows if rowrange[0] < r < rowrange[1]]) +
                                   sum([1 for c in self.__emptycols if colrange[0] < c < colrange[1]]))
                    retval += rowrange[1] - rowrange[0] + colrange[1] - colrange[0]
            self.__distancecache[0] = retval
            self.__distancecache[1] = emptyspace
        return self.__distancecache[0] + (self.__expansionrate - 1) * self.__distancecache[1]


def main() -> int:
    with open('../Inputfiles/aoc11.txt', 'r') as file:
        space = Space(file.read().strip('\n').splitlines())
    print("Part 1:", space.get_distancesum())
    space.set_expansionrate(1000000)
    print("Part 2:", space.get_distancesum())
    return 0


if __name__ == "__main__":
    sys.exit(main())
