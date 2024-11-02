"""
Stores the SNAFU value in a simple class which then implements the 'add' function, which adds two SNAFU numbers
directly without converting to/from decimal. Then simply add all the numbers read from the input data.
"""
import time
from pathlib import Path
from itertools import zip_longest


class SNAFU:
    strtoint_map = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}
    inttostr_map = {v: k for k, v in strtoint_map.items()}

    def __init__(self, nbrstr: str) -> None:
        self.nbr = [self.strtoint_map[c] for c in reversed(nbrstr)]
        # Store the number "backwards" so the first number in the list is the least significant value and so on
        # That way, the index in the list will correspond to the power coefficient for that same column

    def __add__(self, other: "SNAFU"):
        retval = SNAFU('')  # Temporary just for testing
        combined = list(map(sum, zip_longest(self.nbr, other.nbr, fillvalue=0)))
        carry = 0
        for c in combined:
            val = carry + c
            if val > 2:
                carry = 1
            elif val < -2:
                carry = -1
            else:
                carry = 0
            retval.nbr.append(((val + 2) % 5) - 2)
        if carry != 0:
            retval.nbr.append(carry)
        return retval

    def __str__(self):
        return ''.join([self.inttostr_map[i] for i in reversed(self.nbr)])


class FuelRequirements:
    def __init__(self, rawstr: str) -> None:
        self.__snafus = [SNAFU(line) for line in rawstr.splitlines()]

    def get_console_nbr(self) -> SNAFU:
        result = SNAFU('0')
        for sn in self.__snafus:
            result += sn
        return result


def main(aoc_input: str) -> None:
    reqs = FuelRequirements(aoc_input)
    print(f"Part 1: {reqs.get_console_nbr()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2022/day25.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
