import time
from pathlib import Path


class Locations:
    def __init__(self, rawstr: str) -> None:
        self.__left: list[int] = []
        self.__right: list[int] = []
        for line in rawstr.splitlines():
            left, right = line.split()
            self.__left.append(int(left))
            self.__right.append(int(right))
        self.__left.sort()
        self.__right.sort()

    def get_total_distance(self) -> int:
        total = 0
        for left, right in zip(self.__left, self.__right):
            total += abs(left - right)
        return total

    def get_similarity_score(self) -> int:
        score = 0
        right_idx = 0
        for left in self.__left:
            delta = 0
            while right_idx + delta < len(self.__right):
                if self.__right[right_idx + delta] > left:
                    break
                if self.__right[right_idx + delta] == left:
                    score += left
                    delta += 1
                else:
                    right_idx += 1
        return score


def main(aoc_input: str) -> None:
    records = Locations(aoc_input)
    print(f"Part 1: {records.get_total_distance()}")
    print(f"Part 2: {records.get_similarity_score()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2024/day01.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
