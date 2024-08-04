"""
Pretty much just walk through the string and generate the new number, so basically brute-force. Part 1 is decently
fast but part 2 takes a couple of seconds. Might need to investigate further in the future if there are more clever
ways to approach this, such as grouping by repeating patterns of sub-numbers or similar.
"""
import sys
from pathlib import Path

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2015/day10.txt')


class LookAndSay:
    def __init__(self, rawstr: str) -> None:
        self.__startnbrs = rawstr

    def get_generated_length(self, rounds: int) -> int:
        sequence = self.__startnbrs
        for _ in range(rounds):
            new_seq = ''
            count = 0
            currentchar = ''
            for c in sequence:
                if c == currentchar:
                    count += 1
                else:
                    if count > 0:
                        new_seq += str(count) + currentchar
                    count = 1
                    currentchar = c
            if count > 0:
                new_seq += str(count) + currentchar
            sequence = new_seq
        return len(sequence)


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        game = LookAndSay(file.read().strip('\n'))
    print(f"Part 1: {game.get_generated_length(40)}")
    print(f"Part 2: {game.get_generated_length(50)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
