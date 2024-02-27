import sys


XYZ = tuple[int, int, int]


def get_adjacent(point: XYZ) -> iter:
    for p in ((0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)):
        yield tuple(sum(x) for x in zip(point, p))


class Lavapool:
    def __init__(self, indata):
        self.__adj: dict[XYZ: list[XYZ]] = {}
        for point in indata:
            self.__adj[point] = [p for p in get_adjacent(point) if p in indata]

    def get_surfacearea(self) -> int:
        return sum([6 - len(adj) for adj in list(self.__adj.values())])


def main() -> int:
    with open('../Inputfiles/aoc18.txt', 'r') as file:
        pool = Lavapool([tuple(map(int, line.split(','))) for line in file.read().strip('\n').splitlines()])
    print("Part 1:", pool.get_surfacearea())
    return 0


if __name__ == "__main__":
    sys.exit(main())
