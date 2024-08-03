"""
Stores the input as ranges in a number of maps. For part 1 it's mainly a matter of running the seeds through the maps
and see what it has been translated to in the other end.
For part 2 however it gets a lot more messy when the seeds are ranges themselves, which then gets split into other
ranges as they travel through the map filters, which means a bit of recursion when evaluating the filter translations.
"""
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Mapfilter:
    mask: range
    offset: int


class Map:
    def __init__(self, mapinput: list[str]) -> None:
        self.source, self.destination = mapinput[0].strip(" map:").split("-to-")
        self.__filterlist: list[Mapfilter] = []
        for line in mapinput[1:]:
            dest_start, source_start, size = map(int, line.split())
            self.__filterlist.append(Mapfilter(range(source_start, source_start + size), dest_start - source_start))

    def map_number(self, nbr: int) -> int:
        for mapfilter in self.__filterlist:
            if nbr in mapfilter.mask:
                return nbr + mapfilter.offset
        return nbr

    def map_range(self, i: range) -> iter:
        for f in self.__filterlist:
            if f.mask.start < i.stop and f.mask.stop > i.start:  # At least some overlap
                if f.mask.start <= i.start and i.stop <= f.mask.stop:  # Filter completely covers input range
                    yield range(i.start + f.offset, i.stop + f.offset)
                    return
                if i.start < f.mask.start and f.mask.stop < i.stop:  # Input range sticks out on both sides
                    yield from self.map_range(range(i.start, f.mask.start))
                    yield range(f.mask.start + f.offset, f.mask.stop + f.offset)
                    yield from self.map_range(range(f.mask.stop, i.stop))
                    return
                if f.mask.start <= i.start and f.mask.stop < i.stop:  # Input range sticks out only above
                    yield range(i.start + f.offset, f.mask.stop + f.offset)
                    yield from self.map_range(range(f.mask.stop, i.stop))
                    return
                if i.start < f.mask.start and i.stop <= f.mask.stop:  # Input range sticks out only below
                    yield from self.map_range(range(i.start, f.mask.start))
                    yield range(f.mask.start + f.offset, i.stop + f.offset)
                    return
            # else - no overlap, try next filter
        yield i


class Almanac:
    def __init__(self, rawstr: str) -> None:
        blocks = rawstr.split('\n\n')
        self.__seeds: list[int] = [int(seed) for seed in blocks[0].strip("seeds: ").split()]
        self.__maps = {m.source: m for m in [Map(block.splitlines()) for block in blocks[1:]]}

    def get_lowest_location(self) -> int:
        currentseeds = list(self.__seeds)
        currenttype = 'seed'
        while currenttype != 'location':
            tmp = [self.__maps[currenttype].map_number(seed) for seed in currentseeds]
            currentseeds = tmp
            currenttype = self.__maps[currenttype].destination
        return min(currentseeds)

    def get_lowest_ranged_location(self) -> int:
        seedranges: list[range] = [range(self.__seeds[idx], self.__seeds[idx] + self.__seeds[idx + 1])
                                   for idx in range(0, len(self.__seeds), 2)]
        currenttype = 'seed'
        while currenttype != 'location':
            tmp = []
            for s in seedranges:
                for newrange in self.__maps[currenttype].map_range(s):
                    tmp.append(newrange)
            seedranges = tmp
            currenttype = self.__maps[currenttype].destination
        return sorted(seedranges, key=lambda r: r.start)[0].start


def main() -> int:
    with open('../Inputfiles/aoc5.txt') as file:
        myalmanac = Almanac(file.read().strip('\n'))
    print(f"Part 1: {myalmanac.get_lowest_location()}")
    print(f"Part 2: {myalmanac.get_lowest_ranged_location()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
