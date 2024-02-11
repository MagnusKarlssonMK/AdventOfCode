"""
Solution: store the input as an adjacency list, and then perform a sort of modified BFS, where instead of saving a
'visited' list, the entire path is stored instead of just previously visited. Once the end node is found, the
path is stored and finally counted once the queue is emptied. For Part 2, just add a condition that one small cave
be visited one extra time, and add that flag to the queue.
"""
import sys


class Cavesystem:
    def __init__(self, pathlist: list[tuple[str, str]]):
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


def main() -> int:
    with open('../Inputfiles/aoc12.txt', 'r') as file:
        paths = [(node[0], node[1]) for node in [line.split('-') for line in file.read().strip('\n').splitlines()]]
    cave = Cavesystem(paths)
    print("Part 1:", cave.findallpaths())
    print("Part 2:", cave.findallpaths(1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
