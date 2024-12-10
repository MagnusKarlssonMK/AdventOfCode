import time
from pathlib import Path


class Grid:
    def __init__(self, rawstr: str) -> None:
        lines = rawstr.splitlines()
        self.__x_max = len(lines[0])
        self.__y_max = len(lines)
        self.__elements = [int(c) for c in rawstr if c != "\n"]

    def get_element(self, x: int, y: int) -> int:
        return self.__elements[self.__x_max * y + x]

    def is_contained(self, x: int, y: int) -> bool:
        return 0 <= x < self.__x_max and 0 <= y < self.__y_max

    def find(self, val: int) -> iter:
        for i, v in enumerate(self.__elements):
            if v == val:
                yield i % self.__x_max, i // self.__y_max


class Map:
    def __init__(self, rawstr: str) -> None:
        self.__grid = Grid(rawstr)
        self.__trailheads = [(x, y) for x, y in self.__grid.find(0)]

    def get_score_and_rating(self) -> tuple[int, int]:
        score = rating = 0
        for head in self.__trailheads:
            peaks: set[(int, int)] = set()
            queue = [head]
            while queue:
                current = queue.pop(0)
                if self.__grid.get_element(*current) == 9:
                    peaks.add(current)
                    rating += 1
                else:
                    for direction in ((1, 0), (0, 1), (-1, 0), (0, -1)):
                        neighbor = direction[0] + current[0], direction[1] + current[1]
                        if self.__grid.is_contained(*neighbor):
                            neighbor_val = self.__grid.get_element(*neighbor)
                            if neighbor_val == self.__grid.get_element(*current) + 1:
                                queue.append(neighbor)
            score += len(peaks)
        return score, rating


def main(aoc_input: str) -> None:
    p = Map(aoc_input)
    score, rating = p.get_score_and_rating()
    print(f"Part 1: {score}")
    print(f"Part 2: {rating}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2024/day10.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
