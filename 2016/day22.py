"""
Part 1: Just parse the data into a dict representing the nodes keyed with (x, y) of each node. Then go through the
possible pair combinations of the nodes and count how many are fulfilling the conditions for transfer.

Part 2: Uhhhh....

So.... I guess this is kind of the equivalent of getting Rick-rolled in AoC...

All pairs in part 1 contain the same empty node (x=15, y=29 in my case). So for part 2 we first need to move that empty
node to the top right corner, and the path is partially blocked by a line of full nodes. Once there we can move the
'G' node to the left by stepping around it, so moving it one tile costs 5 steps. This is easiest done by simply printing
the grid and then calculate the answer by hand, but to keep it at least a little bit as a programming exercise:
1. Find the closest path from the empty node to G with a quick BFS, just to get a generic solution to handle the full
nodes.
2. Add the row length multiplied by 5 for the cost of moving G to the top left.
"""
import sys
from pathlib import Path
import re
from dataclasses import dataclass
from itertools import combinations

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2016/day22.txt')


@dataclass
class Node:
    size: int
    used: int
    avail: int
    use: int


class Cluster:
    def __init__(self, rawstr: str) -> None:
        self.__nodes = {}
        self.__max_x = 0
        self.__max_y = 0
        self.__zeronode = None
        for line in rawstr.splitlines():
            nbrs = list(map(int, re.findall(r"\d+", line)))
            if len(nbrs) == 6:
                self.__nodes[(nbrs[0], nbrs[1])] = Node(*nbrs[2:])
                self.__max_x = max(self.__max_x, nbrs[0])
                self.__max_y = max(self.__max_y, nbrs[1])
                if not self.__zeronode and nbrs[3] == 0:
                    self.__zeronode = nbrs[0], nbrs[1]

    def get_viable_pairs_count(self) -> int:
        count = 0
        for a, b in combinations(self.__nodes, 2):
            if 0 < self.__nodes[a].used < self.__nodes[b].avail:
                count += 1
            elif 0 < self.__nodes[b].used < self.__nodes[a].avail:
                count += 1
        return count

    def get_fewest_steps_count(self) -> int:
        # Step 1 - find nbr of steps to move zero-node to G
        g_steps = 0
        node_g = self.__max_x, 0
        seen = set()
        queue = [(self.__zeronode, 0)]
        while queue:
            nextnode, steps = queue.pop(0)
            if nextnode == node_g:
                g_steps = steps
                break
            if nextnode in seen:
                continue
            seen.add(nextnode)
            for d in ((-1, 0), (1, 0), (0, -1)):  # No reason to ever go +1 in y
                n = nextnode[0] + d[0], nextnode[1] + d[1]
                if n in self.__nodes and self.__nodes[n].used < self.__nodes[self.__zeronode].size:
                    queue.append((n, steps + 1))

        # Step 2 - add the cost for moving G to top left
        return g_steps + (5 * (self.__max_x - 1))


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        cluster = Cluster(file.read().strip('\n'))
    print(f"Part 1: {cluster.get_viable_pairs_count()}")
    print(f"Part 2: {cluster.get_fewest_steps_count()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
