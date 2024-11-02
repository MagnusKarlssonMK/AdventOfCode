"""
Kinda straightforward, just a bit messy with the recursion bit, and somewhat slow, can probably be improved by using
dequeue instead of the regular pop.
"""
import time
from pathlib import Path
from copy import deepcopy


class Combat:
    def __init__(self, rawstr: str) -> None:
        self.__players = {}
        for i, nbrs in enumerate(rawstr.split('\n\n')):
            self.__players[i] = list(map(int, nbrs.splitlines()[1:]))

    def play_combat(self) -> int:
        players = deepcopy(self.__players)
        while all([len(nbrs) > 0 for nbrs in players.values()]):
            draw = [players[p].pop(0) for p in players]
            winner = draw.index(max(draw))
            players[winner].append(draw[winner])
            players[winner].append(draw[(winner + 1) % 2])
        return sum([(i + 1) * card for i, card in enumerate(reversed(players[0 if len(players[0]) > 0 else 1]))])

    def __play_recursive_game(self, players_data):
        players = deepcopy(players_data)
        seen = set()
        while all([len(nbrs) > 0 for nbrs in players.values()]):
            if (current := str(players[0]) + str(players[1])) in seen:
                players[0] += players[1]
                players[1] = []
                return players
            else:
                seen.add(current)
            draw = [players[p].pop(0) for p in players]
            if all(draw[p] <= len(players[p]) for p in players):
                recursive_players = {p: list(players[p][:draw[p]]) for p in players}
                recursion = self.__play_recursive_game(recursive_players)
                winner = 0 if not recursion[1] else 1
            else:
                winner = draw.index(max(draw))
            players[winner].append(draw[winner])
            players[winner].append(draw[(winner + 1) % 2])
        return players

    def play_recursive_combat(self) -> int:
        players = deepcopy(self.__players)
        players = self.__play_recursive_game(players)
        return sum([(i + 1) * card for i, card in enumerate(reversed(players[0 if len(players[0]) > 0 else 1]))])


def main(aoc_input: str) -> None:
    mygame = Combat(aoc_input)
    print(f"Part 1: {mygame.play_combat()}")
    print(f"Part 2: {mygame.play_recursive_combat()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2020/day22.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
