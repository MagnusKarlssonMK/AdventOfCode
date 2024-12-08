import time
from pathlib import Path
from dataclasses import dataclass
from itertools import combinations


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def get_anti_points(self, other: "Point", harmonic: int) -> tuple["Point", "Point"]:
        return (Point(self.x + harmonic * (self.x - other.x), self.y + harmonic * (self.y - other.y)),
                Point(other.x + harmonic * (other.x - self.x), other.y + harmonic * (other.y - self.y)))


class Antennas:
    def __init__(self, rawstr: str) -> None:
        self.__height = 0
        self.__width = 0
        self.__antennas: dict[str: list[Point]] = {}
        for y, line in enumerate(rawstr.splitlines()):
            self.__height += 1
            if y == 0:
                self.__width = len(line)
            for x, c in enumerate(line):
                if c != '.':
                    if c in self.__antennas:
                        self.__antennas[c].append(Point(x, y))
                    else:
                        self.__antennas[c] = [Point(x, y)]

    def get_antinode_counts(self) -> tuple[int, int]:
        antinodes: set[Point] = set()
        antinodes_w_harmonics: set[Point] = set()
        for antennas in self.__antennas.values():
            for a1, a2 in combinations(antennas, 2):
                inside = True
                harmonic = 0
                while inside:
                    inside = False
                    an1, an2 = a1.get_anti_points(a2, harmonic)
                    if 0 <= an1.x < self.__width and 0 <= an1.y < self.__height:
                        inside = True
                        if harmonic == 1:
                            antinodes.add(an1)
                        antinodes_w_harmonics.add(an1)
                    if 0 <= an2.x < self.__width and 0 <= an2.y < self.__height:
                        inside = True
                        if harmonic == 1:
                            antinodes.add(an2)
                        antinodes_w_harmonics.add(an2)
                    harmonic += 1
        return len(antinodes), len(antinodes_w_harmonics)


def main(aoc_input: str) -> None:
    ant = Antennas(aoc_input)
    p1, p2 = ant.get_antinode_counts()
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2024/day08.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
