import sys
from pathlib import Path
from enum import Enum

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2022/day02.txt')


class Hand(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2

    def get_score(self, other: "Hand") -> int:
        if self == other:  # Draw
            return 3 + other.value + 1
        elif (self.value + 1) % 3 == other.value:  # Other wins
            return 6 + other.value + 1
        return other.value + 1

    def determine_response(self, guide: str) -> "Hand":
        match guide:
            case 'X':  # Lose
                return Hand((self.value + 2) % 3)
            case 'Z':  # Win
                return Hand((self.value + 1) % 3)
            case _:  # Draw
                return self


class StrategyBook:
    def __init__(self, rawstr: str) -> None:
        left_map = {'A': Hand.ROCK, 'B': Hand.PAPER, 'C': Hand.SCISSORS}
        self.__rounds: list[tuple[Hand, str]] = [(left_map[left], right) for left, right in
                                                 [line.split() for line in rawstr.splitlines()]]

    def get_assumed_total_score(self) -> int:
        right_map = {'X': Hand.ROCK, 'Y': Hand.PAPER, 'Z': Hand.SCISSORS}
        return sum([opponent.get_score(right_map[you]) for opponent, you in self.__rounds])

    def get_correct_total_score(self) -> int:
        return sum([opponent.get_score(opponent.determine_response(you)) for opponent, you in self.__rounds])


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        book = StrategyBook(file.read().strip('\n'))
    print(f"Part 1: {book.get_assumed_total_score()}")
    print(f"Part 2: {book.get_correct_total_score()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
