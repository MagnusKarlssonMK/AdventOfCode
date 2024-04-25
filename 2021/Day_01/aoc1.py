"""
For part 2, we actually only need to compare the first element of the first window with the last element of the
second window, since all the elements in between are shared by both. So by making use of that logic, the answer
for both part 1 and 2 can be calculated with one function, taking the window length as an input.
"""
import sys


def count_depth_increase(nbrlist: list[int], windowsize: int) -> int:
    return sum([1 for i in range(windowsize, len(nbrlist)) if nbrlist[i] > nbrlist[i - windowsize]])


def main() -> int:
    with open('../Inputfiles/aoc1.txt', 'r') as file:
        numbers = list(map(int, file.read().strip('\n').splitlines()))
    print(f"Part 1: {count_depth_increase(numbers, 1)}")
    print(f"Part 2: {count_depth_increase(numbers, 3)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
