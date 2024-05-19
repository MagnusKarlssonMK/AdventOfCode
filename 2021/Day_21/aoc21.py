"""
Recursive solution, using pre-computed values for part 2 to generate possible rolls and the corresponding number of
combinations yielding that roll. Also uses memo from functools to get the recursion done in decent time.
"""
import sys
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class Gamestate:
    """Note that player positions and score changes place after every move, so the player in turn for the next move
    is always in the first position."""
    playerpos: tuple
    diceroll_count: int = 0
    playerscore: tuple = (0, 0)

    def get_practice_score(self) -> int:
        """Gets the answer for part 1. A bit fiddly to get right since the positions and dice rolls start from 1,
        not 0."""
        newpos = 1 + (self.playerpos[0] + 2 + 3 * (self.diceroll_count + 1)) % 10
        if (newscore := self.playerscore[0] + newpos) >= 1000:
            return self.playerscore[1] * (self.diceroll_count + 3)
        else:
            nextstate = Gamestate((self.playerpos[1], newpos), self.diceroll_count + 3, (self.playerscore[1], newscore))
            return nextstate.get_practice_score()

    @lru_cache(maxsize=None)
    def get_dirac_score(self) -> tuple[int, int]:
        __FR_MAP = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}
        if self.playerscore[1] >= 21:
            return 0, 1
        else:
            wins1, wins2 = 0, 0
            for roll, nbr in __FR_MAP.items():
                newpos = 1 + (self.playerpos[0] + roll - 1) % 10
                w = Gamestate((self.playerpos[1], newpos), self.diceroll_count,
                              (self.playerscore[1], self.playerscore[0] + newpos)).get_dirac_score()
                wins1 = wins1 + nbr * w[1]
                wins2 = wins2 + nbr * w[0]
            return wins1, wins2


class Game:
    def __init__(self, rawstr: str) -> None:
        self.__players_startpositions = tuple([int(line.split()[-1]) for line in rawstr.splitlines()])

    def get_finalscore(self, practice: bool = True) -> int:
        game = Gamestate(self.__players_startpositions)
        if practice:
            return game.get_practice_score()
        else:
            return max(game.get_dirac_score())


def main() -> int:
    with open('../Inputfiles/aoc21.txt', 'r') as file:
        game = Game(file.read().strip('\n'))
    print(f"Part 1: {game.get_finalscore()}")
    print(f"Part 2: {game.get_finalscore(False)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
