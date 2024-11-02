"""
Part 1 fairly straightforward simulation, just a bit fiddly to get the signs of gravity and velocity calculations
correct.
For part 2, find the individual cycles for the x, y, z directions separately, since they are independent, and then
use LCM to calculate the total cycle.
"""
import time
from pathlib import Path
import re
from dataclasses import dataclass
from itertools import combinations
from math import lcm
from copy import deepcopy


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    def __get_point(self) -> tuple[int, int, int]:
        return self.x, self.y, self.z

    def gravity(self, other: "Point") -> "Point":
        a = zip(self.__get_point(), other.__get_point())
        b = [0 if s == o else abs(o - s) // (o - s) for s, o in a]
        return Point(*b)

    def energy(self) -> int:
        return sum([abs(v) for v in self.__get_point()])

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)


@dataclass
class Moon:
    position: Point
    velocity: Point

    def apply_gravity(self, other: "Moon") -> None:
        self.velocity += self.position.gravity(other.position)

    def step(self) -> None:
        self.position += self.velocity

    def get_energy(self) -> int:
        return self.position.energy() * self.velocity.energy()

    def compare_dimensions(self, other: "Moon") -> tuple[bool, bool, bool]:
        x = (self.position.x == other.position.x) and (self.velocity.x == other.velocity.x)
        y = (self.position.y == other.position.y) and (self.velocity.y == other.velocity.y)
        z = (self.position.z == other.position.z) and (self.velocity.z == other.velocity.z)
        return x, y, z


class MoonTracker:
    def __init__(self, rawstr: str) -> None:
        self.__scans = [Point(x, y, z) for x, y, z in
                        [list(map(int, re.findall(r"-?\d+", line))) for line in rawstr.splitlines()]]

    def get_total_energy(self) -> int:
        moons = [Moon(start, Point(0, 0, 0)) for start in self.__scans]
        for _ in range(1000):
            for m1, m2 in combinations(moons, 2):
                m1.apply_gravity(m2)
                m2.apply_gravity(m1)
            for m in moons:
                m.step()
        return sum(m.get_energy() for m in moons)

    def get_cycle_length(self) -> int:
        moons = [Moon(start, Point(0, 0, 0)) for start in self.__scans]
        start = deepcopy(moons)
        cycles = [0, 0, 0]
        count = 0
        while any([c == 0 for c in cycles]):
            count += 1
            for m1, m2 in combinations(moons, 2):
                m1.apply_gravity(m2)
                m2.apply_gravity(m1)
            matches = [True, True, True]
            for i, m in enumerate(moons):
                m.step()
                compare = m.compare_dimensions(start[i])
                matches = [x and y for x, y in zip(matches, compare)]

            for i in range(len(matches)):
                if cycles[i] == 0 and matches[i]:
                    cycles[i] = count

        return lcm(*cycles)


def main(aoc_input: str) -> None:
    tracker = MoonTracker(aoc_input)
    print(f"Part 1: {tracker.get_total_energy()}")
    print(f"Part 2: {tracker.get_cycle_length()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2019/day12.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
