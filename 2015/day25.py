"""
A simple function to translate the input coordinate to code number according to the diagonally generated table in the
description text. This is then used to determine how many times to re-calculate the starting value, which will give
the answer.
"""
import sys
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


def main() -> int:
    with open('../Inputfiles/aoc25.txt', 'r') as file:
        code = CodeGenerator(file.read().strip('\n'))
    print(f"Part 1: {code.get_code()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
