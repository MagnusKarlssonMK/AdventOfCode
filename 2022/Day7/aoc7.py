import re
import sys


class Directory:
    def __init__(self, name: str):
        self.name = name
        self.totalfilesize = 0
        self.files: dict[str: int] = {}
        self.subdirectories: dict[str: Directory] = {}

    def addsubdir(self, path: list[str]) -> None:
        if len(path) > 1:
            self.subdirectories[path[0]].addsubdir(path[1:])
        else:
            if path[0] not in list(self.subdirectories.keys()):
                self.subdirectories[path[0]] = Directory(path[0])

    def addfiles(self, path: list[str], newfiles) -> None:
        if len(path) > 0:
            self.subdirectories[path[0]].addfiles(path[1:], newfiles)
        else:
            for line in newfiles:
                left, right = line.split()
                if left == "dir":
                    if right not in list(self.subdirectories.keys()):
                        self.subdirectories[right] = Directory(right)
                else:
                    self.files[right] = int(left)
                    self.totalfilesize += int(left)

    def gettotalsize(self, maxsize: int) -> tuple[int, bool]:
        capped = False
        fromdirs = 0
        for subdir in list(self.subdirectories.keys()):
            val, cap = self.subdirectories[subdir].gettotalsize(maxsize)
            fromdirs += val
            if cap:
                capped = True
        fromself = fromdirs + self.totalfilesize
        if maxsize > 0:
            if fromself > maxsize or capped:
                return fromdirs, True
            else:
                return fromself + fromdirs, False
        else:
            return fromself, False
        # The code handling part 1 makes no sense but works somehow, probably need to rethink something

    def getsmallest(self, threshold: int) -> int:
        fromdirs = 0
        bestfromdirs = 0
        for subdir in list(self.subdirectories.keys()):
            dirsize = self.subdirectories[subdir].getsmallest(threshold)
            fromdirs += dirsize
            if dirsize >= threshold:
                bestfromdirs = dirsize if bestfromdirs == 0 else min(dirsize, bestfromdirs)
        if bestfromdirs != 0:
            return bestfromdirs
        else:
            fromself = fromdirs + self.totalfilesize
            return fromself

    def __str__(self):
        return f"<dir>{list(self.subdirectories.keys())} <f>{list(self.files.keys())}"


class Filesystem:
    def __init__(self):
        self.head = ["/"]
        self.root: Directory = Directory("/")

    def handlecommand(self, cmdlist: list[str]) -> None:
        cmd, _, arg = re.findall(r"(\w+)(\s)?(.*)?", cmdlist[0])[0]
        match cmd:
            case 'cd':
                match arg:
                    case '/':
                        self.head = ['/']
                    case '..':
                        self.head.pop()
                    case _:
                        self.head.append(arg)
                        self.root.addsubdir(self.head[1:])
            case 'ls':
                self.root.addfiles(self.head[1:], cmdlist[1:])

    def gettotalsize(self, maxsize: int = 0) -> int:
        return self.root.gettotalsize(maxsize)[0]

    def getsmallestsizeabove(self, threshold: int) -> int:
        return self.root.getsmallest(threshold)


def main() -> int:
    myfs = Filesystem()
    cmdlines = []
    with open('aoc7.txt', 'r') as file:
        rawinput = file.read().strip('\n')
    for cmdlist in rawinput.strip("$ ").split("\n$ "):
        cmdlines.append(cmdlist.splitlines())

    for line in cmdlines:
        myfs.handlecommand(line)

    print("Part1: ", myfs.gettotalsize(100000))

    sizetodelete = myfs.gettotalsize() - (70000000 - 30000000)
    print("Total size: ", myfs.gettotalsize())
    print("Part2: ", myfs.getsmallestsizeabove(sizetodelete))
    return 0


if __name__ == "__main__":
    sys.exit(main())
