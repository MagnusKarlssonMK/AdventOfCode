# Needs refactoring. The direction mapping from splitters can definitely be made smoother.
# The gridwidth/height in global scope is nasty.

lightdirections = {'0': 0, 'N': 1, 'W': 2, 'S': 4, 'E': 8}

gridwidth = 0
gridheight = 0


class Lighthead:
    def __init__(self, newrow: int, column: int, direction: lightdirections):
        self.direction = direction
        self.rowposition = newrow
        self.colposition = column

    def takeonestep(self) -> bool:   # Returns true if grid edge has been reached
        retval = True
        if self.direction == lightdirections["E"]:
            self.colposition += 1
            retval = True if self.colposition >= gridwidth - 1 else False
        elif self.direction == lightdirections["W"]:
            self.colposition -= 1
            retval = True if self.colposition <= 0 else False
        elif self.direction == lightdirections["N"]:
            self.rowposition -= 1
            retval = True if self.rowposition <= 0 else False
        elif self.direction == lightdirections["S"]:
            self.rowposition += 1
            retval = True if self.rowposition >= gridheight - 1 else False
        return retval

    def setdirection(self, newdirection: lightdirections) -> None:
        self.direction = newdirection

    def mirrorhead(self, mirrorchar: str) -> lightdirections:  # Returns new direction for a new split head
        retval = lightdirections["0"]                          # Sets direction to "0" if new direction runs into wall
        if self.direction == lightdirections["E"]:
            if mirrorchar == "-":
                if self.colposition >= gridwidth - 1:
                    self.direction = lightdirections["0"]
            elif mirrorchar == "/":
                if self.rowposition <= 0:
                    self.direction = lightdirections["0"]
                else:
                    self.direction = lightdirections["N"]
            elif mirrorchar == "\\":
                if self.rowposition >= gridheight - 1:
                    self.direction = lightdirections["0"]
                else:
                    self.direction = lightdirections["S"]
            elif mirrorchar == "|":
                if self.rowposition < gridheight - 1:
                    self.direction = lightdirections["S"]
                    if self.rowposition > 0:
                        retval = lightdirections["N"]
                else:
                    self.direction = lightdirections["N"]
        elif self.direction == lightdirections["W"]:
            if mirrorchar == "-":
                if self.colposition <= 0:
                    self.direction = lightdirections["0"]
            elif mirrorchar == "/":
                if self.rowposition >= gridheight - 1:
                    self.direction = lightdirections["0"]
                else:
                    self.direction = lightdirections["S"]
            elif mirrorchar == "\\":
                if self.rowposition <= 0:
                    self.direction = lightdirections["0"]
                else:
                    self.direction = lightdirections["N"]
            elif mirrorchar == "|":
                if self.rowposition < gridheight - 1:
                    self.direction = lightdirections["S"]
                    if self.rowposition > 0:
                        retval = lightdirections["N"]
                else:
                    self.direction = lightdirections["N"]
        elif self.direction == lightdirections["N"]:
            if mirrorchar == "-":
                if self.colposition < gridwidth - 1:
                    self.direction = lightdirections["E"]
                    if self.colposition > 0:
                        retval = lightdirections["W"]
                else:
                    self.direction = lightdirections["W"]
            elif mirrorchar == "/":
                if self.colposition >= gridwidth - 1:
                    self.direction = lightdirections["0"]
                else:
                    self.direction = lightdirections["E"]
            elif mirrorchar == "\\":
                if self.colposition <= 0:
                    self.direction = lightdirections["0"]
                else:
                    self.direction = lightdirections["W"]
            elif mirrorchar == "|":
                if self.rowposition <= 0:
                    self.direction = lightdirections["0"]
        elif self.direction == lightdirections["S"]:
            if mirrorchar == "-":
                if self.colposition < gridwidth - 1:
                    self.direction = lightdirections["E"]
                    if self.colposition > 0:
                        retval = lightdirections["W"]
                else:
                    self.direction = lightdirections["W"]
            elif mirrorchar == "/":
                if self.colposition <= 0:
                    self.direction = lightdirections["0"]
                else:
                    self.direction = lightdirections["W"]
            elif mirrorchar == "\\":
                if self.colposition >= gridwidth - 1:
                    self.direction = lightdirections["0"]
                else:
                    self.direction = lightdirections["E"]
            elif mirrorchar == "|":
                if self.rowposition >= gridheight - 1:
                    self.direction = lightdirections["0"]
        return retval

    def __str__(self):
        return f"{self.direction} @ {self.rowposition}:{self.colposition}"

    def __reversed__(self):
        retval = lightdirections['0']
        if self.direction == lightdirections['N']:
            retval = lightdirections['S']
        elif self.direction == lightdirections['S']:
            retval = lightdirections['N']
        elif self.direction == lightdirections['E']:
            retval = lightdirections['W']
        elif self.direction == lightdirections['W']:
            retval = lightdirections['E']
        else:
            print("This shouldn't happen!?!?!")
        return retval


mirrorgrid = []
lightgrid = []

with open("aoc16.txt", "r") as file:
    for line in file.readlines():
        mirrorgrid.append(line.strip("\n"))
        lightgrid.append([0] * len(mirrorgrid[-1]))

# Create first light in top left corner
heads = [Lighthead(0, 0, lightdirections["E"])]
lightgrid[0][0] |= lightdirections['W']
print(heads[0])
gridwidth = len(lightgrid[0])
gridheight = len(lightgrid)

while len(heads) > 0:
    # For every iteration, step every head to its next mirror / edge
    newheadbuffer = []
    for head in heads:
        mirror = "."
        while mirror == ".":
            edgereached = head.takeonestep()
            if lightgrid[head.rowposition][head.colposition] & head.__reversed__() != 0:
                head.setdirection(lightdirections["0"])
                mirror = "X"
                break
            lightgrid[head.rowposition][head.colposition] |= head.__reversed__()
            mirror = mirrorgrid[head.rowposition][head.colposition]
            if edgereached and mirror == ".":
                mirror = "X"
                head.setdirection(lightdirections["0"])
        if mirror not in {"X", "."} and head.direction != lightdirections["0"]:
            newdir = head.mirrorhead(mirror)
            if newdir != lightdirections["0"]:
                newheadbuffer.append(Lighthead(head.rowposition, head.colposition, newdir))
    for newhead in newheadbuffer:
        heads.append(newhead)
    newheadbuffer.clear()
    for i, head in enumerate(heads):
        if head.direction == lightdirections["0"]:
            heads.pop(i)

for line in mirrorgrid:
    print(line)
print("")
for line in lightgrid:
    print(line)
print("")

count = 0
for row in lightgrid:
    for col in row:
        if col > 0:
            count += 1

print("Energized tiles: ", count)
