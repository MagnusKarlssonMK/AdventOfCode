"""
Pretty much just do the pixel transformations according to the instructions, use numpy to make the rotation operations
a bit easier.
"""
import sys
import re
import numpy as np
from dataclasses import dataclass


@dataclass(frozen=True)
class Instruction:
    instr: str
    val1: int
    val2: int


class Display:
    __SCREEN_WIDTH = 50
    __SCREEN_HEIGHT = 6

    def __init__(self, rawstr: str) -> None:
        self.__instructions = []
        for line in rawstr.splitlines():
            tokens = line.split()
            if tokens[0] == 'rotate':
                self.__instructions.append(Instruction(tokens[1], *list(map(int, re.findall(r"\d+", line)))))
            else:
                self.__instructions.append(Instruction(tokens[0], *list(map(int, tokens[1].split('x')))))
        self.__grid = np.zeros((Display.__SCREEN_HEIGHT, Display.__SCREEN_WIDTH))

    def get_lit_pixel_count(self) -> int:
        for i in self.__instructions:
            if i.instr == 'rect':
                self.__grid[0: i.val2, 0: i.val1] = 1
            elif i.instr == 'column':
                col = self.__grid[:, i.val1]
                rotated = list(col[-i.val2:]) + list(col[:-i.val2])
                self.__grid[:, i.val1] = rotated
            elif i.instr == 'row':
                row = self.__grid[i.val1, :]
                rotated = list(row[-i.val2:]) + list(row[:-i.val2])
                self.__grid[i.val1, :] = rotated
        return int(np.sum(self.__grid))

    def draw_screen(self) -> str:
        displaytext = ''
        for row in range(Display.__SCREEN_HEIGHT):
            for col in range(Display.__SCREEN_WIDTH):
                if self.__grid[row][col] == 0:
                    displaytext += ' '
                else:
                    displaytext += '#'
                if (col + 1) % 5 == 0:
                    displaytext += ' '  # Add an extra space between characters to make it a bit easier to read
            displaytext += '\n'
        return displaytext


def main() -> int:
    with open('../Inputfiles/aoc8.txt', 'r') as file:
        display = Display(file.read().strip('\n'))
    print(f"Part 1: {display.get_lit_pixel_count()}")
    print("Part 2:")
    print(display.draw_screen())
    return 0


if __name__ == "__main__":
    sys.exit(main())
