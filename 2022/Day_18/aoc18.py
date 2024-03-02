"""
Store the cubes in a dict pointing to a list of surrounding non-cube points. The answer to Part 1 is given by the
sum of number of such points.
For Part 2, use BFS to walk the surrounding 'air' points and see which ones are unreachable. Start from a point
which is guaranteed to be exterior, which can be given by the point with the smallest value in any axis (x-axis is
used here). Store the enclosed nodes and use as filter for calculating the surface area. BUT - to be able to walk
around 'corners', we need to add some additional air nodes, just not the diagonal ones, and then ignore them at the end
when calculating the number of enclosed nodes.
"""
import sys


XYZ = tuple[int, int, int]


def get_adjacent(point: XYZ) -> iter:
    for delta in ((0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)):
        yield tuple(sum(x) for x in zip(point, delta))


def get_additionalair(point: XYZ) -> iter:
    for delta in ((0, 1, 1), (0, 1, -1), (0, -1, 1), (0, -1, -1),
                  (1, 0, 1), (-1, 0, 1), (1, 0, -1), (-1, 0, -1),
                  (1, 1, 0), (-1, 1, 0), (1, -1, 0), (-1, -1, 0)):
        yield tuple(sum(x) for x in zip(point, delta))


class Lavapool:
    def __init__(self, indata):
        self.__adj: dict[XYZ: list[XYZ]] = {}
        start: XYZ = (999, 999, 999)
        air = set()
        for point in indata:
            self.__adj[point] = []
            for adj in get_adjacent(point):
                if adj not in indata:
                    self.__adj[point].append(adj)
                    air.add(adj)
                    if adj[0] < start[0]:
                        start = adj
            for additional_air in get_additionalair(point):
                if additional_air not in indata:
                    air.add(additional_air)
        # Use BFS on the air from the start point which is guaranteed to be exterior, and any unreachable points are
        # interior pockets.
        queue = [start]
        seen = set()
        while queue:
            current = queue.pop(0)
            if current in seen:
                continue
            for adj_air in get_adjacent(current):
                if adj_air in air:
                    queue.append(adj_air)
            seen.add(current)
            air.remove(current)
        self.enclosedair = 0
        for key in self.__adj:
            for a in air:
                if a in self.__adj[key]:
                    self.enclosedair += 1

    def get_surfacearea(self, remove_interior: bool = False) -> int:
        result = sum([len(adj) for adj in list(self.__adj.values())])
        if remove_interior:
            result -= self.enclosedair
        return result


def main() -> int:
    with open('../Inputfiles/aoc18.txt', 'r') as file:
        pool = Lavapool([tuple(map(int, line.split(','))) for line in file.read().strip('\n').splitlines()])
    print("Part 1:", pool.get_surfacearea())
    print("Part 2:", pool.get_surfacearea(True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
