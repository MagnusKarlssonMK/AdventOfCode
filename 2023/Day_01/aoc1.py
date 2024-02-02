import sys

Digits = {'one': 'o1ne', 'two': 't2wo', 'three': 'th3ree', 'four': 'fo4ur', 'five': 'fi5ve',
          'six': 'si6x', 'seven': 'se7ven', 'eight': 'eig8th', 'nine': 'ni9ne'}

CalibrationRule = {"A", "B"}


class Calibrationstring:
    def __init__(self, inputstr: str):
        self.calstring = inputstr

    def getcalibrationvalue(self, ruleset: CalibrationRule) -> int:
        strcopy = self.calstring
        if ruleset == "B":
            for digit in Digits:
                strcopy = strcopy.replace(digit, Digits[digit])
        digits = [char for char in strcopy if char.isdigit()]
        return 0 if len(digits) == 0 else int(digits[0] + digits[-1])

    def __str__(self):
        return self.calstring


def main() -> int:
    calibrationsum_part1 = 0
    calibrationsum_part2 = 0

    with open("../Inputfiles/aoc1.txt", "r") as file:
        for line in file.readlines():
            newcal = Calibrationstring(line.strip("\n"))
            calibrationsum_part1 += newcal.getcalibrationvalue("A")
            calibrationsum_part2 += newcal.getcalibrationvalue("B")

    print("Calibration value sum (Part1): ", calibrationsum_part1)
    print("Calibration value sum (Part2): ", calibrationsum_part2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
