"""
Most of the work here is parsing the input, with that done it's mostly down to walking through the content and checking
the specified conditions.
"""
import sys
import re

Colors = {"red", "green", "blue"}


class Game:
    def __init__(self, inputstr: str):
        gameidstring, handstring = inputstr.split(": ")
        self.gameid = int(gameidstring.split()[1])
        self.hands = []
        for hand in handstring.split("; "):
            self.hands.append(dict(red=0, green=0, blue=0))
            for count, color in re.findall(r"(\d+) (\w+)", hand):
                self.hands[-1][color] = int(count)

    def ishandvalid(self) -> bool:
        colorlimits = {'green': 13, 'blue': 14, 'red': 12}
        for hand in self.hands:
            if any(hand[color] > colorlimits[color] for color in Colors):
                return False
        return True

    def gethandpower(self) -> int:
        mins = dict(red=0, green=0, blue=0)
        for hand in self.hands:
            for color in Colors:
                mins[color] = max(mins[color], hand[color])
        retval = 1
        for color in Colors:
            retval *= mins[color]
        return retval


def main() -> int:
    totalsum_part1 = 0
    totalpower_part2 = 0

    with open("../Inputfiles/aoc2.txt", "r") as file:
        for line in file.read().strip('\n').splitlines():
            newgame = Game(line)
            if newgame.ishandvalid():
                totalsum_part1 += newgame.gameid
            totalpower_part2 += newgame.gethandpower()

    print("Part1:", totalsum_part1)
    print("Part2:", totalpower_part2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
