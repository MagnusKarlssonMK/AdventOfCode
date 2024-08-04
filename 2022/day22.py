"""
Stores the input data in a map class, which splits the input into 6 different 'faces' and then generates
the neighbor relations in all 4 directions between those. These relations will be different for part 1 and 2.
For part 1, if there is no immediate neighbor in a certain direction, keep searching in that direction until it wraps
around and finds the first face on the other side.
For part 2, the relations can be found by determining the closest distance between faces, with the additional rules
that a face can only connect to a specific face once.

With the neighbor relations (including relative rotation information) setup, we can simply follow the instructions
and walk the map, using the face relation info whenever going out of bounds of the current face.

A lot of the coordinate and direction handling would probably have been much smoother by using a proper point class
or vector or similar, so there is quite a bit of room for improvement in the details.
"""
import sys
from pathlib import Path
import re

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2022/day22.txt')


class Face:
    def __init__(self, faceid: tuple[int, int], rawgrid: list[str],
                 startrow: int, endrow: int, startcol: int, endcol: int) -> None:
        self.id = faceid
        self.gridlines = [''.join([rawgrid[row][col] for col in range(startcol, endcol)])
                          for row in range(startrow, endrow)]
        self.neighbors = {}  # Flat mapping according to Part 1
        self.cube_neighbors = {}  # Cube mapping according to Part 2

    def add_neighbor(self, neighbor: tuple[int, int], src_direction: tuple[int, int],
                     dest_direction: tuple[int, int], iscube: bool) -> None:
        if iscube:
            self.cube_neighbors[src_direction] = (neighbor, dest_direction)
        else:
            self.neighbors[src_direction] = (neighbor, dest_direction)

    def __repr__(self):
        return f"FaceID: {self.id}"


class MonkeyMap:
    DIRECTIONS = ((-1, 0), (0, 1), (1, 0), (0, -1))
    FACING = {(0, 1): 0, (1, 0): 1, (0, -1): 2, (-1, 0): 3}

    def __init__(self, grid: str, path: str):
        self.__path: list[str] = re.findall(r"\d+|\w", path)
        self.__startface = -1
        self.__startpos = -1, 1
        self.__direction = 0, 1
        lines = grid.splitlines()
        rows = len(lines)
        cols = max(len(line) for line in lines)
        face_rows = 4
        face_cols = 4
        # We know it has to be either a 3x4 or a 4x3 grid size for the face layout
        if rows > cols:
            face_cols -= 1
        else:
            face_rows -= 1
        # We also know that the faces have to be square, i.e. width == height, so just keep one value for both
        self.__face_len = rows // face_rows
        if (cols // face_cols) != self.__face_len:
            print("Input warning: mismatch face dimensions!")
        self.__faces = {}
        startfound = False
        for f_row in range(face_rows):
            for f_col in range(face_cols):
                c = f_col * self.__face_len
                r = f_row * self.__face_len
                if c < len(lines[r]):
                    if lines[r][c] != " ":
                        self.__faces[(f_row, f_col)] = Face((f_row, f_col),
                                                            lines, r, r + self.__face_len, c, c + self.__face_len)
                        if not startfound:
                            self.__startface = f_row, f_col
                            # Get start position - Top left entry will be in the first face we find
                            for i, c in enumerate(self.__faces[(f_row, f_col)].gridlines[0]):
                                if c != "#":
                                    self.__startpos = 0, i
                                    startfound = True
                                    break
        # Find neighbors
        # Part 1 - when reaching an edge (no neighbor face), jump to the other side and keep going in the same direction
        for f in self.__faces:
            row, col = f
            for dr, dc in self.DIRECTIONS:
                for step in range(1, 5):  # Keep going in one direction until we hit the first match (% for wrap)
                    r = (row + dr * step) % face_rows
                    c = (col + dc * step) % face_cols
                    if (r, c) in self.__faces:
                        self.__faces[f].add_neighbor((r, c), (dr, dc),
                                                     (dr, dc), False)
                        break
        # Part 2 - BFS to find the connecting sides and relative rotations
        queue = []
        for node in self.__faces:
            for d in self.DIRECTIONS:
                queue.append((node, d, (node[0] + d[0], node[1] + d[1]), d, {node}))
        while queue:
            originnode, outdir, currentnode, currentdir, seen = queue.pop(0)
            if outdir in self.__faces[originnode].cube_neighbors:  # Skip if we have already found a neighbor here
                continue
            if currentnode in self.__faces:
                if (currentnode != originnode and
                        (-currentdir[0], -currentdir[1]) not in self.__faces[currentnode].cube_neighbors):
                    for d in self.__faces[originnode].cube_neighbors:
                        if self.__faces[originnode].cube_neighbors[d][0] == currentnode:
                            break  # Can only connect to the same face once
                    else:
                        self.__faces[originnode].add_neighbor(currentnode, outdir, currentdir, True)
                        self.__faces[currentnode].add_neighbor(originnode, (-currentdir[0], -currentdir[1]),
                                                               (-outdir[0], -outdir[1]), True)
            else:
                seen.add(currentnode)
                for newdir in self.DIRECTIONS:
                    newnode = currentnode[0] + newdir[0], currentnode[1] + newdir[1]
                    if -1 <= newnode[0] <= face_rows and -1 <= newnode[1] <= face_cols:  # Limit the travel space
                        if newnode not in seen:
                            queue.append((originnode, outdir, newnode, newdir, seen))

    def get_password(self, iscube: bool = False) -> int:
        direction = self.__direction
        face = self.__startface
        row, col = self.__startpos
        for instruction in self.__path:
            if instruction.isdigit():
                for _ in range(int(instruction)):
                    newrow = row + direction[0]
                    newcol = col + direction[1]
                    if 0 <= newrow < self.__face_len and 0 <= newcol < self.__face_len:
                        if self.__faces[face].gridlines[newrow][newcol] == '#':
                            break
                        row = newrow
                        col = newcol
                    else:  # Move to neighbor face and rotate direction if needed
                        newface, newdir = (self.__faces[face].cube_neighbors[direction] if iscube
                                           else self.__faces[face].neighbors[direction])
                        newrow %= self.__face_len  # Flip the coordinate in our direction to the other side
                        newcol %= self.__face_len  # Lazy way - mod on both instead of checking against direction
                        rotation = direction
                        while rotation != newdir:
                            # Rotate clock-wise until our direction is correct
                            rotation = self.DIRECTIONS[(self.DIRECTIONS.index(rotation) + 1) % len(self.DIRECTIONS)]
                            tmp = newrow
                            newrow = newcol
                            newcol = self.__face_len - 1 - tmp
                        if self.__faces[newface].gridlines[newrow][newcol] == '#':
                            # No need to keep the loop going if we bump into a wall
                            break
                        row = newrow
                        col = newcol
                        direction = newdir
                        face = newface
            else:
                if instruction == 'R':
                    direction = self.DIRECTIONS[(self.DIRECTIONS.index(direction) + 1) % len(self.DIRECTIONS)]
                elif instruction == 'L':
                    direction = self.DIRECTIONS[(self.DIRECTIONS.index(direction) - 1) % len(self.DIRECTIONS)]
        # Convert to global coordinates for the final calculation
        row += face[0] * self.__face_len
        col += face[1] * self.__face_len
        return (1000 * (row + 1)) + (4 * (col + 1)) + self.FACING[direction]


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        grid, path = file.read().strip('\n').split('\n\n')
    mymap = MonkeyMap(grid, path)
    print(f"Part 1: {mymap.get_password()}")
    print(f"Part 2: {mymap.get_password(True)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
