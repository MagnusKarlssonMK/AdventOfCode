"""
Most of the work here is parsing the input, with that done it's mostly down to walking through the content and checking
the specified conditions.
"""
import sys
import re
from dataclasses import dataclass


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


class Game:
    __COLORS = ["red", "blue", "green"]

    def __init__(self, inputstr: str) -> None:
        gameidstring, handstring = inputstr.split(": ")
        self.gameid = int(gameidstring.split()[1])
        self.__hands = []
        for hand in handstring.split("; "):
            newhand = {color: 0 for color in Game.__COLORS}
            for count, color in re.findall(r"(\d+) (\w+)", hand):
                newhand[color] = int(count)
            self.__hands.append(Hand(newhand[Game.__COLORS[0]], newhand[Game.__COLORS[1]], newhand[Game.__COLORS[2]]))

    def is_valid(self) -> bool:
        return all([hand.is_valid() for hand in self.__hands])

    def get_power(self) -> int:
        minimum_required = Hand(0, 0, 0)
        for hand in self.__hands:
            minimum_required = hand.get_max(minimum_required)
        return minimum_required.get_power()


def main() -> int:
    totalsum_part1 = 0
    totalpower_part2 = 0

    with open("../Inputfiles/aoc2.txt", "r") as file:
        for line in file.read().strip('\n').splitlines():
            newgame = Game(line)
            if newgame.is_valid():
                totalsum_part1 += newgame.gameid
            totalpower_part2 += newgame.get_power()

    print(f"Part1: {totalsum_part1}")
    print(f"Part2: {totalpower_part2}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
