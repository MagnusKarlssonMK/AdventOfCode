import time
from pathlib import Path
from enum import Enum


class SafetyLevels(Enum):
    SAFE = 1
    DAMPENER_SAFE = 2
    UNSAFE = 3


class Report:
    def __init__(self, line: str) -> None:
        self.__levels = [int(c) for c in line.split()]

    def get_safety_level(self) -> SafetyLevels:
        def is_safe(levels: list[int]) -> bool:
            diffs = [(abs(j - i), 1 if j - i > 0 else -1) for i, j in zip(levels[:-1], levels[1:])]
            if all([1 <= v <= 3 and o == diffs[0][1] for v, o in diffs]):
                return True
            return False
        if is_safe(self.__levels):
            return SafetyLevels.SAFE
        else:
            for n, _ in enumerate(self.__levels):
                if is_safe(self.__levels[0:n] + self.__levels[n+1:]):
                    return SafetyLevels.DAMPENER_SAFE
        return SafetyLevels.UNSAFE


class Reports:
    def __init__(self, rawstr: str) -> None:
        self.__reports = [Report(line) for line in rawstr.splitlines()]

    def get_safe_reports(self) -> tuple[int, int]:
        safety = [r.get_safety_level() for r in self.__reports]
        safe = safety.count(SafetyLevels.SAFE)
        almost_safe = safety.count(SafetyLevels.DAMPENER_SAFE)
        return safe, safe + almost_safe

def main(aoc_input: str) -> None:
    reports = Reports(aoc_input)
    p1, p2 = reports.get_safe_reports()
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2024/day02.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
