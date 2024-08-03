"""
Part 1: Simply take the sum of the numbers.
Part 2: Iterate through the numbers, updating the frequency and storing it in a set, and break when finding a
repetition.
"""
import sys


class Device:
    def __init__(self, rawstr: str) -> None:
        self.__nbrs = [int(nbr.strip('+')) for nbr in rawstr.splitlines()]

    def get_frequency(self) -> int:
        return sum(self.__nbrs)

    def get_calibration_value(self) -> int:
        seen = set()
        i = 0
        freq = 0
        while True:
            freq += self.__nbrs[i]
            if freq in seen:
                break
            seen.add(freq)
            i = (i + 1) % len(self.__nbrs)
        return freq


def main() -> int:
    with open('../Inputfiles/aoc1.txt', 'r') as file:
        device = Device(file.read().strip('\n'))
    print(f"Part 1: {device.get_frequency()}")
    print(f"Part 2: {device.get_calibration_value()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
