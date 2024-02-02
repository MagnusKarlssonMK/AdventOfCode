import sys
import re


class CardInpuError(Exception):
    pass


class Scratchcard:
    def __init__(self, inputstring: str):
        if inputstring.count("Card ") == 1:
            self.drawnumbers = []
            cardstr, reststr = inputstring.split(":")
            self.cardid = int(re.findall(r"\d+", cardstr)[0])
            winstr, drawstr = reststr.split(" | ")
            self.winningnumbers = list(map(int, [nbr for nbr in winstr.split()]))
            self.drawnumbers = list(map(int, [nbr for nbr in drawstr.split()]))
            self.wincount = len(set(self.winningnumbers) & set(self.drawnumbers))
            self.score = 2 ** (self.wincount - 1) if self.wincount > 0 else 0
        else:
            raise CardInpuError

    def __str__(self):
        return f"CardID: {self.cardid} - Wincount: {self.wincount} - Score: {self.score}"


def main() -> int:
    totalscore = 0
    totalnbrofcards = 0
    copylist = [0] * 10

    with open("../Inputfiles/aoc4.txt", "r") as file:
        for line in file.readlines():
            try:
                newcard = Scratchcard(line.strip("\n"))
                newcardcount = 1 + copylist.pop(0)
                totalnbrofcards += newcardcount
                copylist.append(0)
                for copyidx in range(len(copylist)):
                    if copyidx < newcard.wincount:
                        copylist[copyidx] += newcardcount
                totalscore += newcard.score
            except CardInpuError:
                print("Discarding line")

    print("Total score (Part1): ", totalscore, " Nbr of cards (Part2): ", totalnbrofcards)
    return 0


if __name__ == "__main__":
    sys.exit(main())
