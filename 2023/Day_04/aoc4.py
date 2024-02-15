"""
Basically decodes the input into a Scratchcard class, and then counts the scores according to the rules.
Having a class for the card is a bit over the top, I expected it to be beneficial for part 2 before seeing it.
"""
import sys
import re


class Scratchcard:
    def __init__(self, inputstring: str):
        self.drawnumbers = []
        cardstr, reststr = inputstring.split(":")
        self.cardid = int(re.findall(r"\d+", cardstr)[0])
        winstr, drawstr = reststr.split(" | ")
        self.winningnumbers = list(map(int, [nbr for nbr in winstr.split()]))
        self.drawnumbers = list(map(int, [nbr for nbr in drawstr.split()]))
        self.wincount = len(set(self.winningnumbers) & set(self.drawnumbers))
        self.score = 2 ** (self.wincount - 1) if self.wincount > 0 else 0


def main() -> int:
    totalscore = 0
    totalnbrofcards = 0
    copylist = [0 for _ in range(10)]

    with open("../Inputfiles/aoc4.txt", "r") as file:
        for line in file.read().strip('\n').splitlines():
            newcard = Scratchcard(line)
            newcardcount = 1 + copylist.pop(0)
            totalnbrofcards += newcardcount
            copylist.append(0)
            for copyidx in range(len(copylist)):
                if copyidx < newcard.wincount:
                    copylist[copyidx] += newcardcount
            totalscore += newcard.score

    print("Part1:", totalscore)
    print("Part2:", totalnbrofcards)
    return 0


if __name__ == "__main__":
    sys.exit(main())
