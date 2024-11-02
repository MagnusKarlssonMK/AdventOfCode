"""
Pretty much tetris with side controls determined by the jet stream input.
Shapes and grid stored in binary format per row in lists and bitshifted / bitmasked to move and check for overlap.
After every dropped rock, trim the lower part of uncreachable rows by flood-filling from above with a simple BFS,
and store number of trimmed rows.
For part 2, the result will eventually enter a cycle after an initial stabilization phase. So, store a hashed value
based on rock index, jet index and current grid for each dropped rock, and then once a cycle is found, the answer
can be derived from the stored information.
As it turns out, a cycle is found even before getting the answer to Part 1, so the same solution can actually be
used for both anwers. The solution could be optimized to store the result and get the answer to Part 2 immediately,
but it's already fast enough that it isn't really worth the effort.
Breaking the giant drop_rocks function into smaller pieces would be welcome.
"""
import time
from pathlib import Path
from enum import Enum


class Shape(Enum):
    MINUS = 0
    PLUS = 1
    HOOK = 2
    VER_LINE = 3
    BOX = 4

    def get_binary_shape(self) -> tuple[int, list[int]]:  # width, pattern-mask
        match self:
            case Shape.MINUS:
                return 4, [int('1111', 2)]
            case Shape.PLUS:
                return 3, [int('010', 2), int('111', 2), int('010', 2)]
            case Shape.HOOK:
                return 3, [int('111', 2), int('001', 2), int('001', 2)]
            case Shape.VER_LINE:
                return 1, [int('1', 2) for _ in range(4)]
            case Shape.BOX:
                return 2, [int('11', 2) for _ in range(2)]


class Rock:
    def __init__(self, shape: Shape, x: int, y: int) -> None:
        self.__shape = shape
        self.width, self.__pattern = self.__shape.get_binary_shape()
        self.x_pos = x
        self.y_pos = y

    def get_gridpattern(self, gridwidth: int) -> list[int]:
        return [val << gridwidth - self.x_pos - self.width for val in self.__pattern]


class Cave:
    def __init__(self, jetstream: str) -> None:
        self.__jetstream = [1 if c == '>' else -1 for c in jetstream]
        self.__cavewidth = 7
        self.__grid = []
        self.__trimmedrows = 0
        self.__stepcount = 0

    def drop_rocks(self, totalrocks: int) -> int:
        self.__grid = []
        self.__trimmedrows = 0
        self.__stepcount = 0
        seen_states = []
        seen_trims = []
        maxheight = 0
        for rock_nbr in range(totalrocks):
            currentrock_idx = rock_nbr % len(Shape)
            currentrock = Rock(Shape(currentrock_idx), 2, maxheight + 3)
            while True:
                # Move sideways if possible
                x_delta = self.__jetstream[self.__stepcount % len(self.__jetstream)]
                if 0 <= x_delta + currentrock.x_pos <= self.__cavewidth - currentrock.width:
                    movedrock = []
                    for idx, xval in enumerate(currentrock.get_gridpattern(self.__cavewidth)):
                        if x_delta > 0:
                            movedrock.append(xval >> 1)
                        else:
                            movedrock.append(xval << 1)
                        if (currentrock.y_pos + idx < len(self.__grid) and
                                (self.__grid[currentrock.y_pos + idx] & movedrock[-1] > 0)):
                            break
                    else:  # If we didn't break the loop, there was no collision - accept the new x-position
                        currentrock.x_pos += x_delta
                self.__stepcount += 1
                # Try to move down; if not possible, lock the rock in place in the grid and break the loop
                if currentrock.y_pos > maxheight:
                    currentrock.y_pos -= 1
                else:
                    for idx, xval in enumerate(currentrock.get_gridpattern(self.__cavewidth)):
                        if currentrock.y_pos == 0 or (currentrock.y_pos - 1 + idx < len(self.__grid) and
                                                      (self.__grid[currentrock.y_pos - 1 + idx] & xval > 0)):
                            break
                    else:
                        currentrock.y_pos -= 1
                        continue
                    # Couldn't move down - lock it in to the grid
                    for idx, xval in enumerate(currentrock.get_gridpattern(self.__cavewidth)):
                        if currentrock.y_pos + idx < len(self.__grid):
                            self.__grid[currentrock.y_pos + idx] |= xval
                        else:
                            self.__grid.append(xval)
                    # Trim the grid
                    self.__trimgrid()
                    maxheight = len(self.__grid)
                    break
            state = hash((currentrock_idx, self.__stepcount % len(self.__jetstream), tuple(self.__grid)))
            if state in seen_states:
                offset = seen_states.index(state)
                cycle_len = rock_nbr - offset
                trim_per_cycle = self.__trimmedrows - seen_trims[offset][0]
                nbr_cycles = (totalrocks - 1 - offset) // cycle_len  # Cached list is zero-indexed, rock counter is not.
                idx = offset + (totalrocks - 1 - offset) % cycle_len
                answer = seen_trims[idx][0] + seen_trims[idx][1] + (nbr_cycles * trim_per_cycle)
                return answer
            seen_states.append(state)
            seen_trims.append((self.__trimmedrows, len(self.__grid)))
        return self.__trimmedrows + len(self.__grid)

    def __trimgrid(self) -> None:
        # Floodfill the grid from the top, one row above the highest row to guarantee clear space, and then trim
        # anything below rows we can't reach
        seen = set()
        queue = [(0, len(self.__grid))]
        while queue:
            x, y = queue.pop(0)
            if (x, y) in seen:
                continue
            seen.add((x, y))
            for dx, dy in [(-1, 0), (1, 0), (0, -1)]:  # There should never be a need to go up
                new_x = x + dx
                new_y = y + dy
                if 0 <= new_x < self.__cavewidth and new_y > 0:
                    if new_y >= len(self.__grid) or self.__grid[new_y] & 2**(self.__cavewidth - new_x - 1) == 0:
                        queue.append((new_x, new_y))
        min_y = min([y for _, y in seen])
        while min_y > 1:
            self.__grid.pop(0)
            self.__trimmedrows += 1
            min_y -= 1


def main(aoc_input: str) -> None:
    mycave = Cave(aoc_input)
    print(f"Part 1: {mycave.drop_rocks(2022)}")
    print(f"Part 2: {mycave.drop_rocks(1_000_000_000_000)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2022/day17.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
