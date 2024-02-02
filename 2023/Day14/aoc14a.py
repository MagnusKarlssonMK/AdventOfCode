# Advent of code - Day 14 part A.
# This day definitely needs refactoring - trying to convert it to binary representation just made it a complete mess.


tiltdirections = {"None": 0, "North": 1, "East": 2, "South": 3, "West": 4}

base = 160


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

        while len(binroundstring) % base != 0:
            binroundstring = "0" + binroundstring
            bincubestring = "0" + bincubestring
        self.roundrows.append([int(binroundstring[i:i + base], 2) for i in range(0, len(binroundstring), base)])
        self.cuberows.append([int(bincubestring[i:i + base], 2) for i in range(0, len(bincubestring), base)])
        # print(self.cuberows[-1], " : ", self.roundrows[-1])

    def settilt(self, newdirection: tiltdirections):
        if newdirection == tiltdirections["North"]:
            self.tilt = newdirection
            isinrest = False
            while not isinrest:
                isinrest = True
                for rowindex in range(0, len(self.roundrows) - 1):
                    for numindex in range(0, len(self.roundrows[rowindex])):
                        a = self.roundrows[rowindex][numindex]
                        b = self.roundrows[rowindex + 1][numindex]
                        c = self.cuberows[rowindex][numindex]
                        new_a = (b & ~c) | a
                        new_b = (a | c) & b
                        if a != new_a or b != new_b:
                            isinrest = False
                            self.roundrows[rowindex][numindex] = new_a
                            self.roundrows[rowindex + 1][numindex] = new_b
        else:
            print("Tilt direction not implemented yet")

    def getload(self):
        totalsum = 0
        if self.tilt == tiltdirections["North"]:
            size = len(self.roundrows)
            for rowindex, roundrow in enumerate(self.roundrows):
                for rock in roundrow:
                    totalsum += rock.bit_count() * (size - rowindex)
        else:
            print("Current tilt direction not implemented yet")
            # Code from first attempt, calculating load on cube rocks, keeping it for now just in case...
            for rowindex in range(0, len(self.cuberows) - 1):
                for numindex in range(0, len(self.cuberows[rowindex])):
                    bitmask = self.cuberows[rowindex][numindex]
                    q = 1
                    while bitmask > 0:
                        bitmask = self.roundrows[rowindex + q][numindex] & bitmask
                        totalsum += bitmask.bit_count()
                        q += 1
                        if rowindex + q > len(self.cuberows):
                            break
        return totalsum

    def __str__(self):
        tmpstring = ""
        for tmprow in range(0, len(self.roundrows)):
            for nbrindex in range(0, len(self.roundrows[tmprow])):
                tmpbinround = format(self.roundrows[tmprow][nbrindex], str(base)+'b')
                tmpbincube = format(self.cuberows[tmprow][nbrindex], str(base)+'b')
                for charindex in range(0, len(tmpbinround)):
                    if nbrindex > 0 or charindex >= base - (self.width % base):
                        if tmpbincube[charindex] == "1":
                            tmpstring += "#"
                        elif tmpbinround[charindex] == "1":
                            tmpstring += "0"
                        else:
                            tmpstring += "."
            tmpstring += "\n"
        return tmpstring


myboard = Board()

with open("../Inputfiles/aoc14.txt", "r") as file:
    for line in file.readlines():
        myboard.addrow(line.strip("\n"))

myboard.settilt(tiltdirections["North"])

print("Load calculation: ", myboard.getload())
