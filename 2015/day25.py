"""
A simple function to translate the input coordinate to code number according to the diagonally generated table in the
description text. This is then used to determine how many times to re-calculate the starting value, which will give
the answer.
"""
import time
from pathlib import Path
import re


class CodeGenerator:
    __START_CODE = 20151125
    __MULTIPLIER = 252533
    __DIVISOR = 33554393

    def __init__(self, rawstr: str) -> None:
        self.__row, self.__col = list(map(int, re.findall(r"\d+", rawstr)))

    def __get_code_nbr(self) -> int:
        """Calculates the value according to the diagonally generated table."""
        nbr = 0
        for i in range(self.__col + 1):
            nbr += i
        for i in range(self.__col, self.__col + self.__row - 1):
            nbr += i
        return nbr

    def get_code(self) -> int:
        """Performs X recalculations of the start code, where X is given by the code number."""
        code_nbr = self.__get_code_nbr()
        code = CodeGenerator.__START_CODE
        for _ in range(code_nbr - 1):
            code = (code * CodeGenerator.__MULTIPLIER) % CodeGenerator.__DIVISOR
        return code


def main(aoc_input: str) -> None:
    code = CodeGenerator(aoc_input)
    print(f"Part 1: {code.get_code()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2015/day25.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
