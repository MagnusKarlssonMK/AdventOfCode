"""
Using deque with rotations to get some decent performance.
"""
import sys
from pathlib import Path
from collections import deque

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2018/day09.txt')


class MarbleGame:
    __MULTIPLE = 23
    __REMOVE = 7

    def __init__(self, rawstr: str) -> None:
        w = rawstr.split()
        self.__nbr_players = int(w[0])
        self.__last_marble = int(w[6])

    def get_winning_score(self, marble_multiplier: int = 1) -> int:
        scores: dict[int: int] = {}
        marble_circle = deque([0])
        for marble in range(1, (self.__last_marble * marble_multiplier) + 1):
            if marble % MarbleGame.__MULTIPLE != 0:
                marble_circle.rotate(-1)
                marble_circle.append(marble)
            else:
                marble_circle.rotate(MarbleGame.__REMOVE)
                if marble % self.__nbr_players not in scores:
                    scores[marble % self.__nbr_players] = 0
                scores[marble % self.__nbr_players] += marble + marble_circle.pop()
                marble_circle.rotate(-1)
        return max(scores.values())


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        game = MarbleGame(file.read().strip('\n'))
    print(f"Part 1: {game.get_winning_score()}")
    print(f"Part 2: {game.get_winning_score(100)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
