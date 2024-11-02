import time
from pathlib import Path


class Directions:
    def __init__(self, rawstr: str) -> None:
        self.__steps = [1 if c == '(' else -1 for c in rawstr]

    def get_final_floor(self) -> int:
        return sum(self.__steps)

    def get_basement_step(self) -> int:
        floor = 0
        for i, v in enumerate(self.__steps):
            floor += v
            if floor < 0:
                return i + 1
        return -1


def main(aoc_input: str) -> None:
    directions = Directions(aoc_input)
    print(f"Part 1: {directions.get_final_floor()}")
    print(f"Part 2: {directions.get_basement_step()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2015/day01.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")

