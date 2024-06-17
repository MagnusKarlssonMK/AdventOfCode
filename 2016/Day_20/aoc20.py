"""
Parse the input into tuples of low & high and sort the list. The sorting function will default to sort by first
element (i.e. lowest boundary) with no key specified.
Then start with a list of values +1 higher than the upper bound of each blocked range, and check one by one if it's
inside any blocked range; if it is, there is another blocked range overlapping, so we discard the current candidate
and try the next.
Similar deal for part 2, making use of the sorted list and keeping track of the upper bound we've checked for allowed
numbers while counting numbers not covered by blocked intervals.
"""
import sys


class Firewall:
    def __init__(self, rawstr: str) -> None:
        self.__blocklist = sorted([(int(low), int(high)) for low, high in
                                   [line.split('-') for line in rawstr.splitlines()]])

    def get_lowest_ip(self) -> int:
        candidate = 0
        for low, high in self.__blocklist:
            if low <= candidate <= high:
                candidate = high + 1
        return candidate

    def get_allowed_ip_count(self) -> int:
        allowed_total = 0
        highest_allowed = 0
        for low, high in self.__blocklist:
            if highest_allowed < low:
                allowed_total += low - highest_allowed - 1
            highest_allowed = max(high, highest_allowed)
        allowed_total += 2 ** 32 - 1 - highest_allowed
        return allowed_total


def main() -> int:
    with open('../Inputfiles/aoc20.txt', 'r') as file:
        firewall = Firewall(file.read().strip('\n'))
    print(f"Part 1: {firewall.get_lowest_ip()}")
    print(f"Part 2: {firewall.get_allowed_ip_count()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
