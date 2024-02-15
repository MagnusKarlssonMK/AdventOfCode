"""
For part 1, simply extract all numbers from the string and combine the first and last digit.
For part 2, first pre-process the string by replacing spelled out digits with the same word but with the actual digit
inserted in the middle, in a place where it won't destroy the string in case numbers are overlapping (e.g. 'threeight').
"""
import sys


class Calibrationstring:
    def __init__(self, inputstr: str):
        self.calstring = inputstr

    def getcalibrationvalue(self, spelled_out: bool = False) -> int:
        digits = {'one': 'o1ne', 'two': 't2wo', 'three': 'th3ree', 'four': 'fo4ur', 'five': 'fi5ve',
                  'six': 'si6x', 'seven': 'se7ven', 'eight': 'eig8th', 'nine': 'ni9ne'}
        strcopy = self.calstring
        if spelled_out:
            for digit in digits:
                strcopy = strcopy.replace(digit, digits[digit])
        digits = [char for char in strcopy if char.isdigit()]
        return 0 if len(digits) == 0 else int(digits[0] + digits[-1])


def main() -> int:
    calibrationsum_part1 = 0
    calibrationsum_part2 = 0

    with open("../Inputfiles/aoc1.txt", "r") as file:
        for line in file.read().strip('\n').splitlines():
            newcal = Calibrationstring(line)
            calibrationsum_part1 += newcal.getcalibrationvalue()
            calibrationsum_part2 += newcal.getcalibrationvalue(True)

    print("Part1:", calibrationsum_part1)
    print("Part2:", calibrationsum_part2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
