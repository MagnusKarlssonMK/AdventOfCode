import sys
from collections import Counter


Cardlist = {"J": '1', "2": '2', "3": '3', "4": '4', "5": '5', "6": '6', "7": '7', "8": '8', "9": '9',
            "T": 'A', "Q": 'C', "K": 'D', "A": 'E'}

Handresults = {"High card": 1, "One pair": 2, "Two pair": 3, "Three of a kind": 4,
               "Full house": 5, "Four of a kind": 6, "Five of a kind": 7}


class Hand:
    def __init__(self, newcardstring: str, newbid: int):
        self.bid = newbid
        self.cards = ""
        for i in newcardstring:
            self.cards += Cardlist[i]
        if (jokercount := self.cards.count('1')) >= 4:
            self.result = Handresults["Five of a kind"]
        else:
            nonjokercards = self.cards.replace('1', '')
            cardcount = sorted(Counter(nonjokercards).values(), reverse=True)

            match cardcount[0] + jokercount:
                case 5:
                    self.result = Handresults["Five of a kind"]
                case 4:
                    self.result = Handresults["Four of a kind"]
                case 3:
                    if cardcount[1] == 2:
                        self.result = Handresults["Full house"]
                    else:
                        self.result = Handresults["Three of a kind"]
                case 2:
                    if cardcount[1] == 2:
                        self.result = Handresults["Two pair"]
                    else:
                        self.result = Handresults["One pair"]
                case 1:
                    self.result = Handresults["High card"]

        self.power = int(str(self.result) + self.cards, 16)


def main() -> int:
    handlist: list[Hand] = []

    with open("../Inputfiles/aoc7.txt", "r") as file:
        for line in file.readlines():
            left, right = line.strip("\n").split()
            handlist.append(Hand(left, int(right)))

    handlist.sort(key=lambda a: a.power)

    totalscore = 0

    for rank, hand in enumerate(handlist):
        totalscore += hand.bid * (rank + 1)

    print("Total score: ", totalscore)
    return 0


if __name__ == "__main__":
    sys.exit(main())
