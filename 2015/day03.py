import time
from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class Coordinate:
    x: int = 0
    y: int = 0

    def __add__(self, other: "Coordinate") -> "Coordinate":
        return Coordinate(self.x + other.x, self.y + other.y)


class Santa:
    __DIRMAP = {'^': (0, 1), '>': (1, 0), 'v': (0, -1), '<': (-1, 0)}

    def __init__(self, rawstr: str) -> None:
        self.__instructions = rawstr

    def get_uniquehouses_count(self, use_robot: bool = False) -> int:
        santa_pos = [Coordinate()]
        if use_robot:
            santa_pos.append(Coordinate())
        houses: set[Coordinate] = {santa_pos[0]}
        for i, c in enumerate(self.__instructions):
            santa_pos[i % len(santa_pos)] += Coordinate(*Santa.__DIRMAP[c])
            houses.add(santa_pos[i % len(santa_pos)])
        return len(houses)


def main(aoc_input: str) -> None:
    santa = Santa(aoc_input)
    print(f"Part 1: {santa.get_uniquehouses_count()}")
    print(f"Part 2: {santa.get_uniquehouses_count(True)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2015/day03.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
