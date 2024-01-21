# Advent of code - Day 5 part A

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
            for n, val in enumerate(seeds):
                seeds[n] = maps[-1].convertvalue(val)
                # print("Conversion - %d -> " % val, seeds[n])
            state = "mapsearch"
            if maps[-1].destination == "location":
                break

print("Lowest location: %d" % min(seeds))

f.close()
