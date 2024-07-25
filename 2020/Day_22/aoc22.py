"""
Kinda straightforward, just a bit messy with the recursion bit, and somewhat slow, can probably be improved by using
dequeue instead of the regular pop.
"""
import sys
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


def main() -> int:
    with open('../Inputfiles/aoc22.txt', 'r') as file:
        mygame = Combat(file.read().strip('\n'))
    print(f"Part 1: {mygame.play_combat()}")
    print(f"Part 2: {mygame.play_recursive_combat()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())