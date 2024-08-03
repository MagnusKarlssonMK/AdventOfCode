"""
Mainly (ab)using the ord() function to compare characters while generating reacted values or removing units.
"""
import sys


class Polymer:
    def __init__(self, rawstr: str) -> None:
        self.__polymer = rawstr
        self.__offset = ord('a') - ord('A')

    def __get_reacted_unit_count(self, polymer: str) -> int:
        i = 0
        poly = list(polymer)
        while i < len(poly) - 1:
            if abs(ord(poly[i]) - ord(poly[i+1])) == self.__offset:
                del poly[i:i+2]
                if i > 0:
                    i -= 1
            else:
                i += 1
        return len(poly)

    def __delete_unit(self, unit: int) -> str:
        u = unit, unit + self.__offset
        return ''.join(c for c in self.__polymer if ord(c) not in u)

    def get_full_reacted_units(self) -> int:
        return self.__get_reacted_unit_count(self.__polymer)

    def get_shortest_poly(self) -> int:
        shortest = None
        for c in range(ord('A'), ord('Z') + 1):
            removed_len = self.__get_reacted_unit_count(self.__delete_unit(c))
            if not shortest or removed_len < shortest:
                shortest = removed_len
        return shortest


def main() -> int:
    with open('../Inputfiles/aoc5.txt', 'r') as file:
        polymer = Polymer(file.read().strip('\n'))
    print(f"Part 1: {polymer.get_full_reacted_units()}")
    print(f"Part 2: {polymer.get_shortest_poly()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
