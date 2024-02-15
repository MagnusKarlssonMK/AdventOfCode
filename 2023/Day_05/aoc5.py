"""
Stores the input as ranges in a number of maps. For part 1 it's mainly a matter of running the seeds through the maps
and see what it has been translated to in the other end.
For part 2 however it gets a lot more messy when the seeds are ranges themselves, which then gets split into other
ranges as they travel through the map filters.
Consider changing the maprange() function to a 'yield' iterator kind of return instead, so the caller can put the
result into a list, rather than having the function returning a nested list like it is now which then needs to be
flattened before processed further.
"""
import sys
from itertools import chain

Mapfilter = tuple[range, int]


class Map:
    def __init__(self, mapinput: list[str]):
        self.source, self.destination = mapinput[0].strip(" map:").split("-to-")
        self.filterlist: list[Mapfilter] = []
        for line in mapinput[1:]:
            dest_start, source_start, size = map(int, line.split())
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
    with open("../Inputfiles/aoc5.txt", "r") as file:
        blocks = file.read().strip('\n').split('\n\n')
    seedlist: list[int] = [int(seed) for seed in blocks[0].strip("seeds: ").split()]
    seedrangelist: list[range] = [range(seedlist[idx], seedlist[idx] + seedlist[idx + 1])
                                  for idx in range(0, len(seedlist), 2)]
    maplist: list[Map] = [Map(block.splitlines()) for block in blocks[1:]]

    result_p1 = [seedlist]
    """ Note: this step assumes that all maps are stored in order. A more advanced and safe approach could
        be to match the 'source' and 'destination' attributes in the maps. """
    for nextmap in maplist:
        tmplist = [nextmap.mapnumber(seed) for seed in result_p1[-1]]
        result_p1.append(tmplist)

    print("Part1:", min(result_p1[-1]))

    tmp = list(seedrangelist)
    result_p2 = None
    for nextmap in maplist:
        tmp2 = []
        while len(tmp) > 0:
            nextrange = tmp.pop(0)
            tmp2.append(nextmap.maprange(nextrange))
        tmp = list(chain.from_iterable(tmp2))
        result_p2 = sorted(tmp, key=lambda r: r.start)
    print("Part2:", result_p2[0].start)

    return 0


if __name__ == "__main__":
    sys.exit(main())
