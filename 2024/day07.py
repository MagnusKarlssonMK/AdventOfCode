import time
from pathlib import Path
from enum import Enum


class CalibrationResult(Enum):
    OK = 0,
    CONCATINATED_OK = 1,
    NOT_OK = 2


def concatinate(right: int) -> int:
    multiplier = 10
    while multiplier <= right:
        multiplier *= 10
    return multiplier


class Equation:
    def __init__(self, rawstr: str):
        tv, nbrs = rawstr.split(": ")
        self.__testvalue = int(tv)
        self.__numbers = [int(nbr) for nbr in nbrs.split()]

    def calibrate(self) -> tuple[CalibrationResult, int]:
        return self.__validate(self.__numbers[0], self.__numbers[1:])

    def __validate(self, total, nbrs) -> tuple[CalibrationResult, int]:
        if len(nbrs) == 0:
            return (CalibrationResult.OK, total) if total == self.__testvalue else (CalibrationResult.NOT_OK, 0)
        elif total > self.__testvalue:
            return CalibrationResult.NOT_OK, 0
        else:
            add_result, add_value = self.__validate(total + nbrs[0], nbrs[1:])
            if add_result == CalibrationResult.OK:
                return add_result, add_value
            mul_result, mul_value = self.__validate(total * nbrs[0], nbrs[1:])
            if mul_result == CalibrationResult.OK:
                return mul_result, mul_value
            if add_result == CalibrationResult.CONCATINATED_OK:
                return add_result, add_value
            if mul_result == CalibrationResult.CONCATINATED_OK:
                return mul_result, mul_value
            conc_result, conc_value = self.__validate(total * concatinate(nbrs[0]) + nbrs[0], nbrs[1:])
            if conc_result != CalibrationResult.NOT_OK:
                return CalibrationResult.CONCATINATED_OK, conc_value
        return CalibrationResult.NOT_OK, 0


class CalibrationData:
    def __init__(self, rawstr: str) -> None:
        self.__equations = [Equation(line) for line in rawstr.splitlines()]

    def get_calibration_result(self) -> tuple[int, int]:
        p1 = p2 = 0
        for e in self.__equations:
            r, v = e.calibrate()
            if r == CalibrationResult.OK:
                p1 += v
                p2 += v
            elif r == CalibrationResult.CONCATINATED_OK:
                p2 += v
        return p1, p2


def main(aoc_input: str) -> None:
    data = CalibrationData(aoc_input)
    p1, p2 = data.get_calibration_result()
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2024/day07.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
