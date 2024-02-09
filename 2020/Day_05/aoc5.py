"""
Basically just decode the data as specified and store in a sorted list. The last item will be the largest and thus
the answer to Part 1, then loop through the list to find a gap in the ID:s which will be the answer to Part 2.
"""
import sys


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


def main() -> int:
    with open('../Inputfiles/aoc5.txt', 'r') as file:
        lines = file.read().strip('\n').splitlines()
    seat_ids = sorted([decode_seat_id(line[0:7], line[7:10]) for line in lines])
    print("Part 1:", seat_ids[-1])
    while len(seat_ids) > 1:
        if seat_ids[1] == seat_ids[0] + 2:
            print("Part 2:", seat_ids[1] - 1)
            break
        seat_ids.pop(0)
    return 0


if __name__ == "__main__":
    sys.exit(main())
