"""
Stores the SNAFU value in a simple class which then implements the 'add' function, which adds two SNAFU numbers
directly without converting to/from decimal. Then simply add all the numbers read from the input data.
"""
import sys
from itertools import zip_longest


class SNAFU:
    strtoint_map = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}
    inttostr_map = {v: k for k, v in strtoint_map.items()}

    def __init__(self, nbrstr: str):
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


def main() -> int:
    with open('../Inputfiles/aoc25.txt', 'r') as file:
        snafu_nbrs = [SNAFU(line) for line in file.read().strip('\n').splitlines()]
    p1 = SNAFU('0')
    for sn in snafu_nbrs:
        p1 += sn
    print(f"Part 1: {p1}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
