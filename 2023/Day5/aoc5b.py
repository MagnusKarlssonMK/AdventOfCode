# Advent of code - Day 5 part B

class Range:
    def __init__(self, src, dst, lngt):
        self.srcstart = src
        self.dststart = dst
        self.length = lngt


class Map:
    def __init__(self, mapinput):
        self.destination = mapinput.split("-to-")[1]
        self.source = mapinput.split("-to-")[0]
        self.ranges = []
        # print("New map - From: -%s- " % self.source, "To: -%s-" % self.destination)

    def addrange(self, rangeinput):
        nbrs = rangeinput.split(" ")
        if len(nbrs) == 3:
            self.ranges.append(Range(int(nbrs[1]), int(nbrs[0]), int(nbrs[2])))
            return True
        return False

    def convertvalue(self, srcval):
        for rangepart in self.ranges:
            if srcval in range(rangepart.srcstart, rangepart.srcstart + rangepart.length + 1):
                return rangepart.dststart + srcval - rangepart.srcstart
        return srcval

    def convertrange(self, startval, rangeval):
        inval = [startval, rangeval]
        retval = []
        while len(inval) > 1:
            match = False
            for rangepart in self.ranges:
                lowedge = rangepart.srcstart
                upedge = rangepart.srcstart + rangepart.length
                if inval[0] < upedge and inval[0] + inval[1] > lowedge:
                    # Case 1: startval > upper range of map -> no match, go to next
                    # Case 2: startval + rangeval < lower range of map -> no match, go to next
                    if inval[0] < lowedge:
                        # Case 3: startval < lower range of map - at least partial match
                        if inval[0] + inval[1] <= upedge:
                            # Case 3a: startval + rangeval < upper range of map - the upper part is covered by this map
                            # print("3a")
                            retval.append(rangepart.dststart)
                            retval.append(inval[0] + inval[1] - lowedge)
                            inval[1] = lowedge - inval[0]
                        else:
                            # Case 3b: startval + rangeval > upper range of map - the middle part is covered
                            # print("Uh oh...")
                            retval.append(rangepart.dststart)
                            retval.append(rangepart.length)
                            inval.append(upedge)
                            inval.append(inval[0] + inval[1] - upedge)
                            inval[1] = lowedge - inval[0]
                    else:
                        # Case 4: startval > lower range of map - at least partial map
                        if inval[0] + inval[1] <= upedge:
                            # Case 4a: startval + rangeval < upper range of map - the interval is fully covered
                            # print("4a")
                            retval.append(rangepart.dststart + inval[0] - lowedge)
                            retval.append(inval[1])
                            del inval[0:2]
                        else:
                            # Case 4b: startval + rangeval > upper range of map - the lower part is covered by this map
                            # print("4b")
                            retval.append(rangepart.dststart + inval[0] - lowedge)
                            retval.append(upedge - inval[0])
                            inval[1] = inval[0] + inval[1] - upedge
                            inval[0] = upedge
                            # print(inval)
                            # print(retval)
                    match = True
                    break  # There was at least a partial match, inval was updated -> rerun the remainder if any
            if not match:
                # There was no map defined - default to convert to itself
                # print("Nope")
                retval.append(inval[0])
                retval.append(inval[1])
                del inval[0:2]

        return retval


seeds = []
maps = []

state = "seedsearch"

f = open("aoc5.txt", "r")

while True:
    line = f.readline().strip("\n")
    if state == "seedsearch":
        if line.__contains__("seeds: "):
            seedstring = line.split("seeds: ")[1].split(" ")
            for entry in seedstring:
                if entry.isnumeric():
                    seeds.append(int(entry))
            print(seeds)
            state = "mapsearch"
    elif state == "mapsearch":
        if line.__contains__(" map:"):
            maps.append(Map(line.split(" map")[0]))
            state = "mapping"
    elif state == "mapping":
        if not maps[-1].addrange(line):
            # Map done - conversion time!
            # for n, val in enumerate(seeds):
            #     seeds[n] = maps[-1].convertvalue(val)
            srcseeds = seeds
            dstseeds = []
            while len(srcseeds) > 1:
                newrange = maps[-1].convertrange(srcseeds[0], srcseeds[1])
                for q in newrange:
                    dstseeds.append(q)
                del srcseeds[0:2]
                # print(srcseeds)
                # print(dstseeds)
                seeds = dstseeds

            state = "mapsearch"
            print(seeds)
            if maps[-1].destination == "location":
                break

print("Lowest location: %d" % min(seeds[0::2]))

f.close()

"""""
Vid konvertering:
- Kolla om seed-start ligger mellan maprange-start och maprange-stop (annars gå till nästa maprange)
- Om så, kolla om seed-stop också är inom denna range
-   Är den det, konvertera hela rangen och markera denna seed som klar
-   Om inte, splitta denna seed vid maprange-stop och gör om samma igen för resten
"""
