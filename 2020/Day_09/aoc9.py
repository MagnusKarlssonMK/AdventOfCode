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


def main() -> int:
    with open('../Inputfiles/aoc9.txt', 'r') as file:
        nbrs = list(map(int, file.read().strip('\n').splitlines()))
    preamble_len = 25  # Change to 5 if running the example input
    preamble = [nbrs[i] for i in range(preamble_len)]
    invalid_nbr = -1
    for i in range(preamble_len, len(nbrs)):
        if not validatenumber(preamble, nbrs[i]):
            invalid_nbr = nbrs[i]
            break
        preamble.pop(0)
        preamble.append(nbrs[i])
    print("Part 1:", invalid_nbr)
    window = [nbrs[0]]
    idx = 0
    while idx < len(nbrs):
        if (wsum := sum(window)) == invalid_nbr:
            windowsort = sorted(window)
            print("Part 2:", windowsort[0] + windowsort[-1])
            break
        if wsum > invalid_nbr:
            window.pop(0)
        else:
            idx += 1
            window.append(nbrs[idx])
    return 0


if __name__ == "__main__":
    sys.exit(main())
