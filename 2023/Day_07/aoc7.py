"""
Create Hand class to store the cards and bid, and provides methods to calculate a power value that can be used to
sort the hands. The power value is generated as a hex value with the hand result in the MSB and card values in LSB,
this way the different hands can be sorted according to the rules. The power calculation method is done in two variants,
one basic for Part 1 and one using jokers for Part 2.
"""
import sys
from collections import Counter


class Hand:
    __CARDLIST = {"2": '2', "3": '3', "4": '4', "5": '5', "6": '6', "7": '7', "8": '8', "9": '9',
                  "T": 'A', "J": 'B', "Q": 'C', "K": 'D', "A": 'E'}

    __HANDRESULTS = {"High card": 1, "One pair": 2, "Two pair": 3, "Three of a kind": 4,
                     "Full house": 5, "Four of a kind": 6, "Five of a kind": 7}

    def __init__(self, newcardstring: str, newbid: int):
        self.bid = newbid
        self.cards = [c for c in newcardstring]

    def gethandpower(self) -> int:
        """Returns the input to Part 1 for this hand."""
        result = 0
        cardcount = sorted(Counter(self.cards).values(), reverse=True)
        match cardcount[0]:
            case 5:
                result = Hand.__HANDRESULTS["Five of a kind"]
            case 4:
                result = Hand.__HANDRESULTS["Four of a kind"]
            case 3:
                if cardcount[1] == 2:
                    result = Hand.__HANDRESULTS["Full house"]
                else:
                    result = Hand.__HANDRESULTS["Three of a kind"]
            case 2:
                if cardcount[1] == 2:
                    result = Hand.__HANDRESULTS["Two pair"]
                else:
                    result = Hand.__HANDRESULTS["One pair"]
            case 1:
                result = Hand.__HANDRESULTS["High card"]
        cardstring = ''.join([Hand.__CARDLIST[c] for c in self.cards])
        return int(str(result) + cardstring, 16)

    def gethandpower_jokers(self) -> int:
        """Returns the input to Part 2 for this hand."""
        result = 0
        if (jokercount := self.cards.count('J')) >= 4:
            result = Hand.__HANDRESULTS["Five of a kind"]
        else:
            nonjokercards = [c for c in self.cards if c != 'J']
            cardcount = sorted(Counter(nonjokercards).values(), reverse=True)

            match cardcount[0] + jokercount:
                case 5:
                    result = Hand.__HANDRESULTS["Five of a kind"]
                case 4:
                    result = Hand.__HANDRESULTS["Four of a kind"]
                case 3:
                    if cardcount[1] == 2:
                        result = Hand.__HANDRESULTS["Full house"]
                    else:
                        result = Hand.__HANDRESULTS["Three of a kind"]
                case 2:
                    if cardcount[1] == 2:
                        result = Hand.__HANDRESULTS["Two pair"]
                    else:
                        result = Hand.__HANDRESULTS["One pair"]
                case 1:
                    result = Hand.__HANDRESULTS["High card"]
        cardstring = ''
        for card in self.cards:
            if card == 'J':
                cardstring += '1'
            else:
                cardstring += Hand.__CARDLIST[card]
        return int(str(result) + cardstring, 16)


class CamelCards:
    def __init__(self, rawstr: str) -> None:
        self.__hands = []
        for line in rawstr.splitlines():
            left, right = line.split()
            self.__hands.append(Hand(left, int(right)))

    def get_winnings(self, use_jokers: bool = False) -> int:
        if use_jokers:
            self.__hands.sort(key=lambda a: a.gethandpower_jokers())
        else:
            self.__hands.sort(key=lambda a: a.gethandpower())
        return sum([hand.bid * (rank + 1) for rank, hand in enumerate(self.__hands)])


def main() -> int:
    with open("../Inputfiles/aoc7.txt", "r") as file:
        mygame = CamelCards(file.read().strip('\n'))
    print(f"Part 1: {mygame.get_winnings()}")
    print(f"Part 2: {mygame.get_winnings(True)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
