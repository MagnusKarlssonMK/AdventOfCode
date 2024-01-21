# Advent of code - Day 14 part B


tiltdirections = {"None": 0, "North": 1, "East": 2, "South": 3, "West": 4}


class Board:
    def __init__(self):
        self.width = 0
        self.tilt = tiltdirections["None"]
        self.roundrows = []
        self.cuberows = []

    def addrow(self, rowstring: str):
        self.width = max(self.width, len(rowstring))
        binroundstring = ""
        bincubestring = ""
        for char in rowstring:
            binroundstring += "1" if char == "O" else "0"
            bincubestring += "1" if char == "#" else "0"
        self.roundrows.append(int(binroundstring, 2))
        self.cuberows.append(int(bincubestring, 2))
        # print(self.cuberows[-1], " : ", self.roundrows[-1])

    def settilt(self, newdirection: tiltdirections):
        if newdirection == tiltdirections["North"]:
            self.tilt = newdirection
            isinrest = False
            while not isinrest:
                isinrest = True
                for rowindex in range(0, len(self.roundrows) - 1):
                    a = self.roundrows[rowindex]
                    b = self.roundrows[rowindex + 1]
                    c = self.cuberows[rowindex]
                    new_a = (b & ~c) | a
                    new_b = (a | c) & b
                    if a != new_a or b != new_b:
                        isinrest = False
                        self.roundrows[rowindex] = new_a
                        self.roundrows[rowindex + 1] = new_b
        elif newdirection == tiltdirections["South"]:
            self.tilt = newdirection
            isinrest = False
            while not isinrest:
                isinrest = True
                for rowindex in reversed(range(1, len(self.roundrows))):
                    a = self.roundrows[rowindex]
                    b = self.roundrows[rowindex - 1]
                    c = self.cuberows[rowindex]
                    new_a = (b & ~c) | a
                    new_b = (a | c) & b
                    if a != new_a or b != new_b:
                        isinrest = False
                        self.roundrows[rowindex] = new_a
                        self.roundrows[rowindex - 1] = new_b
        elif newdirection == tiltdirections["East"]:
            self.tilt = newdirection
            isinrest = False
            while not isinrest:
                isinrest = True
                for rowindex in range(0, len(self.roundrows)):
                    oldvalue = self.roundrows[rowindex]
                    for n in range(0, self.width):
                        b1 = (self.roundrows[rowindex] >> n) & 1
                        g1 = (self.cuberows[rowindex] >> n) & 1
                        if g1 | b1 == 0:
                            b2 = (self.roundrows[rowindex] >> (n + 1)) & 1
                            tmp = b1 ^ b2
                            tmp = (tmp << n) | (tmp << (n + 1))
                            self.roundrows[rowindex] ^= tmp
                    if oldvalue != self.roundrows[rowindex]:
                        isinrest = False
        elif newdirection == tiltdirections["West"]:
            self.tilt = newdirection
            isinrest = False
            while not isinrest:
                isinrest = True
                for rowindex in range(0, len(self.roundrows)):
                    oldvalue = self.roundrows[rowindex]
                    for n in reversed(range(1, self.width)):
                        b1 = (self.roundrows[rowindex] >> n) & 1
                        g1 = (self.cuberows[rowindex] >> n) & 1
                        if g1 | b1 == 0:
                            b2 = (self.roundrows[rowindex] >> (n - 1)) & 1
                            tmp = b1 ^ b2
                            tmp = (tmp << n) | (tmp << (n - 1))
                            self.roundrows[rowindex] ^= tmp
                    if oldvalue != self.roundrows[rowindex]:
                        isinrest = False
        else:
            print("Tilt direction not implemented yet")

    def getidstring(self):
        retval = ""
        for nbr in self.roundrows:
            retval += str(nbr) + ":"
        return retval

    def getload(self, supportbeamdirection: tiltdirections):
        totalsum = 0
        if supportbeamdirection == tiltdirections["North"]:
            size = len(self.roundrows)
            for rowindex, roundrow in enumerate(self.roundrows):
                totalsum += roundrow.bit_count() * (size - rowindex)
        else:
            print("Current tilt direction not implemented yet")
        return totalsum

    def __str__(self):
        tmpstring = ""
        for tmprow in range(0, len(self.roundrows)):
            tmpbinround = format(self.roundrows[tmprow], str(self.width)+'b')
            tmpbincube = format(self.cuberows[tmprow], str(self.width)+'b')
            for charindex in range(0, len(tmpbinround)):
                if tmpbincube[charindex] == "1":
                    tmpstring += "#"
                elif tmpbinround[charindex] == "1":
                    tmpstring += "0"
                else:
                    tmpstring += "."
            tmpstring += "\n"
        return tmpstring


myboard = Board()

with open("aoc14.txt", "r") as file:
    for line in file.readlines():
        myboard.addrow(line.strip("\n"))

print(myboard)

cycles = 1000000000
count = 0
cyclelength = 0
seen = {myboard.getidstring()}
seenlist = [myboard.getidstring()]

while count < cycles:
    count += 1
    myboard.settilt(tiltdirections["North"])
    myboard.settilt(tiltdirections["West"])
    myboard.settilt(tiltdirections["South"])
    myboard.settilt(tiltdirections["East"])
    thiscycle = myboard.getidstring()
    if cyclelength == 0 and thiscycle in seen:
        firstcycleindex = seenlist.index(thiscycle)
        cyclelength = count - firstcycleindex
        print("We are cycling! Count = ", count, "Cyclelen = ", cyclelength)
        count += cyclelength * ((cycles - count) // cyclelength)
        print("New count = ", count)
    seen.add(thiscycle)
    seenlist.append(thiscycle)

print("")
print(myboard)
print("")
print("Load calculation: ", myboard.getload(tiltdirections["North"]))
