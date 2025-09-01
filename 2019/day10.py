"""
Use atan2 to calculate angles between asteroids, with some extra trickery to compensate for the 'upside-down'
coordinate system.
"""
import time
from pathlib import Path
from dataclasses import dataclass
from math import atan2, degrees


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def get_angle(self, other: "Point") -> float:
        return (degrees(atan2(self.y - other.y, self.x - other.x)) + 270) % 360  # Rotate so that 0 is north

    def get_distance(self, other: "Point") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


class AsteriodMap:
    def __init__(self, rawstr: str) -> None:
        self.__asteroids = [Point(x, y) for y, line in enumerate(rawstr.splitlines())
                            for x, c in enumerate(line) if c == '#']
        self.__best: Point = Point(-1, -1)

    def get_best_asteroid_count(self) -> int:
        result = 0
        for a in self.__asteroids:
            if (visible := len(set([a.get_angle(other) for other in self.__asteroids if other != a]))) > result:
                result = visible
                self.__best = a
        return result

    def get_winning_asteroid(self) -> int:
        visible: dict[float, list[tuple[Point, int]]] = {}
        for a in self.__asteroids:
            if a != self.__best:
                if (angle := self.__best.get_angle(a)) not in visible:
                    visible[angle] = [(a, self.__best.get_distance(a))]
                else:
                    visible[angle].append((a, self.__best.get_distance(a)))
        for angle in visible:  # Sort by distance
            visible[angle].sort(key=lambda x: x[1])
        angles = sorted(list(visible.keys()))
        idx = 0
        winner = Point(-1, -1)
        for _ in range(200):
            winner, _ = visible[angles[idx]].pop(0)
            if not visible[angles[idx]]:
                angles.pop(idx)
                idx -= 1
            idx = (idx + 1) % len(angles)
        return (100 * winner.x) + winner.y


def main(aoc_input: str) -> None:
    asteroids = AsteriodMap(aoc_input)
    print(f"Part 1: {asteroids.get_best_asteroid_count()}")
    print(f"Part 2: {asteroids.get_winning_asteroid()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2019/day10.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
