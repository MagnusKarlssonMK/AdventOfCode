"""
This mostly comes down to figuring out how to calculate the expected position of each scanner per layer at the time we
will pass by it.
Brute force approach for part 2; basically iterate through a start number until we find a delay where none of the
layers will catch us. There are probably some clever ways to reduce the search space (it should be possible to determine
something with knowing the layer delay and the modulo factor for each layer), but this runs in about a second or so, so
it isn't too bad.
"""
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Layer:
    depth: int
    range: int

    def is_at_top_at_time(self, t: int) -> bool:
        return t % ((self.range - 1) * 2) == 0

    def get_severity(self) -> int:
        return self.depth * self.range


class Firewall:
    def __init__(self, rawstr: str) -> None:
        self.__layers: dict[int: int] = {int(d): Layer(int(d), int(r)) for d, r in
                                         [line.split(': ') for line in rawstr.splitlines()]}

    def get_trip_severity(self) -> int:
        return sum([self.__layers[t].get_severity() for t in self.__layers if self.__layers[t].is_at_top_at_time(t)])

    def __is_caught_at_time(self, delay: int) -> bool:
        for t in self.__layers:
            if self.__layers[t].is_at_top_at_time(delay + self.__layers[t].depth):
                return True
        return False

    def get_safe_delay(self) -> int:
        delay = 1  # We already know from part 1 that delay = 0 will fail
        while self.__is_caught_at_time(delay):
            delay += 1
        return delay


def main() -> int:
    with open('../Inputfiles/aoc13.txt', 'r') as file:
        firewall = Firewall(file.read().strip('\n'))
    print(f"Part 1: {firewall.get_trip_severity()}")
    print(f"Part 2: {firewall.get_safe_delay()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
