import sys
import re

Colors = {"red", "green", "blue"}
Colorlimits = {'green': 13, 'blue': 14, 'red': 12}


class GameInputError(Exception):
    pass


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
        for hand in self.hands:
            if any(hand[color] > Colorlimits[color] for color in Colors):
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

    def __str__(self):
        retstr = "GameID: " + str(self.gameid) + " "
        for n in self.hands:
            retstr += str(n) + " "
        return retstr


def main() -> int:
    totalsum_part1 = 0
    totalpower_part2 = 0

    with open("aoc2.txt", "r") as file:
        for line in file.readlines():
            try:
                newgame = Game(line.strip("\n"))
                print(newgame)
                if newgame.ishandvalid():
                    totalsum_part1 += newgame.gameid
                totalpower_part2 += newgame.gethandpower()
            except GameInputError:
                print("Invalid line, discarding")

    print("Sum of game ids for valid games (Part1): ", totalsum_part1)
    print("Sum of hand power values (Part2): ", totalpower_part2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
