"""
Pretty much tetris with side controls determined by the jet stream input.
Shapes and grid stored in binary format per row in dicts and bitshifted / bitmasked to move and check for overlap.
For part 2, will need cycle recognition. Try store a hashed tuple for every dropped rock containing rock index,
jet stream index, and top grid shape (per column).
"""
import sys


class Rock:
    def __init__(self, shape: str):
        self.shape = shape
        self.width = 0
        self.pattern: dict[int: set[int]] = {}
        match self.shape:
            case '-':
                self.pattern[0] = int('1111', 2)
                self.width = 4
            case '+':
                self.pattern[0] = int('010', 2)
                self.pattern[1] = int('111', 2)
                self.pattern[2] = int('010', 2)
                self.width = 3
            case 'J':
                self.pattern[0] = int('111', 2)
                self.pattern[1] = int('001', 2)
                self.pattern[2] = int('001', 2)
                self.width = 3
            case 'I':
                for i in range(4):
                    self.pattern[i] = int('1', 2)
                self.width = 1
            case 'o':
                self.pattern[0] = int('11', 2)
                self.pattern[1] = int('11', 2)
                self.width = 2

    def __repr__(self):
        return self.shape


class Cave:
    def __init__(self, jetstream: str):
        self.jetstream = jetstream
        self.cavewidth = 7
        self.rockqueue: list[Rock] = [Rock(s) for s in ['-', '+', 'J', 'I', 'o']]

    def droprocks(self, nbr_rocks: int) -> int:
        xmove = {'>': 1, '<': -1}
        grid: dict[int: str] = {}
        stepcount = 0
        maxheight = 0
        for nbr in range(nbr_rocks):
            currentrock_idx = nbr % len(self.rockqueue)
            x_pos = 2
            y_pos = maxheight + 3
            currentrock = [self.rockqueue[currentrock_idx].pattern[r] <<
                           (self.cavewidth - x_pos - self.rockqueue[currentrock_idx].width)
                           for r in list(self.rockqueue[currentrock_idx].pattern.keys())]
            while True:
                x_delta = xmove[self.jetstream[stepcount % len(self.jetstream)]]
                if 0 <= x_delta + x_pos <= self.cavewidth - self.rockqueue[currentrock_idx].width:
                    movedrock = []
                    for idx in range(len(currentrock)):
                        if x_delta > 0:
                            movedrock.append(currentrock[idx] >> 1)
                        else:
                            movedrock.append(currentrock[idx] << 1)
                        if y_pos + idx in grid and (grid[y_pos + idx] & movedrock[-1] > 0):
                            break
                    else:
                        x_pos += x_delta
                        currentrock = list(movedrock)
                stepcount += 1
                if y_pos > maxheight:
                    y_pos -= 1
                else:
                    for idx in range(len(currentrock)):
                        if y_pos == 0 or (y_pos - 1 + idx in grid and (grid[y_pos - 1 + idx] & currentrock[idx] > 0)):
                            break
                    else:
                        y_pos -= 1
                        continue
                    for idx in range(len(currentrock)):  # Couldn't move down - lock it in to the grid
                        if y_pos + idx in grid:
                            grid[y_pos + idx] |= currentrock[idx]
                        else:
                            grid[y_pos + idx] = currentrock[idx]
                    maxheight = max(grid.keys()) + 1
                    break
        return max(grid.keys()) + 1


def main() -> int:
    with open('../Inputfiles/aoc17_example.txt', 'r') as file:
        mycave = Cave(file.read().strip('\n'))
    print("Part 1:", mycave.droprocks(2022))
    return 0


if __name__ == "__main__":
    sys.exit(main())
