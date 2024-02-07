"""
Create Hand class to store the cards and bid, and provides methods to calculate a power value that can be used to
sort the hands. The power value is generated as a hex value with the hand result in the MSB and card values in LSB,
this way the different hands can be sorted according to the rules. The power calculation method is done in two vaiants,
one for Part 1 and one for Part 2.
"""
import sys
from collections import Counter


Cardlist = {"2": '2', "3": '3', "4": '4', "5": '5', "6": '6', "7": '7', "8": '8', "9": '9',
            "T": 'A', "J": 'B', "Q": 'C', "K": 'D', "A": 'E'}

Handresults = {"High card": 1, "One pair": 2, "Two pair": 3, "Three of a kind": 4,
               "Full house": 5, "Four of a kind": 6, "Five of a kind": 7}


class Hand:
    def __init__(self, newcardstring: str, newbid: int):
        self.bid = newbid
        self.cards = [c for c in newcardstring]

    def gethandpower(self) -> int:
        """Returns the input to Part 1 for this hand."""
        result = 0
        cardcount = sorted(Counter(self.cards).values(), reverse=True)
        match cardcount[0]:
            case 5:
                result = Handresults["Five of a kind"]
            case 4:
                result = Handresults["Four of a kind"]
            case 3:
                if cardcount[1] == 2:
                    result = Handresults["Full house"]
                else:
                    result = Handresults["Three of a kind"]
            case 2:
                if cardcount[1] == 2:
                    result = Handresults["Two pair"]
                else:
                    result = Handresults["One pair"]
            case 1:
                result = Handresults["High card"]
        cardstring = ''.join([Cardlist[c] for c in self.cards])
        return int(str(result) + cardstring, 16)

    def gethandpower_jokers(self) -> int:
        """Returns the input to Part 2 for this hand."""
        result = 0
        if (jokercount := self.cards.count('J')) >= 4:
            result = Handresults["Five of a kind"]
        else:
            nonjokercards = [c for c in self.cards if c != 'J']
            cardcount = sorted(Counter(nonjokercards).values(), reverse=True)

            match cardcount[0] + jokercount:
                case 5:
                    result = Handresults["Five of a kind"]
                case 4:
                    result = Handresults["Four of a kind"]
                case 3:
                    if cardcount[1] == 2:
                        result = Handresults["Full house"]
                    else:
                        result = Handresults["Three of a kind"]
                case 2:
                    if cardcount[1] == 2:
                        result = Handresults["Two pair"]
                    else:
                        result = Handresults["One pair"]
                case 1:
                    result = Handresults["High card"]
        cardstring = ''
        for card in self.cards:
            if card == 'J':
                cardstring += '1'
            else:
                cardstring += Cardlist[card]
        return int(str(result) + cardstring, 16)


def main() -> int:
    handlist: list[Hand] = []

    with open("../Inputfiles/aoc7.txt", "r") as file:
        for line in file.readlines():
            left, right = line.strip("\n").split()
            handlist.append(Hand(left, int(right)))

    # Part 1
    handlist.sort(key=lambda a: a.gethandpower())
    score_p1 = 0
    for rank, hand in enumerate(handlist):
        score_p1 += hand.bid * (rank + 1)
    print("Part 1:", score_p1)

    # Part 2
    handlist.sort(key=lambda a: a.gethandpower_jokers())
    score_p2 = 0
    for rank, hand in enumerate(handlist):
        score_p2 += hand.bid * (rank + 1)
    print("Part 2:", score_p2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
