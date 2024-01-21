# Advent of coding 2023 - Day 17
# Not giving correct answer for part B, (777 instead of 773), giving up for now, probably start from scratch... >:(

from heapq import heappop, heappush


GridCoordinate = tuple[int, int]  # row, col
Grid = dict[GridCoordinate, int]
Direction = tuple[int, int]  # dx, dy


def rotate_cw(fromdir: Direction) -> Direction:
    return fromdir[1], -fromdir[0]


def rotate_ccw(fromdir: Direction) -> Direction:
    return -fromdir[1], fromdir[0]


class Position:
    def __init__(self, newloc: GridCoordinate, newdir: Direction):
        self.location = newloc
        self.direction = newdir

    def nextloc(self) -> GridCoordinate:
        return self.location[0] + self.direction[0], self.location[1] + self.direction[1]

    def step(self) -> "Position":
        return Position(self.nextloc(), self.direction)

    def rotate_and_step(self, newdir: Direction) -> "Position":
        return Position(self.location, newdir).step()

    def __lt__(self, other):
        return sum(self.location) < sum(other.location)

    def __le__(self, other):
        return sum(self.location) <= sum(other.location)

    def __eq__(self, other):
        if isinstance(other, Position):
            if (self.location[0] == other.location[0] and self.location[1] == other.location[1] and
               self.direction[0] == other.direction[0] and self.direction[1] == other.direction[1]):
                return True
        return False
    
    def __str__(self):
        return f"Row: {self.location[0]} Col: {self.location[1]}, Dir dR:{self.direction[0]} dC:{self.direction[1]}"


State = tuple[int, Position, int]  # value, coordinate, stepcount


class Cityboard:
    def __init__(self):
        self.gridwidth: int = 0
        self.gridheight: int = 0
        self.grid: Grid = {}
        self.target: GridCoordinate = (0, 0)
        self.start: GridCoordinate = (0, 0)
        self.minsteps: int = 4
        self.maxsteps: int = 10

    def addgridline(self, newline: str) -> None:
        if len(newline) > 1:
            for idx, value in enumerate(newline):
                self.grid[self.gridheight, idx] = int(value)
            self.gridheight += 1
            self.gridwidth = max(self.gridwidth, len(newline))
            self.target = self.gridheight - 1, self.gridwidth - 1

    def settargetnode(self, targetnode: GridCoordinate) -> None:
        self.target = targetnode

    def findshortestpath(self) -> int:
        queue: list[State] = [(0, Position(self.start, (0, 1)), 0),
                              (0, Position(self.start, (-1, 0)), 0)]
        seen: set[tuple[int, int, int, int, int]] = set()
        while queue:
            cost, pos, num_steps = heappop(queue)
            if pos.location == self.target and num_steps >= self.minsteps:
                return cost

            # print("Visiting: ", pos, " NumSteps=", num_steps, " Cost=", cost)
            if (pos.location[0], pos.location[1], pos.direction[0], pos.direction[1], num_steps) in seen:
                # print("Already seen")
                continue
            seen.add((pos.location[0], pos.location[1], pos.direction[0], pos.direction[1], num_steps))

            if (num_steps >= self.minsteps and
               (left := pos.rotate_and_step(rotate_ccw(pos.direction))).location in self.grid):
                # print("Pushing(1): ", left, " NumSteps=", num_steps, " Cost=", cost)
                heappush(queue, (cost + self.grid[left.location], left, 1))

            if (num_steps >= self.minsteps and
               (right := pos.rotate_and_step(rotate_cw(pos.direction))).location in self.grid):
                # print("Pushing(2): ", right, " NumSteps=", num_steps, " Cost=", cost)
                heappush(queue, (cost + self.grid[right.location], right, 1))

            if (num_steps < self.maxsteps) and ((forward := pos.step()).location in self.grid):
                # print("Pushing(3): ", forward, " NumSteps=", num_steps, " Cost=", cost)
                heappush(queue, (cost + self.grid[forward.location], forward, num_steps + 1))
        return -1


""" ********************* """

mycityboard = Cityboard()

with open("aoc17.txt", "r") as file:
    for line in file:
        mycityboard.addgridline(line.strip("\n"))

# result_p1 = mycityboard.findshortestpath()

# print("A: ", result_p1)

# mycityboard.minsteps = 4
# mycityboard.maxsteps = 10

resultB = mycityboard.findshortestpath()

print("B: ", resultB)
