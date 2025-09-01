"""
Pretty much just do the pixel transformations according to the instructions, use numpy to make the rotation operations
a bit easier.
"""
import time
from pathlib import Path
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
        self.__instructions: list[Instruction] = []
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


def main(aoc_input: str) -> None:
    display = Display(aoc_input)
    print(f"Part 1: {display.get_lit_pixel_count()}")
    print("Part 2:")
    print(display.draw_screen())


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2016/day08.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
