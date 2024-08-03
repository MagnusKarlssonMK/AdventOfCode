"""
Rather than representing the keypad as a grid, instead build it as an adjacency list, to make it easier to deal with
boundaries.
Might look a bit fancier if rather than manually hardcoding the maps, instead directly copying the text mapping from the
description and then having a parsing function to convert it to the layouts, but isn't quite worth it for such simple
mappings.
"""
import sys
from enum import Enum, auto


class Directions(Enum):
    LEFT = auto()
    RIGHT = auto()
    DOWN = auto()
    UP = auto()


class KeyPad:
    __LAYOUTS = [
        {'1': {Directions.RIGHT: '2', Directions.DOWN: '4'},
         '2': {Directions.LEFT: '1', Directions.RIGHT: '3', Directions.DOWN: '5'},
         '3': {Directions.LEFT: '2', Directions.DOWN: '6'},
         '4': {Directions.UP: '1', Directions.RIGHT: '5', Directions.DOWN: '7'},
         '5': {Directions.UP: '2', Directions.LEFT: '4', Directions.RIGHT: '6', Directions.DOWN: '8'},
         '6': {Directions.UP: '3', Directions.LEFT: '5', Directions.DOWN: '9'},
         '7': {Directions.UP: '4', Directions.RIGHT: '8'},
         '8': {Directions.LEFT: '7', Directions.UP: '5', Directions.RIGHT: '9'},
         '9': {Directions.LEFT: '8', Directions.UP: '6'}},

        {'1': {Directions.DOWN: '3'},
         '2': {Directions.RIGHT: '3', Directions.DOWN: '6'},
         '3': {Directions.UP: '1', Directions.LEFT: '2', Directions.RIGHT: '4', Directions.DOWN: '7'},
         '4': {Directions.LEFT: '3', Directions.DOWN: '8'},
         '5': {Directions.RIGHT: '6'},
         '6': {Directions.LEFT: '5', Directions.UP: '2', Directions.RIGHT: '7', Directions.DOWN: 'A'},
         '7': {Directions.LEFT: '6', Directions.UP: '3', Directions.RIGHT: '8', Directions.DOWN: 'B'},
         '8': {Directions.LEFT: '7', Directions.UP: '4', Directions.RIGHT: '9', Directions.DOWN: 'C'},
         '9': {Directions.LEFT: '8'},
         'A': {Directions.UP: '6', Directions.RIGHT: 'B'},
         'B': {Directions.LEFT: 'A', Directions.UP: '7', Directions.RIGHT: 'C', Directions.DOWN: 'D'},
         'C': {Directions.LEFT: 'B', Directions.UP: '8'},
         'D': {Directions.UP: 'B'}}
    ]

    def __init__(self, rawstr: str) -> None:
        directionmap = {'L': Directions.LEFT, 'R': Directions.RIGHT, 'U': Directions.UP, 'D': Directions.DOWN}
        self.__instructions = [[directionmap[c] for c in line] for line in rawstr.splitlines()]

    def get_bathroom_code(self, advanced_layout: bool = False) -> str:
        code = []
        currentpos = '5'
        layout = KeyPad.__LAYOUTS[1 if advanced_layout else 0]
        for digit in self.__instructions:
            for step in digit:
                if step in layout[currentpos]:
                    currentpos = layout[currentpos][step]
            code.append(currentpos)
        return ''.join(code)


def main() -> int:
    with open('../Inputfiles/aoc2.txt', 'r') as file:
        keypad = KeyPad(file.read().strip('\n'))
    print(f"Part 1: {keypad.get_bathroom_code()}")
    print(f"Part 2: {keypad.get_bathroom_code(True)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
