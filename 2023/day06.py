"""
Uses quadratic formula to calculate the two points where the score intersects the old record. One of the surprising
challenges was to round them off in the right direction, to also account for the few cases where the solution was
exactly the same value as the old record.
"""
import time
from pathlib import Path
from dataclasses import dataclass
import math
import re


@dataclass(frozen=True)
class Race:
    time: int
    distance: int

    def get_score(self) -> int:
        minvelocity = math.floor((self.time - math.sqrt(self.time**2 - (4 * self.distance))) / 2) + 1
        maxvelocity = math.ceil((self.time + math.sqrt(self.time**2 - (4 * self.distance))) / 2) - 1
        return 1 + maxvelocity - minvelocity


class Competition:
    def __init__(self, rawstr: str) -> None:
        t, d = rawstr.splitlines()
        timelist = list(map(int, re.findall(r"\d+", t)))
        distancelist = list(map(int, re.findall(r"\d+", d)))
        self.__races = [Race(timelist[idx], distancelist[idx]) for idx, _ in enumerate(timelist)]

    def get_race_product(self) -> int:
        return math.prod([race.get_score() for race in self.__races])

    def get_megarace_score(self) -> int:
        t = int(''.join([str(race.time) for race in self.__races]))
        d = int(''.join([str(race.distance) for race in self.__races]))
        megarace = Race(t, d)
        return megarace.get_score()


def main(aoc_input: str) -> None:
    myrace = Competition(aoc_input)
    print(f"Part 1: {myrace.get_race_product()}")
    print(f"Part 2: {myrace.get_megarace_score()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2023/day06.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
