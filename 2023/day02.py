"""
Most of the work here is parsing the input, with that done it's mostly down to walking through the content and checking
the specified conditions.
"""
import sys
from pathlib import Path
import re
from dataclasses import dataclass
from enum import Enum

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2023/day02.txt')


@dataclass(frozen=True)
class Hand:
    red: int
    blue: int
    green: int

    def is_valid(self) -> bool:
        return all([self.red <= 12, self.blue <= 14, self.green <= 13])

    def get_power(self) -> int:
        return self.red * self.blue * self.green

    def get_max(self, other: "Hand") -> "Hand":
        return Hand(max(self.red, other.red), max(self.blue, other.blue), max(self.green, other.green))


class Color(Enum):
    RED = 'red'
    BLUE = 'blue'
    GREEN = 'green'


class Game:
    def __init__(self, inputstr: str) -> None:
        gameidstring, handstring = inputstr.split(": ")
        self.gameid = int(gameidstring.split()[1])
        self.__hands = []
        for hand in handstring.split("; "):
            newhand = {color: 0 for color in Color}
            for count, colorstr in re.findall(r"(\d+) (\w+)", hand):
                newhand[Color(colorstr)] = int(count)
            self.__hands.append(Hand(newhand[Color.RED], newhand[Color.BLUE], newhand[Color.GREEN]))

    def is_valid(self) -> bool:
        return all([hand.is_valid() for hand in self.__hands])

    def get_power(self) -> int:
        minimum_required = Hand(0, 0, 0)
        for hand in self.__hands:
            minimum_required = hand.get_max(minimum_required)
        return minimum_required.get_power()


class GameRecord:
    def __init__(self, rawstr: str) -> None:
        self.__games = [Game(line) for line in rawstr.splitlines()]

    def get_valid_games_value(self) -> int:
        return sum([game.gameid for game in self.__games if game.is_valid()])

    def get_total_power(self) -> int:
        return sum([game.get_power() for game in self.__games])


def main() -> int:
    with open(INPUT_FILE, "r") as file:
        record = GameRecord(file.read().strip('\n'))
    print(f"Part 1: {record.get_valid_games_value()}")
    print(f"Part 2: {record.get_total_power()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
