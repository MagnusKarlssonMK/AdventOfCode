"""
Part 1: Straightforward - just search the preamble for a valid combination of two numbers that adds up to the following
number, and gradually move the preamble forwards until an invalid number is found.
Part 2: Scan through the list with a window in the form of a queue, adding numbers from the list until its sum is
larger than the target value, then popping the oldest values from the window until it is again smaller. Break when
the sum is equal to the target value, sort the values in the window and get the answer from the sum of the smallest
and the largest value.
"""
import sys


def validatenumber(preamble: list[int], nbr: int) -> bool:
    for i in range(len(preamble) - 1):
        for j in range(i + 1, len(preamble)):
            if preamble[i] + preamble[j] == nbr:
                return True
    return False


class XMAS:
    __PREAMBLE_LENGTH = 25  # Change to 5 if running the example input

    def __init__(self, rawstr: str) -> None:
        self.__nbrs = list(map(int, rawstr.splitlines()))
        self.__invalid_nbr = -1

    def get_invalid_nbr(self) -> int:
        preamble = [self.__nbrs[i] for i in range(XMAS.__PREAMBLE_LENGTH)]
        for i in range(XMAS.__PREAMBLE_LENGTH, len(self.__nbrs)):
            if not validatenumber(preamble, self.__nbrs[i]):
                self.__invalid_nbr = self.__nbrs[i]
                break
            preamble.pop(0)
            preamble.append(self.__nbrs[i])
        return self.__invalid_nbr

    def get_encryption_weakness(self) -> int:
        window = [self.__nbrs[0]]
        idx = 0
        while idx < len(self.__nbrs):
            if (wsum := sum(window)) == self.__invalid_nbr:
                windowsort = sorted(window)
                return windowsort[0] + windowsort[-1]
            if wsum > self.__invalid_nbr:
                window.pop(0)
            else:
                idx += 1
                window.append(self.__nbrs[idx])
        return -1


def main() -> int:
    with open('../Inputfiles/aoc9.txt', 'r') as file:
        xmas = XMAS(file.read().strip('\n'))
    print(f"Part 1: {xmas.get_invalid_nbr()}")
    print(f"Part 2: {xmas.get_encryption_weakness()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
