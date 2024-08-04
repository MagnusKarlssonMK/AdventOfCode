"""
Stores parsed data in a graph, and generates a trimmed variant of it with only the rooms containing a valve
with Floyd-Warshall algorithm.
Then finds the answer with a recursive search using bitmaps.
"""
import sys
from pathlib import Path
import re
from itertools import permutations

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2022/day16.txt')


class ValveNetwork:
    def __init__(self, rawstr: str) -> None:
        self.__adjlist: dict[str: list[str]] = {}
        self.__valves: dict[str: int] = {}
        for line in rawstr.splitlines():
            valves = re.findall(r'[A-Z]{2}', line.strip('Valve'))
            flow = int(re.findall(r'\d+', line)[0])
            self.__adjlist[valves[0]] = [v for v in valves[1:]]
            if flow > 0:
                self.__valves[valves[0]] = flow
        self.__start = 'AA'
        self.__valve_indicies = {valve: 1 << i for i, valve in enumerate(self.__valves)}
        # Create a trimmed version of the adj list with Floyd-Warshall, keep only the nodes with non-zero valves
        self.__distances: dict[tuple[str, str]: int] = {}
        for valve in self.__adjlist:
            for tunnel_to in self.__adjlist:
                if tunnel_to in self.__adjlist[valve]:
                    self.__distances[(valve, tunnel_to)] = 1
                else:
                    self.__distances[(valve, tunnel_to)] = 1000
        for a, b, c in permutations(self.__adjlist, 3):
            self.__distances[b, c] = min(self.__distances[b, c], self.__distances[b, a] + self.__distances[a, c])

    def get_maxflow(self, maxtime: int, train_elephant: bool = False) -> int:
        if train_elephant:
            result = self.__checkroom(self.__start, maxtime, 0, 0, {})
            maxflow = max([flow1 + flow2 for mask1, flow1 in result.items() for mask2, flow2 in result.items()
                           if not mask1 & mask2])
        else:
            maxflow = max(self.__checkroom(self.__start, maxtime, 0, 0, {}).values())
        return maxflow

    def __checkroom(self, valve: str, time: int, bitmask: int, released: int, flow) -> dict[int: int]:
        flow[bitmask] = max(flow.get(bitmask, 0), released)
        for valve2, f in self.__valves.items():
            timeleft = time - self.__distances[valve, valve2] - 1
            if not (self.__valve_indicies[valve2] & bitmask) and timeleft > 0:
                self.__checkroom(valve2, timeleft, bitmask | self.__valve_indicies[valve2],
                                 released + f * timeleft, flow)
        return flow


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        myvalves = ValveNetwork(file.read().strip('\n'))
    print(f"Part 1: {myvalves.get_maxflow(30)}")
    print(f"Part 2: {myvalves.get_maxflow(26, True)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
