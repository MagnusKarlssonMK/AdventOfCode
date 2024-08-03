"""
Perhaps a bit over-engineered solution, but at least it's fast.
First, convert the component list to an adjacency list, each component is given an id corresponding to its row in the
input (any unique id would do, this was the easiest) and stores its strength and the neighbors on either side.
Then to find the answer, run a DFS starting from the components containing the 'zero' connector (BFS by popping from
the other end of the queue works too, but seems slightly slower). The state contains the head (component at the front)
and its available connector side, and the tail (all previously seen components before the head).
For part 1, keep track of the max strength by any found bridge.
For part 2, keep track of the longest bridge found (use strength as secondary selector for equal lengths).
The answer to both parts can be obtained in one go.
"""
import sys


class Bridge:
    def __init__(self, rawstr: str) -> None:
        self.__components = [tuple(map(int, line.split('/'))) for line in rawstr.splitlines()]
        self.__adj = {}  # id: strength, (left connectors), (right connectors)
        self.__zerostarts = []
        for i, (left, right) in enumerate(self.__components):
            left_connects = []
            right_connects = []
            if left == 0:
                self.__zerostarts.append((i, 2))
            elif right == 0:
                self.__zerostarts.append((i, 1))
            for j, (l_c, r_c) in enumerate(self.__components):
                if j == i:
                    continue
                if l_c == left or r_c == left:
                    left_connects.append(j)
                if l_c == right or r_c == right:
                    right_connects.append(j)
            self.__adj[i] = (left + right, tuple(left_connects), tuple(right_connects))

    def get_max_strength(self) -> tuple[int, int]:
        seen = set()
        maxstr = 0
        longest = []
        queue = [(tuple(), z, s) for z, s in self.__zerostarts]  # Tail, head, available connector side
        while queue:
            state = queue.pop()
            if state in seen:
                continue
            seen.add(state)
            tail, head, side = state
            tail = tuple(sorted(list(tail) + [head]))
            maxstr = max(maxstr, sum([self.__adj[t][0] for t in tail]))
            if len(tail) > len(longest):
                longest = tail
            elif len(tail) == len(longest):
                tailstr = sum([self.__adj[t][0] for t in tail])
                l_str = sum([self.__adj[t][0] for t in longest])
                if tailstr > l_str:
                    longest = tail
            for nxt in self.__adj[head][side]:
                if nxt in tail:
                    continue
                if head in self.__adj[nxt][1]:
                    queue.append((tail, nxt, 2))
                if head in self.__adj[nxt][2]:
                    queue.append((tail, nxt, 1))
        return maxstr, sum([self.__adj[t][0] for t in longest])


def main() -> int:
    with open('../Inputfiles/aoc24.txt', 'r') as file:
        bridge = Bridge(file.read().strip('\n'))
    p1, p2 = bridge.get_max_strength()
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
