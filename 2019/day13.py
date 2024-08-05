"""
Part 1 is mostly just running the Intcode program without any input, storing the output in a dict and then count number
of blocks.
Part 2 is not clear at all from the problem description what the joystick actually controls or how to use it to beat
the game, but apparently all we need to do is to steer the x-position of the paddle towards the ball (so it's basically
sort of an Arkanoid game), e.g. if ball < paddle steer left.
"""
import sys
from pathlib import Path
from enum import Enum
from dataclasses import dataclass
from intcode import Intcode, IntResult

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2019/day13.txt')


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)


class TileId(Enum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    HORIZONTAL_PADDLE = 3
    BALL = 4


class Joystick(Enum):
    NEUTRAL = 0
    LEFT = -1
    RIGHT = 1


class ArcadeGame:
    def __init__(self, rawstr: str) -> None:
        self.__cpu = Intcode(list(map(int, rawstr.split(','))))

    def get_block_tiles(self) -> int:
        tiles: dict[Point: TileId] = {}
        output_buffer = []
        while True:
            val, res = self.__cpu.run_program()
            if res == IntResult.WAIT_INPUT:
                break
            elif res == IntResult.OUTPUT:
                output_buffer.append(val)
                if len(output_buffer) == 3:
                    x, y, t = output_buffer
                    tiles[Point(x, y)] = TileId(t)
                    output_buffer = []
            else:
                break
        self.__cpu.reboot()
        return sum([1 for t in tiles if tiles[t] == TileId.BLOCK])

    def get_winning_score(self) -> int:
        self.__cpu.override_program(0, 2)
        score = 0
        ball = 0
        paddle = 0
        output_buffer = []
        while True:
            val, res = self.__cpu.run_program()
            if res == IntResult.WAIT_INPUT:
                if ball < paddle:
                    self.__cpu.add_input(Joystick.LEFT.value)
                elif ball > paddle:
                    self.__cpu.add_input(Joystick.RIGHT.value)
                else:
                    self.__cpu.add_input(Joystick.NEUTRAL.value)
            elif res == IntResult.OUTPUT:
                output_buffer.append(val)
                if len(output_buffer) == 3:
                    x, y, t = output_buffer
                    if (x, y) == (-1, 0):
                        score = t
                    else:
                        if TileId(t) == TileId.BALL:
                            ball = x
                        elif TileId(t) == TileId.HORIZONTAL_PADDLE:
                            paddle = x
                    output_buffer = []
            else:  # Halted
                break
        return score


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        arcade = ArcadeGame(file.read().strip('\n'))
    print(f"Part 1: {arcade.get_block_tiles()}")
    print(f"Part 2: {arcade.get_winning_score()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
