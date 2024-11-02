"""
Key point here is that the min and max values in each direction forms a "frame", and any location outside that will
extend to infinity. I.e. any coordinate having a location as 'closest' on or outside that area will have an infinite
area.
"""
import time
from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class Coord:
    x: int
    y: int

    def get_distance(self, other: "Coord") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


class ChronalMap:
    def __init__(self, rawstr: str) -> None:
        self.__coordinates = [Coord(*list(map(int, line.split(', ')))) for line in rawstr.splitlines()]
        self.__x_range = range(self.__coordinates[0].x, self.__coordinates[0].x + 1)
        self.__y_range = range(self.__coordinates[0].y, self.__coordinates[0].y + 1)
        for c in self.__coordinates:
            self.__x_range = range(min(c.x, self.__x_range.start), max(c.x + 1, self.__x_range.stop))
            self.__y_range = range(min(c.y, self.__y_range.start), max(c.y + 1, self.__y_range.stop))

    def __get_locations(self) -> iter:
        for x in self.__x_range:
            for y in self.__y_range:
                yield Coord(x, y)

    def get_largest_area_size(self) -> int:
        areas: dict[Coord: set[Coord]] = {}
        # Find areas for each coordinate, i.e. coordinates that have the closest manhattan distance to only that coord
        for loc in self.__get_locations():
            distances = sorted([(loc.get_distance(c), i) for i, c in enumerate(self.__coordinates)], key=lambda x: x[0])
            if len(distances) == 1 or distances[0][0] < distances[1][0]:
                if self.__coordinates[distances[0][1]] not in areas:
                    areas[self.__coordinates[distances[0][1]]] = set()
                areas[self.__coordinates[distances[0][1]]].add(loc)
        # Remove the coords that have infinite areas, i.e. are located on the range border
        infinite_areas = set()
        for a in areas:
            for c in areas[a]:
                if any([c.x == self.__x_range.start, c.x == self.__x_range.stop - 1,
                        c.y == self.__y_range.start, c.y == self.__y_range.stop - 1]):
                    infinite_areas.add(a)
                    break
        for i in infinite_areas:
            areas.pop(i)
        return max(len(areas[a]) for a in areas)

    def get_most_surrounded_size(self, max_total_distance: int = 10_000) -> int:
        # For each location, find the total distance to all coordinates and see if it is smaller than max
        return sum([1 for loc in self.__get_locations()
                    if sum([loc.get_distance(c) for c in self.__coordinates]) < max_total_distance])


def main(aoc_input: str) -> None:
    c_map = ChronalMap(aoc_input)
    print(f"Part 1: {c_map.get_largest_area_size()}")
    print(f"Part 2: {c_map.get_most_surrounded_size()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2018/day06.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
