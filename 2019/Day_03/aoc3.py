"""
Stores the wires in a class which can return all its coordinates from an iterable function. For part 1, we can then
find all intersections by putting those coordinates in sets for both wires and then find the common points, and the
answer is given by the smallest manhattan distance from origin to intersection. For Part 2, we can get the distance
by counting the number of coordinates in the list.
"""
import sys


class Wire:
    def __init__(self, wiredata: list[str]):
        dirmap = {'R': (0, 1), 'L': (0, -1), 'U': (-1, 0), 'D': (1, 0)}
        self.points = [(dirmap[step[0]], int(step[1:])) for step in wiredata]
        self.coordinates = [c for c in self.__get_coordinates()]

    def __get_coordinates(self) -> iter:
        current = 0, 0
        for point in self.points:
            for _ in range(point[1]):
                current = tuple(map(sum, zip(current, point[0])))
                yield current


def main() -> int:
    with open('../Inputfiles/aoc3.txt', 'r') as file:
        wires = [Wire(w) for w in [line.split(',') for line in file.read().strip('\n').splitlines()]]
    intersections = set(wires[0].coordinates) & set(wires[1].coordinates)
    print("Part 1:", min([abs(w[0]) + abs(w[1]) for w in intersections if w != (0, 0)]))
    print("Part 2:", min([sum([1 + wire.coordinates.index(i) for wire in wires]) for i in intersections]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
