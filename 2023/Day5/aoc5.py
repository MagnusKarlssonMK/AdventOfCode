import sys
from itertools import chain

Mapfilter = tuple[range, int]


class Map:
    def __init__(self, inputstr: str):
        self.source, self.destination = inputstr.strip(" map:").split("-to-")
        self.filterlist: list[Mapfilter] = []

    def addfilter(self, inputstr: str) -> None:
        dest_start, source_start, size = map(int, inputstr.split())
        self.filterlist.append((range(source_start, source_start + size), dest_start - source_start))

    def mapnumber(self, inputnbr: int) -> int:
        for rangemask, offset in self.filterlist:
            if inputnbr in rangemask:
                return inputnbr + offset
        return inputnbr

    def maprange(self, inputrange: range) -> list[range]:
        for rangemask, offset in self.filterlist:
            a: range = rangemask
            b: range = inputrange
            if a.start < b.stop and a.stop > b.start:  # At least some overlap
                if a.start <= b.start and b.stop <= a.stop:  # Filter completely covers input range
                    return [range(b.start + offset, b.stop + offset)]
                if b.start < a.start and a.stop < b.stop:  # Input range sticks out on both sides of filter
                    return [*self.maprange(range(b.start, a.start)),
                            range(a.start + offset, a.stop + offset),
                            *self.maprange(range(a.stop, b.stop))]
                if a.start <= b.start and a.stop < b.stop:  # Input range sticks out only above the filter
                    return [range(b.start + offset, a.stop + offset),
                            *self.maprange(range(a.stop, b.stop))]
                if b.start < a.start and b.stop <= a.stop:  # Input range sticks out only below the filter
                    return [*self.maprange(range(b.start, a.start)),
                            range(a.start + offset, b.stop + offset)]
            # else - no overlap, try next filter
        return [inputrange]

    def __str__(self):
        return f"From: {self.source} To: {self.destination} NbrOfFilters: {len(self.filterlist)}"


def main() -> int:
    seedlist: list[int] = []
    maplist: list[Map] = []
    seedrangelist: list[range] = []

    with open("../Inputfiles/aoc5.txt", "r") as file:
        for line in file.readlines():
            if len(seedlist) == 0 and line.__contains__("seeds: "):
                [seedlist.append(int(seed)) for seed in line.strip("seeds: ").strip("\n").split()]
                for idx in range(len(seedlist)):
                    if idx % 2 == 0:
                        seedrangelist.append(range(seedlist[idx], seedlist[idx] + seedlist[idx + 1]))
            elif line.__contains__(" map:"):
                maplist.append(Map(line.strip("\n")))
            elif len(line) > 1 and len(maplist) > 0:
                maplist[-1].addfilter(line.strip("\n"))

    result_p1 = [seedlist]

    """ Note: this step assumes that all maps are stored in order. A more advanced and safe approach could
        be to match the 'source' and 'destination' attributes in the maps. """
    for nextmap in maplist:
        tmplist = []
        [tmplist.append(nextmap.mapnumber(seed)) for seed in result_p1[-1]]
        result_p1.append(tmplist)

    print("Lowest number (Part1): ", min(result_p1[-1]))

    tmp = seedrangelist.copy()
    result_p2 = None
    for nextmap in maplist:
        tmp2 = []
        while len(tmp) > 0:
            nextrange = tmp.pop(0)
            tmp2.append(nextmap.maprange(nextrange))
        tmp = list(chain.from_iterable(tmp2))
        result_p2 = sorted(tmp, key=lambda r: r.start)
    print("Part2: ", result_p2[0].start)

    return 0


if __name__ == "__main__":
    sys.exit(main())
