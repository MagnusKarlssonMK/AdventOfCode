"""
Basically just decode the data as specified and store in a sorted list. The last item will be the largest and thus
the answer to Part 1, then loop through the list to find a gap in the ID:s which will be the answer to Part 2.
"""
import time
from pathlib import Path


def decode(s: str, up: str, low: str, rng: range) -> int:
    lower, upper = rng.start, rng.stop
    for i in range(len(s)):
        if s[i] == up:
            upper -= (1 + upper - lower) // 2
        elif s[i] == low:
            lower += (1 + upper - lower) // 2
    return lower


def decode_seat_id(rows: str, cols: str) -> int:
    return 8 * decode(rows, 'F', 'B', range(127)) + decode(cols, 'L', 'R', range(7))


class Scanner:
    def __init__(self, rawstr: str) -> None:
        self.__boardingpasses = sorted([decode_seat_id(line[0:7], line[7:10]) for line in rawstr.splitlines()])

    def get_highest_seat(self) -> int:
        return self.__boardingpasses[-1]

    def get_seat_id(self) -> int:
        seat_ids = list(self.__boardingpasses)
        while len(seat_ids) > 1:
            if seat_ids[1] == seat_ids[0] + 2:
                return seat_ids[1] - 1
            seat_ids.pop(0)
        return -1


def main(aoc_input: str) -> None:
    passes = Scanner(aoc_input)
    print(f"Part 1: {passes.get_highest_seat()}")
    print(f"Part 2: {passes.get_seat_id()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2020/day05.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
