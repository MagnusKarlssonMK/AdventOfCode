"""
For part 1, simply extract all numbers from the string and combine the first and last digit.
For part 2, first pre-process the string by replacing spelled out digits with the same word but with the actual digit
inserted in the middle, in a place where it won't destroy the string in case numbers are overlapping (e.g. 'threeight').
"""
import time
from pathlib import Path


class Calibrationstring:
    def __init__(self, inputstr: str) -> None:
        self.__calstring = inputstr

    def getcalibrationvalue(self, spelled_out: bool) -> int:
        digits = {'one': 'o1ne', 'two': 't2wo', 'three': 'th3ree', 'four': 'fo4ur', 'five': 'fi5ve',
                  'six': 'si6x', 'seven': 'se7ven', 'eight': 'eig8th', 'nine': 'ni9ne'}
        strcopy = self.__calstring
        if spelled_out:
            for digit in digits:
                strcopy = strcopy.replace(digit, digits[digit])
        digits = [char for char in strcopy if char.isdigit()]
        return 0 if len(digits) == 0 else int(digits[0] + digits[-1])


class Document:
    def __init__(self, rawstr: str) -> None:
        self.__values = [Calibrationstring(line) for line in rawstr.splitlines()]

    def get_calibration_sum(self, spelled_out: bool = False) -> int:
        return sum([v.getcalibrationvalue(spelled_out) for v in self.__values])


def main(aoc_input: str) -> None:
    document = Document(aoc_input)
    print(f"Part 1: {document.get_calibration_sum()}")
    print(f"Part 2: {document.get_calibration_sum(True)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2023/day01.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
