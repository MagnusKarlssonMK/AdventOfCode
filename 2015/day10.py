"""
Pretty much just walk through the string and generate the new number, so basically brute-force. Part 1 is decently
fast but part 2 takes a couple of seconds. Might need to investigate further in the future if there are more clever
ways to approach this, such as grouping by repeating patterns of sub-numbers or similar.
"""
import time
from pathlib import Path


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


def main(aoc_input: str) -> None:
    game = LookAndSay(aoc_input)
    print(f"Part 1: {game.get_generated_length(40)}")
    print(f"Part 2: {game.get_generated_length(50)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2015/day10.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
