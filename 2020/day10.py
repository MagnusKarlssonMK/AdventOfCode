"""
Part 1: sort the parsed input, add 0 at the start and max+3 at the end, then simply make a counter object to put the
value differences into.
Part 2: create an adjacency list / DAG out of the possible other adapters that one adapter can connect to, then apply a
memoized DFS to count the number of paths.
"""
import time
from pathlib import Path
from collections import Counter


class Device:
    def __init__(self, rawstr: str) -> None:
        self.__ratings = sorted(list(map(int, rawstr.splitlines())))
        self.__ratings.append(self.__ratings[-1] + 3)
        self.__ratings.insert(0, 0)

    def get_jolt_differences(self) -> int:
        diff = Counter()
        for i in range(len(self.__ratings) - 1):
            diff[self.__ratings[i+1] - self.__ratings[i]] += 1
        return diff[1] * diff[3]

    def get_nbr_adapter_arrangements(self) -> int:
        adj = {}
        for i in range(len(self.__ratings) - 1):
            adj[self.__ratings[i]] = []
            for j in range(i + 1, i + 4):
                if j >= len(self.__ratings) or self.__ratings[j] - self.__ratings[i] > 3:
                    break
                else:
                    adj[self.__ratings[i]].append(self.__ratings[j])
        start = self.__ratings[0]
        return pathcount(adj, start, {})


def pathcount(dag, vertex, memo) -> int:
    if vertex in memo:
        return memo[vertex]
    elif vertex in dag:
        memo[vertex] = sum([pathcount(dag, x, memo) for x in dag[vertex]])
        return memo[vertex]
    else:
        return 1


def main(aoc_input: str) -> None:
    device = Device(aoc_input)
    print(f"Part 1: {device.get_jolt_differences()}")
    print(f"Part 2: {device.get_nbr_adapter_arrangements()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2020/day10.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
