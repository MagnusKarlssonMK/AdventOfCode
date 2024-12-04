import time
from pathlib import Path


class WordSearch:
    def __init__(self, rawstr: str) -> None:
        self.__grid = [[c for c in line] for line in rawstr.splitlines()]
        self.__height = len(self.__grid)
        self.__width = len(self.__grid[0])

    def __get_grid_value(self, row:int, col: int) -> chr:
        if row in range(0, self.__height) and col in range(0, self.__width):
            return self.__grid[row][col]
        return "."

    def get_xmas(self) -> int:
        DIRECTIONS = ((1, 0), (1, -1), (0, -1), (-1, -1),
                      (-1, 0), (-1, 1), (0, 1), (1, 1))
        total = 0
        for row, line in enumerate(self.__grid):
            for col, c in enumerate(line):
                if c == 'X':
                    for d_row, d_col in DIRECTIONS:
                        if ('X' +
                               self.__get_grid_value(row + d_row, col + d_col) +
                               self.__get_grid_value(row + 2 * d_row, col + 2 * d_col) +
                               self.__get_grid_value(row + 3 * d_row, col + 3 * d_col) == "XMAS"):
                            total += 1
        return total

    def get_x_mas(self) -> int:
        total = 0
        for row, line in enumerate(self.__grid):
            for col, c in enumerate(line):
                if c == 'A':
                    word1 = self.__get_grid_value(row - 1, col - 1) + "A" + self.__get_grid_value(row + 1, col + 1)
                    if word1 in ("MAS", "SAM"):
                        word2 = self.__get_grid_value(row + 1, col - 1) + "A" + self.__get_grid_value(row - 1, col + 1)
                        if word2 in ("MAS", "SAM"):
                            total += 1
        return total


def main(aoc_input: str) -> None:
    p = WordSearch(aoc_input)
    print(f"Part 1: {p.get_xmas()}")
    print(f"Part 2: {p.get_x_mas()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2024/day04.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
