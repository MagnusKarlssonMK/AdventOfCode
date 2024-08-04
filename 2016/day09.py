"""
Recursive solution with regex, checking if there is a repeat marker in the first character in the current string. If
so, return the length of the repeated segment plus the remaining length recursively, otherwiste step forward one step
and try again.
For Part 2, instead of just calculating the length, use a recursive call again instead.
"""
import sys
from pathlib import Path
import re

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2016/day09.txt')


def get_decompressed_len(compressed: str, version2: bool = False) -> int:
    def len_func(segment: str):
        if version2:
            return get_decompressed_len(segment, version2)
        else:
            return len(segment)

    if not compressed:
        return 0
    if match := re.match(r"\((\d+)x(\d+)\)", compressed):
        count, repeat = list(map(int, match.groups()))
        multiply_start = match.end()
        multiply_end = multiply_start + count
        return ((len_func(compressed[multiply_start: multiply_end]) * repeat) +
                get_decompressed_len(compressed[multiply_end:], version2))
    else:
        # No match at start of string, move one step forward and try again
        return 1 + get_decompressed_len(compressed[1:], version2)


def main() -> int:
    with open(INPUT_FILE) as file:
        decompr = file.read().strip('\n')
    print(f"Part 1: {get_decompressed_len(decompr)}")
    print(f"Part 2: {get_decompressed_len(decompr, True)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
