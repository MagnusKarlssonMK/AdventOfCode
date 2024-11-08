"""
Solution: store the input as an adjacency list, and then perform a sort of modified BFS, where instead of saving a
'visited' list, the entire path is stored instead of just previously visited. Once the end node is found, the
path is stored and finally counted once the queue is emptied. For Part 2, just add a condition that one small cave
be visited one extra time, and add that flag to the queue.
"""
import time
from pathlib import Path


class Cavesystem:
    def __init__(self, rawstr: str) -> None:
        pathlist: list[tuple[str, str]] = [(node[0], node[1]) for node in
                                           [line.split('-') for line in rawstr.splitlines()]]
        self.__adj: dict[str: list[str]] = {}
        for nodes in pathlist:
            for i in range(2):
                if nodes[i] in self.__adj:
                    self.__adj[nodes[i]].append(nodes[(i + 1) % 2])
                else:
                    self.__adj[nodes[i]] = [nodes[(i + 1) % 2]]

    def findallpaths(self, bonusstep: int = 0) -> int:
        """Returns number of possible paths from 'start' to 'end'."""
        foundpaths = []
        q = [('start', [], bonusstep)]
        while q:
            currentnode, path, cbonus = q.pop(0)
            currentpath = [node for node in path]
            currentpath.append(currentnode)
            if currentnode == 'end':
                foundpaths.append(currentpath)
            else:
                for neighbor in self.__adj[currentnode]:
                    nbonus = cbonus
                    if ((neighbor.isupper() and currentnode.isupper() and neighbor == currentpath[-2]) or
                            neighbor == 'start'):
                        continue
                    elif neighbor.islower() and neighbor in currentpath:
                        if nbonus > 0:
                            nbonus -= 1
                        else:
                            continue
                    q.append((neighbor, currentpath, nbonus))
        return len(foundpaths)

    def __str__(self):
        retstr = ""
        for key in list(self.__adj.keys()):
            retstr += key
            retstr += " -> "
            retstr += f"{self.__adj[key]}"
            retstr += '\n'
        return retstr


def main(aoc_input: str) -> None:
    cave = Cavesystem(aoc_input)
    print("Part 1:", cave.findallpaths())
    print("Part 2:", cave.findallpaths(1))


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2021/day12.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
