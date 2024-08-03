"""
Part 1: Straight up the Josephus problem. By using binary representation, the answer can be found by shifting the most
significant 1 to the end.

Part 2: Modified variant of the Josephus problem. It can be solved in a similar manner by converting to base-3 number
and then doig similar modifications, but it gets quite a bit more complicated. Instead, find the largest power of 3
that is still smaller than the target, and then the answer can be found based on that. In short, the pattern resets
with 1 as winner on every 'new' / added digit in the base-3 representation (4, 10, 28...); in the first half in-between
those numbers, the winning number is incremented by 1, while in the second half the winning number is incremented by 2.
"""
import sys


def get_winning_elf(nbr_elfs: int) -> int:
    # Note: the bin() conversion adds 0b at the start of the string; we want to skip those two characters.
    return int(bin(nbr_elfs)[3:] + bin(nbr_elfs)[2], 2)


def get_winning_elf_opposite(nbr_elfs: int) -> int:
    if nbr_elfs <= 2:
        return 1
    # Find the largest power of 3 smaller than the number of elfs
    b3_p = 1
    while 3 * b3_p < nbr_elfs:
        b3_p *= 3
    # If nbr of elfs in the 'lower half' of the interval between base-3 values, the anwer starts on 1 and increases by 1
    if nbr_elfs <= 2 * b3_p:
        return nbr_elfs - b3_p
    else:  # If the nbr of elfs is in the 'upper half', the answer increases by 2 for each number
        if (rem := nbr_elfs % b3_p) == 0:
            rem = b3_p
        return nbr_elfs - b3_p + rem


def main() -> int:
    with open('../Inputfiles/aoc19.txt', 'r') as file:
        nbr = int(file.read().strip('\n'))
    print(f"Part 1: {get_winning_elf(nbr)}")
    print(f"Part 2: {get_winning_elf_opposite(nbr)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
