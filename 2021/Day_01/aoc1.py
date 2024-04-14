"""
Part 1: Simply parse the input to a list, and loop through the list comparing elements and counting the number of times
the depth increases.
Part 2: Keep a buffer of 3 values and compare for each step and count the number of times the sum of the buffer
increases from one time to the next.
"""
import sys


def count_depth_increase(nbrlist: list[int]) -> int:
    """Returns the answer to Part 1."""
    return sum([int(nbrlist[n] > nbrlist[n-1]) for n in range(1, len(nbrlist))])


def count_window_depth_increase(nbrlist: list[int]) -> int:
    """Returns the answer to Part 2."""
    window_buffer = []
    previous = 999999  # Initialize to something large to make sure we don't count the first window as an increase.
    inc_count = 0
    for n, _ in enumerate(nbrlist):
        window_buffer.append(nbrlist[n])
        if len(window_buffer) > 3:
            window_buffer.pop(0)
            if (newvalue := sum(window_buffer)) > previous:
                inc_count += 1
            previous = newvalue
    return inc_count


def main() -> int:
    with open('../Inputfiles/aoc1.txt', 'r') as file:
        numbers = list(map(int, file.read().strip('\n').splitlines()))
    print(f"Part 1: {count_depth_increase(numbers)}")
    print(f"Part 2: {count_window_depth_increase(numbers)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
