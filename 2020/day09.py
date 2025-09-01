"""
Part 1: Straightforward - just search the preamble for a valid combination of two numbers that adds up to the following
number, and gradually move the preamble forwards until an invalid number is found.
Part 2: Scan through the list with a window in the form of a queue, adding numbers from the list until its sum is
larger than the target value, then popping the oldest values from the window until it is again smaller. Break when
the sum is equal to the target value, sort the values in the window and get the answer from the sum of the smallest
and the largest value.
"""
import time
from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class Number:
    value: int

    def validatenumber(self, preamble: list[int]) -> bool:
        for i in range(len(preamble) - 1):
            for j in range(i + 1, len(preamble)):
                if preamble[i] + preamble[j] == self.value:
                    return True
        return False


class XMAS:
    __preamble_length = 25

    def __init__(self, rawstr: str) -> None:
        self.__nbrs = [Number(int(c)) for c in rawstr.splitlines()]
        self.__invalid_nbr = -1
        if len(self.__nbrs) < 25:
            XMAS.__preamble_length = 5  # Assume test input for smaller inputs

    def get_invalid_nbr(self) -> int:
        preamble = [self.__nbrs[i].value for i in range(XMAS.__preamble_length)]
        for i in range(XMAS.__preamble_length, len(self.__nbrs)):
            if not self.__nbrs[i].validatenumber(preamble):
                self.__invalid_nbr = self.__nbrs[i].value
                break
            preamble.pop(0)
            preamble.append(self.__nbrs[i].value)
        return self.__invalid_nbr

    def get_encryption_weakness(self) -> int:
        window = [self.__nbrs[0].value]
        idx = 0
        while idx < len(self.__nbrs):
            if (wsum := sum(window)) == self.__invalid_nbr:
                windowsort = sorted(window)
                return windowsort[0] + windowsort[-1]
            if wsum > self.__invalid_nbr:
                window.pop(0)
            else:
                idx += 1
                window.append(self.__nbrs[idx].value)
        return -1


def main(aoc_input: str) -> None:
    xmas = XMAS(aoc_input)
    print(f"Part 1: {xmas.get_invalid_nbr()}")
    print(f"Part 2: {xmas.get_encryption_weakness()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2020/day09.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
