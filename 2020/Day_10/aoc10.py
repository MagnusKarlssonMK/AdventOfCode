"""
Part 1: sort the parsed input, add 0 at the start and max+3 at the end, then simply make a counter object to put the
value differences into.
Part 2: create an adjacency list / DAG out of the possible other adapters that one adapter can connect to, then apply a
memoized DFS to count the number of paths.
"""
import sys
from collections import Counter


def part1(ratings: list[int]) -> int:
    diff = Counter()
    for i in range(len(ratings) - 1):
        diff[ratings[i+1] - ratings[i]] += 1
    return diff[1] * diff[3]


def part2(ratings: list[int]) -> int:
    adj = {}
    for i in range(len(ratings) - 1):
        adj[ratings[i]] = []
        for j in range(i + 1, i + 4):
            if j >= len(ratings) or ratings[j] - ratings[i] > 3:
                break
            else:
                adj[ratings[i]].append(ratings[j])
    start = ratings[0]
    return pathcount(adj, start, {})


def pathcount(dag, vertex, memo) -> int:
    if vertex in memo:
        return memo[vertex]
    elif vertex in dag:
        memo[vertex] = sum([pathcount(dag, x, memo) for x in dag[vertex]])
        return memo[vertex]
    else:
        return 1


def main() -> int:
    with open('../Inputfiles/aoc10.txt', 'r') as file:
        ratings = sorted(list(map(int, file.read().strip('\n').splitlines())))
    ratings.append(ratings[-1] + 3)
    ratings.insert(0, 0)
    print("Part 1:", part1(ratings))
    print("Part 2:", part2(ratings))
    return 0


if __name__ == "__main__":
    sys.exit(main())
