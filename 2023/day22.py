"""
Sort of 3d tetris in the start to let the bricks fall down as far as possible. To speed this up, bricks are dropped in
order of original height, and the highest point for any XY coordinate is stored as a sort 'ground zero' and updated
after every dropped brick.
"""
import sys
from dataclasses import dataclass


@dataclass
class Coord3D:
    x: int
    y: int
    z: int

    def __add__(self, other: "Coord3D") -> "Coord3D":
        return Coord3D(self.x + other.x, self.y + other.y, self.z + other.z)


class Brick:
    """A simple coordinate holder for a brick. The representation is one [X,Y,Z] list and one [dX,dY,dZ] list"""
    def __init__(self, xyz1: Coord3D, xyz2: Coord3D):
        self.pos: Coord3D = Coord3D(min(xyz1.x, xyz2.x), min(xyz1.y, xyz2.y), min(xyz1.z, xyz2.z))
        self.dpos: Coord3D = Coord3D(abs(xyz1.x - xyz2.x), abs(xyz1.y - xyz2.y), abs(xyz1.z - xyz2.z))
        self.id: str = str(self.pos.x) + "-" + str(self.pos.y) + "-" + str(self.pos.z)

    def __str__(self):
        return f"XYZ: {self.pos} - dXYZ: {self.dpos}"


class GroundZero:
    """Class used to create a 3d grid of the highest Z position for each XY tile along with the ID of the brick
    that added that tile."""
    def __init__(self, x_size: int, y_size: int) -> None:
        self.__count = 0
        self.__grid = [[(0, '') for _ in range(y_size)] for _ in range(x_size)]

    def drop_newbrick(self, brick: Brick) -> [int, set[str]]:
        """Finds the lowest available Z-coordinate for brick with ID 'uid' and updates the grid with the new brick.
        Returns the new lowest Z-value and a list of the id's of the bricks it is resting on."""
        new_z = 0
        ret_idlist = []
        nextpos = brick.pos + brick.dpos
        for x in range(brick.pos.x, nextpos.x + 1):
            for y in range(brick.pos.y, nextpos.y + 1):
                if self.__grid[x][y][0] + 1 >= new_z:
                    if self.__grid[x][y][0] + 1 > new_z:
                        ret_idlist.clear()
                        new_z = self.__grid[x][y][0] + 1
                    ret_idlist.append(self.__grid[x][y][1])
        for x in range(brick.pos.x, nextpos.x + 1):
            for y in range(brick.pos.y, nextpos.y + 1):
                self.__grid[x][y] = (new_z + brick.dpos.z, brick.id)
        self.__count += 1
        filtered_ret_idlist = {someid for someid in ret_idlist if someid != ""}
        return [new_z, filtered_ret_idlist]


class Grid:
    def __init__(self, rawstr: str) -> None:
        self.__moving_bricks: list[Brick] = []
        self.__resting_bricks: dict[str: Brick, [str], [str]] = {}  # {id: Brick, down-ids, up-ids}
        for line in rawstr.splitlines():
            left, right = line.split("~")
            x1, y1, z1 = [int(nbr) for nbr in left.split(',')]
            x2, y2, z2 = [int(nbr) for nbr in right.split(',')]
            self.__moving_bricks.append(Brick(Coord3D(x1, y1, z1), Coord3D(x2, y2, z2)))

    def get_safebricks_count(self) -> int:
        """Drops the bricks to rest state and returns the number of bricks that can safely be removed from the resting
        grid without causing any other brick to fall."""
        x_max = 0
        y_max = 0
        for brick in self.__moving_bricks:
            x_max = max(x_max, brick.pos.x + brick.dpos.x + 1)
            y_max = max(y_max, brick.pos.y + brick.dpos.y + 1)
        groundzero = GroundZero(x_max, y_max)
        # Sort elements in moving bricks by z
        self.__moving_bricks.sort(key=lambda br: br.pos.z)
        # Start dropping bricks
        while self.__moving_bricks:
            nextbrick = self.__moving_bricks.pop(0)
            newz = groundzero.drop_newbrick(nextbrick)
            self.__resting_bricks[nextbrick.id] = \
                [Brick(Coord3D(nextbrick.pos.x, nextbrick.pos.y, newz[0]),
                       Coord3D(nextbrick.pos.x + nextbrick.dpos.x, nextbrick.pos.y + nextbrick.dpos.y, newz[0] +
                               nextbrick.dpos.z)), newz[1], []]
            for uplink in newz[1]:
                self.__resting_bricks[uplink][2].append(nextbrick.id)
        # Find number of bricks that can be safely removed
        retval = 0
        for brickid in self.__resting_bricks:
            upholdingbricks = self.__resting_bricks[brickid][2]
            if all(len(self.__resting_bricks[up][1]) > 1 for up in upholdingbricks):
                retval += 1
        return retval

    def get_disintegrated_count(self) -> int:
        """Solves the second part of calculating the total sum number of bricks that would disintegrate as chain
        reaction when disintegrating each individual brick."""
        retval = 0
        for brick in self.__resting_bricks:
            queue: list[str] = self.__resting_bricks[brick][2]
            disintegrated = {brick}
            while queue:
                poof = queue.pop(0)
                if all(down in disintegrated for down in self.__resting_bricks[poof][1]):
                    disintegrated.update({poof})
                    [queue.append(up) for up in self.__resting_bricks[poof][2] if up not in queue]
            retval += len(disintegrated) - 1
        return retval


def main() -> int:
    with open('../Inputfiles/aoc22.txt', 'r') as file:
        mygrid = Grid(file.read().strip('\n'))
    print(f"Part 1: {mygrid.get_safebricks_count()}")
    print(f"Part 2: {mygrid.get_disintegrated_count()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
