"""

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

    def findallpaths(self) -> int:
        """Returns number of possible paths from 'start' to 'end'."""
        foundpaths = []
        q = [('start', [])]
        while q:
            currentnode, path = q.pop(0)
            currentpath = [node for node in path]
            currentpath.append(currentnode)
            if currentnode == 'end':
                foundpaths.append(currentpath)
            else:
                for neighbor in self.__adj[currentnode]:
                    if ((neighbor.islower() and neighbor in currentpath) or
                            (neighbor.isupper() and currentnode.isupper() and neighbor == currentpath[-2])):
                        continue
                    q.append((neighbor, currentpath))
        # for path in foundpaths:
        #     print(path)
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
    # print(cave)
    print("Part 1:", cave.findallpaths())
    return 0


if __name__ == "__main__":
    sys.exit(main())
