"""
No need to actually make any dict of the different conversion layers, just put them all in an array
in the order of parsing it and process them one by one.
"""
import time
from pathlib import Path
from dataclasses import dataclass
from collections.abc import Generator


@dataclass(frozen=True)
class Mapfilter:
    mask: range
    offset: int


class Map:
    def __init__(self, mapinput: list[str]) -> None:
        self.__filterlist: list[Mapfilter] = []
        for line in mapinput[1:]:
            dest_start, source_start, size = map(int, line.split())
            self.__filterlist.append(Mapfilter(range(source_start, source_start + size), dest_start - source_start))

    def map_number(self, nbr: int) -> int:
        for mapfilter in self.__filterlist:
            if nbr in mapfilter.mask:
                return nbr + mapfilter.offset
        return nbr

    def map_range(self, i: range) -> Generator[range]:
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
        self.__maps = [m for m in [Map(block.splitlines()) for block in blocks[1:]]]

    def get_lowest_location(self) -> int:
        currentseeds = list(self.__seeds)
        for layer in self.__maps:
            currentseeds = [layer.map_number(seed) for seed in currentseeds]
        return min(currentseeds)

    def get_lowest_ranged_location(self) -> int:
        seedranges: list[range] = [range(self.__seeds[idx], self.__seeds[idx] + self.__seeds[idx + 1])
                                   for idx in range(0, len(self.__seeds), 2)]
        for layer in self.__maps:
            tmp: list[range] = []
            for s in seedranges:
                for newrange in layer.map_range(s):
                    tmp.append(newrange)
            seedranges = tmp
        return sorted(seedranges, key=lambda r: r.start)[0].start


def main(aoc_input: str) -> None:
    myalmanac = Almanac(aoc_input)
    print(f"Part 1: {myalmanac.get_lowest_location()}")
    print(f"Part 2: {myalmanac.get_lowest_ranged_location()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2023/day05.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
