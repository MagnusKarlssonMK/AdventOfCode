"""
A bit of numpy exercise to make things run decently fast.
"""
import sys
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
import re
import numpy as np

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2015/day06.txt')


class Action(Enum):
    TOGGLE = 0
    TURN_ON = 1
    TURN_OFF = 2


@dataclass(frozen=True)
class Instruction:
    action: Action
    x1: int
    y1: int
    x2: int
    y2: int


class LightGrid:
    def __init__(self, rawstr: str) -> None:
        self.__instructions = []
        for line in rawstr.splitlines():
            nbrs = list(map(int, re.findall(r'\d+', line)))
            words = line.split()
            action = Action.TOGGLE
            if words[0] != 'toggle':
                action = Action.TURN_ON if words[1] == 'on' else Action.TURN_OFF
            self.__instructions.append(Instruction(action, *nbrs))

    def get_lights_count(self) -> int:
        grid = np.zeros((1000, 1000))
        for instr in self.__instructions:
            match instr.action:
                case Action.TURN_ON:
                    grid[instr.x1: instr.x2 + 1, instr.y1: instr.y2 + 1] = 1
                case Action.TURN_OFF:
                    grid[instr.x1: instr.x2 + 1, instr.y1: instr.y2 + 1] = 0
                case Action.TOGGLE:
                    grid[instr.x1: instr.x2 + 1, instr.y1: instr.y2 + 1] += 1
                    grid[instr.x1: instr.x2 + 1, instr.y1: instr.y2 + 1] %= 2
        return int(grid.sum())

    def get_correct_lights_count(self) -> int:
        grid = np.zeros((1000, 1000))
        for instr in self.__instructions:
            match instr.action:
                case Action.TURN_ON:
                    grid[instr.x1: instr.x2 + 1, instr.y1: instr.y2 + 1] += 1
                case Action.TURN_OFF:
                    grid[instr.x1: instr.x2 + 1, instr.y1: instr.y2 + 1] -= 1
                    grid.clip(min=0, out=grid)
                case Action.TOGGLE:
                    grid[instr.x1: instr.x2 + 1, instr.y1: instr.y2 + 1] += 2
        return int(grid.sum())


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        grid = LightGrid(file.read().strip('\n'))
    print(f"Part 1: {grid.get_lights_count()}")
    print(f"Part 2: {grid.get_correct_lights_count()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
