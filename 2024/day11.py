import time
from pathlib import Path
from math import log10
from collections import defaultdict


class Stones:
    def __init__(self, rawstr: str) -> None:
        self.__stones = [int(n) for n in rawstr.split()]

    def get_stone_count(self, blinks1: int, blinks2: int) -> int:
        results = []
        blink_counter = 0
        stones: dict[int: int] = {s: 1 for s in self.__stones}
        while len(results) < 2:
            blink_counter += 1
            stones = blink(stones)
            if blink_counter in (blinks1, blinks2):
                results.append(sum(stones.values()))
        return tuple(results)


def blink(stones: dict[int: int]) -> tuple[int, int]:
    newstones: dict[int: int] = defaultdict(int)
    for stone, amount in stones.items():
        if stone == 0:
            newstones[1] += amount
        else:
            if int(digits := 1 + log10(stone)) % 2 == 0:
                power = 10**(digits // 2)
                newstones[stone // power] += amount
                newstones[stone % power] += amount
            else:
                newstones[stone * 2024] += amount
    return newstones


def main(aoc_input: str) -> None:
    stones = Stones(aoc_input)
    p1, p2 = stones.get_stone_count(25, 75)
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2024/day11.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
