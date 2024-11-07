"""
Part 1: Simply take the sum of the numbers.
Part 2: Iterate through the numbers, updating the frequency and storing it in a set, and break when finding a
repetition.
"""
import time
from pathlib import Path


class Device:
    def __init__(self, rawstr: str) -> None:
        self.__nbrs = [int(nbr.strip('+')) for nbr in rawstr.splitlines()]

    def get_frequency(self) -> int:
        return sum(self.__nbrs)

    def get_calibration_value(self) -> int:
        i = 0
        freq = 0
        seen = {freq}
        while True:
            freq += self.__nbrs[i]
            if freq in seen:
                break
            seen.add(freq)
            i = (i + 1) % len(self.__nbrs)
        return freq


def main(aoc_input: str) -> None:
    device = Device(aoc_input)
    print(f"Part 1: {device.get_frequency()}")
    print(f"Part 2: {device.get_calibration_value()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2018/day01.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
