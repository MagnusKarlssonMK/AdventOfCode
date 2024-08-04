"""
Create Hand class to store the cards and bid, and provides methods to calculate a power value that can be used to
sort the hands. The power value is generated as a hex value with the hand result in the MSB and card values in LSB,
this way the different hands can be sorted according to the rules. The power calculation method is done in two variants,
one basic for Part 1 and one using jokers for Part 2.
"""
import sys
from pathlib import Path
from enum import Enum
from collections import Counter

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2023/day07.txt')


class HandResults(Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7


class Hand:
    __CARDLIST = {"2": '2', "3": '3', "4": '4', "5": '5', "6": '6', "7": '7', "8": '8', "9": '9',
                  "T": 'A', "J": 'B', "Q": 'C', "K": 'D', "A": 'E'}

    def __init__(self, newcardstring: str, newbid: int):
        self.bid = newbid
        self.__cards = [c for c in newcardstring]

    def gethandpower(self) -> int:
        """Returns the input to Part 1 for this hand."""
        result = HandResults.HIGH_CARD
        cardcount = sorted(Counter(self.__cards).values(), reverse=True)
        match cardcount[0]:
            case 5:
                result = HandResults.FIVE_OF_A_KIND
            case 4:
                result = HandResults.FOUR_OF_A_KIND
            case 3:
                if cardcount[1] == 2:
                    result = HandResults.FULL_HOUSE
                else:
                    result = HandResults.THREE_OF_A_KIND
            case 2:
                if cardcount[1] == 2:
                    result = HandResults.TWO_PAIR
                else:
                    result = HandResults.ONE_PAIR
            case 1:
                result = HandResults.HIGH_CARD
        cardstring = ''.join([Hand.__CARDLIST[c] for c in self.__cards])
        return int(str(result.value) + cardstring, 16)

    def gethandpower_jokers(self) -> int:
        """Returns the input to Part 2 for this hand."""
        result = HandResults.HIGH_CARD
        if (jokercount := self.__cards.count('J')) >= 4:
            result = HandResults.FIVE_OF_A_KIND
        else:
            nonjokercards = [c for c in self.__cards if c != 'J']
            cardcount = sorted(Counter(nonjokercards).values(), reverse=True)

            match cardcount[0] + jokercount:
                case 5:
                    result = HandResults.FIVE_OF_A_KIND
                case 4:
                    result = HandResults.FOUR_OF_A_KIND
                case 3:
                    if cardcount[1] == 2:
                        result = HandResults.FULL_HOUSE
                    else:
                        result = HandResults.THREE_OF_A_KIND
                case 2:
                    if cardcount[1] == 2:
                        result = HandResults.TWO_PAIR
                    else:
                        result = HandResults.ONE_PAIR
                case 1:
                    result = HandResults.HIGH_CARD
        cardstring = ''
        for card in self.__cards:
            if card == 'J':
                cardstring += '1'
            else:
                cardstring += Hand.__CARDLIST[card]
        return int(str(result.value) + cardstring, 16)


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
    with open(INPUT_FILE, 'r') as file:
        mygame = CamelCards(file.read().strip('\n'))
    print(f"Part 1: {mygame.get_winnings()}")
    print(f"Part 2: {mygame.get_winnings(True)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
