import sys
import re
import timeit

XYZ_Coordinate = tuple[int, int, int]


class GroundZero:
    """Class used to create a 3d grid of the highest Z position for each XY tile along with the ID of the brick
    that added that tile."""
    def __init__(self, x_size: int, y_size: int):
        self.count = 0
        self.grid = [[[0, ""] for _ in range(y_size)] for _ in range(x_size)]

    def dropnewbrick(self, xyz: XYZ_Coordinate, dxyz: XYZ_Coordinate, uid: str) -> [int, [str]]:
        """Finds the lowest available Z-coordinate for brick with ID 'uid' and updates the grid with the new brick.
        Returns the new lowest Z-value and a list of the id's of the bricks it is resting on."""
        new_z = 0
        retidlist = []
        for x in range(xyz[0], xyz[0] + dxyz[0] + 1):
            for y in range(xyz[1], xyz[1] + dxyz[1] + 1):
                if self.grid[x][y][0] + 1 >= new_z:
                    if self.grid[x][y][0] + 1 > new_z:
                        retidlist.clear()
                        new_z = self.grid[x][y][0] + 1
                    retidlist.append(self.grid[x][y][1])
        for x in range(xyz[0], xyz[0] + dxyz[0] + 1):
            for y in range(xyz[1], xyz[1] + dxyz[1] + 1):
                self.grid[x][y] = [new_z + dxyz[2], uid]
        self.count += 1
        filtered_retidlist = []
        [filtered_retidlist.append(someid) for someid in retidlist if someid not in filtered_retidlist and someid != ""]
        return [new_z, filtered_retidlist]


class Brick:
    """A simple coordinate holder for a brick. The representation is one [X,Y,Z] list and one [dX,dY,dZ] list"""
    def __init__(self, xyz1: XYZ_Coordinate, xyz2: XYZ_Coordinate):
        self.xyz: XYZ_Coordinate = min(xyz1[0], xyz2[0]), min(xyz1[1], xyz2[1]), min(xyz1[2], xyz2[2])
        self.dxyz: XYZ_Coordinate = abs(xyz1[0] - xyz2[0]), abs(xyz1[1] - xyz2[1]), abs(xyz1[2] - xyz2[2])

    def __str__(self):
        return f"XYZ: {self.xyz} - dXYZ: {self.dxyz}"


class Grid:
    def __init__(self):
        self.moving_bricks: list[Brick] = []
        self.resting_bricks: dict[str: Brick, [str], [str]] = {}  # {id: Brick, down-ids, up-ids}
        self.state = "open"
        self.gz = None
        self.x_max = 0
        self.y_max = 0

    def addbrick(self, rawstr: str) -> None:
        """Adds a brick to the grid with the raw string from AoC input row."""
        if self.state != "open":
            return
        left, right = rawstr.split("~")
        l_list = [int(nbr) for nbr in re.findall(r"\d+", left)]
        r_list = [int(nbr) for nbr in re.findall(r"\d+", right)]
        self.moving_bricks.append(Brick(tuple(l_list), tuple(r_list)))
        # print(self.moving_bricks[-1])

    def unfreeze(self) -> None:
        """Locks the grid and drops the bricks as far down in Z-plane as possible."""
        self.state = "locked"
        for brick in self.moving_bricks:
            self.x_max = max(self.x_max, 1 + brick.xyz[0] + brick.dxyz[0])
            self.y_max = max(self.y_max, 1 + brick.xyz[1] + brick.dxyz[1])
        self.gz = GroundZero(self.x_max, self.y_max)
        # sort elements in moving bricks by z
        self.moving_bricks.sort(key=lambda br: br.xyz[2])

        # tmpbrickids = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
        while len(self.moving_bricks) > 0:
            nextbrick = self.moving_bricks.pop(0)
            brickid = str(nextbrick.xyz[0]) + "-" + str(nextbrick.xyz[1]) + "-" + str(nextbrick.xyz[2])
            newz = self.gz.dropnewbrick(nextbrick.xyz, nextbrick.dxyz, brickid)
            self.resting_bricks[brickid] = [Brick((nextbrick.xyz[0], nextbrick.xyz[1], newz[0]),
                                                  (nextbrick.xyz[0] + nextbrick.dxyz[0],
                                                   nextbrick.xyz[1] + nextbrick.dxyz[1], newz[0] + nextbrick.dxyz[2])),
                                            newz[1], []]
            for uplink in newz[1]:
                self.resting_bricks[uplink][2].append(brickid)

    def getnbrofsafebricks(self) -> int:
        """Returns the number of bricks that can safely be removed from the resting grid
        without causing any other brick to fall."""
        if self.state != "locked":
            return -1
        retval = 0
        for itemkey in list(self.resting_bricks.keys()):
            upholdingbricks = self.resting_bricks[itemkey][2]
            if all(len(self.resting_bricks[up][1]) > 1 for up in upholdingbricks):
                retval += 1
        return retval

    def gettotalnbrofdisintegratedbricks(self) -> int:
        """Solves the second part of calculating the total sum number of bricks that would disintegrate as chain
        reaction when disintegrating each individual brick."""
        retval = 0
        for nextkey in list(self.resting_bricks.keys()):
            poofqueue: list[str] = self.resting_bricks[nextkey][2]
            poofed = {nextkey}
            while len(poofqueue) > 0:
                poof = poofqueue.pop(0)
                if all(down in poofed for down in self.resting_bricks[poof][1]):
                    poofed.update({poof})
                    for up in self.resting_bricks[poof][2]:
                        if up not in poofqueue:
                            poofqueue.append(up)
            retval += len(poofed) - 1
        return retval


def main() -> int:
    mygrid = Grid()

    with open("aoc22.txt", "r") as file:
        for line in file.readlines():
            mygrid.addbrick(line.strip("\n"))

    timestamp = timeit.default_timer()
    mygrid.unfreeze()
    timestamp = timeit.default_timer() - timestamp
    print("Part1: ", mygrid.getnbrofsafebricks())
    print("Time: ", timestamp)

    timestamp = timeit.default_timer()
    partb = mygrid.gettotalnbrofdisintegratedbricks()
    timestamp = timeit.default_timer() - timestamp
    print("Part2: ", partb)
    print("Time: ", timestamp)
    return 0


if __name__ == "__main__":
    sys.exit(main())
