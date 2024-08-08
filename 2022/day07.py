"""
Create a main class to hold the file system and a class to represent a directory, which in turn contains a list of
__files and directories. This is initialized while parsing the input, using a 'head' attribute in the file system
containing a list of the directory path to where the commands are issues, and calls to directires are done recursively.
"""
import sys
from pathlib import Path

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2022/day07.txt')


class Directory:
    def __init__(self, name: str) -> None:
        self.name = name
        self.__totalfilesize = 0
        self.__totalsubdirsize = -1
        self.__files: dict[str: int] = {}
        self.__subdirectories: dict[str: Directory] = {}

    def addsubdir(self, path: list[str], dirname: str) -> None:
        if len(path) > 0:
            self.__subdirectories[path[0]].addsubdir(path[1:], dirname)
        else:
            if dirname not in self.__subdirectories.keys():
                self.__subdirectories[dirname] = Directory(dirname)

    def addfile(self, path: list[str], filename: str, size: int) -> None:
        if len(path) > 0:
            self.__subdirectories[path[0]].addfile(path[1:], filename, size)
        else:
            self.__files[filename] = size
            self.__totalfilesize += size

    def gettotalsize(self) -> int:
        if self.__totalsubdirsize >= 0:
            return self.__totalsubdirsize + self.__totalfilesize
        else:
            self.__totalsubdirsize = 0
            for key in list(self.__subdirectories.keys()):
                self.__totalsubdirsize += self.__subdirectories[key].gettotalsize()
            return self.__totalsubdirsize + self.__totalfilesize

    def getfilteredsize(self, limit: int) -> int:
        """Assumes that 'gettotalsize()' has been called first to initialize the cached total size."""
        result = sum([self.__subdirectories[key].getfilteredsize(limit) for key in list(self.__subdirectories.keys())])
        if (self.__totalsubdirsize + self.__totalfilesize) <= limit:
            result += self.__totalsubdirsize + self.__totalfilesize
        return result

    def getsmallest_todelete(self, threshold: int) -> int:
        fromdirs = 0
        bestfromdirs = 0
        for subdir in list(self.__subdirectories.keys()):
            dirsize = self.__subdirectories[subdir].getsmallest_todelete(threshold)
            fromdirs += dirsize
            if dirsize >= threshold:
                bestfromdirs = dirsize if bestfromdirs == 0 else min(dirsize, bestfromdirs)
        if bestfromdirs != 0:  # There is a subdirectory that satisfies the condition
            return bestfromdirs
        else:  # No subdirectory is large enough, best we can do is to return our own size
            return self.__totalfilesize + self.__totalsubdirsize

    def __repr__(self):
        return f"<dir>{list(self.__subdirectories.keys())} <f>{list(self.__files.keys())}"


class FileSystem:
    def __init__(self, rawstr: str):
        self.__root = Directory("/")
        self.__head = []
        for line in [lines.split() for lines in rawstr.splitlines()]:
            match line[0]:
                case "$":
                    if line[1] == "cd":
                        if line[2] == "/":
                            self.__head = []
                        elif line[2] == "..":
                            self.__head.pop()
                        else:
                            self.__head.append(line[2])
                case "dir":
                    self.__root.addsubdir(self.__head, line[1])
                case _:
                    self.__root.addfile(self.__head, line[1], int(line[0]))
        self.__needtodelete = self.__root.gettotalsize() - (70000000 - 30000000)  # Initialize the internal sizes

    def get_filtered_size(self) -> int:
        return self.__root.getfilteredsize(100000)

    def get_smallest_to_delete(self) -> int:
        return self.__root.getsmallest_todelete(self.__needtodelete)


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        myfs = FileSystem(file.read().strip('\n'))
    print(f"Part 1: {myfs.get_filtered_size()}")
    print(f"Part 2: {myfs.get_smallest_to_delete()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
