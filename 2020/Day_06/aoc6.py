"""
Collect the data per group in sets. For Part 1, just combine the sets for each person in the group to get the answer.
For Part 2 instead get the shared values in the sets for all persons in the group. This can be done with the same
function just passing the comparison function as an input.
"""
import sys


def getyescount(group: list[str], mask) -> int:
    yes = set(group[0])
    for i in range(1, len(group)):
        yes = mask(yes, set(group[i]))
    return len(yes)


def main() -> int:
    with open('../Inputfiles/aoc6.txt', 'r') as file:
        groups = [g.splitlines() for g in file.read().strip('\n').split('\n\n')]
    print("Part 1:", sum([getyescount(group, lambda x, y: x | y) for group in groups]))
    print("Part 2:", sum([getyescount(group, lambda x, y: x & y) for group in groups]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
