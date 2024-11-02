"""
So we're basically building a hasher. I probably spent 98% of the time on this problem just trying to understand the
description, but the actual coding of it is mostly straightforward.
"""
import time
from pathlib import Path


class KnotHasher:
    __NBR_OF_ELEMENTS = 256

    def __init__(self) -> None:
        self.__current_pos = 0
        self.__skipsize = 0

    def __generate_hash(self, input_list: list[int], lengths: list[int]) -> list[int]:
        nbrs = [i for i in input_list]
        for length in lengths:
            if length > len(nbrs):
                continue
            buffer = [nbrs[n % len(nbrs)] for n in range(self.__current_pos, self.__current_pos + length)]
            while buffer:
                nbrs[self.__current_pos] = buffer.pop()
                self.__current_pos = (self.__current_pos + 1) % len(nbrs)
            self.__current_pos = (self.__current_pos + self.__skipsize) % len(nbrs)
            self.__skipsize += 1
        return nbrs

    def get_test_multiple(self, input_vec: list[int]) -> int:
        nbrs = [i for i in range(KnotHasher.__NBR_OF_ELEMENTS)]
        nbrs = self.__generate_hash(nbrs, input_vec)
        self.__current_pos = 0
        self.__skipsize = 0
        return nbrs[0] * nbrs[1]

    def get_knot_hash(self, input_vec: list[int]) -> str:
        sparse = [i for i in range(KnotHasher.__NBR_OF_ELEMENTS)]
        for _ in range(64):
            sparse = self.__generate_hash(sparse, input_vec)
        self.__current_pos = 0
        self.__skipsize = 0

        dense = []
        for block_idx in range(0, 256, 16):
            val = sparse[block_idx]
            for i in range(1, 16):
                val ^= sparse[block_idx + i]
            dense.append(val)

        return ''.join([f"{v:0>2x}" for v in dense])  # Convert to hex representation and enforce two digits


def parse_input(rawstr: str, use_ascii: bool = False) -> list[int]:
    if use_ascii:
        return [ord(c) for c in rawstr] + [17, 31, 73, 47, 23]
    else:
        result = []
        for c in rawstr.split(','):
            if c.isdigit():
                result.append(int(c))
            else:  # Just in case we're passing in some non-integer strings for testing part 2
                result.append(0)
        return result


def main(aoc_input: str) -> None:
    knot = KnotHasher()
    print(f"Part 1: {knot.get_test_multiple(parse_input(aoc_input))}")
    print(f"Part 2: {knot.get_knot_hash(parse_input(aoc_input, True))}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2017/day10.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
