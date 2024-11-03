# Boilerplate template - update the XX in INPUT_FILE to correct day.
import time
from pathlib import Path


def main(aoc_input: str) -> None:
    print(f"Part 1: {aoc_input}")
    print(f"Part 2: {aoc_input}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2024/dayXX.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
